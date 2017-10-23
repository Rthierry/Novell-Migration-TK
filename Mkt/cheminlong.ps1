Param(
  [string]$roadlist,
  [string]$copyto
)

#Import-Module NTFSSecurity
Get-Content $roadlist | Set-Content -Encoding utf8 $roadlist-utf8

Import-Csv $roadlist-utf8 | Foreach {
    $filepath = $_.path
#    $copyto = "c:\Test"
    
    Write-Host Copy-Item -Path "${filepath} to ${copyto}"
    try {
        Copy-Item -Path "${filepath}" -Destination "${copyto}"     
        echo "copy ${filepath} to ${copyto}" >> $copyto\chemin_long.log
    }
    catch
    {
      "Error when Copy file to directory ${filepath} on ${copyto}." | Out-File $copyto\errorscopychemin.log -Append
      "$_.Message" | Out-File $copyto\errorscopychemin.log -Append
    }
}