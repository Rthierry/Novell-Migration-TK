![NetOnline](http://www.net-online.fr/var/ezwebin_site/storage/images/design/net-online/172-11-fre-FR/Net-Online.png)

Title: **README file for NovellToMs migration toolkit**

Date: 07/11/2017

Auteur: Adrien Néel Net Online

Emails: aneel@net-online.fr

---

Content
=======

1.	Important Notes
2.	Scenario
3.	Scripts
4.	Installation
5.	Legal Notices

###### This is NovellToMs migration toolkit, version 1.0.0 (2017-11-07).

### 1. Important Notes

This tools is used to migrate Novell File Server on Microsoft File Server. To optimase your sucessful project, you devez: - Novell server on OES2 SP1 to OES2015 SP2 - Microsoft server on 2012 to 2016 server - Install Microsoft powershell Module NTFSSecurity - Use Copy software (Vice Versa Pro) or robocopy or rsync

### 2 Scenario

You are a Novell file server with NSS shared installed on this. You would like to migrate the data file on conseve rights. You can used this tool! - First you devez extarct data on OES server to created an inventory file (Used Inventory-XXX.xls) - Second you apply script on metadata file to extract NSS rights. - Third you apply script to modify NSS rights on NTFS right - Fourth you copy data - Five you apply NTFS rights - Sixe you testing!

### 3. Scripts

-	Launch inventory-script.py script to extract data for complete Inventory-XXX.xls
-	Connect to NRM (Novell Remote Manager) to extrat NSS Volumes information to complete Inventory-XXX.xls
-	Launch trustee2csv.py script to extract NSS rights on metadata file (metamig-SERVER-VOL.xml)
-	Launch NW_Trustees_TO_NTFS.py script to modifiy NSS rights on NTFS rights
-	Copy files to NSS on MS server
-	Launch N2N-SetRights.ps1 on windows server after validate NTFS rights file and verify that your copy is finish
