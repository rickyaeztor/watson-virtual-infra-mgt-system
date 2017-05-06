

class cluster_problem_desc:

     def __init__(self, clusters):
         self.clusters = clusters


     def generate_problem(self):
         problem = {}
         problem["subject"] = "vsphere clusters"
         problem["options"] = self.__get_options()
         problem["columns"] = self.__get_columns()
         return problem


     def __get_options(self):
         data_options = []
         for cluster in self.clusters:
             data_dict = { "values": {
                                    "totalCpuCapacityMhz" : cluster['totalCpuCapacityMhz'],
                                    "clusLoadDeviation" : cluster['clusLoadDeviation'],
                                    "totalMemCapacityMB" : cluster['totalMemCapacityMB'],
                                    "memDemandMhz" : cluster['memDemandMhz'],
                                    "cpuDemandMhz" : cluster['cpuDemandMhz']
                                     },
                           "name": cluster['cluster_name'],
                           "key": cluster['_id']
                         }
             data_options.append(data_dict)
         return data_options


     def __get_columns(self):
         columns = [ {
                       "format": "number:0",
                       "type": "numeric",
                       "full_name": "Cluster Total CPU Capacity",
                       "is_objective": "true",
                       "range": {
                            "low": 1000,
                            "high": 50000
                       },
                       "goal": "max",
                       "key": "totalCpuCapacityMhz"
                      },
                     {
                       "format": "number:0",
                        "type": "numeric",
                       "full_name": "Cluster Total Memory Capacity",
                       "is_objective": "true",
                       "range": {
                            "low": 1000,
                            "high": 50000
                        },
                        "goal": "max",
                        "key": "totalMemCapacityMB"
                   } ]

         return columns