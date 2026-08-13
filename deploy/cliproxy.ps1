<#
.SYNOPSIS
    Build CLIProxyAPI from upstream, push it to ECR, and ship its credentials to staging.

.DESCRIPTION
    Unlike the MLT image, this one is NOT built by GitHub Actions: the source is a third-
    party repository, so there is nothing in our workflow to hook it to and no reason to
    spend Actions minutes on someone else's release cadence. It is built here, from the
    upstream git ref you name, and pushed to a SECOND ECR repository.

    Why a second repository rather than another tag in iitm/ailab: the lifecycle policy on
    that repo keeps only the latest 2 images, so two MLT builds would evict the proxy and
    the next deploy would fail on a missing image.

    KEEP THIS FILE ASCII-ONLY - see the note in deploy.ps1 for why a stray em dash breaks
    Windows PowerShell 5.1 parsing in a way that reports an unrelated error.

.EXAMPLE
    # Build the pinned upstream ref and push it
    .\deploy\cliproxy.ps1 -Build -Push -Env .env

.EXAMPLE
    # Authenticate a provider LOCALLY (a browser opens), then ship the credentials up
    .\deploy\cliproxy.ps1 -Login codex
    .\deploy\cliproxy.ps1 -SeedAuth -Server ec2-user@1.2.3.4 -Key ~\.ssh\iitm-2026.pem
