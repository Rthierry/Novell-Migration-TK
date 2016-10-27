# @Author: Thierry Rangeard <Gandalf>
# @Date:   18-Oct-201
# @Email:  trangeard@net-online.fr
# @Project: Moficication du fichier Groupe en sortie de la commande ldapsearch
# @Last modified by:   Gandalf
# @Last modified time: 27-Oct-2016
#!/usr/bin/python
#-*- coding: utf-8 -*-
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
                list5 = list4.split(',')
                writer.writerow(list5)
                #o.write(list4+'\n')
    return()

def ADDElementGRP(input_file, output_file):
    with open(input_file, 'r') as csvinput:
        csvreader = csv.reader(csvinput)
        with open(output_file, 'w') as csvoutput:
            csvwriter = csv.writer(csvoutput)
            Grp_Data_head = ['oldGroup','groupName','memberCN']
            all = []
            row = next(csvreader)
            row.insert(0, 'oldGroup')
            all.append(row)
            csvwriter.writerows(all)
            row0 = csvreader.next()
            print row0[0]
    return()

if __name__ == "__main__":
    GETclean('listegrp.txt','out1.csv')
    ADDElementGRP('out1.csv','out2.csv')

# for line in grouplistOut:
    # content =
    # print line[1]
    # for line in list2:
    # print line
    #for cn in list:
    #    name = re.sub(r"cn=",r"", cn)
    #print(name)
