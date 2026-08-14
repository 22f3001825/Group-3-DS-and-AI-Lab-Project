<#
.SYNOPSIS
    Build the cross-encoder reranker image, push it to ECR, and restart it on staging.

.DESCRIPTION
    The reranker runs as a fourth container in the staging compose stack (service
    `reranker`, profile `reranker`). This script is the build half.

    Why not GitHub Actions, when the API image is built there: the source is reranker/
    app.py plus a pinned model, which changes approximately never, and the build downloads
    ~80 MB of ONNX weights to bake into the image. Spending Actions minutes on that for
    every push to main buys nothing. Same reasoning as deploy/cliproxy.ps1, for the same
    kind of image.

    Why a SEPARATE ECR repository from the API's: the lifecycle policy on that one keeps
    the latest 2 images, so two MLT builds would evict the reranker and the next deploy
    would fail on a missing image. deploy/terraform creates it as
    <ecr_repository_name>/reranker when create_reranker_repo is true.

    KEEP THIS FILE ASCII-ONLY - see the note in deploy.ps1 for why a stray em dash breaks
    Windows PowerShell 5.1 parsing in a way that reports an unrelated error.

.EXAMPLE
    # Build and push
    .\deploy\reranker.ps1 -Build -Push -Env .env.staging

.EXAMPLE
    # Pull the new image and restart just this service on the box
    .\deploy\reranker.ps1 -Restart -Server ec2-user@1.2.3.4 -Key ~\.ssh\iitm-2026.pem

.EXAMPLE
    # Check what the API can actually reach, without deploying anything
    .\deploy\reranker.ps1 -Probe -Server ec2-user@1.2.3.4 -Key ~\.ssh\iitm-2026.pem
