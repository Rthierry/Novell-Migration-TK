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

import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")
import re

def main(argv):
  inputfile = ''
  try:
     opts, args = getopt.getopt(argv,"hi:",["ifile="])
  except getopt.GetoptError:
     print 'Clean_Grp.py -i <inputfile>'
     sys.exit(2)
  for opt, arg in opts:
     if opt == '-h':
        print 'Clean_Grp.py -i <inputfile> un fichier en entrée <inputfile> et un en sortie out.csv'
        sys.exit()
     elif opt in ("-i", "--ifile"):
        inputfile = arg
  print 'Le fichier traité est :', inputfile
  return()

def CleanHomeDir(input_file, output_file):
   with open (input_file, 'r') as i:
       content = i.readlines()
       with open (output_file, 'w') as o:
           for lines in content:
               print (lines)
               #out = re.sub(r'^\"CN=.*.\"[,]\"', "", lines)
               #out1 = re.sub(r'\"', "", out)
               out12 = re.sub("\r\n", "", lines)
               out2 = out12 + ",\\" + out12 + ",\"Read,ReadAndExecute,Synchronize,Write,CreateFiles,CreateDirectories,Delete,Modify,ListDirectory\",ThisFolderSubFoldersAndFiles\n"
               o.write(out2)
   return()

if __name__ == "__main__":
   main(sys.argv[1:])
   CleanHomeDir(sys.argv[1],'Homedir-out.csv')
