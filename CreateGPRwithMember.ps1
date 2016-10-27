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
    New-ADGroup -Name "$name" -SamAccountName $name -GroupCategory Security -GroupScope Global -DisplayName "$name" -Path "OU=Groupes-AD,DC=tephadet,DC=lan" -Description "Groupe $oldname dans eDirectrory"
    Add-ADGroupMember -identity ${name} -Member $memberadd

    
}
