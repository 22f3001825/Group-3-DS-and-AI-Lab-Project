#!/usr/bin/env bash
# One-time setup for a fresh Ubuntu 22.04/24.04 or Amazon Linux 2023 VM. Idempotent: safe
# to re-run. The two distributions differ in five places — package manager, how Docker and
# the compose v2 plugin are installed, whether a cron daemon exists at all, and what the
# host firewall is — so each of those sections branches on $PKG, set just below.
#
# Shipped to the box and run by deploy/deploy.ps1 -Bootstrap. It is NOT curl'd from
# raw.githubusercontent.com any more — the repo is private, so an unauthenticated fetch
# 404s, and scp avoids needing a PAT on the box just to read one script.
#
#   bash bootstrap.sh --domain mlt-staging.duckdns.org --duckdns-token <token> \
#                     --ecr-registry <acct>.dkr.ecr.<region>.amazonaws.com
#
# It installs Docker, opens 80/443, adds swap on small boxes, wires up DuckDNS and the
# state backup, and configures ECR pull auth. It deliberately handles NO secrets — the
# .env arrives separately via deploy.ps1, so nothing sensitive is in a shell history.
#
# It does NOT clone anything. The image is built by .github/workflows/image.yml and
# pulled from ECR, so this box needs no source, no checkout and no git credential; the
# four files it does need (docker-compose.yml, deploy/Caddyfile, deploy/update.sh, .env)
# all arrive over scp.
set -euo pipefail

DOMAIN=""
DUCKDNS_TOKEN=""
ECR_REGISTRY=""
APP_DIR="${HOME}/mlt-staging"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--domain)         DOMAIN="$2";        shift 2 ;;
		--duckdns-token)  DUCKDNS_TOKEN="$2"; shift 2 ;;
		--ecr-registry)   ECR_REGISTRY="$2";  shift 2 ;;
		--dir)            APP_DIR="$2";       shift 2 ;;
		-h|--help)
			grep '^#' "$0" | sed 's/^# \?//'
			exit 0 ;;
		*) echo "Unknown option: $1" >&2; exit 2 ;;
	esac
done

[[ -n "$DOMAIN" ]] || { echo "ERROR: --domain is required (e.g. mlt-staging.duckdns.org)" >&2; exit 2; }

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }

# Replace this script's own crontab entries, matched by $1, with the lines in $2..$n.
#
# The obvious one-liner — `( crontab -l | grep -v PATTERN; echo NEW ) | crontab -` — aborts
# the whole bootstrap under `set -euo pipefail`, and does it on exactly the machines this
# script targets. Two normal conditions are reported as failures: `crontab -l` exits 1 when
# the user has no crontab yet (every fresh instance), and `grep -v` exits 1 when it filters
# out every line. pipefail then fails the pipeline and `set -e` kills the script mid-setup,
# after the DuckDNS script has been written but before either cron entry is installed.
#
# So each step is run separately with its failure absorbed, and only the final crontab load
# is allowed to fail the script — because that one really is an error.
replace_cron() {
	local pattern="$1"; shift
	local current filtered
	current="$(crontab -l 2>/dev/null || true)"
	filtered="$(printf '%s\n' "$current" | grep -v "$pattern" || true)"
	{
		# Skip a whitespace-only "existing crontab" so a fresh box does not get a leading
		# blank line prepended on every re-run.
		if [[ -n "${filtered//[[:space:]]/}" ]]; then printf '%s\n' "$filtered"; fi
		printf '%s\n' "$@"
	} | crontab -
}

# ── 0. Which distribution is this ─────────────────────────────────────────────
# Ubuntu's AMIs log in as `ubuntu`, Amazon Linux's as `ec2-user` — but the login name is
# not what anything here depends on, so detect the package manager rather than the ID.
# Both are supported and both are x86-64 for this deployment; APP_UID=1000 happens to be
# correct on either (`ubuntu` and `ec2-user` are both the first non-system user).
if command -v apt-get >/dev/null 2>&1; then
	PKG=apt
elif command -v dnf >/dev/null 2>&1; then
	PKG=dnf
else
	echo "ERROR: neither apt-get nor dnf found. This script supports Ubuntu and Amazon Linux 2023." >&2
	exit 1
fi
OS_NAME="$(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME")"
say "Detected ${OS_NAME:-unknown} (package manager: ${PKG})"

# `sudo usermod -aG docker "$USER"` below needs a name, and $USER is not always exported
# through a non-interactive ssh command.
TARGET_USER="${USER:-$(id -un)}"

