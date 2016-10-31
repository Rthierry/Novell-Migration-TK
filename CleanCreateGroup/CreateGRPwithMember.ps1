Param(
  [string]$groupList,
  [string]$groupMemberList,
  [string]$destinationDN
)

#Get-Content $groupList | Set-Content -Encoding utf8 $groupList-utf8
Import-CSV $groupList | Foreach{
    $oldname = $_.oldGroup
    $name = $_.groupName
    $membercn = $_.memberCN
    $memberadd = $membercn.Split("{,}")
    #Write-Host "${dn},${destinationDN}"
    try {
    New-ADGroup -Name "$name" -SamAccountName $name -GroupCategory Security -GroupScope Global -DisplayName "$name" -Path "OU=Group-Annecy,DC=tephadet,DC=lan" -Description "Groupe $oldname dans eDirectrory"
    }
    catch
    {
      "Error when Create group ${name}." | Out-File .\Addgroupe.log -Append
      "$_.Message" | Out-File .\addgroupe.log -Append
    }
    try{
    Add-ADGroupMember -identity ${name} -Member $memberadd
    }
    catch
    {
      "Error when adding user: ${memberadd} on ${name}." | Out-File .\Adduser.log -Append
      "$_.Message" | Out-File .\adduser.log -Append
    }
    
}


