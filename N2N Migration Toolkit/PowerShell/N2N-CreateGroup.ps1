Param(
  [string]$groupList,
  [string]$ADBaseDN,
  [Parameter(Mandatory= $true)][string]$groupcol,
  [Parameter(Mandatory= $true)][string]$membercol,
  [Parameter(Mandatory= $false)][string]$pathcol  
)

function log($text){  
  $logger +=  $text
  Write-Output $text

}


$logger = ""

### Create Group in AD
Import-Csv $groupList -Encoding utf8 | Select-Object -ExpandProperty $groupcol -Unique | ForEach-Object {      
    $SAM = $_

    $grpexist = Get-ADGroup -LDAPFilter "(SAMAccountName=$SAM)"

    if ( $grpexist -eq $null){
      log "$(Get-Date) --- Creating group $SAM"
      
      New-ADGroup -Path "${ADBaseDN}" -SamAccountName $SAM -Name $SAM -GroupCategory Security -GroupScope Global
    }else{
      log "$(Get-Date) --- Group $SAM already exist"      
      
    }
}


### Add Members
Import-Csv $groupList -Encoding utf8 | ForEach-Object {      
  $group = $_."${groupcol}"
  $member = $_."${membercol}"

  $grpexist = Get-ADGroup -LDAPFilter "(SAMAccountName=$group)"

  if ( $grpexist -eq $null){
    log "$(Get-Date) --- Group does not exist : $group, might come from synchronization lag, try to run the script again in a few seconds"   

  }else{
    log "$(Get-Date) --- Adding $member to $group"     
    Add-ADGroupMember -Members $member $group     
    Write-Output $log
  }
}

$logger | Out-File -Encoding utf8 "creategroup.txt"