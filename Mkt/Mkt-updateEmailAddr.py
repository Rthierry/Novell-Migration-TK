#!/usr/bin/python
# -*- coding: latin-1 -*-
#@Author: Thierry Rangeard <Gandalf>
#@Date:   03-May-2017
#@Email:  trangeard@net-online.fr
#@Project: Utilitaire de modification fichier migration MKT
#@Last modified by:   Gandalf
#@Last modified time: 03-May-2017
import unicodedata
import sys
import argparse
import pandas as pd
reload(sys)

sys.setdefaultencoding("utf8")

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, dest='input_file', help=" -> Fichier MergedEdirGroupWiseUsers.csv")
parser.add_argument("-o", type=str, dest='output_file', help=" -> Fichier de sortie")
parser.add_argument("-d", type=str, dest='email_dom', help=" -> Domaine de messagerie")
parser.add_argument("-u", type=str, dest='upn_logon', help=" -> Upn Domaine AD")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

if __name__ == "__main__":
    fichier_in = args.input_file
    fichier_out = args.output_file
    domaine = args.email_dom
    upn = args.upn_logon
    dfi = pd.read_csv(fichier_in,dtype=str);
    dfi = dfi.fillna('')
    for index, row in dfi.iterrows():
        prenom_raw = dfi.firstName[index]
        prenom = remove_accents(prenom_raw.decode("utf8").lower())
        nom_raw = dfi.lastName[index]
        nom = remove_accents(nom_raw.decode("utf8").lower())
        if prenom != "":
            new_email = (prenom + "." + nom +"@" + domaine)
            upn_logon = (prenom + "." + nom +"@" + upn)
        else:
            new_email = (nom +"@" + domaine)
            upn_logon = (nom +"@" + upn)
        print new_email
        print upn_logon
        # modification adresse email destination
        dfi.destinationEmail[index] = new_email
        # modification upnLogon
        dfi.upnLogon[index] = upn_logon
        # Copie gwUserId dans samAccountName
        dfi.samAccountNameLogon[index] = dfi.gwUserID[index]
        # ecriture dans le fichier
        dfi.to_csv(fichier_out, index=False)
        print("%d, ligne traitees" % (index))