#>
[CmdletBinding()]
param(
    # Build the image locally from reranker/.
    [switch]$Build,

    # Push the built image to ECR. Implies an `aws ecr get-login-password` docker login.
    [switch]$Push,

    # Pull and restart the reranker service on the server. Requires -Server.
    [switch]$Restart,

    # Ask the api container whether it can reach the reranker. Requires -Server.
    [switch]$Probe,

    # Tag to build and push. The default matches what .env's RERANKER_IMAGE_REF names;
    # pass a git sha for a pinned rollout.
    [string]$Tag,

    # Env file holding RERANKER_IMAGE_REF (and IMAGE_REF, from which the registry is
    # derived when RERANKER_IMAGE_REF is absent).
    [Alias('Env')][string]$EnvFile = '.env',

    [string]$Server,
    [string]$Key,
    [string]$AppDir = 'mlt-staging'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot

function Write-Step { param([string]$Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Fail { param([string]$Text) Write-Host "FAILED: $Text" -ForegroundColor Red }

if (-not ($Build -or $Push -or $Restart -or $Probe)) {
    Write-Fail 'Nothing to do. Pass -Build, -Push, -Restart or -Probe.'
    exit 2
}

# -- Resolve the image reference ----------------------------------------------
$envPath = Join-Path $RepoRoot $EnvFile
if (-not (Test-Path $envPath)) { $envPath = $EnvFile }

function Get-EnvValue {
    param([string]$Name)
    if (-not (Test-Path $envPath)) { return $null }
    $match = Get-Content $envPath | Where-Object { $_ -match "^\s*$Name\s*=" } | Select-Object -First 1
    if (-not $match) { return $null }
    return ($match -replace "^\s*$Name\s*=", '').Trim().Trim('"').Trim("'")
}

$imageRef = $null
$registry = $null
$region   = $null
if ($Build -or $Push) {
    $imageRef = Get-EnvValue 'RERANKER_IMAGE_REF'
    if (-not $imageRef) {
        # Derive from IMAGE_REF so a fresh setup needs one fewer hand-copied hostname.
        $mltRef = Get-EnvValue 'IMAGE_REF'
        if ($mltRef -match '^([^/]+)/(.+):[^:]+$') {
            $imageRef = "$($Matches[1])/$($Matches[2])/reranker:latest"
            Write-Host "    RERANKER_IMAGE_REF unset; defaulting to $imageRef"
            Write-Host '    Set it explicitly in the env file if your repository is named differently.'
        } else {
            Write-Fail "Set RERANKER_IMAGE_REF in $EnvFile (e.g. <acct>.dkr.ecr.<region>.amazonaws.com/reranker:latest)."
            Write-Host '    terraform output reranker_image_ref prints it verbatim.'
            exit 2
        }
    }
    if ($imageRef -notmatch '^[^/]+/[^:]+:.+$') {
        Write-Fail "RERANKER_IMAGE_REF ('$imageRef') does not look like <registry>/<repository>:<tag>."
        exit 2
    }
    if ($Tag) { $imageRef = ($imageRef -replace ':[^:]+$', '') + ':' + $Tag }
    $registry = $imageRef.Split('/')[0]
    $region   = if ($registry -match '\.dkr\.ecr\.([^.]+)\.amazonaws\.com$') { $Matches[1] } else { $null }
}

# -- Build ---------------------------------------------------------------------
if ($Build) {
    $context = Join-Path $RepoRoot 'reranker'
    if (-not (Test-Path (Join-Path $context 'Dockerfile'))) {
        Write-Fail "No Dockerfile in $context."
        exit 2
    }

    Write-Step "Building $imageRef from reranker/"
    Write-Host '    The build downloads ~80 MB of ONNX weights and bakes them in, so the first'
    Write-Host '    build is slow and every later one is cached. That is deliberate: without it'
    Write-Host '    the container fetches from HuggingFace on every cold start.'

    # --platform is explicit because this Dockerfile does NOT pin it internally (unlike the
    # API's runtime stage). Building on an ARM machine would otherwise produce an image the
    # x86-64 instance cannot run, and it would fail as an exec-format error at startup.
    docker build --platform linux/amd64 -t $imageRef $context
    if ($LASTEXITCODE -ne 0) { Write-Fail "docker build exited $LASTEXITCODE"; exit $LASTEXITCODE }

    $arch = (docker image inspect --format '{{.Architecture}}' $imageRef)
    Write-Host "    Built $imageRef ($arch)"
    if ($arch -ne 'amd64') { Write-Fail "Image architecture is '$arch', not amd64. The instance cannot run it."; exit 1 }
}

# -- Push ----------------------------------------------------------------------
if ($Push) {
    if (-not $region) { Write-Fail "Cannot derive the AWS region from '$registry'."; exit 2 }
    Write-Step "Logging in to $registry"
    $pw = aws ecr get-login-password --region $region
    if ($LASTEXITCODE -ne 0) { Write-Fail 'aws ecr get-login-password failed. Is the AWS CLI configured for the right account?'; exit 1 }
    $pw | docker login --username AWS --password-stdin $registry
    if ($LASTEXITCODE -ne 0) { Write-Fail 'docker login failed.'; exit 1 }

    Write-Step "Pushing $imageRef"
    Write-Host '    ~1 GB on the first push of a given layer set; later pushes send only what changed.'
    docker push $imageRef
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "docker push exited $LASTEXITCODE"
        # ECR answers 403 for a repository that does not exist, so the two causes are
        # indistinguishable from the error text alone - and neither is "wrong password",
        # which is what a 403 normally suggests. ECR never creates a repository on push.
        $repoName = ($imageRef -replace '^[^/]+/', '') -replace ':[^:]+$', ''
        Write-Host "    403 Forbidden and 'repository does not exist' are the SAME two causes:"
        Write-Host "      1. the repository '$repoName' has not been created. Either set"
        Write-Host "         create_reranker_repo = true and re-apply deploy\terraform, or:"
        Write-Host "         aws ecr create-repository --repository-name $repoName --region $region --image-tag-mutability MUTABLE"
        Write-Host "      2. your IAM policy does not cover it. Its ARN is its own, even when the name"
        Write-Host "         shares a prefix with another repository:"
        Write-Host "         arn:aws:ecr:${region}:<account>:repository/$repoName"
        exit 1
    }
    Write-Host "    Pushed $imageRef"
}

# -- Remote helpers ------------------------------------------------------------
# Same treatment deploy.ps1 gives ssh: judge by exit code only, because PowerShell 5.1
# turns any stderr line from a native command into a terminating error.
function Invoke-Remote {
    param([string]$Command, [switch]$Quiet)
    $sshArgs = @('-o', 'StrictHostKeyChecking=accept-new')
    if ($Key) { $sshArgs += @('-i', $Key) }
    $prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try {
        if ($Quiet) { $out = & ssh @sshArgs $Server $Command 2>$null } else { & ssh @sshArgs $Server $Command }
    } finally { $ErrorActionPreference = $prev }
    if ($Quiet) { return $out }
}

# -- Restart on the server -----------------------------------------------------
if ($Restart) {
    if (-not $Server) { Write-Fail '-Restart needs -Server ec2-user@<ip>.'; exit 2 }

    Write-Step "Pulling and restarting the reranker on $Server"
    Write-Host '    Only this service is touched. The api and caddy containers keep serving,'
    Write-Host '    and requests during the gap fall back to retrieval order rather than failing.'

    # --no-deps for exactly that reason: without it compose would also recreate anything
    # this service is declared to depend on, which on a live box means an avoidable
    # restart of the API.
    Invoke-Remote "cd ~/$AppDir && docker compose pull reranker && docker compose up -d --no-deps reranker && docker image prune -f >/dev/null"
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Remote restart exited $LASTEXITCODE"
        Write-Host '    If this is the first deploy of the reranker, check that .env has'
        Write-Host '    COMPOSE_PROFILES including `reranker` - without the profile, compose'
        Write-Host '    reports "no such service: reranker".'
        exit 1
    }
    $Probe = $true
}

# -- Probe ---------------------------------------------------------------------
if ($Probe) {
    if (-not $Server) { Write-Fail '-Probe needs -Server ec2-user@<ip>.'; exit 2 }

    Write-Step 'Asking the api container whether it can reach the reranker'
    Write-Host '    Probed from INSIDE the api container: that is the only position that proves'
    Write-Host '    what matters. The reranker publishes no host port, so curling the box does'
    Write-Host '    not test the path the API actually uses.'

    $health = Invoke-Remote -Quiet "cd ~/$AppDir && docker compose exec -T api curl -fsS --max-time 5 http://reranker:8080/health 2>/dev/null || true"
    if ($health -match '"status"\s*:\s*"ok"') {
        Write-Host "    Reranker is healthy: $health" -ForegroundColor Green
        Write-Host '    It is still OFF until an admin turns it on:'
        Write-Host '      Settings -> Retrieval -> Cross-encoder reranking -> Test connection, then enable.'
    } elseif ($health -match '"status"\s*:\s*"loading"') {
        Write-Host '    Reranker is still constructing its ONNX session (up to ~90s on a burstable vCPU).'
        Write-Host '    Re-run with -Probe in a minute.'
    } else {
        Write-Fail 'The api container could not reach http://reranker:8080/health'
        Write-Host '    Check, in this order:'
        Write-Host '      1. .env has `reranker` in COMPOSE_PROFILES  (else the container does not exist)'
        Write-Host "      2. docker compose ps          on the box - is it running or restarting?"
        Write-Host "      3. docker compose logs --tail=40 reranker"
        Write-Host '      4. .env has RERANKER_URL=http://reranker:8080 - an IP address cannot work'
        exit 1
    }
}

Write-Host "`nDone." -ForegroundColor Green
