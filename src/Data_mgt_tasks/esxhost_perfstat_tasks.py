from watson_developer_cloud import TradeoffAnalyticsV1
from ..Db_operations.cloudant_db_op import  cloundant_db_op

class esxhost_perfstat_tasks():

      DEF_BUCKET_NAME = "esxhost_perfstats"

      def __init__(self):
          self.db_op = cloundant_db_op(self.DEF_BUCKET_NAME)

      def create_esxhost(self, data):
          return self.db_op.create_doc(data)

      def get_esxhost(self, key):
          return self.db_op.get_doc(key)

      def get_all_esxhosts(self):
          docs = []
          rs_collections = self.db_op.get_all_docs()
          for rs in rs_collections:
              docs.append(rs)
          return docs