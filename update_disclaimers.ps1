$ErrorActionPreference = "Stop"
$path = "d:\PROGRAMMING\drcil\content\tr\hizmetler"
$excludeDir = "kardiyovaskuler-korunma"
$alertText = @"

{{< alert type="info" >}}
Bu içerik, Türkiye Cumhuriyeti Sağlık Bakanlığı mevzuatına ve tıbbi etik kurallara uygun olarak, toplum sağlığını korumak ve bilgilendirmek amacıyla hazırlanmıştır. Herhangi bir tanı, tedavi garantisi veya yönlendirme içermez. En doğru bilgi için yetkili bir sağlık kuruluşuna başvurunuz.
{{< /alert >}}
"@

$files = Get-ChildItem -Path $path -Recurse -Filter "index.md"
foreach ($file in $files) {
    if ($file.Directory.Name -eq $excludeDir) { 
        Write-Host "Skipping excluded: $($file.Directory.Name)"
        continue 
    }

    $content = [System.IO.File]::ReadAllText($file.FullName)
    
    if ($content.Contains("Sağlık Bakanlığı mevzuatına")) {
        Write-Host "Skipping $($file.Directory.Name) - Already Contains Disclaimer"
        continue
    }

    # Regex to find end of front matter
    if ($content -match "(?s)^(\s*---.*?---)(.*)$") {
        $frontMatter = $matches[1]
        $restOfContent = $matches[2]
        $newContent = $frontMatter + "`r`n" + $alertText + "`r`n" + $restOfContent
        
        [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.Encoding]::UTF8)
        Write-Host "Updated $($file.Directory.Name)"
    } else {
        Write-Host "Skipping $($file.Directory.Name) - No Front Matter Found"
    }
}
