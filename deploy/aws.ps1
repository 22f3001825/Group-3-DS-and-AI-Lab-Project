<#
.SYNOPSIS
    Start, stop and inspect the staging EC2 instance.

.DESCRIPTION
    This deployment is demo-only: the instance is stopped between demos, which is what
    makes it cost roughly $1.60/month. A stopped instance bills neither compute nor its
    public IPv4 address (that one is released on stop and re-assigned on start) - only the
    16 GB EBS root volume (~$1.46/mo in ap-south-1) and the ECR image (~$0.15/mo) accrue.

    There is deliberately NO Elastic IP. An EIP bills $0.005/hr whether or not it is
    associated and whether or not the instance runs (~$3.65/mo - more than everything
    else here combined), whereas an auto-assigned public IPv4 is released on stop and
    billed only while running. The cost of that choice is a NEW public IP on every start,
    which the @reboot DuckDNS updater installed by bootstrap.sh repoints the domain at.

    Set MLT_INSTANCE_ID in your environment to avoid passing -InstanceId every time.

.EXAMPLE
    # Five minutes before a demo
    .\deploy\aws.ps1 -Start

.EXAMPLE
    .\deploy\aws.ps1 -Status
    .\deploy\aws.ps1 -Stop
#>
[CmdletBinding(DefaultParameterSetName = 'Status')]
param(
    [Parameter(ParameterSetName = 'Start')][switch]$Start,
    [Parameter(ParameterSetName = 'Stop')][switch]$Stop,
    [Parameter(ParameterSetName = 'Status')][switch]$Status,

    # Defaults to $env:MLT_INSTANCE_ID.
    [string]$InstanceId = $env:MLT_INSTANCE_ID,

    # Defaults to the AWS CLI's configured region.
    [string]$Region,

    # Public hostname to poll after starting. Read from .env.staging when omitted.
    [string]$Domain,

    # Wait for the instance to reach 'stopped' rather than returning immediately.
    [switch]$Wait
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot

# PowerShell 5.1 negotiates TLS 1.0 by default on some hosts, which Caddy refuses.
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Write-Step { param([string]$Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Fail { param([string]$Text) Write-Host "FAILED: $Text" -ForegroundColor Red }

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Fail 'aws CLI not found. Install it: https://aws.amazon.com/cli/'
    exit 2
}
if (-not $InstanceId) {
    Write-Fail 'No instance id. Pass -InstanceId i-0123... or set $env:MLT_INSTANCE_ID.'
    exit 2
}

$AwsArgs = @('--instance-ids', $InstanceId)
if ($Region) { $AwsArgs += @('--region', $Region) }

# The AWS CLI writes progress and warnings to stderr; under $ErrorActionPreference='Stop'
# Windows PowerShell 5.1 turns each such line into a terminating NativeCommandError. Same
# treatment as deploy.ps1's ssh wrappers: judge by $LASTEXITCODE only.
function Invoke-Aws {
    param([string[]]$Arguments)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { $out = & aws @Arguments 2>$null } finally { $ErrorActionPreference = $prev }
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "aws $($Arguments -join ' ') exited $LASTEXITCODE"
        exit $LASTEXITCODE
    }
    return ($out | Out-String).Trim()
}

function Get-InstanceField {
    param([string]$Query)
    $a = @('ec2', 'describe-instances') + $AwsArgs + @('--query', $Query, '--output', 'text')
    return Invoke-Aws $a
}

function Get-StagingDomain {
    if ($Domain) { return $Domain }
    $envPath = Join-Path $RepoRoot '.env.staging'
    if (-not (Test-Path $envPath)) { return $null }
    $match = Get-Content $envPath | Where-Object { $_ -match '^\s*STAGING_DOMAIN\s*=' } | Select-Object -First 1
    if (-not $match) { return $null }
    return ($match -replace '^\s*STAGING_DOMAIN\s*=', '').Trim().Trim('"').Trim("'")
}

# -- Status --------------------------------------------------------------------
if ($Status -or $PSCmdlet.ParameterSetName -eq 'Status') {
    $state = Get-InstanceField 'Reservations[0].Instances[0].State.Name'
    $ip    = Get-InstanceField 'Reservations[0].Instances[0].PublicIpAddress'
    $type  = Get-InstanceField 'Reservations[0].Instances[0].InstanceType'

    Write-Host ''
    Write-Host "  Instance : $InstanceId ($type)"
    Write-Host "  State    : $state"
    if ($ip -and $ip -ne 'None') {
        Write-Host "  Public IP: $ip"
        Write-Host ''
        Write-Host "  Deploy to it with:  .\deploy\deploy.ps1 -Server ubuntu@$ip -Key ~\.ssh\mlt.pem"
    } else {
        Write-Host '  Public IP: none (assigned at start, released on stop)'
    }
    $d = Get-StagingDomain
    if ($d) { Write-Host "  URL      : https://$d" }
    Write-Host ''
    exit 0
}

# -- Stop ----------------------------------------------------------------------
if ($Stop) {
    Write-Step "Stopping $InstanceId"
    $null = Invoke-Aws (@('ec2', 'stop-instances') + $AwsArgs)
    if ($Wait) {
        Write-Host '    waiting for state=stopped...'
        $null = Invoke-Aws (@('ec2', 'wait', 'instance-stopped') + $AwsArgs)
        Write-Host '    stopped.'
    } else {
        Write-Host '    stop requested (takes ~30s to settle).'
    }
    Write-Host ''
    Write-Host '  Compute and public-IPv4 billing have ended. The EBS volume (~$1.46/mo) and the ECR image' -ForegroundColor DarkGray
    Write-Host '  (~$0.15/mo) continue to bill - that is the whole standing cost.' -ForegroundColor DarkGray
    exit 0
}

# -- Start ---------------------------------------------------------------------
if ($Start) {
    Write-Step "Starting $InstanceId"
    $null = Invoke-Aws (@('ec2', 'start-instances') + $AwsArgs)
    Write-Host '    waiting for state=running...'
    $null = Invoke-Aws (@('ec2', 'wait', 'instance-running') + $AwsArgs)

    $ip = Get-InstanceField 'Reservations[0].Instances[0].PublicIpAddress'
    Write-Host "    running, public IP $ip"

    $d = Get-StagingDomain
    if (-not $d) {
        Write-Host ''
        Write-Host 'No STAGING_DOMAIN found, so the health poll is skipped.' -ForegroundColor Yellow
        Write-Host "Deploy with:  .\deploy\deploy.ps1 -Server ubuntu@$ip -Key ~\.ssh\mlt.pem"
        exit 0
    }

    # Roughly two minutes of startup, in this order: boot (~40s) -> docker starts the
    # containers via `restart: unless-stopped` -> the @reboot DuckDNS update plus the 60s
    # record TTL -> the ~40s ONNX warm-up thread in src/api/main.py. /health answers
    # before the warm-up finishes; the first chat is what waits for that.
    Write-Step "Waiting for https://$d/health (~2 minutes is normal)"
    $deadline = (Get-Date).AddMinutes(5)
    $ok = $false
    while ((Get-Date) -lt $deadline) {
        try {
            $r = Invoke-WebRequest -Uri "https://$d/health" -UseBasicParsing -TimeoutSec 5
            if ($r.StatusCode -eq 200) { $ok = $true; break }
        } catch {
            Start-Sleep -Seconds 5
        }
    }

    Write-Host ''
    if ($ok) {
        Write-Host "  Ready: https://$d" -ForegroundColor Green
        Write-Host ''
        Write-Host '  Retrieval may still be warming for ~40s - the first chat pays for it.' -ForegroundColor DarkGray
        Write-Host "  Check with:  .\deploy\deploy.ps1 -Server ubuntu@$ip -Key ~\.ssh\mlt.pem -Logs"
    } else {
        Write-Fail "https://$d/health did not answer within 5 minutes."
        Write-Host ''
        Write-Host "  The instance IS running at $ip. Likely causes, in order:"
        Write-Host '   * DNS still points at the previous IP. Check the @reboot DuckDNS cron:'
        Write-Host "       ssh ubuntu@$ip 'crontab -l; cat ~/.duckdns/last.log'"
        Write-Host '     Windows also caches for the record TTL - try  ipconfig /flushdns'
        Write-Host '   * containers did not come back. Check:'
        Write-Host "       .\deploy\deploy.ps1 -Server ubuntu@$ip -Key ~\.ssh\mlt.pem -Status"
        exit 1
    }
    exit 0
}
