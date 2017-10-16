# @Author: Thierry Rangeard <Gandalf>
# @Date:   12-oct-2017
# @Email:  trangeard@net-online.fr
# @Project: Conversion des droits Netware en droits NTFS
# @Last modified by:   Gandalf
# @Last modified time: 12-oct-2017

import re
import sys
import csv
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, dest='input_file', help=" -> Fichier trustees_xxx_trustee.csv")
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()


# distiguisedname;uid;path;trusteeNovell
# exemple: CN=INFO,OU=HDV,DC=ANNECY,DC=LOC,Info,\,RCWMEF
# user,uid,path,trustee,appliesto
# exemple d'une ligne en sortie:"CN=INFO,OU=HDV,DC=ANNECY,DC=LOC","Info","\","Read,ReadAndExecute,Synchronize,Write,CreateFiles,CreateDirectories,Delete,Modify,ListDirectory","ThisFolderSubFoldersAndFiles"

def Trait_1(csv_file):
    with open(csv_file, 'rt') as f:
        csvreader = csv.reader(f, delimiter=';')
        trustee_data = open(args.input_file.strip('.csv')+"_To_NTFS.csv", 'w')
        csvwriter = csv.writer(trustee_data, delimiter=',', quotechar='\"', quoting=csv.QUOTE_NONNUMERIC)
        trustee_data_head = ['user', 'uid', 'path', 'trustee', 'appliesto']
        csvwriter.writerow(trustee_data_head)
        for row in csvreader:
            line = []
            i = 0
            path = ""
            traverse = ""
            user = row[0]
            uid = row[1]
            chemin = row[2]
            rep = Path(chemin).parts
            if len(rep) > 1:
                rep = rep[:-1]
                for path in rep[:-1]:
                    line = []
                    line.append(user)
                    line.append(uid)
                    i = i+1
                    traverse = traverse + '/' + rep[i]
                    print(traverse)
                    line.append(traverse)
                    line.append("ReadAndExecute,Synchronize")
                    line.append("ThisFolderOnly")
                    csvwriter.writerow(line)
                line = []
                line.append(user)
                line.append(uid)
                line.append(chemin)
                droits = row[3]
                aclentry = calcRights(droits)
                line.append(aclentry)
                csvwriter.writerow(line)
            else:
                print (rep)
                line = []
                line.append(user)
                line.append(uid)
                line.append(chemin)
                droits = row[3]
                aclentry = calcRights(droits)
                line.append(aclentry)
                line.append("ThisFolderSubFoldersAndFiles")
                print (user + " " + uid + " " + path + " " + droits)
                print(line)
                csvwriter.writerow(line)
        trustee_data.close()
    return()


def calcRights(droits):
    acl = []
    if re.match('.*R.*', droits):
        acl.append("Read,ReadAndExecute,Synchronize")
    if re.match('.*W.*', droits):
        acl.append("Write")
    if re.match('.*C.*', droits):
        acl.append("CreateFiles,CreateDirectories")
    if re.match('.*E.*', droits):
        acl.append("Delete")
    if re.match('.*M.*', droits):
        acl.append("Modify")
    if re.match('.*F.*', droits):
        acl.append("ListDirectory")
    if re.match('.*A.*', droits):
        acl.append("ReadPermissions,ChangePermissions")
    aclentry = ','.join(acl)
    return(aclentry)

if __name__ == "__main__":
    Trait_1(args.input_file)
