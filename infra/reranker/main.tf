// infra/reranker/main.tf
//
// A single EC2 instance running the cross-encoder reranker container, plus the ECR
// repository it pulls from.
//
// ─────────────────────────────────────────────────────────────────────────────
// THIS IS NO LONGER THE DEFAULT. The reranker now runs as a fourth container on the API
// instance itself — `docker-compose.yml`, service `reranker`, profile `reranker`, built
// by `deploy/reranker.ps1`. That became possible when the API box moved from t3.micro
// (1 GiB) to t3.medium (4 GiB), which holds both ONNX models with room to spare.
//
// Apply THIS stack instead when the reranker outgrows the API box: sustained rerank load
// competing with request handling on the same burstable vCPUs, or a model larger than the
// MiniLM cross-encoder. It costs a second instance (~$16/mo) and a network hop that the
// co-located container does not. The two are alternatives — running both means paying for
// an instance nothing points at, since RERANKER_URL names exactly one endpoint.
// ─────────────────────────────────────────────────────────────────────────────
//
// The shape of this stack is driven by one constraint: an API host too small to hold a
// second ML model in-process. So the reranker gets its own box, and the API reaches it
// over the VPC's private network.
//
// Two things are deliberately absent:
//   * No public ingress. The only way in is from the API's security group.
//   * No SSH key. Shell access is via SSM Session Manager, which leaves an audit trail
//     and needs no open port.
//
// A third is absent on purpose and is worth spelling out: NO NAT GATEWAY. The instance
// goes in a PUBLIC subnet and gets an auto-assigned public IPv4, which is the same shape
// DEPLOY.md:106 already prescribes for the API instance. The box needs egress — ECR, SSM,
// the OS mirrors — but only at boot and on service restart; the container itself needs
// none, because the model is baked into the image. Renting a NAT gateway (~$41/mo, more
// than twice this t3.small) to broker a handful of image pulls is not a trade worth
// making, and ECR + SSM VPC endpoints cost more still. The public IPv4 costs $0.005/h.
//
// The address is for egress only. Nothing may connect IN: `aws_security_group.reranker`
// has exactly one ingress rule and it is SG-to-SG. Note that this is now the ONLY thing
// standing between the internet and port 8080 — in a private subnet the routing table
// was a second, independent barrier. Read the ingress rule below with that in mind.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  tags = merge(
    {
      Project   = "mlt-course-assistant"
      Component = "reranker"
      ManagedBy = "terraform"
    },
    var.tags,
  )
}

// ── Container registry ────────────────────────────────────────────────────────

// A SEPARATE repository from the API's. .env.staging.example:38 notes that the API's
// lifecycle policy keeps only the latest 2 images — sharing one repository would mean
// reranker builds evict API images and vice versa.
resource "aws_ecr_repository" "reranker" {
  name                 = var.name_prefix
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.tags
}

resource "aws_ecr_lifecycle_policy" "reranker" {
  repository = aws_ecr_repository.reranker.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep the last 3 images; older ones are unreachable rollback targets anyway."
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 3
      }
      action = { type = "expire" }
    }]
  })
}

// ── Secret ────────────────────────────────────────────────────────────────────

// The API key goes in Parameter Store, not user_data. user_data is readable through the
// instance metadata service by ANY process on the box (and by anything that finds an
// SSRF in a process on the box), so a secret placed there is a secret shared with the
// whole instance. The instance profile below can read exactly this one parameter.
resource "aws_ssm_parameter" "api_key" {
  name        = "/${var.name_prefix}/api-key"
  description = "Bearer token the MLT API presents to the reranker."
  type        = "SecureString"
  value       = var.api_key
  tags        = local.tags
}

// ── Networking ────────────────────────────────────────────────────────────────

resource "aws_security_group" "reranker" {
  name        = "${var.name_prefix}-sg"
  description = "Reranker: ingress only from the API instance's security group."
  vpc_id      = var.vpc_id
  tags        = merge(local.tags, { Name = "${var.name_prefix}-sg" })

  lifecycle {
    create_before_destroy = true
  }
}

// SG-to-SG, not a CIDR block. This survives the API instance changing its private IP —
// which .env.staging.example:17 says happens on every start, since it runs without an
// Elastic IP.
resource "aws_vpc_security_group_ingress_rule" "from_app" {
  security_group_id            = aws_security_group.reranker.id
  referenced_security_group_id = var.app_security_group_id
  from_port                    = var.port
  to_port                      = var.port
  ip_protocol                  = "tcp"
  description                  = "Reranker HTTP from the API instance only."
  tags                         = local.tags
}

