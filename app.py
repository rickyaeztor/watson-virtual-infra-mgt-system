from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, url_for, redirect
import atexit
import cf_deployment_tracker
import os
import json
import yaml
from watson_developer_cloud import TradeoffAnalyticsV1

from src.Data_mgt_tasks.cluster_perfstat_tasks import cluster_perfstat_tasks
from src.Data_mgt_tasks.esxhost_perfstat_tasks import esxhost_perfstat_tasks
from src.Data_mgt_tasks.datastore_perfstat_tasks import datastore_perfstat_tasks
from src.Db_operations.cloudant_db_op import cloundant_db_op

from src.Models.cluster_problem_desc import cluster_problem_desc
from src.Models.esxhost_problem_desc import esxhost_problem_desc
from src.Models.datastore_problem_desc import  datastore_problem_desc

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)
db_name = 'eknowdb'
client = None
db = None
port = int(os.getenv('PORT', 8080))
td = TradeoffAnalyticsV1(username='2f524550-89d1-4dd7-9394-e395c2d4a75a', password='VTfGUyMJGES0')

@app.route('/')
def homepage():
    vcs = None
    with open(os.path.join(os.path.dirname(__file__), 'resources/vcenters.yaml')) as vcenters:
       vcs =  yaml.load(vcenters)
    return render_template('homepage.html', vcenters = vcs["vcenters"].split(" "))


@app.route('/vcenter_analyze_task')
def vcenter_analyze_task():
    cls = cluster_perfstat_task()
    esx = esxhost_perfstat_task()
    ds = datastore_perfstat_task()
    return render_template('whitespace_calc.html', cls_items=cls, esx_items=esx, ds_items=ds)

def cluster_perfstat_task():
    cluster_docs = []
    pf = cluster_perfstat_tasks()
    clusters = pf.get_all_clusters()
    for clus in clusters:
        cluster_docs.append(clus['doc'])
    problem = cluster_problem_desc(cluster_docs)
    data_for_analysis =  problem.generate_problem()
    dilemma = td.dilemmas(data_for_analysis, generate_visualization=True, find_preferable_options=True)
    pref = dilemma['resolution']['preferable_solutions']['solution_refs']
    cls = pf.get_cluster(pref[0])
    return cls


def esxhost_perfstat_task():
    esxhost_docs = []
    pf = esxhost_perfstat_tasks()
    esxhosts = pf.get_all_esxhosts()
    for esx in esxhosts:
        esxhost_docs.append(esx['doc'])
    problem = esxhost_problem_desc(esxhost_docs)
    data_for_analysis =  problem.generate_problem()
    dilemma = td.dilemmas(data_for_analysis, generate_visualization=True, find_preferable_options=True)
    pref = dilemma['resolution']['preferable_solutions']['solution_refs']
    esxs = pf.get_esxhost(pref[0])
    return esxs


def datastore_perfstat_task():
    ds_docs = []
    pf = datastore_perfstat_tasks()
    datastores = pf.get_all_datastores()
    for ds in datastores:
        ds_docs.append(ds['doc'])
    problem = datastore_problem_desc(ds_docs)
    data_for_analysis =  problem.generate_problem()
    dilemma = td.dilemmas(data_for_analysis, generate_visualization=True, find_preferable_options=True)
    pref = dilemma['resolution']['preferable_solutions']['solution_refs']
    dss = pf.get_datastore(pref[0])
    return dss


@app.route('/cloudant_db')
def cloudant_db():
   return redirect("https://85503c60-2116-40ba-afba-2fac974fd814-bluemix.cloudant.com/dashboard.html")

def initialize_db():
    clus_pf = cluster_perfstat_tasks()
    esx_pf = esxhost_perfstat_tasks()
    ds_pf = datastore_perfstat_tasks()


    try:
        with open(os.path.join(os.path.dirname(__file__), 'resources/clusters.json')) as clusters:
            clus_data = json.loads(clusters)
            for clus in clus_data:
                clus_pf.create_cluster(clus)
    except Exception as e:
        print("Exception occured: {}".format(str(e)))

    try:
        with open(os.path.join(os.path.dirname(__file__), 'resources/esxhosts.json')) as esxs:
            esx_data = json.load(esxs)
            for esx in esx_data:
                print(esx)
                esx_pf.create_esxhost(esx)
    except Exception as e:
        print("Exception occured: {}".format(str(e)))

    try:
        with open(os.path.join(os.path.dirname(__file__), 'resources/datastores.json')) as datastores:
            ds_data = json.load(datastores)
            for ds in ds_data:
                print(ds)
                ds_pf.create_datastore(ds)
    except Exception as e:
        print("Exception occured: {}".format(str(e)))



@atexit.register
def shutdown():
    if client:
        client.disconnect()


if __name__ == '__main__':
    #initialize_db()
    app.run(host='0.0.0.0', port=port, debug=True)
