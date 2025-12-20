param(
  [Parameter(Mandatory=$true)][string]$Root,
  [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'

$pattern = '\{\{<\s*button\s+href="https://wa\.me/905339454639"\s+target="_blank"\s*>\}\}(?s:.*?)\{\{<\s*/button\s*>\}\}'
$regex = [regex]::new($pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

$files = Get-ChildItem -Path $Root -Recurse -File -Filter index.md

$changed = 0
foreach ($f in $files) {
  $text = Get-Content -Path $f.FullName -Raw
  if ($regex.IsMatch($text)) {
    $newText = $regex.Replace($text, "{{< contact-buttons >}}")
    if ($newText -ne $text) {
      $changed++
      Write-Host "PATCH: $($f.FullName)"
      if (-not $WhatIf) {
        Set-Content -Path $f.FullName -Value $newText -NoNewline
      }
    }
  }
}

Write-Host "Done. Changed files: $changed"