#!/usr/bin/env bash
# Runs ON THE SERVER. Pull the CI-built image, verify it matches this box, restart, and
# refuse to report success unless the app actually answers. Normally invoked over SSH by
# deploy/deploy.ps1, but it is also fine to run by hand:
#     bash ~/mlt-staging/deploy/update.sh
#
#   --dir <path>   deployment directory (default: this script's parent directory)
#   --tag <tag>    image tag to deploy (default: whatever IMAGE_REF in .env names)
#
# There is no git here and no build step. The repo is private and the image is built by
# .github/workflows/image.yml and pushed to ECR, so this box holds no source, no checkout
# and no credential for either — only docker-compose.yml, deploy/Caddyfile, .env and
# state/, all of which deploy.ps1 ships over scp.
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TAG=""

while [[ $# -gt 0 ]]; do
	case "$1" in
		--dir) APP_DIR="$2"; shift 2 ;;
		--tag) TAG="$2";     shift 2 ;;
		*) echo "Unknown option: $1" >&2; exit 2 ;;
	esac
done

cd "$APP_DIR"

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
fail() { printf '\n\033[1;31mFAILED: %s\033[0m\n' "$*" >&2; }

# ── Preflight ─────────────────────────────────────────────────────────────────
# Checked before anything is torn down, so a missing .env costs nothing.
if [[ ! -f .env ]]; then
	fail "No .env in ${APP_DIR}. Push one:  deploy.ps1 ... -Env .env.staging"
	exit 1
fi
if [[ ! -f docker-compose.yml ]]; then
	fail "No docker-compose.yml in ${APP_DIR}. Run:  deploy.ps1 ... -Bootstrap"
	exit 1
fi
# Defensive, and idempotent. deploy.ps1 already strips these on upload, but a .env that
# reached the box any other way (scp by hand, an editor on Windows) carries CRLF endings
# and possibly a UTF-8 BOM. Left alone, the BOM corrupts the first key and every value
# ends in \r — which becomes a certificate request for "domain\r" and an API URL with an
# invisible carriage return compared against the image labels below.
if LC_ALL=C grep -q $'\r' .env || [[ "$(LC_ALL=C head -c 3 .env)" == $'\xEF\xBB\xBF' ]]; then
	say "Normalising .env (stripping CR / BOM)"
	sed -i -e '1s/^\xEF\xBB\xBF//' -e 's/\r$//' .env
fi

for required in STAGING_DOMAIN VITE_API_URL VITE_GOOGLE_CLIENT_ID GOOGLE_CLIENT_ID JWT_SECRET QDRANT_URL IMAGE_REF; do
	if ! grep -qE "^${required}=.+" .env; then
		fail "${required} is missing or empty in .env"
		exit 1
	fi
done
mkdir -p state

env_value() { grep -E "^${1}=" .env | head -1 | cut -d= -f2- | sed "s/[\"' ]//g"; }

