<#
.SYNOPSIS
    Deploy or update MLT staging from Windows. Uses the built-in OpenSSH client only.

.DESCRIPTION
    The image is built by .github/workflows/image.yml and pushed to ECR; this script never
    builds anything. It ships the four files the box actually needs - docker-compose.yml,
    deploy/Caddyfile, deploy/update.sh and .env - then runs update.sh, which pulls the
    image, verifies it was built for THIS deployment, and refuses to report success unless
    /health answers.

    The box holds no git checkout and no repo credential, which is what lets the
    repository stay private.

    KEEP THIS FILE ASCII-ONLY. Windows PowerShell 5.1 decodes a .ps1 without a BOM using
    the system ANSI codepage, so a UTF-8 em dash becomes three CP1252 characters - the last
    of which is U+201D, a smart quote that PowerShell honours as a string delimiter. One
    stray dash inside a double-quoted message therefore ends that string early, re-parses
    the remainder of the file as code, and surfaces as a CommandNotFoundException for some
    unrelated word several lines later. Use '-' and '->', not en/em dashes or arrows.

    Secrets never enter git: -Env scp's your local staging env file to the server as .env
    with 600 permissions. -SeedDb ships mlt_learner.db, which is gitignored and carries
    the question bank.

.EXAMPLE
    # One-time setup of a fresh EC2 instance
    .\deploy\deploy.ps1 -Server ubuntu@203.0.113.10 -Key ~\.ssh\mlt.pem -Env .env.staging `
        -Bootstrap -DuckDnsToken abc123

.EXAMPLE
    # First deploy
    .\deploy\deploy.ps1 -Server ubuntu@203.0.113.10 -Key ~\.ssh\mlt.pem -Env .env.staging -SeedDb

.EXAMPLE
    # Routine update after the Actions build finishes
    .\deploy\deploy.ps1 -Server ubuntu@203.0.113.10 -Key ~\.ssh\mlt.pem

.EXAMPLE
    # Roll back to a specific image, and read-only modes
    .\deploy\deploy.ps1 -Server ubuntu@203.0.113.10 -Key ~\.ssh\mlt.pem -Tag 4f2a1c9
    .\deploy\deploy.ps1 -Server ubuntu@203.0.113.10 -Key ~\.ssh\mlt.pem -Logs
    .\deploy\deploy.ps1 -Server ubuntu@203.0.113.10 -Key ~\.ssh\mlt.pem -Status
#>
[CmdletBinding()]
param(
    # user@host of the staging box, e.g. ubuntu@203.0.113.10. The IP changes on every
    # instance start (there is deliberately no Elastic IP) - deploy\aws.ps1 -Status prints
    # the current one.
    [Parameter(Mandatory = $true)][string]$Server,

    # Path to the SSH private key.
    [string]$Key,

    # Path to the local staging env file to push as the server's .env.
    [Alias('Env')][string]$EnvFile,

    # Run deploy/bootstrap.sh on the box first (one-time setup of a fresh instance).
    # Requires -EnvFile: the domain and the ECR registry are read from it.
    [switch]$Bootstrap,

    # DuckDNS token, for -Bootstrap only. Not stored in .env because nothing at runtime
    # reads it - only the updater cron does.
    [string]$DuckDnsToken,

    # Deploy a specific image tag (a git SHA) instead of whatever IMAGE_REF names.
    [string]$Tag,

    # Also upload mlt_learner.db to state/ (refuses to clobber without -Force).
    [switch]$SeedDb,

    # Allow -SeedDb to overwrite an existing server database.
    [switch]$Force,

    # Tail the API logs instead of deploying.
    [switch]$Logs,

    # Show container status instead of deploying.
    [switch]$Status,

    # Remote deployment directory.
    [string]$AppDir = 'mlt-staging'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot

function Write-Step { param([string]$Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Fail { param([string]$Text) Write-Host "FAILED: $Text" -ForegroundColor Red }

# -- SSH plumbing --------------------------------------------------------------
$SshArgs = @()
if ($Key) {
    $resolvedKey = (Resolve-Path $Key -ErrorAction SilentlyContinue)
    if (-not $resolvedKey) { Write-Fail "SSH key not found: $Key"; exit 2 }
    $SshArgs += @('-i', $resolvedKey.Path)
}
# BatchMode: fail fast instead of hanging on an interactive password prompt, which in a
# non-interactive PowerShell pipeline looks like the script has frozen.
# StrictHostKeyChecking=accept-new matters more than it used to: a stopped instance comes
# back on a NEW public IP, so the host is effectively new on most deploys.
$SshArgs += @('-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=accept-new')

# ssh and scp write ordinary diagnostics to stderr (host-key notices, "Connection to X
# closed", banners). Under $ErrorActionPreference='Stop', Windows PowerShell 5.1 wraps
# each such line in a NativeCommandError and TERMINATES - so a harmless banner would kill
# a deploy. These three functions drop to 'Continue' for the duration of the native call
# and judge success by $LASTEXITCODE, which is the only reliable signal here.
function Invoke-Native {
    param([scriptblock]$Action)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { & $Action } finally { $ErrorActionPreference = $prev }
}

function Invoke-Remote {
    param([string]$Command)
    Invoke-Native { & ssh @SshArgs $Server $Command }
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Remote command exited $LASTEXITCODE : $Command"
        exit $LASTEXITCODE
    }
}

# Separate from Invoke-Remote because this one CAPTURES stdout rather than streaming it.
function Get-Remote {
    param([string]$Command)
    $out = Invoke-Native { & ssh @SshArgs $Server $Command 2>$null }
    return ($out | Out-String).Trim()
}

function Send-File {
    param([string]$Local, [string]$Remote)
    Invoke-Native { & scp @SshArgs $Local "${Server}:${Remote}" }
    if ($LASTEXITCODE -ne 0) { Write-Fail "scp failed: $Local -> $Remote"; exit $LASTEXITCODE }
}

if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Fail 'ssh not found. Enable the Windows OpenSSH Client optional feature.'
    exit 2
}

# -- Read-only modes -----------------------------------------------------------
if ($Logs) {
    Write-Step "Tailing API logs (Ctrl+C to stop)"
    Invoke-Remote "cd ~/$AppDir && docker compose logs -f --tail=100 api"
    exit 0
}
if ($Status) {
    Write-Step 'Container status'
    Invoke-Remote "cd ~/$AppDir && docker compose ps && echo && df -h / | tail -1 && free -m | head -2"
    exit 0
}

# -- Local preflight -----------------------------------------------------------
# Runs BEFORE any network call: these are the misconfigurations that otherwise surface
# only at the login screen. Catching them here costs nothing and needs no server.
$envPath = $null
$imageRef = $null
$domain = $null

function Get-EnvValue {
    param([string[]]$Lines, [string]$Name)
    $match = $Lines | Where-Object { $_ -match "^\s*$Name\s*=" } | Select-Object -First 1
    if (-not $match) { return $null }
    return ($match -replace "^\s*$Name\s*=", '').Trim().Trim('"').Trim("'")
}

if ($EnvFile) {
    $envPath = Join-Path $RepoRoot $EnvFile
    if (-not (Test-Path $envPath)) { $envPath = $EnvFile }
    if (-not (Test-Path $envPath)) { Write-Fail "Env file not found: $EnvFile"; exit 2 }
    $envPath = (Resolve-Path $envPath).Path

    Write-Step "Checking $EnvFile"
    $envText = Get-Content $envPath -Raw
    $lines   = @(Get-Content $envPath)

    # These two must be byte-identical or Google's aud check rejects every sign-in, with
    # an error the UI can only report as "login failed". Worth three lines to never debug.
    $backendClient = Get-EnvValue $lines 'GOOGLE_CLIENT_ID'
    $viteClient    = Get-EnvValue $lines 'VITE_GOOGLE_CLIENT_ID'
    if ($backendClient -ne $viteClient) {
        Write-Fail "GOOGLE_CLIENT_ID and VITE_GOOGLE_CLIENT_ID differ in $EnvFile. Google's aud check would reject every sign-in."
        exit 2
    }
    if (-not $backendClient) { Write-Fail "GOOGLE_CLIENT_ID is empty in $EnvFile. Sign-in would 503."; exit 2 }
    if (-not (Get-EnvValue $lines 'JWT_SECRET')) { Write-Fail "JWT_SECRET is empty in $EnvFile. Every auth endpoint would 503."; exit 2 }

    $domain = Get-EnvValue $lines 'STAGING_DOMAIN'
    $apiUrl = Get-EnvValue $lines 'VITE_API_URL'
    $cors   = Get-EnvValue $lines 'CORS_ORIGINS'
    if (-not $domain) { Write-Fail "STAGING_DOMAIN is empty in $EnvFile. Caddy would not know what certificate to request."; exit 2 }
    if ($apiUrl -notmatch '^https://') {
        Write-Fail "VITE_API_URL must be the https:// staging URL (got '$apiUrl'). An empty value does NOT mean same-origin - client.js falls back to http://localhost:8000."
        exit 2
    }
    if ($apiUrl -notlike "*$domain*") {
        Write-Host "WARNING: VITE_API_URL ('$apiUrl') does not contain STAGING_DOMAIN ('$domain')." -ForegroundColor Yellow
    }
    if ($cors -and $cors -notlike "*$domain*") {
        Write-Host "WARNING: CORS_ORIGINS ('$cors') does not mention '$domain'." -ForegroundColor Yellow
    }

    # IMAGE_REF is what docker-compose.yml interpolates and update.sh pulls. An unset or
    # malformed value means the box silently falls back to the local build name and finds
    # no such image.
    $imageRef = Get-EnvValue $lines 'IMAGE_REF'
    if (-not $imageRef) {
        Write-Fail "IMAGE_REF is empty in $EnvFile. It must be the full ECR ref, e.g. 123456789012.dkr.ecr.ap-south-1.amazonaws.com/mlt-api:latest"
        exit 2
    }
    if ($imageRef -notmatch '^[^/]+/[^:]+:.+$') {
        Write-Fail "IMAGE_REF ('$imageRef') does not look like <registry>/<repository>:<tag>."
        exit 2
    }

    # The image bakes VITE_* in at build time, so these values must match the repository
    # variables the workflow built with. update.sh asserts this against the image labels
    # on the box; this is the same check, earlier and cheaper.
    Write-Host "    Image: $imageRef"
    Write-Host "    The workflow must have built it with VITE_API_URL='$apiUrl'"
    Write-Host "    and VITE_GOOGLE_CLIENT_ID='$backendClient' - update.sh will verify."

    # rag_pipeline.py:120-127 sweeps up any variable named api1..api20 / API_1.. / groq_1..
    # and posts its VALUE to Groq as an API key, with no format validation.
    if ($envText -match '(?im)^\s*(api_?\d{1,2}|groq_\d{1,2})\s*=') {
        Write-Fail "$EnvFile defines a variable matching api<N>/groq<N>. rag_pipeline.py harvests those names and sends their values to Groq. Rename it."
        exit 2
    }
    if (Get-EnvValue $lines 'ADMIN_TOKEN') {
        Write-Host 'WARNING: ADMIN_TOKEN is set. Staging is expected to leave it unset (see .env.staging.example).' -ForegroundColor Yellow
    }

    # CLIProxyAPI consistency. Three settings have to agree or the failure is silent: the
    # compose profile decides whether the container runs at all, CLIPROXY_IMAGE_REF is what
    # it runs, and LOCAL_LLM_BASE_URL is whether the API ever calls it.
    $profiles  = Get-EnvValue $lines 'COMPOSE_PROFILES'
    $localBase = Get-EnvValue $lines 'LOCAL_LLM_BASE_URL'
    $cliproxyOn = $profiles -and ($profiles -split '[,\s]+' -contains 'cliproxy')

    if ($cliproxyOn) {
        if (-not (Get-EnvValue $lines 'CLIPROXY_IMAGE_REF')) {
            Write-Fail "COMPOSE_PROFILES enables cliproxy but CLIPROXY_IMAGE_REF is empty. docker compose would abort before starting anything, including the api."
            exit 2
        }
        if (-not (Test-Path (Join-Path $PSScriptRoot 'cliproxy.config.yaml'))) {
            Write-Host 'WARNING: cliproxy is enabled but deploy/cliproxy.config.yaml does not exist here.' -ForegroundColor Yellow
            Write-Host '         The box keeps whatever it already has; if it has none, the container will not start.' -ForegroundColor Yellow
        }
        if (-not $localBase) {
            Write-Host 'NOTE: cliproxy will run, but LOCAL_LLM_BASE_URL is unset so the API will never call it.' -ForegroundColor Yellow
        }
    } elseif ($localBase) {
        Write-Host "WARNING: LOCAL_LLM_BASE_URL is set ('$localBase') but COMPOSE_PROFILES does not enable cliproxy." -ForegroundColor Yellow
        Write-Host '         Every failover walk then pays a connection attempt plus LOCAL_LLM_TIMEOUT for nothing.' -ForegroundColor Yellow
    }

    # In compose, the api container's own localhost is the api container. This one is worth
    # failing on: it looks correct, it matches the docs for running the proxy by hand, and
    # it fails only at request time, buried in a failover walk.
    if ($localBase -match '://(localhost|127\.0\.0\.1)([:/]|$)') {
        Write-Fail "LOCAL_LLM_BASE_URL points at localhost ('$localBase'). Inside the compose network that is the api container itself. Use http://cliproxy:8317/v1."
        exit 2
    }
    Write-Host '    Env file looks consistent.'
}

if ($Bootstrap -and -not $envPath) {
    Write-Fail '-Bootstrap needs -Env: the domain and the ECR registry are read from that file.'
    exit 2
}
if ($SeedDb -and -not (Test-Path (Join-Path $RepoRoot 'mlt_learner.db'))) {
    Write-Fail "-SeedDb was passed but mlt_learner.db is not in $RepoRoot."
    exit 2
}

# -- Bootstrap -----------------------------------------------------------------
# bootstrap.sh used to be curl'd from raw.githubusercontent.com, which 404s now that the
# repo is private. scp'ing it avoids putting a PAT on the box just to read one script.
if ($Bootstrap) {
    $ecrRegistry = $imageRef.Split('/')[0]
    Write-Step "Bootstrapping $Server (ECR registry: $ecrRegistry)"

    Invoke-Remote "mkdir -p ~/$AppDir/deploy ~/$AppDir/state"
    Send-File (Join-Path $PSScriptRoot 'bootstrap.sh') "~/$AppDir/deploy/bootstrap.sh"

    $bootstrapArgs = "--domain '$domain' --ecr-registry '$ecrRegistry'"
    if ($DuckDnsToken) { $bootstrapArgs = "$bootstrapArgs --duckdns-token '$DuckDnsToken'" }
    else { Write-Host 'WARNING: no -DuckDnsToken. DNS will not follow the new IP after a restart.' -ForegroundColor Yellow }

    # sed strips CR even though .gitattributes pins these files to LF: one that reached
    # the working tree another way (an editor, a zip download, a clone predating
    # .gitattributes) would otherwise die on its first line with "$'\r': command not
    # found", which reads like a corrupt script rather than a line-ending problem.
    Invoke-Remote "cd ~/$AppDir/deploy && sed -i 's/\r`$//' bootstrap.sh && bash bootstrap.sh $bootstrapArgs"
}

