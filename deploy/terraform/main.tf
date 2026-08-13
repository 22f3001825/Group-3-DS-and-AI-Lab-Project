# MLT staging on AWS, declared.
#
# This is DEPLOY.md section 2 ("One-time setup / AWS") as code: two ECR repositories, the
# instance role and its INSTANCE PROFILE, the GitHub Actions OIDC push role, the operator
# policy, a security group, and one t3.micro. Everything up to a running, ECR-authorised,
# correctly-firewalled box.
#
# What it deliberately does NOT do:
#   * build or push the image      -> .github/workflows/image.yml
#   * bootstrap the host           -> deploy/deploy.ps1 -Bootstrap (ships bootstrap.sh over scp)
#   * hold any secret              -> .env.staging, shipped by deploy.ps1
# bootstrap.sh takes the DuckDNS token, and instance metadata is readable by anything that
# can reach IMDS from the box, so it is not templated into user_data.
#
#   terraform init
#   terraform plan  -var-file=terraform.tfvars
#   terraform apply -var-file=terraform.tfvars
#
# The defaults create resources ALONGSIDE the existing hand-made stack
# (i-0164d74aeb10ea077, iitm/ailab, mlt-ec2-ecr, gh-actions-ecr-push, mlt-staging-ops) —
# nothing here adopts or destroys any of them. Verify the new box end to end, then
# decommission the old one by hand.

terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  # Every resource below is tagged, so the hand-made stack stays distinguishable from this
  # one in the console for as long as both exist.
  default_tags {
    tags = {
      Project   = "mlt-staging"
      ManagedBy = "terraform"
    }
  }
}


# ── Variables ─────────────────────────────────────────────────────────────────

variable "region" {
  description = "AWS region. Must match AWS_REGION in the GitHub repository variables and the AWS CLI profile aws.ps1 uses — a CLI pointed elsewhere reports the instance does not exist, which reads like a permissions problem and is not."
  type        = string
  default     = "ap-south-1"
}

variable "name_prefix" {
  description = "Prefix for every created name. The default is NOT 'mlt' because mlt-ec2-ecr, gh-actions-ecr-push and mlt-staging-ops already exist in this account; a collision is an apply-time error, not a silent overwrite, but there is no reason to hit one."
  type        = string
  default     = "mlt-tf"
}

variable "ecr_repository_name" {
  description = "ECR repository for the application image. A '/' is fine — deploy.ps1 validates IMAGE_REF as '^[^/]+/[^:]+:.+$' and takes the registry as everything before the FIRST '/'. Changing this means updating the ECR_REPOSITORY GitHub repository variable and re-running the build workflow."
  type        = string
  default     = "iitm/ailab-tf"
}

variable "create_cliproxy_repo" {
  description = "Create a second repository for the optional CLIProxyAPI image. It needs its own repository because the app repository's lifecycle policy keeps only 2 images, and two MLT builds would evict the proxy."
  type        = bool
  default     = true
}

variable "github_repo" {
  description = "owner/repo allowed to assume the Actions push role. This is the security-critical value: the federated principal trusts GitHub's issuer, which issues tokens to every repository on GitHub, so the 'sub' condition built from this is the only thing distinguishing yours."
  type        = string
  default     = "22f3001825/Group-3-DS-and-AI-Lab-Project"

  validation {
    condition     = can(regex("^[^/[:space:]]+/[^/[:space:]]+$", var.github_repo))
    error_message = "github_repo must be exactly 'owner/repo'."
  }
}

variable "github_ref" {
  description = "Git ref allowed to push, as it appears in the OIDC 'sub' claim. 'refs/heads/main' pins pushes to main; a workflow_dispatch from another branch will NOT match and fails with 'Not authorized to perform sts:AssumeRoleWithWebIdentity'. Set github_sub_wildcard = true to allow any ref in the repo."
  type        = string
  default     = "refs/heads/main"
}

