Param(
  [string]$rightsList,
  [string]$rootPath,
  [string]$domain
)

Import-Module NTFSSecurity
Get-Content $rightsList | Set-Content -Encoding utf8 $rightsList-utf8

Import-Csv $rightsList-utf8 | Foreach {
    $upn = $_.uid
    $directory = $_.path
    $rights = $_.trustee
    $appliesto = $_.appliesto
    
    Write-Host New-Item -ItemType Directory -Force -Path "${rootPath}\${directory}"
    try {
        New-Item -ItemType Directory -Force -Path "${rootPath}\${directory}"
        Add-NTFSAccess -Account "${domain}\${upn}" -Path "${rootPath}${directory}" -AccessRights "${rights}" -AppliesTo "${appliesto}"     
    }
    catch
    {
      "Error when Create directory or adding right for ${upn} on ${directory}." | Out-File .\Adddirectory.log -Append
      "$_.Message" | Out-File .\adddirectory.log -Append
    }
}