# ── 1. Base packages ──────────────────────────────────────────────────────────
# No git: this box holds no checkout.
say "Installing base packages"
if [[ "$PKG" == apt ]]; then
	sudo apt-get update -qq
	sudo apt-get install -y -qq ca-certificates curl python3 iptables-persistent
else
	# Deliberately NOT installing `curl` here: Amazon Linux 2023 ships curl-minimal, and
	# `dnf install curl` fails with a package conflict rather than upgrading it. It already
	# provides /usr/bin/curl, which is all this script and the DuckDNS cron need.
	#
	# cronie IS required: AL2023 ships no cron daemon at all, and both the DuckDNS updater
	# and the state backup below are crontab entries. Without it `crontab -` succeeds and
	# nothing ever runs them — a silent failure that only shows up as a stale DNS record
	# after the first stop/start.
	sudo dnf install -y -q ca-certificates python3 cronie
	sudo systemctl enable --now crond
fi

# ── 2. Docker Engine + compose plugin ─────────────────────────────────────────
if command -v docker >/dev/null 2>&1; then
	say "Docker already present ($(docker --version))"
elif [[ "$PKG" == apt ]]; then
	say "Installing Docker Engine from Docker's apt repository"
	# Ubuntu's own docker.io package ships an old engine without the compose v2 plugin.
	sudo install -m 0755 -d /etc/apt/keyrings
	sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
	sudo chmod a+r /etc/apt/keyrings/docker.asc
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
		| sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
	sudo apt-get update -qq
	sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io \
		docker-buildx-plugin docker-compose-plugin
else
	# Amazon Linux 2023 packages Docker Engine itself, and Docker's own RPM repository does
	# not support AL2023 (its URLs are keyed on a RHEL $releasever that AL does not match).
	say "Installing Docker Engine from the Amazon Linux repositories"
	sudo dnf install -y -q docker
fi

# The compose v2 plugin is a SEPARATE concern from the engine, and only the apt path gets
# it for free: AL2023's `docker` package is the engine alone, so `docker compose` would be
# "unknown command" and every deploy would fail at update.sh's first line. Installed as a
# CLI plugin binary (the officially documented manual install), not the deprecated
# standalone `docker-compose`, because everything here calls `docker compose`.
if ! docker compose version >/dev/null 2>&1; then
	say "Installing the Docker Compose v2 plugin"
	case "$(uname -m)" in
		x86_64)  COMPOSE_ARCH=x86_64 ;;
		aarch64) COMPOSE_ARCH=aarch64 ;;
		*) echo "ERROR: no compose binary published for $(uname -m)" >&2; exit 1 ;;
	esac
	# /releases/latest/download resolves to the newest tag, so there is no version to go
	# stale in this script. The asset name has been stable across every v2 release.
	CLI_PLUGINS=/usr/local/lib/docker/cli-plugins
	sudo mkdir -p "$CLI_PLUGINS"
	sudo curl -fsSL -o "$CLI_PLUGINS/docker-compose" \
		"https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${COMPOSE_ARCH}"
	sudo chmod +x "$CLI_PLUGINS/docker-compose"
	echo "    $(docker compose version)"
fi

sudo usermod -aG docker "$TARGET_USER"

# Cap container logs BEFORE the daemon starts. Docker's default json-file driver has no
# max-size, so a container's stdout grows without bound on the root volume — the only
# unbounded consumer on it, since the box never builds and update.sh prunes images after
# every deploy. A box that is stopped nightly rarely reaches the limit; one left up for a
# month can, and it fails as a full disk rather than as anything mentioning logs.
#
# Merged with any existing daemon.json for the same reason ~/.docker/config.json is below.
say "Capping container log size (3 x 10 MB per container)"
sudo mkdir -p /etc/docker
[[ -f /etc/docker/daemon.json ]] || echo '{}' | sudo tee /etc/docker/daemon.json >/dev/null
sudo python3 - /etc/docker/daemon.json <<'PY'
import json, sys
path = sys.argv[1]
try:
    with open(path) as fh:
        cfg = json.load(fh)
except (ValueError, OSError):
    cfg = {}
cfg["log-driver"] = "json-file"
cfg.setdefault("log-opts", {}).update({"max-size": "10m", "max-file": "3"})
with open(path, "w") as fh:
    json.dump(cfg, fh, indent=2)
PY

# enable, not just start: the box is stopped between demos, and this plus
# `restart: unless-stopped` in docker-compose.yml is what brings the app back on boot
# with nobody SSH'd in.
sudo systemctl enable --now docker
# Applies the log settings above to an ALREADY-RUNNING daemon (re-bootstrapping an
# existing box). A no-op on first boot, and it does not stop containers — the setting
# takes effect for containers created after it, which is every one update.sh recreates.
sudo systemctl reload docker 2>/dev/null || true