# -- Remote preflight ----------------------------------------------------------
Write-Step "Checking the connection to $Server"
Invoke-Remote "test -d ~/$AppDir || (echo 'No ~/$AppDir - run with -Bootstrap first' && exit 1)"

# -- Ship the deployment files -------------------------------------------------
# The box has no checkout, so these four files ARE the deployment. Everything else it
# needs is inside the image.
Write-Step 'Uploading docker-compose.yml, Caddyfile and update.sh'
Invoke-Remote "mkdir -p ~/$AppDir/deploy ~/$AppDir/state"
Send-File (Join-Path $RepoRoot 'docker-compose.yml') "~/$AppDir/docker-compose.yml"
Send-File (Join-Path $PSScriptRoot 'Caddyfile')       "~/$AppDir/deploy/Caddyfile"
Send-File (Join-Path $PSScriptRoot 'update.sh')       "~/$AppDir/deploy/update.sh"
Invoke-Remote "cd ~/$AppDir && sed -i 's/\r`$//' docker-compose.yml deploy/Caddyfile deploy/update.sh && echo '    3 files installed (LF)'"

# CLIProxyAPI's config, when there is one. Shipped like .env rather than like the Caddyfile
# because it carries the proxy's api-keys, so the real file is gitignored and only
# cliproxy.config.example.yaml is committed. Absent locally = the box keeps whatever it has.
$cliproxyCfg = Join-Path $PSScriptRoot 'cliproxy.config.yaml'
if (Test-Path $cliproxyCfg) {
    Write-Step 'Uploading cliproxy.config.yaml'
    Invoke-Remote "mkdir -p ~/$AppDir/cliproxy/auth ~/$AppDir/cliproxy/plugins"
    Send-File $cliproxyCfg "~/$AppDir/deploy/cliproxy.config.yaml.upload"
    Invoke-Remote "cd ~/$AppDir/deploy && sed -e '1s/^\xEF\xBB\xBF//' -e 's/\r`$//' cliproxy.config.yaml.upload > cliproxy.config.yaml && rm -f cliproxy.config.yaml.upload && chmod 600 cliproxy.config.yaml && echo '    cliproxy.config.yaml installed (600, LF, no BOM)'"
}

