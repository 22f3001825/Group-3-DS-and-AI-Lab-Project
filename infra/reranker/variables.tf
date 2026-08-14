// Inputs for the reranker instance.
//
// The three network variables have no defaults on purpose: this stack attaches to
// infrastructure that already exists (the VPC your API instance runs in) and guessing
// any of them would either fail at apply time or, worse, succeed against the wrong VPC.

variable "vpc_id" {
  description = "VPC that already hosts the API instance. The reranker joins it so the two can talk over private IPs."
  type        = string
}

variable "subnet_id" {
  description = "PUBLIC subnet for the reranker instance. Must be in var.vpc_id, and its route table must carry 0.0.0.0/0 -> igw-... — the instance gets a public IPv4 for egress instead of a NAT gateway (see the header of main.tf), and apply fails with a precondition if the route is missing. Nothing may reach the instance from outside: ingress is the API's security group only."
  type        = string
}

variable "app_security_group_id" {
  description = "Security group attached to the API instance. This is the ONLY source allowed to reach the reranker port — there is no CIDR-based ingress rule anywhere in this stack."
  type        = string
}

variable "region" {
  description = "AWS region. Defaults to the region in .env.staging.example's ECR reference."
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "t3.small (2 GiB) fits the ONNX cross-encoder with room to spare; the model itself needs ~200-300 MB resident. t3.micro does NOT — that is the whole reason this service is not co-located with the API."
  type        = string
  default     = "t3.small"
}

variable "port" {
  description = "Port the container listens on, matching reranker/Dockerfile's EXPOSE."
  type        = number
  default     = 8080
}

variable "image_tag" {
  description = "ECR image tag the instance pulls at boot. Pin to a git SHA for a reproducible rollout rather than chasing 'latest'."
  type        = string
  default     = "latest"
}

variable "api_key" {
  description = "Shared secret the API sends as a bearer token. Generate a long random string; it is stored as an SSM SecureString, never in user_data."
  type        = string
  sensitive   = true
}

variable "name_prefix" {
  description = "Prefix for every named resource, so this stack is greppable in the console."
  type        = string
  default     = "mlt-reranker"
}

variable "root_volume_gb" {
  description = "Root EBS size. The image is ~1 GB; the rest is headroom for Docker layers and logs."
  type        = number
  default     = 20
}

variable "tags" {
  description = "Extra tags merged into every resource."
  type        = map(string)
  default     = {}
}
