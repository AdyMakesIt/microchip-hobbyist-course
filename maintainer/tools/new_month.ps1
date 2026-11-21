param(
    [Parameter(Mandatory = $true)][int]$Month,
    [Parameter(Mandatory = $true)][string]$Slug,
    [string]$Prefix = "main",
    [string]$Title = ""
)

$ErrorActionPreference = "Stop"

$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$circuitsDir = Join-Path $toolsDir "circuits"
$mm = $Month.ToString("00")
$fnName = "month$Month"
if ([string]::IsNullOrWhiteSpace($Title)) {
    $Title = "Month $Month"
}

$modulePath = Join-Path $circuitsDir "month$mm.py"
if (-not (Test-Path $modulePath)) {
    $template = @"
from mhc_draw import Circuit, Board
from ._helpers import add_standard_rails, add_decoupling_cap


def $fnName():
    c = Circuit("$Title")
    b = Board(c)
    add_standard_rails(b, build=1)
    # TODO: Add IC, schematic chains, and breadboard placement for $Title
    return c, b
"@
    Set-Content -Path $modulePath -Value $template -Encoding UTF8
    Write-Host "Created $modulePath"
} else {
    Write-Host "Module already exists: $modulePath"
}

Write-Host ""
Write-Host "Add this import and entry to maintainer/tools/circuits/__init__.py:"
Write-Host "  from .month$mm import $fnName"
Write-Host "  {\"id\": \"m$Month\", \"month\": $Month, \"track\": \"$Prefix\", \"folder\": \"$Slug\", \"prefix\": \"$Prefix\", \"title\": \"$Title\", \"fn\": $fnName},"