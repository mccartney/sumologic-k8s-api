# coding=utf-8
"""
This script will extract useful information about your Kubernetes cluster that is not available in the logs, but is
available in the Kubernetes API.
"""
import logging
import json
import requests
import os
import sched
import sys
import time

s = sched.scheduler(time.time, time.sleep)
if os.environ.get('SUMO_HTTP_URL') is not None:
    if os.environ.get('SUMO_HTTP_URL'):
        SUMO_COLLECTOR_URL = os.environ.get('SUMO_HTTP_URL')
    else:
        logging.error("Collector was defined but is Empty")
        sys.exit(os.EX_CONFIG) 
else:
    logging.error("NO Collector was Defined")
    sys.exit(os.EX_CONFIG)

if os.environ.get('K8S_API_URL') is not None:
    if os.environ.get('K8S_API_URL'):
        K8S_API_URL = os.environ.get('K8S_API_URL')
    else:
        logging.error("K8s_API_URL was defined but is Empty")
        sys.exit(os.EX_CONFIG)
else:
    logging.error("No Kubernetes API defined")
    sys.exit(os.EX_CONFIG)

''' Default to 60 seconds'''
RUN_EVERYTIME = int(os.getenv('RUN_TIME', 60))


def fetch_push():
    logging.info("getting data for nodes")
    nodes = requests.get(url="{}/api/v1/nodes".format(K8S_API_URL)).json()
    for node in nodes["items"]:
        logging.info("pushing to sumo")
        requests.post(url=SUMO_COLLECTOR_URL, data=json.dumps(node))

    logging.info("getting data for nodes")
    pods = requests.get(url="{}/api/v1/pods".format(K8S_API_URL)).json()
    for pod in pods["items"]:
        logging.info("pushing to sumo")
        requests.post(url=SUMO_COLLECTOR_URL, data=json.dumps(pod))


s.enter(RUN_EVERYTIME, 1, fetch_push, ())
s.run()
