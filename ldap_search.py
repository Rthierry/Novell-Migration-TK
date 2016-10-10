# @Author: Thierry Rangeard <Gandalf>
# @Date:   04-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de conversion metamig - csv - pandas
# @Last modified by:   Gandalf
# @Last modified time: 04-Oct-2016

import ldap
l =ldap.initialize('ldap://172.16.48.222:389')
r = l.search_s('O=netonline', ldap.SCOPE_SUBTREE, '(objectClass=Group)', ['member'])
for dn in r:
    print 'Processing', repr(dn)
