output "private_ip" {
  description = "Private IP of the reranker. This is what the API talks to, and what belongs in RERANKER_URL — never the public address below."
  value       = aws_instance.reranker.private_ip
}

// The instance has a public IPv4 because it needs egress and this stack has no NAT
// gateway. It is emitted for cost accounting and for confirming the box has a route out —
// NOT as an endpoint. The security group admits the API's SG and nothing else, so curling
// this address times out, and RERANKER_URL pointed at it would send the API's bearer token
// over the public internet.
output "public_ip" {
  description = "Egress address. Not reachable — the SG allows ingress from the API only. Do not put this in RERANKER_URL."
  value       = aws_instance.reranker.public_ip
}

output "instance_id" {
  description = "For `aws ssm start-session --target <id>` when you need a shell."
  value       = aws_instance.reranker.id
}

output "ecr_repository_url" {
  description = "Push target. infra/reranker/push.ps1 reads this."
  value       = aws_ecr_repository.reranker.repository_url
}

output "security_group_id" {
  description = "The reranker's security group, for reference when auditing ingress."
  value       = aws_security_group.reranker.id
}

// Paste-ready, because hand-assembling this from the pieces above is exactly where a
// typo turns into a silent fallback to RRF ordering that nobody notices for a week.
output "env_line" {
  description = "Drop this into the API's .env, then restart the API."
  value       = "RERANKER_URL=http://${aws_instance.reranker.private_ip}:${var.port}"
}

output "next_steps" {
  description = "What to do after apply."
  value       = <<-EOT
    1. Build and push the image:
         ./push.ps1 -Region ${var.region} -Repo ${aws_ecr_repository.reranker.repository_url}
    2. Add to the API's .env (the API key is the value you passed as var.api_key):
         RERANKER_URL=http://${aws_instance.reranker.private_ip}:${var.port}
         RERANKER_API_KEY=<the same secret>
    3. Restart the API, then in the admin panel: Retrieval -> Test connection.
    4. Only once the test passes, switch the toggle on.

    Shell access (no SSH port is open):
         aws ssm start-session --target ${aws_instance.reranker.id} --region ${var.region}
  EOT
}
