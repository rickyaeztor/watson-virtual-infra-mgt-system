

class datastore_problem_desc:

     def __init__(self, datastores):
         self.datastores = datastores


     def generate_problem(self):
         problem = {}
         problem["subject"] = "vsphere datastores"
         problem["options"] = self.__get_options()
         problem["columns"] = self.__get_columns()
         return problem


     def __get_options(self):
         data_options = []
         for datastore in self.datastores:
             data_dict = { "values": {
                                    "capacityMB" : datastore['capacityMB'],
                                    "freeSpaceMB" : datastore['freeSpaceMB']
                                     },
                           "name": datastore['datastore_name'],
                           "key": datastore['_id']
                         }
             data_options.append(data_dict)
         return data_options


     def __get_columns(self):
         columns = [ {
                       "format": "number:0",
                       "type": "numeric",
                       "full_name": "Datastore Total Capacity",
                       "is_objective": "true",
                       "range": {
                            "low": 1000,
                            "high": 100000
                       },
                       "goal": "max",
                       "key": "capacityMB"
                      },
                     {
                       "format": "number:0",
                       "type": "numeric",
                       "full_name": "Datastore Free Space",
                       "is_objective": "true",
                       "range": {
                            "low": 100,
                            "high": 100000
                        },
                        "goal": "min",
                        "key": "freeSpaceMB"
                   } ]

         return columns