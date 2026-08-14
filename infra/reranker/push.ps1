<#
.SYNOPSIS
    Build the reranker image and push it to ECR, then roll the instance onto it.

.DESCRIPTION
    PowerShell to match the deploy.ps1 convention .env.staging.example already describes.

    The build is slow the first time (~80 MB of ONNX weights are baked into a layer) and
    fast afterwards, because that RUN layer only re-executes when requirements.txt or the
    model argument changes.

.EXAMPLE
    ./push.ps1 -Region ap-south-1 -Repo 1234.dkr.ecr.ap-south-1.amazonaws.com/mlt-reranker

.EXAMPLE
    # Pin a build to the current commit and restart the instance onto it.
    ./push.ps1 -Repo $repo -Tag (git rev-parse --short HEAD) -InstanceId i-0abc123 -Restart
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [string]$Region = "ap-south-1",

    [string]$Tag = "latest",

    # Instance id from `terraform output instance_id`. Only needed with -Restart.
    [string]$InstanceId,

    # Roll the running instance onto the newly pushed image via SSM. Without this the
    # instance keeps serving the old image until it is rebooted.
    [switch]$Restart
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$context = Join-Path (Split-Path -Parent (Split-Path -Parent $here)) "reranker"

if (-not (Test-Path (Join-Path $context "Dockerfile"))) {
    throw "Cannot find the reranker Dockerfile at $context. Run this from infra/reranker."
}

$registry = $Repo.Split("/")[0]
$image = "$($Repo):$($Tag)"

Write-Host "Building $image from $context ..." -ForegroundColor Cyan
docker build -t $image $context
if ($LASTEXITCODE -ne 0) { throw "docker build failed." }

Write-Host "Logging in to $registry ..." -ForegroundColor Cyan
# The pipe is intentional: the password never becomes a process argument, so it stays out
# of the local shell history and out of `ps` on any machine running this.
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $registry
if ($LASTEXITCODE -ne 0) { throw "ECR login failed. Is your AWS CLI configured for $Region?" }

Write-Host "Pushing $image ..." -ForegroundColor Cyan
docker push $image
if ($LASTEXITCODE -ne 0) { throw "docker push failed." }

Write-Host "Pushed $image" -ForegroundColor Green

if ($Restart) {
    if (-not $InstanceId) {
        throw "-Restart needs -InstanceId (get it from: terraform output instance_id)."
    }

    Write-Host "Restarting the service on $InstanceId ..." -ForegroundColor Cyan
    # The systemd unit re-pulls on every start, so a plain restart is enough to adopt the
    # new image — no separate `docker pull` step from here.
    $command = aws ssm send-command `
        --instance-ids $InstanceId `
        --region $Region `
        --document-name "AWS-RunShellScript" `
        --parameters 'commands=["systemctl restart reranker.service"]' `
        --query "Command.CommandId" --output text
    if ($LASTEXITCODE -ne 0) { throw "SSM send-command failed." }

    Write-Host "Sent. Follow it with:" -ForegroundColor Green
    Write-Host "  aws ssm get-command-invocation --command-id $command --instance-id $InstanceId --region $Region"
    Write-Host "Then confirm from the API instance:  curl http://<private_ip>:8080/health"
}
