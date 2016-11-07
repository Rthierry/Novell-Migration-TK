#!/usr/bin/python
# -*- coding: latin-1 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   07-Nov-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de conversion trustee - csv
# @Last modified by:   Gandalf
# @Last modified time: 07-Nov-2016
from xml.etree import ElementTree
import csv
import argparse
import re
import sys
reload(sys)

sys.setdefaultencoding("utf8")
parser = argparse.ArgumentParser()
parser.add_argument("input_trustee", type=str, help=" -> Fichier trustee XXX.xml")
parser.add_argument("input_metamig", type=str, help=" -> Fichier metamig XXX.xml")

args = parser.parse_args()

def GETtrustee(xml_file):
    Killpoint = re.compile("^.(.*?)\.", re.IGNORECASE)
    with open(xml_file, 'rt') as f:
        tree = ElementTree.parse(f)
        root = tree.getroot()
        trustee_data = open(xml_file.strip('.xml')+"_trustee.csv", 'w')
        csvwriter = csv.writer(trustee_data, lineterminator='\n')
        trustee_data_head = ['ayant-droits', 'chemin', 'droits']
        csvwriter.writerow(trustee_data_head)
        for trustee in root.findall('trustee'):
            fichier = []
            nom = trustee.find('name').text
            user = re.findall(Killpoint, nom)
            fichier.append(str(user))
            chemin = trustee.get('path')
            fichier.append(chemin)
            droits = trustee.find('rights').text
            fichier.append(droits)
            print ("Chemin:"), chemin
            print ("nom :"), user
            # droits = member.find('trustee/rights').get('value')
            print ("droits:"), droits
            csvwriter.writerow(fichier)
        trustee_data.close()
        return()


def GETclean(xml_file):
    with open(xml_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('&', '&amp;'))
        return()


def GETmetamig(xml_file):
    with open(xml_file, 'rt') as f:
        tree = ElementTree.parse(f)
        root = tree.getroot()

        trustee_data = open(xml_file.strip('.xml')+"_trustee.csv", 'w')
        csvwriter = csv.writer(trustee_data)
        trustee_data_head = ['chemin', 'ayant-droits', 'droits']
        csvwriter.writerow(trustee_data_head)
        ldapgetcn = re.compile(".CN=(.*?)\..", re.IGNORECASE)
        for member in root.findall('trusteeInfo/file'):
            fichier = []
            for element in member.findall('path'):
                chemin = element.text
                print ("path :"), chemin
                for trustees in member.findall('trustee'):
                    fichier = []
                    fichier.append(chemin)
                    ayant_droits = trustees.find('name').text
                    ayant_droit = re.findall(ldapgetcn, ayant_droits)
                    print ("ayant_droits:"), ayant_droit
                    fichier.append(ayant_droit)
                    # droits = member.find('trustee/rights').get('value')
                    droits = trustees.find('rights').get('value')
                    print ("droits:"), droits
                    fichier.append(droits)
                    csvwriter.writerow(fichier)
        trustee_data.close()
        return()


def CompRights(input_user1, input_user2):
    with open(input_user1, 'rb') as fileuser1:
        # open file as dictionnary the columns headers:values
        csvuser1 = csv.DictReader(fileuser1)
        # open file with all the groups into the first row[0]
        with open(input_user2, 'rb') as fileuser2:
            csvreaderuser2 = csv.reader(fileuser2)
            # open a new file for writing the resulting match elements
            with open('rightsnotmatch.csv', 'wb') as csvnotmatch:
                writeracl = csv.DictWriter(csvnotmatch, csvuser1.fieldnames)
                # Use the same field names for the output file.
                writeracl.writeheader()
                # list built from the first row
                rows_user2 = [row[1] for row in csvreaderuser2]
                print rows_user2
                linenum = 0
                for item in csvuser1:
                    # looking for the key 'uid'
                    if item.get('ayant-droits') in rows_user2:
                        linenum = linenum + 1
                        # print("Correspondance trouvé : " + str(linenum) + " " + item.get('Users'))
                        # writing
                    else:
                        # if match get the value with the 'uid' key
                        print ("Différence trouvée entre metamig: " + item['ayant-droits'] + " et Trustees")
                        # writing the row to the new file
                        print(item)
                        writeracl.writerow(item)
    return()


if __name__ == "__main__":
    trustee_file = args.input_trustee
    metamig_file = args.input_metamig
    # Netoyage des fichiers
    # GETclean(trustee_file)
    # GETclean(metamig_file)
    # Exportation des trustees csv
    # GETtrustee(trustee_file)
    # GETmetamig(metamig_file)
    # Comparaison des fichiers
    CompRights(metamig_file, trustee_file)
