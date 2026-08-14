#!/bin/bash
# Bootstrap for the reranker instance. Rendered by Terraform's templatefile(), so a bare
# dollar-brace is a Terraform interpolation and a SHELL variable must be written with a
# doubled dollar sign to survive rendering. (This paragraph avoids writing either form
# literally: templatefile parses comments too, and an unescaped example here is itself a
# syntax error — which is exactly how this file failed to validate the first time.)
#
# Runs once per instance. Because main.tf sets user_data_replace_on_change, editing this
# file replaces the instance rather than leaving a stale box running old instructions.
set -euxo pipefail

REGION="${aws_region}"
IMAGE="${ecr_repo_url}:${image_tag}"
REGISTRY="$(echo "${ecr_repo_url}" | cut -d/ -f1)"
PORT="${port}"

# ── Docker ────────────────────────────────────────────────────────────────────
dnf install -y docker
systemctl enable --now docker

# ── Credentials ───────────────────────────────────────────────────────────────
# The key is fetched at boot and written to a root-only env file. It is deliberately NOT
# passed on the `docker run` command line, where it would be visible to anyone who can
# run `docker inspect` or read /proc.
API_KEY="$(aws ssm get-parameter \
  --name "${ssm_param_name}" \
  --with-decryption \
  --region "$${REGION}" \
  --query 'Parameter.Value' \
  --output text)"

install -m 600 /dev/null /etc/reranker.env
cat > /etc/reranker.env <<EOF
RERANKER_API_KEY=$${API_KEY}
EOF
unset API_KEY

# ── Pull ──────────────────────────────────────────────────────────────────────
aws ecr get-login-password --region "$${REGION}" \
  | docker login --username AWS --password-stdin "$${REGISTRY}"
docker pull "$${IMAGE}"

# ── Service ───────────────────────────────────────────────────────────────────
# systemd rather than `docker run --restart=always` alone: this re-authenticates to ECR
# and re-pulls on every start, so a rebooted instance picks up a newly pushed image
# instead of silently running whatever it had cached at first boot.
cat > /etc/systemd/system/reranker.service <<EOF
[Unit]
Description=MLT cross-encoder reranker
After=docker.service
Requires=docker.service

[Service]
Restart=always
RestartSec=10
TimeoutStartSec=600
ExecStartPre=-/usr/bin/docker rm -f reranker
ExecStartPre=/bin/sh -c 'aws ecr get-login-password --region $${REGION} | docker login --username AWS --password-stdin $${REGISTRY}'
ExecStartPre=/usr/bin/docker pull $${IMAGE}
# One line on purpose. This heredoc is unquoted (it has to be — REGION, IMAGE and PORT
# are substituted below), and in an unquoted heredoc a trailing backslash is consumed as
# a line continuation rather than emitted. Backslash-wrapping this command would silently
# join it onto one line anyway; writing it that way makes what ships obvious.
ExecStart=/usr/bin/docker run --rm --name reranker --env-file /etc/reranker.env -p $${PORT}:8080 --memory=1500m $${IMAGE}
ExecStop=/usr/bin/docker stop reranker

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now reranker.service

# Leave a breadcrumb for anyone who SSMs in wondering whether bootstrap finished.
echo "reranker bootstrap complete: $${IMAGE} on port $${PORT}" > /var/log/reranker-bootstrap.done