if ($envPath) {
    Write-Step "Uploading $EnvFile -> ~/$AppDir/.env"
    Send-File $envPath "~/$AppDir/.env.upload"
    # Normalise on the way in. A file authored on Windows arrives with CRLF endings, and
    # PowerShell's Set-Content -Encoding utf8 prepends a BOM - so without this the first
    # key parses as "<BOM>STAGING_DOMAIN" and EVERY value carries a trailing \r. That
    # yields a certificate request for "domain.duckdns.org\r" and an IMAGE_REF with an
    # invisible carriage return that will never match a real image.
    $normalise = "cd ~/$AppDir && sed -e '1s/^\xEF\xBB\xBF//' -e 's/\r`$//' .env.upload > .env && rm -f .env.upload && chmod 600 .env && echo '    .env installed (600, LF, no BOM)'"
    Invoke-Remote $normalise
}

# -- Database seed -------------------------------------------------------------
if ($SeedDb) {
    $dbPath = Join-Path $RepoRoot 'mlt_learner.db'
    if (-not (Test-Path $dbPath)) { Write-Fail "mlt_learner.db not found at $dbPath"; exit 2 }

    # Guard, not paranoia: this file accumulates every student, quiz attempt and mastery
    # row created on staging. Overwriting it with the local copy is unrecoverable.
    $remoteHas = Get-Remote "test -f ~/$AppDir/state/mlt_learner.db && echo yes || echo no"
    if ($remoteHas -eq 'yes' -and -not $Force) {
        Write-Fail "state/mlt_learner.db already exists on the server. It holds live staging data. Re-run with -Force to overwrite."
        exit 2
    }

    $sizeMb = [math]::Round((Get-Item $dbPath).Length / 1MB, 1)
    Write-Step "Uploading mlt_learner.db ($sizeMb MB) -> ~/$AppDir/state/"
    if ($remoteHas -eq 'yes') {
        Invoke-Remote "cd ~/$AppDir/state && cp mlt_learner.db pre-seed-backup-`$(date +%Y%m%d%H%M%S).db && echo '    existing DB backed up'"
    }

    # Stop the API first. scp TRUNCATES and rewrites the destination in place, so the file
    # the running container holds open is replaced underneath it: SQLAlchemy's pooled
    # connections keep reading a file whose contents changed mid-transaction, and any WAL
    # or journal left by the old database no longer matches. The symptom is not a clean
    # failure - it is "database disk image is malformed" some minutes later.
    #
    # update.sh runs after this and brings it back up, so there is no explicit start here.
    Invoke-Remote "cd ~/$AppDir && docker compose stop api >/dev/null 2>&1; echo '    api stopped for the swap'"
    Send-File $dbPath "~/$AppDir/state/mlt_learner.db"
}

# -- Deploy --------------------------------------------------------------------
# Run in place: nothing rewrites update.sh mid-run any more. The old copy-to-/tmp dance
# existed only because `git reset --hard` used to overwrite this file underneath a bash
# that reads scripts incrementally, and there is no git here now.
$updateCmd = "bash ~/$AppDir/deploy/update.sh --dir ~/$AppDir"
if ($Tag) { $updateCmd = "$updateCmd --tag $Tag" }

Write-Step 'Running deploy/update.sh on the server'
Invoke-Remote $updateCmd

Write-Host "`nDone." -ForegroundColor Green