#>
[CmdletBinding()]
param(
    # Build the image locally from upstream.
    [switch]$Build,

    # Push the built image to ECR. Implies an `aws ecr get-login-password` docker login.
    [switch]$Push,

    # Run a provider OAuth login on THIS machine, writing credentials to -AuthDir.
    # One of: codex, claude, antigravity, gemini, qwen.
    [string]$Login,

    # Upload -AuthDir to the server. Requires -Server.
    [switch]$SeedAuth,

    # Upstream git ref to build. Pin a tag for anything you care about reproducing;
    # 'main' is a moving target on a third-party repo.
    [string]$Ref = 'main',

    # Env file holding CLIPROXY_IMAGE_REF (and IMAGE_REF, from which the registry is
    # derived when CLIPROXY_IMAGE_REF is absent).
    [Alias('Env')][string]$EnvFile = '.env',

    # Where provider credentials live on THIS machine.
    [string]$AuthDir = "$env:USERPROFILE\.cli-proxy-api",

    [string]$Server,
    [string]$Key,
    [string]$AppDir = 'mlt-staging',
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$UpstreamRepo = 'https://github.com/router-for-me/CLIProxyAPI.git'

function Write-Step { param([string]$Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Fail { param([string]$Text) Write-Host "FAILED: $Text" -ForegroundColor Red }

if (-not ($Build -or $Push -or $Login -or $SeedAuth)) {
    Write-Fail 'Nothing to do. Pass -Build, -Push, -Login <provider> or -SeedAuth.'
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
if ($Build -or $Push) {
    $imageRef = Get-EnvValue 'CLIPROXY_IMAGE_REF'
    if (-not $imageRef) {
        # Derive from IMAGE_REF so a fresh setup needs one fewer hand-copied hostname.
        $mltRef = Get-EnvValue 'IMAGE_REF'
        if ($mltRef -match '^([^/]+)/') {
            $imageRef = "$($Matches[1])/iitm/ailab/cliproxy:latest"
            Write-Host "    CLIPROXY_IMAGE_REF unset; defaulting to $imageRef"
            Write-Host '    Set it explicitly in the env file if your repository is named differently.'
        } else {
            Write-Fail "Set CLIPROXY_IMAGE_REF in $EnvFile (e.g. <acct>.dkr.ecr.<region>.amazonaws.com/iitm/ailab/cliproxy:latest)."
            exit 2
        }
    }
    if ($imageRef -notmatch '^[^/]+/[^:]+:.+$') {
        Write-Fail "CLIPROXY_IMAGE_REF ('$imageRef') does not look like <registry>/<repository>:<tag>."
        exit 2
    }
    $registry = $imageRef.Split('/')[0]
    $region   = if ($registry -match '\.dkr\.ecr\.([^.]+)\.amazonaws\.com$') { $Matches[1] } else { $null }
}

# -- Build ---------------------------------------------------------------------
if ($Build) {
    Write-Step "Building CLIProxyAPI from $UpstreamRepo#$Ref"
    Write-Host '    Docker builds straight from the git URL, so there is no clone to keep in sync.'
    Write-Host '    Upstream is a CGO-enabled Go build on golang:1.26-bookworm; expect a few minutes.'

    $refTag = ($imageRef -replace ':[^:]+$', '') + ':' + ($Ref -replace '[^A-Za-z0-9._-]', '-')
    # --platform is explicit here (unlike our own Dockerfile, which pins it internally)
    # because upstream's Dockerfile does not, and a build on an ARM machine would produce
    # an image the t3.micro cannot run.
    docker build --platform linux/amd64 -t $imageRef -t $refTag "$UpstreamRepo#$Ref"
    if ($LASTEXITCODE -ne 0) { Write-Fail "docker build exited $LASTEXITCODE"; exit $LASTEXITCODE }

    $arch = (docker image inspect --format '{{.Architecture}}' $imageRef)
    Write-Host "    Built $imageRef ($arch) and $refTag"
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
    Write-Host '    ~100 MB, and only on the first push of a given layer set.'
    docker push $imageRef
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "docker push exited $LASTEXITCODE"
        # ECR answers 403 for a repository that does not exist, so the two causes are
        # indistinguishable from the error text alone - and neither is "wrong password",
        # which is what a 403 normally suggests. ECR never creates a repository on push.
        $repoName = ($imageRef -replace '^[^/]+/', '') -replace ':[^:]+$', ''
        Write-Host "    403 Forbidden and 'repository does not exist' are the SAME two causes:"
        Write-Host "      1. the repository '$repoName' has not been created:"
        Write-Host "         aws ecr create-repository --repository-name $repoName --region $region --image-tag-mutability MUTABLE"
        Write-Host "      2. your IAM policy does not cover it. Its ARN is its own, even when the name"
        Write-Host "         shares a prefix with another repository:"
        Write-Host "         arn:aws:ecr:${region}:<account>:repository/$repoName"
        Write-Host '    See DEPLOY.md, "Optional: CLIProxyAPI as a third container".'
        exit 1
    }
    $refTag = ($imageRef -replace ':[^:]+$', '') + ':' + ($Ref -replace '[^A-Za-z0-9._-]', '-')
    docker push $refTag | Out-Null
    Write-Host "    Pushed $imageRef and $refTag"
}

# -- Local provider login ------------------------------------------------------
# The login flows are browser OAuth on fixed callback ports, which is why they run HERE
# and not on the box: the instance has no browser, and those ports are not (and should not
# be) open in the Security Group. Credentials are portable JSON files, so authenticate on
# the machine that has a browser and ship the result with -SeedAuth.
if ($Login) {
    # Only the three flows whose callback ports upstream actually documents
    # (help.router-for.me/docker/docker). Others exist - Gemini, Qwen - but their ports are
    # not published there, and a wrong -p mapping fails as a browser redirect that never
    # arrives, which is a poor thing to guess at. For those, read the current upstream docs
    # and run the container by hand with the right port; the -SeedAuth half still applies.
    $flows = @{
        codex       = @{ flag = '--codex-login';       port = 1455  }
        claude      = @{ flag = '--claude-login';      port = 54545 }
        antigravity = @{ flag = '--antigravity-login'; port = 51121 }
    }
    if (-not $flows.ContainsKey($Login)) {
        Write-Fail "Unknown or undocumented provider '$Login'. Supported here: $($flows.Keys -join ', ')"
        Write-Host '    Other providers exist upstream but their OAuth callback ports are not documented'
        Write-Host '    at help.router-for.me/docker/docker. Run those logins by hand, then -SeedAuth.'
        exit 2
    }
    $flow = $flows[$Login]
    $cfg  = Join-Path $PSScriptRoot 'cliproxy.config.yaml'
    if (-not (Test-Path $cfg)) {
        Write-Fail "deploy/cliproxy.config.yaml not found. Copy cliproxy.config.example.yaml to it first."
        exit 2
    }
    if (-not (Test-Path $AuthDir)) { New-Item -ItemType Directory -Path $AuthDir | Out-Null }

    $localRef = if ($imageRef) { $imageRef } else { (Get-EnvValue 'CLIPROXY_IMAGE_REF') }
    if (-not $localRef) { Write-Fail 'No image to run. Build one first: -Build.'; exit 2 }

    Write-Step "Starting the $Login login flow on http://localhost:$($flow.port)"
    Write-Host '    A browser window is expected. Complete the consent screen, then this exits.'
    docker run --rm -p "$($flow.port):$($flow.port)" `
        -v "${cfg}:/CLIProxyAPI/config.yaml" `
        -v "${AuthDir}:/root/.cli-proxy-api" `
        $localRef /CLIProxyAPI/CLIProxyAPI $flow.flag
    if ($LASTEXITCODE -ne 0) { Write-Fail "Login exited $LASTEXITCODE"; exit $LASTEXITCODE }

    $n = @(Get-ChildItem $AuthDir -Filter *.json -ErrorAction SilentlyContinue).Count
    Write-Host "    $AuthDir now holds $n credential file(s). Ship them with -SeedAuth."
}

# -- Ship credentials to the server --------------------------------------------
if ($SeedAuth) {
    if (-not $Server) { Write-Fail '-SeedAuth needs -Server ec2-user@<ip>.'; exit 2 }
    $files = @(Get-ChildItem $AuthDir -Filter *.json -ErrorAction SilentlyContinue)
    if (-not $files) { Write-Fail "No *.json credentials in $AuthDir. Run -Login <provider> first."; exit 2 }

    $sshArgs = @('-o', 'StrictHostKeyChecking=accept-new')
    if ($Key) { $sshArgs += @('-i', $Key) }

    # Same treatment deploy.ps1 gives ssh: judge by exit code only, because PowerShell 5.1
    # turns any stderr line from a native command into a terminating error.
    function Invoke-Remote {
        param([string]$Command)
        $prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
        try { & ssh @sshArgs $Server $Command } finally { $ErrorActionPreference = $prev }
        if ($LASTEXITCODE -ne 0) { Write-Fail "Remote command exited $LASTEXITCODE : $Command"; exit $LASTEXITCODE }
    }

    $remoteHas = (& ssh @sshArgs $Server "ls ~/$AppDir/cliproxy/auth/*.json >/dev/null 2>&1 && echo yes || echo no")
    if ($remoteHas -eq 'yes' -and -not $Force) {
        Write-Fail "The server already has credentials in ~/$AppDir/cliproxy/auth. Re-run with -Force to overwrite."
        Write-Host '    They may have been refreshed in place by the running proxy, in which case the'
        Write-Host '    copies here are stale and overwriting them forces every login again.'
        exit 2
    }

    Write-Step "Uploading $($files.Count) credential file(s) to ~/$AppDir/cliproxy/auth/"
    Invoke-Remote "mkdir -p ~/$AppDir/cliproxy/auth ~/$AppDir/cliproxy/plugins && chmod 700 ~/$AppDir/cliproxy/auth"
    foreach ($f in $files) {
        $scpArgs = @('-o', 'StrictHostKeyChecking=accept-new')
        if ($Key) { $scpArgs += @('-i', $Key) }
        & scp @scpArgs $f.FullName "${Server}:~/$AppDir/cliproxy/auth/"
        if ($LASTEXITCODE -ne 0) { Write-Fail "scp of $($f.Name) exited $LASTEXITCODE"; exit $LASTEXITCODE }
    }
    Invoke-Remote "chmod 600 ~/$AppDir/cliproxy/auth/*.json && ls -la ~/$AppDir/cliproxy/auth"
    Write-Host '    Restart the proxy to pick them up:  docker compose restart cliproxy'
}

Write-Host "`nDone." -ForegroundColor Green
