# coding=utf-8
"""
This script will extract useful information about your Kubernetes cluster that is not available in the logs, but is
available in the Kubernetes API.
"""
import json
import requests
import os
import sched
import sys
import time

from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

s = sched.scheduler(time.time, time.sleep)
if os.environ.get('SUMO_HTTP_URL') is not None:
    if os.environ.get('SUMO_HTTP_URL'):
        SUMO_COLLECTOR_URL = os.environ.get('SUMO_HTTP_URL')
    else:
        print("Collector was defined but is Empty")
        sys.exit(os.EX_CONFIG) 
else:
    print("NO Collector was Defined")
    sys.exit(os.EX_CONFIG)

if os.environ.get('K8S_API_URL') is not None:
    if os.environ.get('K8S_API_URL'):
        K8S_API_URL = os.environ.get('K8S_API_URL')
    else:
        print("K8s_API_URL was defined but is Empty")
        sys.exit(os.EX_CONFIG)
else:
    print("No Kubernetes API defined")
    sys.exit(os.EX_CONFIG)

''' Default to 60 seconds'''
RUN_EVERYTIME = int(os.environ.get('RUN_TIME', 60))


def fetch_push():
    nodes = requests.get(url="{}/api/v1/nodes".format(K8S_API_URL)).json()
    for node in nodes["items"]:
        requests.post(url=SUMO_COLLECTOR_URL, data=json.dumps(node))

    pods = requests.get(url="{}/api/v1/pods".format(K8S_API_URL)).json()

    for pod in pods["items"]:
        requests.post(url=SUMO_COLLECTOR_URL, data=json.dumps(pod))


s.enter(RUN_EVERYTIME, 1, fetch_push, (s,))
s.run()
