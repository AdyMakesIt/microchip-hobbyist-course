[CmdletBinding()]
param(
    [switch]$PullProjects
)

$ErrorActionPreference = "Stop"

$ToolsDir = $PSScriptRoot
$RepoRoot = (Resolve-Path (Join-Path $ToolsDir "..\..")).Path
$MakeProjects = Join-Path $ToolsDir "make_projects.py"
$SyncReadmeMonths = Join-Path $ToolsDir "sync_readme_months.py"
$CheckAllPy = Join-Path $ToolsDir "check_all.py"

$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) {
    $pyCmd = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $pyCmd) {
    Write-Error "Python was not found on PATH."
    exit 1
}
$Python = $pyCmd.Source

Push-Location $RepoRoot
try {
    if ($PullProjects) {
        Write-Host "Pulling tested project changes back into code/..." -ForegroundColor Cyan
        & $Python $MakeProjects --pull
        if ($LASTEXITCODE -ne 0) {
            Write-Host "FAIL could not pull project changes into code/." -ForegroundColor Red
            exit $LASTEXITCODE
        }
    }

    & $Python $MakeProjects --check
    if ($LASTEXITCODE -ne 0) {
        $canPrompt = [Environment]::UserInteractive -and (-not [Console]::IsInputRedirected)
        if ($canPrompt) {
            Write-Host ""
            Write-Host "Project files differ from code/." -ForegroundColor Yellow
            $answer = Read-Host "Sync from the project into code/ now? [y/N]"
            if ($answer.Trim().ToLower() -in @("y", "yes")) {
                & $Python $MakeProjects --pull
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "FAIL could not pull project changes into code/." -ForegroundColor Red
                    exit $LASTEXITCODE
                }
            }
            else {
                Write-Host "Skipping sync. Update code/<build>/main.c manually or run with -PullProjects." -ForegroundColor Yellow
                exit 1
            }
        }
        else {
            Write-Host ""
            Write-Host "FAIL project files differ from code/ (non-interactive session)." -ForegroundColor Red
            Write-Host "Update code/<build>/main.c from the project, or re-run with -PullProjects." -ForegroundColor Yellow
            exit $LASTEXITCODE
        }
    }

    Write-Host "Updating README.md months table from course_data.PLAN..." -ForegroundColor Cyan
    & $Python $SyncReadmeMonths
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAIL could not update README.md months table." -ForegroundColor Red
        exit $LASTEXITCODE
    }

    & $Python $CheckAllPy
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
