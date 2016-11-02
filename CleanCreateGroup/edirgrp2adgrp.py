#!/usr/bin/python
#-*- coding: utf-8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   18-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Moficication du fichier Groupe en sortie de la commande ldapsearch
# fichier entrée : listegrp en sortie out1.csv
# Création du fichier importAD_Group.csv
# @Last modified by:   Gandalf
# @Last modified time: 02-Nov-2016

import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")
import re
import csv

def GETclean(input_file, output_file):
    ldapgetcn = re.compile("cn=[0-9A-Z_a-z--]+", re.IGNORECASE)
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

def ADDElementGRP(input_file, listuser, output_file):
    with open(input_file, 'r') as csvinput:
        csvreader = csv.reader(csvinput)
        with open(listuser, 'rb') as csvuserlist:
            csvreaderrowuser = csv.reader(csvuserlist)
            onlyUserComm = [row[0] for row in csvreaderrowuser]
            with open(output_file, 'w') as csvoutput:
                csvwriter = csv.writer(csvoutput)
                Grp_Data_head = ['oldGroup','groupName','memberCN']
                all =[]
                sep =", "
                for row in csvreader:
                    if row[0] not in onlyUserComm:
                        oldGroup = "GG-"+row[0]
                        row.insert(1, oldGroup)
                        merged = sep.join(x for x in row[2:] if x.strip())
                        row[2:] = [merged]
                        csvwriter.writerow(row)
                    else:
                        print ("Found:" + row[0])
                        continue
            print('File parsed, columns added, users direct assigments cleared')
    return()

def FINDUserGRP(input_user, input_group):
    with open(input_user, 'rb') as csvuserlist:
        csvreaderrowuser = csv.reader(csvuserlist)
        with open(input_group, 'rb') as csvgrplist:
            csvreaderrowgrp = csv.reader(csvgrplist)
            rows_user_col1 = [row[0] for row in csvreaderrowuser]
            rows_grp_col2 = [row[0] for row in csvreaderrowgrp]
            linenum = 0
            for item in rows_grp_col2:
                if item not in rows_user_col1:
                    linenum = linenum + 1
                else:
                    linenum = linenum + 1
                    print("trouvé:" + item)
                    print("ligne :" + str(linenum))
                    print "dans fichier :" + input_group
    return()

if __name__ == "__main__":
    GETclean('listegrp.txt','out1.csv')
    ADDElementGRP('out1.csv','only-user-comm.csv','importAD_Group.csv')
    #FINDUserGRP('only-user-comm.csv','importAD_Group.csv')