variable "github_sub_wildcard" {
  description = "Allow any ref in github_repo (StringLike 'repo:owner/name:*') instead of the single github_ref. Still scoped to the one repository — never widen beyond that."
  type        = bool
  default     = false
}

variable "create_github_oidc_provider" {
  description = "Create the GitHub OIDC provider. It is ACCOUNT-UNIQUE: one already exists in this account (DEPLOY.md section 2, Role 2), and creating a second fails with EntityAlreadyExists. Leave false here; set true only in a fresh account."
  type        = bool
  default     = false
}

variable "key_pair_name" {
  description = "Name of an EXISTING EC2 key pair to attach (e.g. 'iitm-2026'). Terraform never generates the key: a generated private key is written to terraform.tfstate in plaintext. Create it in the console or with 'aws ec2 create-key-pair', then name it here."
  type        = string
}

variable "ssh_cidr" {
  description = "CIDR allowed to reach TCP 22, e.g. '203.0.113.4/32'. Ports 80 and 443 are open to the world by necessity (Let's Encrypt validates from unpublished IPs); 22 is the only one that can be narrowed, so narrow it."
  type        = string

  validation {
    condition     = can(cidrhost(var.ssh_cidr, 0))
    error_message = "ssh_cidr must be a CIDR block, e.g. 203.0.113.4/32."
  }
}

variable "instance_type" {
  description = "x86-64 only. The image is linux/amd64 (Dockerfile runtime stage, the workflow's platforms:, and docker-compose.yml all pin it), so a Graviton t4g.* fails at 'docker compose up' with an exec-format error."
  type        = string
  default     = "t3.micro"

  validation {
    condition     = !can(regex("^[a-z]+[0-9]+g", var.instance_type))
    error_message = "That looks like a Graviton (arm64) type. The image is linux/amd64 — use a t3/t2/m5-class instance."
  }
}

variable "root_volume_gb" {
  description = "Root volume size. Billed 24/7 whether the instance runs or not, and at 16 GB gp3 in ap-south-1 it is essentially the entire standing bill (~$1.46/mo). 16 is enough because the box never builds — it only pulls the ~1.4 GB image."
  type        = number
  default     = 16
}

variable "create_ops_user" {
  description = "Create the IAM user for your laptop (start/stop + ECR) and attach the operator policy. No access key is created — see the ops_user_next_step output."
  type        = bool
  default     = true
}

variable "enable_nightly_stop" {
  description = "Create an EventBridge Scheduler rule that stops the instance nightly. Forgetting the box running for a month is a ~$8 surprise; forgetting it stopped costs nothing."
  type        = bool
  default     = false
}

variable "nightly_stop_expression" {
  description = "Schedule expression for the nightly stop, interpreted in nightly_stop_timezone."
  type        = string
  default     = "cron(0 23 * * ? *)"
}

variable "nightly_stop_timezone" {
  description = "IANA timezone for nightly_stop_expression. Without this the expression is UTC."
  type        = string
  default     = "Asia/Kolkata"
}


# ── Data sources ──────────────────────────────────────────────────────────────

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# The default VPC suffices and is what DEPLOY.md assumes. A custom VPC needs an Internet
# Gateway ATTACHED, a 0.0.0.0/0 route to it, and auto-assign public IPv4 on the subnet —
# all three, or the instance boots, passes its status checks and answers nothing.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Amazon Linux 2023, x86-64. Resolved through SSM so there is no AMI id to go stale in this
# file; the instance's lifecycle block below stops a new AL2023 release from replacing a
# running box.
data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64"
}

# The existing account-level provider, unless we are creating one.
data "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 0 : 1
  url   = "https://token.actions.githubusercontent.com"
}

locals {
  # Both repository ARNs, so the pull role and the operator policy cover cliproxy without
  # a second edit when it is enabled.
  ecr_repository_arns = concat(
    [aws_ecr_repository.app.arn],
    var.create_cliproxy_repo ? [aws_ecr_repository.cliproxy[0].arn] : [],
  )

  github_oidc_provider_arn = var.create_github_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.github[0].arn

  ecr_registry = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com"
}


