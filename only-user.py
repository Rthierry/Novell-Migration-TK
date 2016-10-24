#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   16-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: CleanUp GRP
# @Last modified by:   Gandalf
# @Last modified time: 16-Oct-2016
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

def GETclean(input_file, output_file):
   with open (input_file, 'r') as i:
       content = i.readlines()
       with open (output_file, 'w') as o:
           for lines in content:
               if re.match('^\"CN=*', lines):
                   print (lines)
                   out = re.sub(r'^\"CN=', "", lines)
                   out1 = re.sub('[,].*', "", out)
                   o.write(out1)
               if re.match('^Processing*', lines):
                   print (lines)
                   out = re.sub(r'Processing \'cn=', "", lines)
                   out1 = re.sub('[,].*', "", out)
                   o.write(out1)
               else:
                   print ("Fichier non valide")
   return()

if __name__ == "__main__":
   main(sys.argv[1:])
   GETclean(sys.argv[1],'only-user.csv')
