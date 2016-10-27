#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Adrien Néel <FullTacos>
# @Date:   24-Oct-2016
# @Email:  aneel@net-online.fr
# @Project: GetUser LDAP
# @Last modified by:   FullTacos
# @Last modified time: 24-Oct-2016

import sys, getopt
import ldap

def main(argv):
   servername = ''
   username = ''
   password = ''
   dnbase = ''
   try:
       opts, args = getopt.getopt(argv,"hs:u:p:d:",["help","server_ldap=","username=","password=","dn_base="])
   except getopt.GetoptError:
       print 'getuser_ldap.py -s <Ldap_Serveur_Adresse>'
       sys.exit(2)
   for opt, arg in opts:
       if opt in ("-h","--help"):
           print ("getuser_ldap.py -s adresse du serveur ldap")
           sys.exit()
       elif opt in ("-s","--server_ldap"):
           servername = arg
       elif opt in ("-u", "--username"):
           username = arg
       elif opt in ("-p", "--password"):
           password = arg
       elif opt in ("-d", "--dn_base"):
           dnbase = arg
       else:
           assert False, "unhandled option"
   print 'Le traitement recuperation'
   print (servername)

if __name__ == "__main__":
   main(sys.argv[1:])
   servername = str(sys.argv[2:3])
   username = str(sys.argv[4:5])
   password = str(sys.argv[6:7])
   dnbase = str(sys.argv[8:9])
   print (servername,username,password,dnbase)
   # adjust this to your base dn for searching
   connect = ldap.open('ldap://'servername':389')
   try:
       #if authentication successful, get the full user data
       connect.bind_s(username,password)
       r = connect.search_s(dnbase, ldap.SCOPE_SUBTREE, '(|(objectClass=User)(objectClass=Person)(objectClass=inetOrgPerson))', ['cn', 'mail'])
       for dn,entry in r:
          print 'Processing', repr(dn)
   except ldap.LDAPError:
       connect.unbind_s()
       print "authentication error"