# ── ECR ───────────────────────────────────────────────────────────────────────
# ECR Private rather than ghcr: GitHub Free allows 500 MB of private package storage and
# this image is ~1.4 GB, so with the default $0 spending limit the push is BLOCKED, not
# billed. ECR is ~$0.14/mo and same-region pulls to EC2 are free.

resource "aws_ecr_repository" "app" {
  name = var.ecr_repository_name

  # MUTABLE is required, not a preference: image.yml pushes :latest AND :<sha> on every
  # run, and an IMMUTABLE repository rejects the second push to :latest.
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep the last 2 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 2
      }
      action = { type = "expire" }
    }]
  })
}

# CLIProxyAPI. A separate repository, not a separate tag: the policy above keeps 2 images,
# so two MLT builds would evict the proxy from a shared repository.
resource "aws_ecr_repository" "cliproxy" {
  count = var.create_cliproxy_repo ? 1 : 0

  name                 = "${var.ecr_repository_name}/cliproxy"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "cliproxy" {
  count = var.create_cliproxy_repo ? 1 : 0

  repository = aws_ecr_repository.cliproxy[0].name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep the last 2 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 2
      }
      action = { type = "expire" }
    }]
  })
}


# ── IAM role 1: the instance (ECR pull) ───────────────────────────────────────
# The box authenticates to ECR through this role via the amazon-ecr-credential-helper,
# which reads IMDS and mints a fresh token per pull — no `docker login`, no 12-hour token
# to expire. bootstrap.sh configures the helper; this is the half that makes it work.

data "aws_iam_policy_document" "ec2_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ecr_pull" {
  # ecr:GetAuthorizationToken is an ACCOUNT-LEVEL action and cannot be resource-scoped.
  # The "*" here is correct, not an oversight — same in every policy below.
  statement {
    sid       = "EcrAuthIsAccountWide"
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  # Scoped to these repositories. AmazonEC2ContainerRegistryReadOnly also works but grants
  # read on every repository in the account.
  statement {
    sid    = "PullTheseReposOnly"
    effect = "Allow"
    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchCheckLayerAvailability",
    ]
    resources = local.ecr_repository_arns
  }
}

resource "aws_iam_role" "instance" {
  name               = "${var.name_prefix}-ec2-ecr"
  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
}

resource "aws_iam_role_policy" "instance_ecr_pull" {
  name   = "ecr-pull"
  role   = aws_iam_role.instance.id
  policy = data.aws_iam_policy_document.ecr_pull.json
}

# An EC2 instance cannot be given a ROLE — it is given an INSTANCE PROFILE containing one.
# The console does this silently; doing it by hand does not, and a missing profile is the
# usual reason a correct-looking role has no effect ("docker compose pull" 401s from ECR).
# Wiring it to the instance below is what makes that unforgettable here.
resource "aws_iam_instance_profile" "instance" {
  name = "${var.name_prefix}-ec2-ecr"
  role = aws_iam_role.instance.name
}


# ── IAM role 2: GitHub Actions (ECR push, via OIDC) ───────────────────────────

# Only in a fresh account — see var.create_github_oidc_provider.
resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 1 : 0

  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_policy_document" "github_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.github_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # THE security-critical condition. The federated principal above trusts GitHub's
    # issuer, which issues tokens to EVERY repository on GitHub — this is the only thing
    # limiting the role to yours. Never widen it to "repo:*" and never drop it; that is
    # the most common way GitHub-OIDC setups are misconfigured.
    condition {
      test     = var.github_sub_wildcard ? "StringLike" : "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        var.github_sub_wildcard
        ? "repo:${var.github_repo}:*"
        : "repo:${var.github_repo}:ref:${var.github_ref}"
      ]
    }
  }
}

data "aws_iam_policy_document" "ecr_push" {
  statement {
    sid       = "EcrAuthIsAccountWide"
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    sid    = "PushTheseReposOnly"
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage",
      # The two read actions are here because buildx reads existing manifests for its
      # cache; without them the push fails with "no basic auth credentials".
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
    ]
    resources = local.ecr_repository_arns
  }
}

