#!/usr/bin/python
# -*- coding: latin-1 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   20-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de conversion trustee - csv - pandas
# @Last modified by:   Gandalf
# @Last modified time: 13-01-2017

from xml.etree import ElementTree
import csv
import sys
import argparse
reload(sys)
sys.setdefaultencoding("utf8")

parser = argparse.ArgumentParser()
parser.add_argument("xml_file", type=str, help=" -> Fichier trustee.xml")

args = parser.parse_args()


def GETclean(xml_file):
    with open(xml_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('&', '&amp;'))
    return()


def GETtrustee(xml_file):
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
                print (ayant_droits)
                droits = []
                fichier.append(ayant_droits)
                droits = element.find('rights')
                print (droits.text)
                fichier.append(droits.text)
                csvwriter.writerow(fichier)
        trustee_data.close()
        return()


def GETtrustee1(xml_file):
    with open(xml_file, 'rt') as f:
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
                print ("path :"), chemin
                for trustees in member.findall('trustee'):
                    fichier = []
                    fichier.append(chemin)
                    ayant_droits = trustees.find('name').text
                    print ("ayant_droits:"), ayant_droits
                    fichier.append(ayant_droits)
                    # droits = member.find('trustee/rights').get('value')
                    droits = trustees.find('rights').get('value')
                    print ("droits:"),droits
                    fichier.append(droits)
                    csvwriter.writerow(fichier)
        trustee_data.close()
        return()


def GETUserquota(xml_file):
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


def GETDirquota(xml_file):
        f = xml_file
        tree = ElementTree.parse(f)
        root = tree.getroot()

        quota_data = open(sys.argv[1].strip('.xml')+"_dirquota.csv", 'w')
        csvwriter = csv.writer(quota_data)
        quota_data_head = ['Répertoire', 'Espace utilisé', 'Quota']
        csvwriter.writerow(quota_data_head)

        for items in root.findall('dirInfo/directory'):
            fichier = []
            name = items.find('path')
            path = name.text
            fichier.append(path)
            spaceused = items.find('spaceUsed')
            used = spaceused.text
            fichier.append(used)
            quotaAmount = items.find('quotaAmount')
            quota = quotaAmount.text
            fichier.append(quota)
            csvwriter.writerow(fichier)
        quota_data.close()
        return()


def GETIrf(xml_file):
    f = xml_file
    tree = ElementTree.parse(f)
    root = tree.getroot()
    irf_data = open(sys.argv[1].strip('.xml')+"_irf.csv", 'w')
    csvwriter = csv.writer(irf_data)
    irf_data_head = ['Path', 'irf']
    csvwriter.writerow(irf_data_head)

    for member in root.findall('trusteeInfo/file'):
        fichier = []
        for element in member.findall('path'):
            chemin = element.text
            print ("path :"), chemin
            for irf in member.findall('inheritedRightsFilter'):
                fichier = []
                fichier.append(chemin)
                irf_mask = irf.get('value')
                print ("irf:"), irf_mask
                fichier.append(irf_mask)
                # droits = member.find('trustee/rights').get('value')
                # droits = trustees.find('rights').get('value')
                csvwriter.writerow(fichier)
        csvwriter.writerow(fichier)
    irf_data.close()
    return()


if __name__ == "__main__":
    xml_file = args.xml_file
    print (xml_file)
# GETclean(xml_file)
    #GETtrustee1(xml_file)
# GETUserquota(xml_file)
# GETDirquota(xml_file)
    GETIrf(xml_file)
