#!/usr/bin/env python3
from pymongo import MongoClient

import pandas as pd
import re




class DirectoryDB(object):

    client = MongoClient()
    errorLog = []
    verbose = 0

    def __init__(self, db, verbose):
        DirectoryDB.db = db
        DirectoryDB.verbose = verbose

        ### Connect to DB
        DirectoryDB.dbclient = self.client[DirectoryDB.db]

        ### User and group database collection
        DirectoryDB.UserCollection = self.dbclient['Users']
        DirectoryDB.GroupCollection = self.dbclient['Groups']
        DirectoryDB.GroupMemberCollection = self.dbclient['GroupMembers']

        ##Import Directory collection from DB
        DirectoryDB.UserList = self.importCollectionFromDB(self.UserCollection)
        DirectoryDB.GroupList = self.importCollectionFromDB(self.GroupCollection)
        DirectoryDB.GroupMemberList = self.importCollectionFromDB(self.GroupMemberCollection)


    # -----------------------------------------------
    # -----------   Extraction Method ---------------
    # -----------------------------------------------
    @classmethod
    def importCollectionFromDB(self, collection):
        acelist = collection.find()
        return acelist

    @classmethod
    def insertLineToDB(self, post, collection):
        post_id = collection.update_one(post, { '$set' : post }, upsert=True)


    @classmethod
    def exportToCSV(self):

        pd.DataFrame(list(self.UserList)).to_csv(self.db+"-users.csv")
        pd.DataFrame(list(self.GroupMemberList)).to_csv(self.db+"-groupmembers.csv")
        print ("User List : "+self.db+"-users.csv")
        print ("Group List : "+self.db+"-groups.csv")


    # -----------------------------------------------
    # -----------   Generation Method ---------------
    # -----------------------------------------------
    @classmethod
    def generateMemberList(self):
        self.GroupMemberList = []
        for group in self.GroupList:
            for member in group['member']:
                for user in group['member'][0]:
                    if user is not None:
                        userMatch = self.UserCollection.find_one({ 'dn' : user})
                        if self.verbose : print ("Looking for : "+user)
                        if userMatch is not None:
                            if self.verbose : print ("Matched with "+userMatch['uid'])
                            self.insertLineToDB({ 'dn' : group['dn'], 'groupid' : group['cn'], 'member' : user, 'uid' : userMatch['uid'] }, self.GroupMemberCollection )

                        else:
                            if self.verbose : print("No match for "+user)
