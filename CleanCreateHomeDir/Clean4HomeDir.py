#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   16-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: CreateHomeDir
# @Fonction: nettoyage et ajout au bon format pour utiliser CreateDirwithRigths.ps1
# @Aide: python Clean4HomeDir.py liste.txt
# @Last modified by:   AdrienN
# @Last modified time: 23-Oct-2016

import sys
import re
import argparse
reload(sys)
sys.setdefaultencoding("utf8")


parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=str, help=" -> Fichier trustee liste.txt")

args = parser.parse_args()

def  CleanHomeDir(input_file, output_file):
    with open(input_file, 'r') as i:
        content = i.readlines()
        with open(output_file, 'w') as o:
            for lines in content:
                print (lines)
                out = re.sub(r'^\"CN=.*.\"[,]\"', "", lines)
                out1 = re.sub(r'\"', "", out)
                out12 = re.sub("\r\n", "", out1)
                out2 = out12 + ",\\" + out12 + ",\"Read,ReadAndExecute,Synchronize,Write,CreateFiles,CreateDirectories,Delete,Modify,ListDirectory\",ThisFolderSubFoldersAndFiles\n"
                o.write(out2)
    return()

if __name__ == "__main__":
    CleanHomeDir(input_file, 'CleanHomedir-out.csv')
