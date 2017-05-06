from cloudant import Cloudant
import os
import json



class cloundant_proxy:

    DEF_USER =  "85503c60-2116-40ba-afba-2fac974fd814-bluemix"
    DEF_PASS = "d3af0265b2427f7fff9fa3f011291bc498dcc3fc1bb7cf9be3bc95d8041460c1"
    DEF_URL = "85503c60-2116-40ba-afba-2fac974fd814-bluemix.cloudant.com"

    def __init__(self, db_name):
        self.db_name = db_name
        self.db = self.connect()

    def connect(self):
        self.client = Cloudant(self.DEF_USER, self.DEF_PASS, url='https://' + self.DEF_URL, connect=True)
        self.client.connect()
        db = self.client.create_database(self.db_name, throw_on_exists=False)
        return db

    def disconnect(self):
        self.client.disconnect()

    def __del__(self):
        self.disconnect()


