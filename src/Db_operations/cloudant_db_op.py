

from ..cloudant_proxy import cloundant_proxy
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey


class cloundant_db_op(cloundant_proxy):

     def __init__(self, db_name):
         super(cloundant_db_op, self).__init__(db_name)

     def get_doc(self, key):
         return self.db[key]

     def get_all_docs(self):
         rs_collection =  Result(self.db.all_docs, include_docs=True)
         return rs_collection

     def create_doc(self, data):
         new_doc = self.db.create_document(data)
         if new_doc.exists():
              print("A document was created")
         return new_doc



