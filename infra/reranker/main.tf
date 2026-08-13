// infra/reranker/main.tf
//
// A single EC2 instance running the cross-encoder reranker container, plus the ECR
// repository it pulls from.
//
// The shape of this stack is driven by one constraint: the API host is a t3.micro with
// ~1 GiB of RAM, which cannot hold a second ML model in-process. So the reranker gets
// its own box, and the API reaches it over the VPC's private network.
//
// Two things are deliberately absent:
//   * No public ingress. The only way in is from the API's security group.
//   * No SSH key. Shell access is via SSM Session Manager, which leaves an audit trail
//     and needs no open port.

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

resource "aws_instance" "reranker" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.reranker.id]
  iam_instance_profile   = aws_iam_instance_profile.reranker.name

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

  tags = merge(local.tags, { Name = var.name_prefix })
}