resource "aws_iam_role" "github_actions" {
  name               = "${var.name_prefix}-gh-actions-ecr-push"
  assume_role_policy = data.aws_iam_policy_document.github_trust.json
}

resource "aws_iam_role_policy" "github_actions_ecr_push" {
  name   = "ecr-push"
  role   = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.ecr_push.json
}


# ── IAM: the local operator (start/stop from your laptop) ─────────────────────
# This is what deploy/aws.ps1 calls, and nothing more. deploy.ps1 needs NONE of it —
# bootstrap, deploy and -SeedDb are ssh/scp, and the box authenticates to ECR through its
# instance profile.
#
# Do NOT add the setup permissions to this user: the rest of this file needs
# iam:CreateRole + iam:PutRolePolicy + iam:PassRole, which together are administrator
# access in practice. Run terraform as an admin identity instead.

data "aws_iam_policy_document" "ops" {
  # ec2:Describe* cannot take a resource ARN.
  statement {
    sid       = "DescribeIsAccountWide"
    effect    = "Allow"
    actions   = ["ec2:DescribeInstances", "ec2:DescribeInstanceStatus"]
    resources = ["*"]
  }

  # Start/stop IS instance-scoped, so this key cannot touch anything else in the account.
  statement {
    sid       = "StartStopThisInstanceOnly"
    effect    = "Allow"
    actions   = ["ec2:StartInstances", "ec2:StopInstances"]
    resources = [aws_instance.app.arn]
  }

  statement {
    sid       = "EcrAuthIsAccountWide"
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  # Only needed if you build and push images from Windows instead of via Actions
  # (DEPLOY.md, "Building and pushing from Windows"). Drop this statement otherwise.
  statement {
    sid    = "EcrPushPullTheseReposOnly"
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:DescribeImages",
      "ecr:ListImages",
    ]
    resources = local.ecr_repository_arns
  }
}

resource "aws_iam_policy" "ops" {
  name        = "${var.name_prefix}-staging-ops"
  description = "Start/stop the staging instance and read/write its ECR repositories. Attach to the laptop IAM user; see deploy/aws.ps1."
  policy      = data.aws_iam_policy_document.ops.json
}

# No console password, and deliberately NO aws_iam_access_key: the secret would be stored
# in terraform.tfstate in plaintext. Mint it with `aws iam create-access-key` — see the
# ops_user_next_step output.
resource "aws_iam_user" "ops" {
  count = var.create_ops_user ? 1 : 0
  name  = "${var.name_prefix}-staging-ops"
}

resource "aws_iam_user_policy_attachment" "ops" {
  count = var.create_ops_user ? 1 : 0

  user       = aws_iam_user.ops[0].name
  policy_arn = aws_iam_policy.ops.arn
}


# ── Network ───────────────────────────────────────────────────────────────────

resource "aws_security_group" "app" {
  name        = "${var.name_prefix}-staging"
  description = "MLT staging: HTTP/HTTPS from anywhere, SSH from the operator only."
  vpc_id      = data.aws_vpc.default.id
}

# 80 and 443 CANNOT be narrowed to your own address. Let's Encrypt validates from
# unpublished IPs, so an SG that allows only you produces the confusing failure where http
# works from your machine while ACME reports "Timeout during connect" and the browser shows
# ERR_SSL_PROTOCOL_ERROR. Port 80 is required as well as 443 — HTTP-01 challenge plus the
# http->https redirect.
resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = aws_security_group.app.id
  description       = "HTTP: ACME HTTP-01 challenge and the redirect to https"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = aws_security_group.app.id
  description       = "HTTPS: the application"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_vpc_security_group_ingress_rule" "ssh" {
  security_group_id = aws_security_group.app.id
  description       = "SSH: deploy.ps1 (scp + ssh). The only rule that can be narrowed."
  cidr_ipv4         = var.ssh_cidr
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22
}