# ── CLIProxyAPI preflight (only when .env opts in) ────────────────────────────
# Two failure modes worth catching before anything is torn down, both of which otherwise
# surface as a container that exits immediately with a message about a file:
#
#   * a MISSING config file - docker creates a DIRECTORY at the bind-mount source, and the
#     proxy reports "failed to read config file: ... is a directory", which reads like
#     corruption rather than an absent file;
#   * a config without an explicit absolute auth-dir - upstream does not apply its own
#     documented default under Docker and exits with an empty-path mkdir error.
#     See https://github.com/router-for-me/CLIProxyAPI/issues/3272
if grep -qE '^COMPOSE_PROFILES=.*\bcliproxy\b' .env; then
	say "CLIProxyAPI is enabled - checking its config"
	if ! grep -qE '^CLIPROXY_IMAGE_REF=.+' .env; then
		fail "COMPOSE_PROFILES enables cliproxy but CLIPROXY_IMAGE_REF is not set in .env."
		echo "    docker-compose.yml falls back to a placeholder name that does not exist,"
		echo "    so the pull would fail. Set it, or drop cliproxy from COMPOSE_PROFILES."
		exit 1
	fi
	if [[ -d deploy/cliproxy.config.yaml ]]; then
		fail "deploy/cliproxy.config.yaml is a DIRECTORY. Docker created it when the file was missing."
		echo "    rmdir it and re-run:  deploy.ps1 ... -Env .env   (which ships the real file)"
		exit 1
	fi
	if [[ ! -f deploy/cliproxy.config.yaml ]]; then
		fail "COMPOSE_PROFILES enables cliproxy but deploy/cliproxy.config.yaml is missing."
		echo "    Copy deploy/cliproxy.config.example.yaml locally, fill in api-keys, and deploy"
		echo "    with -Env so it is shipped. Nothing was changed."
		exit 1
	fi
	if ! grep -qE '^\s*auth-dir:\s*"?/' deploy/cliproxy.config.yaml; then
		fail "cliproxy.config.yaml has no absolute auth-dir. The container would exit at startup."
		echo "    Add:  auth-dir: \"/root/.cli-proxy-api\""
		exit 1
	fi
	mkdir -p cliproxy/auth cliproxy/plugins
	chmod 700 cliproxy/auth
	if ! ls cliproxy/auth/*.json >/dev/null 2>&1; then
		echo "    WARNING: no provider credentials in cliproxy/auth - the proxy will start but"
		echo "    answer nothing. Ship them with:  deploy\\cliproxy.ps1 -SeedAuth -Server ..."
	fi
fi

IMAGE_REF="$(env_value IMAGE_REF)"
if [[ -n "$TAG" ]]; then
	IMAGE_REF="${IMAGE_REF%:*}:${TAG}"
	say "Deploying pinned tag: ${IMAGE_REF}"
fi
# Exported so compose interpolates THIS value: a shell variable outranks the .env file,
# which is what makes --tag work without editing .env.
export IMAGE_REF

# ── Pull ──────────────────────────────────────────────────────────────────────
say "Pulling ${IMAGE_REF}"
if ! docker compose pull; then
	fail "Could not pull the image."
	echo
	echo "  * ECR auth is the usual cause. It comes from the instance profile via the"
	echo "    credential helper, so check the instance has a role with"
	echo "    AmazonEC2ContainerRegistryReadOnly and that ~/.docker/config.json contains"
	echo "    \"credsStore\": \"ecr-login\".  Re-run deploy/bootstrap.sh to fix both."
	echo "  * If the tag does not exist, check the Actions run that should have pushed it."
	exit 1
fi

# ── Verify the image matches THIS box ─────────────────────────────────────────
# Three values are compiled into the image and cannot be corrected at runtime. While the
# image was built here they came from this same .env at the same moment, so they could not
# disagree; CI sets them elsewhere, at another time, and every mismatch fails in a way
# that is hard to trace back:
#
#   VITE_GOOGLE_CLIENT_ID  →  Google's `aud` check rejects every sign-in
#   VITE_API_URL           →  the bundle calls the wrong origin
#   APP_UID                →  "attempt to write a readonly database" on the first write
#
# Better to refuse to start than to serve any of those.
say "Verifying the image matches this deployment"

image_label() { docker image inspect --format "{{index .Config.Labels \"$1\"}}" "$IMAGE_REF" 2>/dev/null || true; }

MISMATCH=0
check_label() {
	local label="$1" expected="$2" what="$3" consequence="$4" actual
	actual="$(image_label "$label")"
	if [[ -z "$actual" ]]; then
		fail "The image carries no ${label} label."
		echo "    It predates the provenance labels in the Dockerfile. Re-run the"
		echo "    'Build and push staging image' workflow and deploy again."
		MISMATCH=1
	elif [[ "$actual" != "$expected" ]]; then
		fail "${what} disagrees between the image and this server."
		echo "    image:  ${actual}"
		echo "    server: ${expected}"
		echo "    ${consequence}"
		MISMATCH=1
	else
		echo "    ${what}: OK"
	fi
}

check_label org.mlt.vite-api-url "$(env_value VITE_API_URL)" \
	"VITE_API_URL" \
	"The bundle would call the wrong origin. Fix the repository variable and rebuild."
check_label org.mlt.vite-google-client-id "$(env_value VITE_GOOGLE_CLIENT_ID)" \
	"VITE_GOOGLE_CLIENT_ID" \
	"Google's aud check would reject every sign-in. Fix the repository variable and rebuild."
check_label org.mlt.app-uid "$(id -u)" \
	"APP_UID" \
	"./state is a bind mount that keeps host ownership, so SQLite would fail with 'attempt to write a readonly database'. Either rebuild with APP_UID=$(id -u), or chown state to the image's UID."

# The fourth compiled-in fact, and the only one Docker records itself rather than in a
# label: the CPU architecture. The workflow builds linux/amd64 for this x86-64 box, and a
# mismatch starts a container that immediately dies with "exec format error" — a message
# that names neither the image nor the cause. docker-compose.yml asks for linux/amd64, so
# a wrong image usually fails at pull; this catches the ones that are already on disk.
HOST_ARCH="$(dpkg --print-architecture 2>/dev/null || uname -m)"
case "$HOST_ARCH" in
	x86_64)  HOST_ARCH=amd64 ;;
	aarch64) HOST_ARCH=arm64 ;;
esac
IMAGE_ARCH="$(docker image inspect --format '{{.Architecture}}' "$IMAGE_REF" 2>/dev/null || true)"
if [[ -n "$IMAGE_ARCH" && "$IMAGE_ARCH" != "$HOST_ARCH" ]]; then
	fail "Architecture disagrees between the image and this server."
	echo "    image:  ${IMAGE_ARCH}"
	echo "    server: ${HOST_ARCH}"
	echo "    The container would die with 'exec format error'. The workflow pins"
	echo "    linux/amd64 (an x86-64 instance); an arm64/Graviton box needs either an"
	echo "    x86-64 instance or a rebuild with platforms: linux/arm64."
	MISMATCH=1
else
	echo "    Architecture: OK (${IMAGE_ARCH:-unknown})"
fi

if (( MISMATCH )); then
	fail "Refusing to start. Nothing was changed."
	exit 1
fi

# ── Start ─────────────────────────────────────────────────────────────────────
# --no-build: docker-compose.yml keeps a `build:` block for local development, and this
# box has no source. Without the flag a missing image would trigger a build that fails on
# a missing Dockerfile, which is a far less obvious error than "image not found".
say "Starting containers"
docker compose up -d --remove-orphans --no-build

# ── Health gate ───────────────────────────────────────────────────────────────
say "Waiting for /health"
HEALTHY=0
for _ in $(seq 1 45); do        # 45 x 2s = 90s
	if curl -fsS --max-time 3 http://127.0.0.1:8000/health >/dev/null 2>&1; then
		HEALTHY=1
		break
	fi
	sleep 2
done

if (( ! HEALTHY )); then
	fail "The API never answered /health within 90s."
	echo
	docker compose ps
	echo
	docker compose logs --tail=60 api
	exit 1
fi
echo "    API is up."

# ── Warm-up (advisory) ────────────────────────────────────────────────────────
# The lifespan thread loads the embedding models off the request path. Not being warm is
# not a failure — it only means the first user pays the ONNX init — so this never exits
# non-zero. It IS the fastest way to spot an unreachable Qdrant, though.
say "Waiting for retrieval warm-up (advisory)"
WARM=0
for _ in $(seq 1 30); do        # 30 x 2s = 60s
	if docker compose logs api 2>/dev/null | grep -q "Warm-up complete"; then
		WARM=1; break
	fi
	if docker compose logs api 2>/dev/null | grep -q "Warm-up skipped"; then
		echo "    Warm-up FAILED — check QDRANT_URL / QDRANT_API_KEY:"
		docker compose logs api | grep "Warm-up skipped" | tail -1
		break
	fi
	sleep 2
done
(( WARM )) && echo "    Retrieval is warm."

# ── Housekeeping ──────────────────────────────────────────────────────────────
# Matters more than it used to: every deploy pulls a new image and leaves the previous
# one untagged on a 16 GB volume.
say "Pruning superseded images"
docker image prune -f >/dev/null

DOMAIN="$(env_value STAGING_DOMAIN)"
IMAGE_ID="$(docker image inspect --format '{{.Id}}' "$IMAGE_REF" 2>/dev/null | cut -c8-19)"
cat <<EOF

────────────────────────────────────────────────────────────────────────────────
 Deployed:  https://${DOMAIN}
 Image:     ${IMAGE_REF}
 Image id:  ${IMAGE_ID:-unknown}
 State:     $(du -h state/mlt_learner.db 2>/dev/null | cut -f1 || echo 'no DB yet — use deploy.ps1 -SeedDb')

 The first request over HTTPS may take a few seconds while Caddy obtains the
 certificate. Watch it with:  docker compose logs -f caddy
────────────────────────────────────────────────────────────────────────────────
EOF
