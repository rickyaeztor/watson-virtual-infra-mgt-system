
class esxhost_problem_desc:

     def __init__(self, esxhosts):
         self.esxhosts = esxhosts

     def generate_problem(self):
         problem = {}
         problem["subject"] = "vsphere esxhosts"
         problem["options"] = self.__get_options()
         problem["columns"] = self.__get_columns()
         return problem


     def __get_options(self):
         data_options = []
         for esxhost in self.esxhosts:
             data_dict = { "values": {
                                    "cpu_utilization" : esxhost['cpu_utilization'],
                                    "memory_utilization" : esxhost['memory_utilization'],
                                    "disk_utilization" : esxhost['disk_utilization'],
                                    "network_utilization" : esxhost['network_utilization'],
                                     },
                           "name": esxhost['hostname'],
                           "key": esxhost['_id']
                         }
             data_options.append(data_dict)
         return data_options


     def __get_columns(self):
         columns = [ {
                       "format": "number:0",
                       "type": "numeric",
                       "full_name": "Esxhost % CPU Utilization",
                       "is_objective": "true",
                       "range": {
                            "low": 0,
                            "high": 100
                       },
                       "goal": "min",
                       "key": "cpu_utilization"
                      },
                     {
                       "format": "number:0",
                        "type": "numeric",
                       "full_name": "Esxhost % Memory Utilization",
                       "is_objective": "true",
                       "range": {
                            "low": 0,
                            "high": 100
                        },
                        "goal": "min",
                        "key": "memory_utilization"
                      },
                     {
                         "format": "number:0",
                         "type": "numeric",
                         "full_name": "Esxhost % Disk Utilization",
                         "is_objective": "true",
                         "range": {
                             "low": 0,
                             "high": 100
                         },
                         "goal": "min",
                         "key": "disk_utilization"
                     },
                     {
                         "format": "number:0",
                         "type": "categorical",
                         "full_name": "Esxhost Network Utilization",
                         "is_objective": "true",
                         "range": ['low', 'med', 'high'],
                         "goal": "min",
                         "key": "network_utilization"
                     }]

         return columns