# Egress must stay open: image pulls from ECR and Docker Hub, ACME, DuckDNS, Qdrant Cloud
# and every LLM provider are all outbound from this box.
resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.app.id
  description       = "All outbound"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}


# ── The instance ──────────────────────────────────────────────────────────────

resource "aws_instance" "app" {
  ami           = data.aws_ssm_parameter.al2023.value
  instance_type = var.instance_type
  key_name      = var.key_pair_name

  subnet_id              = sort(data.aws_subnets.default.ids)[0]
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile   = aws_iam_instance_profile.instance.name

  # An auto-assigned public IPv4, and deliberately no aws_eip. Since Feb 2024 AWS bills
  # every in-use public IPv4 at $0.005/hr, so the address is not free either way — the
  # difference is WHEN. An EIP bills always, including while the instance is stopped
  # (~$3.65/mo, more than everything else here combined); an auto-assigned address is
  # released on stop. The cost is a new address on every start, which bootstrap.sh's
  # @reboot DuckDNS cron repoints the domain at within seconds.
  associate_public_ip_address = true

  root_block_device {
    volume_size = var.root_volume_gb
    volume_type = "gp3"
    encrypted   = true
    # Left at the default (true). This volume holds state/mlt_learner.db, so terminating
    # the instance destroys the database — see the lifecycle note below.
  }

  # IMDSv2 only. The ECR credential helper runs on the HOST (docker invokes it), not inside
  # a container, so the default hop limit of 1 is enough and nothing needs 2.
  metadata_options {
    http_tokens                 = "required"
    http_endpoint               = "enabled"
    http_put_response_hop_limit = 1
  }

  tags = {
    Name = "${var.name_prefix}-staging"
  }

  lifecycle {
    # This volume holds state/mlt_learner.db — every student, quiz attempt and mastery row,
    # PLUS the question bank's question_units vector BLOBs, which cost real embedding calls
    # to regenerate. There is no replica; bootstrap.sh's backups sit on this same volume.
    #
    # ami: SSM resolves to the CURRENT AL2023 release, so without this a routine `apply`
    # months later would replace a running box because Amazon published a new AMI.
    ignore_changes = [ami]

    # Uncomment once this instance is the live one. It makes `terraform destroy` and any
    # replacement-forcing change (instance_type, subnet, key_name) fail loudly instead of
    # taking the database with them. Take an EBS snapshot before commenting it back out.
    # prevent_destroy = true
  }
}


# ── Optional: nightly stop ────────────────────────────────────────────────────

data "aws_iam_policy_document" "scheduler_trust" {
  count = var.enable_nightly_stop ? 1 : 0

  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }

    # Confused-deputy guard: only schedules in this account may assume the role.
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }
}

resource "aws_iam_role" "scheduler" {
  count = var.enable_nightly_stop ? 1 : 0

  name               = "${var.name_prefix}-nightly-stop"
  assume_role_policy = data.aws_iam_policy_document.scheduler_trust[0].json
}

# A separate resource rather than an `inline_policy` block on the role above: that block is
# deprecated in the AWS provider and removed in v6.
resource "aws_iam_role_policy" "scheduler" {
  count = var.enable_nightly_stop ? 1 : 0

  name = "stop-this-instance"
  role = aws_iam_role.scheduler[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "ec2:StopInstances"
      Resource = aws_instance.app.arn
    }]
  })
}

resource "aws_scheduler_schedule" "nightly_stop" {
  count = var.enable_nightly_stop ? 1 : 0

  name                         = "${var.name_prefix}-nightly-stop"
  description                  = "Stop the staging instance overnight. Forgetting it running for a month is a ~$8 surprise; forgetting it stopped costs nothing."
  schedule_expression          = var.nightly_stop_expression
  schedule_expression_timezone = var.nightly_stop_timezone

  flexible_time_window {
    mode = "OFF"
  }

  target {
    # The universal target for the EC2 StopInstances API. Stopping an already-stopped
    # instance is a no-op, so this is safe to fire on a night with no demo.
    arn      = "arn:aws:scheduler:::aws-sdk:ec2:stopInstances"
    role_arn = aws_iam_role.scheduler[0].arn
    input    = jsonencode({ InstanceIds = [aws_instance.app.id] })
  }
}


