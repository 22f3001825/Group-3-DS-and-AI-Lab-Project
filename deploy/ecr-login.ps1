<#
.SYNOPSIS
    Log this machine's Docker daemon in to the ECR registry named by an env file.

.DESCRIPTION
    Wraps the one-liner in DEPLOY.md ("Building and pushing from Windows, without
    Actions"):

        aws ecr get-login-password --region <r> |
            docker login --username AWS --password-stdin <registry>

    What it adds over typing that is the registry: it is read from IMAGE_REF in your
    env file rather than retyped, so the credential is always minted for the registry
    the build is about to push to. A mistyped hostname otherwise logs you in to a
    registry that exists, succeeds, and fails later at `docker push` with a 403 that
    reads like a permissions problem.

    THIS IS A LAPTOP SCRIPT. The EC2 box never runs docker login: bootstrap.sh puts
    "credHelpers": {"<registry>": "ecr-login"} in its ~/.docker/config.json, and the
    helper mints a fresh token from IMDS on every pull. If you find yourself wanting
    this script on the server, the instance profile is missing - see DEPLOY.md,
    "docker compose pull fails 401/403 from ECR".

    The token this obtains is valid for 12 hours and is written to your Docker
    credential store, so a push tomorrow needs another run.

    KEEP THIS FILE ASCII-ONLY - see the note in deploy.ps1 for why a stray em dash
    breaks Windows PowerShell 5.1 parsing in a way that reports an unrelated error.

.EXAMPLE
    # Log in to the registry .env.staging points at
    .\deploy\ecr-login.ps1

.EXAMPLE
    # Log in and confirm the account, then build and push by hand
    .\deploy\ecr-login.ps1 -Env .env.staging -Verify
    docker compose --env-file .env.staging build api
    docker compose --env-file .env.staging push api

.EXAMPLE
    # The CLIProxyAPI repository lives at a second path in the same registry
    .\deploy\ecr-login.ps1 -Cliproxy

.EXAMPLE
    # Drop the stored credential
    .\deploy\ecr-login.ps1 -Logout
#>
[CmdletBinding()]
param(
    # Env file holding IMAGE_REF. Defaults to .env.staging, falling back to .env.
    [Alias('Env')][string]$EnvFile,

    # Registry hostname, bypassing the env file entirely. Accepts a full image
    # reference too - everything before the first '/' is taken as the registry,
    # matching how deploy.ps1 and bootstrap.sh read IMAGE_REF.
    [string]$Registry,

    # AWS region. Derived from the registry hostname when omitted; pass it only for
    # a registry that is not a *.dkr.ecr.<region>.amazonaws.com name.
    [string]$Region,

    # Named AWS profile to mint the token with, for a machine configured with more
    # than one account.
    [Alias('Profile')][string]$AwsProfile,

    # Read CLIPROXY_IMAGE_REF instead of IMAGE_REF.
    [switch]$Cliproxy,

    # After logging in, print the caller identity and the repository's recent tags.
    # Both calls are covered by the mlt-staging-ops policy in DEPLOY.md.
    [switch]$Verify,

    # Remove the stored credential for this registry instead of creating one.
    [switch]$Logout
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot

function Write-Step { param([string]$Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Fail { param([string]$Text) Write-Host "FAILED: $Text" -ForegroundColor Red }
function Write-Note { param([string]$Text) Write-Host "    $Text" }

# aws and docker both write ordinary diagnostics to stderr. Under
# $ErrorActionPreference='Stop', Windows PowerShell 5.1 wraps each such line in a
# NativeCommandError and TERMINATES, so a harmless notice would kill the login.
# Drop to 'Continue' around every native call and judge by $LASTEXITCODE, which is
# the only reliable signal here. Same reasoning as deploy.ps1's Invoke-Native.
function Invoke-Native {
    param([scriptblock]$Action)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { & $Action } finally { $ErrorActionPreference = $prev }
}

# -- Preflight -----------------------------------------------------------------
foreach ($exe in @('aws', 'docker')) {
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) {
        Write-Fail "'$exe' is not on PATH."
        if ($exe -eq 'aws') {
            Write-Note 'winget install --id Amazon.AWSCLI --source winget, then open a NEW terminal.'
        } else {
            Write-Note 'Install Docker Desktop, or run the build in GitHub Actions instead.'
        }
        exit 2
    }
}

# docker login writes to the daemon's credential store via the CLI, but a stopped
# daemon fails with a connect error that reads like an auth failure.
Invoke-Native { & docker info --format '{{.ServerVersion}}' | Out-Null }
if ($LASTEXITCODE -ne 0) {
    Write-Fail 'The Docker daemon is not responding. Start Docker Desktop and retry.'
    exit 1
}

# -- Resolve the registry ------------------------------------------------------
function Get-EnvValue {
    param([string]$Name, [string]$Path)
    if (-not (Test-Path $Path)) { return $null }
    $match = Get-Content $Path | Where-Object { $_ -match "^\s*$Name\s*=" } | Select-Object -First 1
    if (-not $match) { return $null }
    return ($match -replace "^\s*$Name\s*=", '').Trim().Trim('"').Trim("'")
}

$imageRef = $null
$source   = $null

if ($Registry) {
    $source = '-Registry'
} else {
    # Candidate env files, in the order DEPLOY.md uses them.
    $candidates = if ($EnvFile) { @($EnvFile) } else { @('.env.staging', '.env') }
    $varName    = if ($Cliproxy) { 'CLIPROXY_IMAGE_REF' } else { 'IMAGE_REF' }

    foreach ($candidate in $candidates) {
        $path = Join-Path $RepoRoot $candidate
        if (-not (Test-Path $path)) { $path = $candidate }
        if (-not (Test-Path $path)) { continue }

        $value = Get-EnvValue -Name $varName -Path $path
        # CLIPROXY_IMAGE_REF is optional by design (cliproxy.ps1 derives it from
        # IMAGE_REF), and the registry is the same either way - so fall back rather
        # than failing on an env file that simply never opted in to the proxy.
        if (-not $value -and $Cliproxy) { $value = Get-EnvValue -Name 'IMAGE_REF' -Path $path }
        if ($value) { $imageRef = $value; $source = $candidate; break }
    }

    if (-not $imageRef) {
        Write-Fail "No $varName found in: $($candidates -join ', ')"
        Write-Note 'Copy .env.staging.example to .env.staging, or pass -Registry explicitly:'
        Write-Note '  .\deploy\ecr-login.ps1 -Registry 512705760700.dkr.ecr.ap-south-1.amazonaws.com'
        exit 2
    }
    if ($imageRef -notmatch '^[^/]+/[^:]+:.+$') {
        Write-Fail "$varName ('$imageRef') does not look like <registry>/<repository>:<tag>."
        exit 2
    }
    $Registry = $imageRef.Split('/')[0]
}

# Tolerate a full image reference in -Registry: everything before the first '/'.
if ($Registry -match '/') {
    if (-not $imageRef) { $imageRef = $Registry }
    $Registry = $Registry.Split('/')[0]
}

if (-not $Region) {
    if ($Registry -match '\.dkr\.ecr\.([^.]+)\.amazonaws\.com$') {
        $Region = $Matches[1]
    } else {
        Write-Fail "Cannot derive an AWS region from '$Registry'."
        Write-Note 'Pass -Region, or check the hostname: an ECR registry is'
        Write-Note '  <account-id>.dkr.ecr.<region>.amazonaws.com'
        Write-Note 'Note that get-login-password only issues credentials for ECR - another'
        Write-Note 'registry (Docker Hub, GHCR) needs its own docker login.'
        exit 2
    }
}

$awsArgs = @('--region', $Region)
if ($AwsProfile) { $awsArgs += @('--profile', $AwsProfile) }

# -- Logout --------------------------------------------------------------------
if ($Logout) {
    Write-Step "Removing the stored credential for $Registry"
    Invoke-Native { & docker logout $Registry }
    if ($LASTEXITCODE -ne 0) { Write-Fail "docker logout exited $LASTEXITCODE"; exit $LASTEXITCODE }
    Write-Note 'Done. Pulls and pushes to this registry will now fail until you log in again.'
    exit 0
}

# -- Login ---------------------------------------------------------------------
Write-Step "Logging in to $Registry"
Write-Note "registry from : $source"
Write-Note "region        : $Region"
if ($AwsProfile) { Write-Note "profile       : $AwsProfile" }

$pw = Invoke-Native { & aws ecr get-login-password @awsArgs }
if ($LASTEXITCODE -ne 0 -or -not $pw) {
    Write-Fail 'aws ecr get-login-password failed.'
    Write-Note 'Usual causes, in order:'
    Write-Note '  1. no credentials on this machine       -> aws configure'
    Write-Note "  2. the CLI is set to another region     -> aws configure set region $Region"
    Write-Note '  3. the IAM identity lacks ecr:GetAuthorizationToken (it is account-wide'
    Write-Note '     and cannot be resource-scoped - see mlt-staging-ops in DEPLOY.md)'
    exit 1
}

# --password-stdin so the token never lands in the process table or PSReadLine history.
# The pipe has to be INSIDE the scriptblock: piping into Invoke-Native would feed the
# scriptblock's (unread) pipeline input instead of docker's stdin, and docker exits
# with "password is empty".
Invoke-Native { $pw | & docker login --username AWS --password-stdin $Registry }
if ($LASTEXITCODE -ne 0) {
    Write-Fail 'docker login failed.'

    # AWS already handed us a token, so the interesting question is whether the
    # REGISTRY rejects it or DOCKER does - and the error text does not say. Ask the
    # registry directly with the same Basic credential the daemon would have sent.
    # A 200 here means the credential is fine and the fault is entirely Docker-side,
    # which is a different day's problem from an IAM one.
    $probe = $null
    try {
        $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("AWS:$pw"))
        $resp  = Invoke-WebRequest -Uri "https://$Registry/v2/" -Headers @{ Authorization = "Basic $basic" } `
                    -UseBasicParsing -TimeoutSec 30
        $probe = [int]$resp.StatusCode
    } catch {
        if ($_.Exception.Response) { $probe = [int]$_.Exception.Response.StatusCode.value__ }
    }

    if ($probe -eq 200) {
        Write-Note "The registry ACCEPTS this token (GET /v2/ -> 200), so the credential and"
        Write-Note 'the IAM identity behind it are both good - Docker is the broken half.'
        Write-Note 'Things worth trying, cheapest first:'
        Write-Note '  - restart Docker Desktop, then retry'
        Write-Note '  - a clock-skewed Docker VM makes ECR reject a valid token:'
        Write-Note '      docker run --rm busybox date -u    (compare against UTC now)'
        Write-Note '  - rule out the credential store with an isolated config:'
        Write-Note '      docker --config $env:TEMP\dockercfg login ...'
        Write-Note 'Until it is fixed, build in GitHub Actions instead - the local build is'
        Write-Note 'only the documented fallback, and CI authenticates over OIDC, not this.'
    } elseif ($probe) {
        Write-Note "The registry itself rejected the token (GET /v2/ -> $probe), so this is not"
        Write-Note 'a Docker problem. 401/403 means the IAM identity cannot see this registry;'
        Write-Note 'confirm which account you are: aws sts get-caller-identity'
    } else {
        Write-Note "Could not reach https://$Registry/v2/ to tell whether the token or Docker"
        Write-Note 'is at fault. Check connectivity and any corporate TLS proxy.'
    }
    exit 1
}
Write-Note 'Logged in. The token is valid for 12 hours.'

# -- Verify --------------------------------------------------------------------
if ($Verify) {
    Write-Step 'Verifying'

    # ECR answers 403 - not 404 - for a repository you cannot see, so "wrong account"
    # and "repository does not exist" are indistinguishable from a push error alone.
    # Printing the account here separates them before you spend a 1.4 GB upload.
    $identity = Invoke-Native { & aws sts get-caller-identity --query 'Arn' --output text @awsArgs }
    if ($LASTEXITCODE -eq 0) { Write-Note "identity : $identity" }

    if ($imageRef -and $imageRef -match '/') {
        $repoName = ($imageRef -replace '^[^/]+/', '') -replace ':[^:]+$', ''
        Write-Note "repository: $repoName"
        # imageTags[0] rather than a join(): a JMESPath json-literal separator needs
        # backticks, which are PowerShell's escape character, and the quoting to get
        # one through intact is not worth a second column. An untagged image simply
        # prints None here.
        $tags = Invoke-Native {
            & aws ecr describe-images --repository-name $repoName @awsArgs `
                --query 'reverse(sort_by(imageDetails,&imagePushedAt))[:5].[imagePushedAt,imageTags[0]]' `
                --output text
        }
        if ($LASTEXITCODE -ne 0) {
            Write-Note 'Could not list images. The login above still succeeded - this only means'
            Write-Note 'the identity lacks ecr:DescribeImages on this repository, or it does not'
            Write-Note 'exist yet (ECR never creates a repository on push):'
            Write-Note "  aws ecr create-repository --repository-name $repoName --region $Region --image-tag-mutability MUTABLE"
        } elseif (-not $tags) {
            Write-Note 'The repository is empty. Run the "Build and push staging image" workflow'
            Write-Note 'before deploying - update.sh pulls, it never builds.'
        } else {
            Write-Note 'recent images (newest first):'
            $tags | ForEach-Object { Write-Host "      $_" }
        }
    }
}

Write-Host ''
