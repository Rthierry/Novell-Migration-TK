#!/usr/bin/python
#-*- coding: utf-8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   18-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Moficication du fichier Groupe en sortie de la commande ldapsearch
# fichier entrée : listegrp en sortie out1.csv
# Création du fichier importAD_Group.csv
# @Last modified by:   Gandalf
# @Last modified time: 27-Oct-2016

import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")
import re
import csv

def GETclean(input_file, output_file):
    ldapgetcn = re.compile("cn=[0-9A-Za-z--]+", re.IGNORECASE)
    list0 = []
    grouplistOut = []
    with open(input_file, 'r') as i:
        content = i.readlines()
        with open(output_file, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            for line in content:
                list0 = re.findall(ldapgetcn,str(line))
                list1 = re.sub(r'\'cn=','',str(list0))
                list2 = re.sub(r'\'','',list1)
                list3 = re.sub(r'\[','',list2)
                list4 = re.sub(r'\]','',list3)
                list5 = re.sub(r' ','',list4)
                list6 = list5.split(',')
                writer.writerow(list6)
    print('Nettoyage du fichier')
    return()

def ADDElementGRP(input_file, output_file):
    with open(input_file, 'r') as csvinput:
        csvreader = csv.reader(csvinput)
        with open(output_file, 'w') as csvoutput:
            csvwriter = csv.writer(csvoutput)
            Grp_Data_head = ['oldGroup','groupName','memberCN']
            all =[]
            sep =", "
            for row in csvreader:
                oldGroup = "GG-"+row[0]
                row.insert(1, oldGroup)
                merged = sep.join(x for x in row[2:] if x.strip())
                row[2:] = [merged]
                csvwriter.writerow(row)
    print('Ajout colonne')
    return()

if __name__ == "__main__":
    GETclean('listegrp.txt','out1.csv')
    ADDElementGRP('out1.csv','importAD_Group.csv')
