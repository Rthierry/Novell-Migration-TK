#!/usr/bin/python
# -*- coding: latin-1 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   02-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de conversion metamig - csv - pandas
# @Last modified by:   Gandalf
# @Last modified time: 10-Oct-2016
import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")
from xml.etree import ElementTree
import csv

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'nss2csv.py -i <inputfile.xml>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'nss2csv.py -i <inputfile.xml> deux fichiers en sortie _trustee.csv et _quota.csv'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print 'Le fichier traité est :', inputfile
   return()


def GETclean(xml_file):
    with open (xml_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('&', '&amp;'))
        return()

def GETtrustee(xml_file):
    with open( xml_file, 'rt') as f:
        tree = ElementTree.parse(f)
        root = tree.getroot()

        trustee_data = open(sys.argv[1].strip('.xml')+"_trustee.csv", 'w')
        csvwriter = csv.writer(trustee_data)
        trustee_data_head = ['chemin', 'ayant-droits', 'droits']
        csvwriter.writerow(trustee_data_head)

        for member in root.findall('trusteeInfo/file'):
            fichier = []
            for element in member.findall('path'):
                chemin = element.text
                print ("path :"),chemin
                for trustees in member.findall('trustee'):
                    fichier = []
                    fichier.append(chemin)
                    ayant_droits = trustees.find('name').text
                    print ("ayant_droits:"), ayant_droits
                    fichier.append(ayant_droits)
                    #droits = member.find('trustee/rights').get('value')
                    droits = trustees.find('rights').get('value')
                    print ("droits:"),droits
                    fichier.append(droits)
                    csvwriter.writerow(fichier)
        trustee_data.close()
        return()

def GETquota(xml_file):
        f = xml_file
        tree = ElementTree.parse(f)
        root = tree.getroot()

        quota_data = open(sys.argv[1].strip('.xml')+"_quota.csv", 'w')
        csvwriter = csv.writer(quota_data)
        quota_data_head = ['Utilisateur' ,'Espace utilisé' ,'Quota']
        csvwriter.writerow(quota_data_head)

        for items in root.findall('userInfo/user'):
            fichier = []
            name = items.find('name')
            user = name.text
            fichier.append(user)
            spaceused = items.find('spaceUsed')
            used = spaceused.text
            fichier.append(used)
            quotaAmount = items.find('quotaAmount')
            quota = quotaAmount.text
            fichier.append(quota)
            csvwriter.writerow(fichier)
        quota_data.close()
        return()


if __name__ == "__main__":
    main(sys.argv[1:])
    GETclean(sys.argv[1])
    GETtrustee(sys.argv[1])
    # GETquota(sys.argv[1])