// Egress stays open: the instance must reach ECR, SSM and the OS package mirrors. The
// container itself needs no egress at all — the model is baked into the image.
resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.reranker.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
  description       = "ECR pulls, SSM agent, package updates."
  tags              = local.tags
}

// ── Instance identity ─────────────────────────────────────────────────────────

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "reranker" {
  name               = "${var.name_prefix}-role"
  assume_role_policy = data.aws_iam_policy_document.assume.json
  tags               = local.tags
}

// Shell access without an open SSH port or a key pair to lose.
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.reranker.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "ecr" {
  role       = aws_iam_role.reranker.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

// Scoped to the one parameter, not ssm:* on everything. kms:Decrypt is required because
// SecureString values are encrypted with the account's default SSM key.
data "aws_iam_policy_document" "read_api_key" {
  statement {
    actions   = ["ssm:GetParameter", "ssm:GetParameters"]
    resources = [aws_ssm_parameter.api_key.arn]
  }

  statement {
    actions   = ["kms:Decrypt"]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "kms:ViaService"
      values   = ["ssm.${var.region}.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "read_api_key" {
  name   = "${var.name_prefix}-read-api-key"
  role   = aws_iam_role.reranker.id
  policy = data.aws_iam_policy_document.read_api_key.json
}

resource "aws_iam_instance_profile" "reranker" {
  name = "${var.name_prefix}-profile"
  role = aws_iam_role.reranker.name
  tags = local.tags
}

// ── The instance ──────────────────────────────────────────────────────────────

// Resolved through SSM rather than hardcoded: AMI ids are region-specific and a pinned
// one goes stale (and unpatched) within weeks.
data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

data "aws_region" "current" {}

// The route table the subnet actually uses — an explicitly associated one, or the VPC's
// main table when there is no association. Only read so the precondition below can check
// it; nothing here modifies routing.
data "aws_route_table" "subnet" {
  subnet_id = var.subnet_id
}

resource "aws_instance" "reranker" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.reranker.id]
  iam_instance_profile   = aws_iam_instance_profile.reranker.name

  // Egress without a NAT gateway. Set explicitly rather than inherited from the subnet's
  // map_public_ip_on_launch, so the stack does not silently depend on a subnet attribute
  // that someone can flip in the console.
  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user_data.sh", {
    aws_region     = data.aws_region.current.name
    ecr_repo_url   = aws_ecr_repository.reranker.repository_url
    image_tag      = var.image_tag
    port           = var.port
    ssm_param_name = aws_ssm_parameter.api_key.name
  })

  // Rebuild the instance when the bootstrap script or the pinned tag changes. Without
  // this, editing user_data updates the attribute in state and changes nothing on the
  // running box, which is a genuinely confusing way to lose an afternoon.
  user_data_replace_on_change = true

  root_block_device {
    volume_size           = var.root_volume_gb
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  // IMDSv2 required: the token handshake is what stops a server-side request forgery in
  // the app from reading the instance's credentials.
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }

  // Fail at plan time, not four minutes into a boot that goes nowhere.
  //
  // Without an IGW route the instance still launches and still passes both status checks;
  // what fails is user_data, silently, because `dnf install` and `docker pull` have no
  // path out. You get a healthy-looking box that serves nothing, and the only evidence is
  // in /var/log/cloud-init-output.log on a machine you have to SSM into to read. That is
  // the exact failure DEPLOY.md:106 warns about for the API instance.
  //
  // `try(..., false)` because a route with no gateway_id (a peering, NAT or endpoint
  // route) leaves the attribute null, and an unguarded startswith() on it errors out —
  // turning a clear message into a Terraform type error.
  lifecycle {
    precondition {
      condition = anytrue([
        for r in data.aws_route_table.subnet.routes :
        try(r.cidr_block == "0.0.0.0/0" && startswith(r.gateway_id, "igw-"), false)
      ])
      error_message = join("", [
        "subnet_id ${var.subnet_id} has no 0.0.0.0/0 route to an Internet Gateway. ",
        "This stack has no NAT gateway by design, so the instance would boot, pass its ",
        "status checks, and never reach ECR. Pass a PUBLIC subnet: attach an IGW to the ",
        "VPC and add 0.0.0.0/0 -> igw-... to this subnet's route table.",
      ])
    }
  }

  tags = merge(local.tags, { Name = var.name_prefix })
}
