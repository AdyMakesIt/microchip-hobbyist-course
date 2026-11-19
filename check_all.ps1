#!/usr/bin/env pwsh
<#
.SYNOPSIS
Runs the repository's full consistency check.

.DESCRIPTION
Locates the repository root from this script's location, then runs
maintainer/tools/check_all.py using the available Python interpreter.

Works on Windows PowerShell 5.1+ and PowerShell 7+.
#>

$ErrorActionPreference = "Stop"

# Repository root is the parent of the directory containing this script.
$RepoRoot = $PSScriptRoot
$CheckScript = Join-Path $RepoRoot "maintainer\tools\check_all.py"

if (-not (Test-Path -LiteralPath $CheckScript)) {
    Write-Error "Could not find check script: $CheckScript"
    exit 1
}

# Find Python: prefer "python", then "python3".
$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $Python) {
    Write-Error "Python was not found on PATH. Install Python or add it to PATH."
    exit 1
}

Write-Host "Repository: $RepoRoot"
Write-Host "Python:     $($Python.Source)"
Write-Host "Running checks..."
Write-Host ""

& $Python.Source $CheckScript
$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "Checks completed successfully." -ForegroundColor Green
}
else {
    Write-Host "Checks failed." -ForegroundColor Red
}

exit $exitCode
