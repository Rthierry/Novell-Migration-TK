#!/usr/bin/env/python3

from classes.Group import group
from classes.User import User
from pymongo import MongoClient
import sys
import pandas as pd
import re


class Directory(object):

    client = MongoClient()
    groups = []
    users = []


    def __init__(self, db):

        Directory.db = db
        Directory.dbclient = self.client[Directory.db]
