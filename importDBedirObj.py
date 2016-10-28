#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   16-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: CleanUp GRP
# @Last modified by:   Gandalf
# @Last modified time: 16-Oct-2016
import sqlite3
import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")
import re

CreateDataBase = sqlite3.connect('nss2db.db')
QueryCurs = CreateDataBase.cursor()

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'Clean_Grp.py -i <inputfile.txt>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'Clean_Grp.py -i <inputfile.xml> deux fichiers en sortie _trustee.csv et _quota.csv'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print 'Le fichier traité est :', inputfile
   return()

def removeSub(item):
    if re.match("^\w+\.\w+$", str(item)):
        return(item)
    else:
        rowsub = re.sub(r'^\w+\.',"",str(item))
        return(rowsub)


def GETclean(input_file, output_file):
    ldappattern = re.compile("cn=[\w-]+\b", re.IGNORECASE)
    with open (input_file, 'r') as i:
        content = i.readlines()
        with open (output_file, 'w') as o:
            for lines in content:
                print (lines)
                out = re.sub(r'Processing \(\'', "groupe=\'", lines)
                out1 = re.sub(r', {\'member\'\: \[',",",out)
                out2 = re.sub(r'\]\}\)',"",out1)
                o.write(out2)
    return()

def CreateTables():
    QueryCurs.execute('''CREATE TABLE Users(id INTEGER PRIMARY KEY, Nom TEXT, Dn TEXT)''')
    QueryCurs.execute('''CREATE TABLE Groups(id INTEGER PRIMARY KEY, Nom TEXT, DN TEXT)''')

def AddEntryUser(Nom,Dn):
    QueryCurs.execute('''INSERT INTO Users (Nom,Dn)
    VALUES (?,?)''',(Nom,Dn))

def AddEntrygroup(Nom,Dn):
    QueryCurs.execute('''INSERT INTO Groups (Nom,Dn)
    VALUES (?,?)''',(Nom,Dn))


if __name__ == "__main__":
    GETclean('listegrp.txt','out.txt')
    CreateTables()