# ── 3. ECR pull authentication ────────────────────────────────────────────────
# The credential helper reads the instance profile through the normal AWS credential
# chain and mints a fresh ECR token per pull, so there is no `docker login` to run and no
# 12-hour token to expire. The instance needs a role with AmazonEC2ContainerRegistryReadOnly.
#
# credHelpers (per registry), NOT credsStore (global): credsStore would route EVERY
# registry through ecr-login, including the Docker Hub pull of caddy:2-alpine, which the
# helper cannot serve.
if [[ -n "$ECR_REGISTRY" ]]; then
	say "Configuring ECR pull auth for ${ECR_REGISTRY}"
	if [[ "$PKG" == apt ]]; then
		sudo apt-get install -y -qq amazon-ecr-credential-helper
	else
		sudo dnf install -y -q amazon-ecr-credential-helper
	fi
	mkdir -p "${HOME}/.docker"
	CFG="${HOME}/.docker/config.json"
	[[ -f "$CFG" ]] || echo '{}' > "$CFG"
	# Merged rather than overwritten: docker writes other keys here (auths, plugins) and
	# clobbering them would silently drop any other registry's credentials.
	python3 - "$CFG" "$ECR_REGISTRY" <<'PY'
import json, sys
path, registry = sys.argv[1], sys.argv[2]
try:
    with open(path) as fh:
        cfg = json.load(fh)
except (ValueError, OSError):
    cfg = {}
cfg.setdefault("credHelpers", {})[registry] = "ecr-login"
with open(path, "w") as fh:
    json.dump(cfg, fh, indent=2)
PY
	echo "    credHelpers → ecr-login for ${ECR_REGISTRY}"
else
	say "No --ecr-registry given — skipping ECR auth setup"
	echo "    'docker compose pull' will fail on a private ECR image until this is set."
fi

# ── 4. Firewall ───────────────────────────────────────────────────────────────
# THE classic silent failure. Oracle's and AWS's Ubuntu images ship an iptables INPUT
# chain ending in a REJECT rule, so opening 80/443 in the cloud console's security group
# is only half the job — the packets still die on the host. Without this, Caddy's ACME
# HTTP-01 challenge times out and you get a certificate error with no obvious cause.
#
# Amazon Linux 2023 is the opposite: it ships no firewalld, no iptables rules and an empty
# INPUT chain, so the Security Group is the only gate and there is nothing to open. Doing
# it anyway would mean installing iptables-services purely to persist rules that permit
# what is already permitted.
say "Opening TCP 80 and 443"
if [[ "$PKG" == apt ]]; then
	for port in 80 443; do
		if ! sudo iptables -C INPUT -p tcp --dport "$port" -j ACCEPT 2>/dev/null; then
			# Insert ABOVE the trailing REJECT rather than appending after it.
			sudo iptables -I INPUT -p tcp --dport "$port" -m conntrack --ctstate NEW -j ACCEPT
		fi
	done
	sudo netfilter-persistent save >/dev/null 2>&1 || sudo iptables-save | sudo tee /etc/iptables/rules.v4 >/dev/null
	if command -v ufw >/dev/null 2>&1 && sudo ufw status | grep -q "Status: active"; then
		sudo ufw allow 80/tcp  >/dev/null
		sudo ufw allow 443/tcp >/dev/null
	fi
elif systemctl is-active --quiet firewalld 2>/dev/null; then
	sudo firewall-cmd --permanent --add-service=http  >/dev/null
	sudo firewall-cmd --permanent --add-service=https >/dev/null
	sudo firewall-cmd --reload >/dev/null
	echo "    firewalld: http + https allowed"
else
	echo "    No host firewall active — the Security Group is the only gate."
fi
echo "    Reminder: also add ingress rules for TCP 80 and 443 in your cloud console"
echo "    (AWS: the instance's Security Group; Oracle: VCN → Security List)."

# ── 5. Swap on small instances ────────────────────────────────────────────────
# Steady state is ~500-700 MB but the first model load peaks near 1 GB, so a 1 GB box
# (t3.micro, t2.micro) OOM-kills the container mid-warm-up without this.
#
# The threshold is 3 GB rather than 2 so a t3.small also gets a swapfile: with the
# reranker profile on, two ONNX models can be constructing sessions at the same moment,
# and `free -m` on a 2 GiB box reports ~1900, which is under 2048 only by accident of
# accounting. A t3.medium (the default, ~3900 MB) is above the line and gets none — it has
# the headroom in RAM, and swap is not a substitute for it: the box would still be slow if
# it ever swapped an inference.
TOTAL_MB=$(free -m | awk '/^Mem:/{print $2}')
if (( TOTAL_MB < 3072 )) && [[ ! -f /swapfile ]]; then
	say "Only ${TOTAL_MB} MB RAM — creating a 2 GB swapfile"
	sudo fallocate -l 2G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
	sudo chmod 600 /swapfile
	sudo mkswap /swapfile
	sudo swapon /swapfile
	grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
