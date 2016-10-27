# @Author: Adrien Neel <AdrienN>
# @Date:   27-Oct-2016
# @Email:  aneel@net-online.fr
# @Project: CreateGRPwithMember
# @Fonction: cree des groupe dans un AD en ajoutant des membres avec un fichiers csv en entree
# @Last modified by:   AdrienN
# @Last modified time: 27-Oct-2016

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
