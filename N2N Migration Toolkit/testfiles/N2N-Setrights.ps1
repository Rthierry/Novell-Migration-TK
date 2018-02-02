Param(
  [string]$rightsList,
  [string]$rootPath,
  [string]$domain,
  

  #### Niveau de log, le mode Verbose affiche à l'écran les différentes étapes du script. Sinon seul le rapport est affiché
  [Parameter(Mandatory= $false)][ValidateSet("Normal", "Verbose")][string]$Logging,

  #### Délimiteur CSV, par défaut sur ";"
  [Parameter(Mandatory= $false)][string]$Delimiter = ";",

  #### Valeur à ajuster définitivement en modifiant la ligne ci-dessous. Elle peut également être réécrite en passant l'argument LogFile en ligne de commmande
  [Parameter(Mandatory= $false)][string]$LogFile = "~\Documents\SetRights.log",

  ### Définition des colonnes par défaut
  [Parameter(Mandatory= $false)][string]$idcol = "SAMAccountName",   ###Utilisateurs ou groupes
  [Parameter(Mandatory= $false)][string]$pathcol = "Path",           ###Répertoire
  [Parameter(Mandatory= $false)][string]$rightscol = "Rights",       ###Permissions
  [Parameter(Mandatory= $false)][string]$scopecol = "Scope"          ###Etendue

 
)

Import-Module NTFSSecurity
$Global:logger = ""

function log($text){  
    $Global:logger +=  "${text}`n"
    Write-Output $text
  
}
    
Import-Csv -Delimiter $Delimiter $rightsList -Encoding utf8 | Foreach {
    $upn = $_.${idcol}
    $directory = $_.${pathcol}
    $rights = $_.${rightscol}
    $appliesto = $_.${scopecol}
    
    $directory = $directory -replace "/","\"

    if ( -not [string]::IsNullOrEmpty($rights)) {
    
        log "`n[INFO] - $(Get-Date) --- Add following rights for ${domain}\${upn} to ${rootPath}${directory} : ${rights} " 
        try {        

            if ( -Not (Test-Path ${rootPath}${directory}) ){
                log "[INFO] - $(Get-Date) --- Creating folder ${rootPath}${directory}"
                try {
                    New-Item -Path ${rootPath}${directory} -ItemType directory -Force
                }catch {

                    log "[ERR] - $(Get-Date) --- Could not create directory ${rootPath}${directory}"

                }
            }


            $existingace = ""
        
            try {
                $existingace = Get-NTFSAccess -Path "${rootPath}${directory}" -Account "${domain}\${upn}" -ExcludeInherited | Where { $_.AccessControlType -eq "Allow" }
            }catch {                
                log "[INFO] - $(Get-Date) --- No ACE for ${domain}\${upn} on ${rootPath}${directory}. ACE non existent."
            
            }

            $accname = $existingace.Account.AccountName 
            log "[INFO] $(Get-Date) --- Checking for ${accname} ACE in ${rootPath}${directory}"
        
            
            if ([string]::IsNullOrEmpty($existingace.Account.AccountName)) {
                

                    try {
                        Add-NTFSAccess -Account "${domain}\${upn}" -Path "${rootPath}${directory}" -AccessRights "${rights}" -AppliesTo "${appliesto}"
                        log "[INFO] - $(Get-Date) --- Add ${rights} for ${domain}\${upn} to ${rootPath}${directory}" 
                    }catch{
                        log "[ERR] - $(Get-Date) --- Can't add rights ${domain}\${upn} to ${rootPath}${directory} . Entity exist ? " 
                    }

            }else {                        
           
                    log "[INFO] - $(Get-Date) --- Found existing rights for ${domain}\${upn} to ${rootPath}${directory}. No change applied" 

            }        
        }
        catch
        {
          log "[ERR] - Error when adding right for ${upn} on ${directory}."
          log "[ERR] - $_.Message" 

        }
    }else
    {
        log "[ERR] - Rights for ${upn} on ${directory} is null, skipping."
    }

}


### Ecriture dans le fichier de log
$Global:logger | Out-File -Encoding utf8 $LogFile -Append