# ── Outputs ───────────────────────────────────────────────────────────────────

output "instance_id" {
  description = "Set this as $env:MLT_INSTANCE_ID for deploy/aws.ps1."
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "Current public IPv4. It CHANGES on every stop/start (no Elastic IP) — read it from `aws.ps1 -Status` day to day, not from this output, and use the DuckDNS name everywhere else."
  value       = aws_instance.app.public_ip
}

output "ssh_command" {
  description = "AL2023 logs in as ec2-user (ubuntu@ only on an Ubuntu AMI)."
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_instance.app.public_ip}"
}

output "ecr_registry" {
  description = "Registry host. bootstrap.sh --ecr-registry takes this; deploy.ps1 derives it from IMAGE_REF."
  value       = local.ecr_registry
}

output "image_ref" {
  description = "IMAGE_REF for .env.staging."
  value       = "${aws_ecr_repository.app.repository_url}:latest"
}

output "cliproxy_image_ref" {
  description = "CLIPROXY_IMAGE_REF for .env, if you enable the cliproxy profile."
  value       = var.create_cliproxy_repo ? "${aws_ecr_repository.cliproxy[0].repository_url}:latest" : null
}

output "github_repository_variables" {
  description = "Settings -> Secrets and variables -> Actions -> Variables. The two VITE_* values are not derivable from AWS and must match .env.staging exactly — update.sh compares them against the image's labels and refuses to start on a mismatch."
  value = {
    AWS_REGION     = data.aws_region.current.name
    AWS_ROLE_ARN   = aws_iam_role.github_actions.arn
    ECR_REPOSITORY = aws_ecr_repository.app.name
  }
}

output "ops_policy_arn" {
  description = "The operator policy backing deploy/aws.ps1."
  value       = aws_iam_policy.ops.arn
}

output "ops_user_next_step" {
  description = "Terraform creates the operator user but never its access key — the secret would land in terraform.tfstate in plaintext."
  value = var.create_ops_user ? "aws iam create-access-key --user-name ${aws_iam_user.ops[0].name}   # then: aws configure (region ${data.aws_region.current.name})" : "create_ops_user = false; attach ${aws_iam_policy.ops.arn} to your own IAM user"
}

output "next_steps" {
  description = "What to do after apply. Terraform stops at a provisioned box; the app arrives over SSH."
  value       = <<-EOT
    1. Set the GitHub repository variables from `terraform output github_repository_variables`
       (plus VITE_API_URL and VITE_GOOGLE_CLIENT_ID), then run the
       "Build and push staging image" workflow ONCE. The box pulls; it never builds.

    2. Put IMAGE_REF=${aws_ecr_repository.app.repository_url}:latest in .env.staging,
       along with STAGING_DOMAIN, the two VITE_*, GOOGLE_CLIENT_ID, JWT_SECRET and the
       Qdrant/LLM keys.

    3. Bootstrap and deploy (nothing secret is in this Terraform):
       $env:MLT_INSTANCE_ID = '${aws_instance.app.id}'
       .\deploy\deploy.ps1 -Server ec2-user@${aws_instance.app.public_ip} -Key ~\.ssh\${var.key_pair_name}.pem `
           -Env .env.staging -Bootstrap -DuckDnsToken <token>
       .\deploy\deploy.ps1 -Server ec2-user@${aws_instance.app.public_ip} -Key ~\.ssh\${var.key_pair_name}.pem `
           -Env .env.staging -SeedDb

    4. Point the DuckDNS domain at this box and add https://<domain> as an Authorized
       JavaScript origin on the Google OAuth Web client. Then walk DEPLOY.md ->
       "Verifying a deploy" steps 1-10.
  EOT
}