else
	say "RAM: ${TOTAL_MB} MB — no swapfile needed"
fi

mkdir -p "${APP_DIR}/state"

# ── 6. DuckDNS refresher ──────────────────────────────────────────────────────
# Load-bearing, not belt-and-braces, now that this box runs without an Elastic IP: an EIP
# bills $0.005/hr even while the instance is stopped, so the instance takes a NEW
# auto-assigned public IP on every start. `&ip=` empty makes DuckDNS infer the address
# from the request source, which is exactly what that needs.
if [[ -n "$DUCKDNS_TOKEN" ]]; then
	SUB="${DOMAIN%%.duckdns.org}"
	if [[ "$SUB" == "$DOMAIN" ]]; then
		say "Domain is not a duckdns.org name — skipping the DDNS updater"
	else
		say "Installing the DuckDNS updater for '${SUB}'"
		mkdir -p "${HOME}/.duckdns"
		cat > "${HOME}/.duckdns/update.sh" <<EOF
#!/usr/bin/env bash
curl -fsS "https://www.duckdns.org/update?domains=${SUB}&token=${DUCKDNS_TOKEN}&ip=" \
  -o "${HOME}/.duckdns/last.log" 2>&1
EOF
		# 700, not 755: the file embeds the DuckDNS token.
		chmod 700 "${HOME}/.duckdns/update.sh"
		"${HOME}/.duckdns/update.sh" || true
		# @reboot as well as every 5 minutes. Without the @reboot entry a freshly started
		# instance serves a stale DNS record for up to five minutes — which, on a box that
		# exists to be started five minutes before a demo, is the whole startup budget.
		# The sleep waits for the network to be routable; cron fires early in boot.
		replace_cron '\.duckdns/update\.sh' \
			"@reboot sleep 15 && ${HOME}/.duckdns/update.sh >/dev/null 2>&1" \
			"*/5 * * * * ${HOME}/.duckdns/update.sh >/dev/null 2>&1"
		echo "    DuckDNS says: $(cat "${HOME}/.duckdns/last.log" 2>/dev/null || echo '?')  (expect 'OK')"
	fi
fi

# ── 7. State backup ───────────────────────────────────────────────────────────
# state/mlt_learner.db is the single point of truth — every student, quiz attempt and
# mastery row, plus the question bank's vector BLOBs — and there is no replica anywhere.
#
# @reboot is the one that actually runs. A demo box is off at 03:17, so the daily entry
# below would fire approximately never; @reboot snapshots the PREVIOUS demo's state
# before this one starts mutating it. The daily entry is kept for the case where the box
# does stay up for a stretch. Both name the file by date, so running both in one day just
# rewrites the same snapshot.
say "Installing state backups (@reboot + daily, 7-day rotation)"
BACKUP_CMD="cd ${APP_DIR} && [ -f state/mlt_learner.db ] && cp state/mlt_learner.db state/backup-\$(date +\\%F).db && find state -name 'backup-*.db' -mtime +7 -delete"
replace_cron 'mlt-staging-backup' \
	"@reboot ${BACKUP_CMD} # mlt-staging-backup" \
	"17 3 * * * ${BACKUP_CMD} # mlt-staging-backup"

cat <<EOF

────────────────────────────────────────────────────────────────────────────────
 Bootstrap complete.

 Next, FROM YOUR WINDOWS MACHINE:

   .\\deploy\\deploy.ps1 -Server $(whoami)@<this-ip> -Key ~\\.ssh\\<key> \`
       -Env .env.staging -SeedDb

 That ships the secrets and the seeded database, pulls the image and starts everything.

 Before it will work end to end, confirm:
   * TCP 80 + 443 are open in the instance's SECURITY GROUP (not just iptables above)
   * ${DOMAIN} resolves to this machine's current public IP
   * https://${DOMAIN} is an Authorized JavaScript origin on your Google OAuth Web client
   * this instance has an IAM role granting AmazonEC2ContainerRegistryReadOnly
   * the image has been built at least once by the GitHub Actions workflow

 NOTE: your user was added to the 'docker' group. Log out and back in (or run
 'newgrp docker') before running docker commands by hand.
────────────────────────────────────────────────────────────────────────────────
EOF
