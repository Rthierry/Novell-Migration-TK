#!/usr/bin/python
# -*- coding: latin-1 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   20-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de conversion trustee - csv - pandas
# @Last modified by:   Gandalf
# @Last modified time: 20-Oct-2016

from xml.etree import ElementTree
import csv
import sys
import getopt
reload(sys)
sys.setdefaultencoding("utf8")


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print 'trustee2csv.py -i <inputfile.xml>'
        sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print 'trustee2csv.py -i <inputfile.xml> un fichier en sortie _trustee.csv'
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
        print 'Le fichier traité est :', inputfile
    return()


def  GETclean(xml_file):
    with open(xml_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('&', '&amp;'))
    return()


def  GETtrustee(xml_file):
    with open(xml_file, 'rt') as f:
        tree = ElementTree.parse(f)
        root = tree.getroot()
        print (root)
        trustee_data = open(sys.argv[1].strip('.xml')+"_trustees.csv", 'w')
        csvwriter = csv.writer(trustee_data)
        trustee_data_head = ['chemin', 'ayant-droits', 'droits']
        csvwriter.writerow(trustee_data_head)
        # for member in tree.findall('trustee'):
        #    fichier = []
        for element in root.findall('trustee'):
            print (element)
            chemin = element.get('path')
            print (chemin)
            for trustees in element.findall('name'):
                fichier = []
                fichier.append(chemin)
                ayant_droits = trustees.text
                print ayant_droits
                droits = []
                fichier.append(ayant_droits)
                droits = element.find('rights')
                print droits.text
                fichier.append(droits.text)
                csvwriter.writerow(fichier)
        trustee_data.close()
        return()


def GETquota(xml_file):
        f = xml_file
        tree = ElementTree.parse(f)
        root = tree.getroot()

        quota_data = open(sys.argv[1].strip('.xml')+"_quota.csv", 'w')
        csvwriter = csv.writer(quota_data)
        quota_data_head = ['Utilisateur', 'Espace utilisé', 'Quota']
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
    GETtrustee(sys.argv[1])
