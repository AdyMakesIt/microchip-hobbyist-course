<#
.SYNOPSIS
    Finds Markdown image links pointing to .png files and updates them to .svg
    when a matching .svg file exists on disk.
.PARAMETER DryRun
    Preview matching files and links without prompting or writing changes.
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RelativePathCompat {
    param(
        [Parameter(Mandatory)][string]$BasePath,
        [Parameter(Mandatory)][string]$TargetPath
    )
    $baseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    $targetFull = [System.IO.Path]::GetFullPath($TargetPath)
    if ($targetFull.StartsWith($baseFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $targetFull.Substring($baseFull.Length)
    }
    return $targetFull
}

# Resolve repository root two levels up from maintainer/tools
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Write-Host "Repository root: $RepoRoot" -ForegroundColor DarkCyan

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

$mdFiles = Get-ChildItem -Path $RepoRoot -Recurse -Filter *.md -File |
Where-Object { $_.FullName -notmatch '\\(\.git|node_modules|\.pio|\.venv|venv)\\' }

$totalUpdatedFiles = 0
$totalUpdatedLinks = 0

foreach ($file in $mdFiles) {
    $raw = [System.IO.File]::ReadAllText($file.FullName, $utf8NoBom)
    if ([string]::IsNullOrEmpty($raw)) { continue }

    $fileReplacements = [System.Collections.Generic.List[string]]::new()

    $updated = [regex]::Replace($raw, '(!\[[^\]]*\]\()([^)]+)\.png(\))', {
            param($m)
            $relStem = $m.Groups[2].Value
            # Skip remote URLs
            if ($relStem -match '^(https?:)?//') { return $m.Value }

            $svgCandidate = Join-Path $file.DirectoryName ($relStem + ".svg")
            if (Test-Path -LiteralPath $svgCandidate -PathType Leaf) {
                $newTag = "$($m.Groups[1].Value)$relStem.svg$($m.Groups[3].Value)"
                $fileReplacements.Add("  $($m.Value)  -->  $newTag")
                return $newTag
            }
            return $m.Value
        })

    if ($fileReplacements.Count -gt 0) {
        $relPath = Get-RelativePathCompat -BasePath $RepoRoot -TargetPath $file.FullName
        Write-Host "`n$relPath ($($fileReplacements.Count) match(es)):" -ForegroundColor Cyan
        $fileReplacements | ForEach-Object { Write-Host $_ }

        if ($DryRun) { continue }

        $ans = Read-Host "Update .png -> .svg in ${relPath}? [y/N]"
        if ($ans -match '^(y|yes)$') {
            [System.IO.File]::WriteAllText($file.FullName, $updated, $utf8NoBom)
            Write-Host "Updated $relPath" -ForegroundColor Green
            $totalUpdatedFiles++
            $totalUpdatedLinks += $fileReplacements.Count
        }
        else {
            Write-Host "Skipped $relPath" -ForegroundColor Yellow
        }
    }
}

if ($DryRun) {
    Write-Host "`nDry run complete. No files were modified." -ForegroundColor DarkCyan
}
else {
    Write-Host "`nDone. Updated $totalUpdatedLinks link(s) across $totalUpdatedFiles file(s)." -ForegroundColor Green
}
