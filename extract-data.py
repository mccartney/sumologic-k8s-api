# coding=utf-8
"""
This script will extract useful information about your Kubernetes cluster that is not available in the logs, but is
available in the Kubernetes API.
"""
import logging
import json
import requests
import os
import sys

logging.basicConfig(level="INFO", format="%(asctime)s [level=%(levelname)s] [line=%(lineno)d]: %(message)s")
log = logging.getLogger(__name__)

if os.environ.get('SUMO_HTTP_URL') is not None:
    if os.environ.get('SUMO_HTTP_URL'):
        SUMO_COLLECTOR_URL = os.environ.get('SUMO_HTTP_URL')
    else:
        log.error("Collector was defined but is Empty")
        sys.exit(os.EX_CONFIG)
else:
    log.error("NO Collector was Defined")
    sys.exit(os.EX_CONFIG)

if os.environ.get('K8S_API_URL') is not None:
    if os.environ.get('K8S_API_URL'):
        K8S_API_URL = os.environ.get('K8S_API_URL')
    else:
        log.error("K8s_API_URL was defined but is Empty")
        sys.exit(os.EX_CONFIG)
else:
    log.error("No Kubernetes API defined")
    sys.exit(os.EX_CONFIG)

log.info("getting data for nodes")
nodes = requests.get(url="{}/api/v1/nodes".format(K8S_API_URL)).json()
for node in nodes["items"]:
    log.info("pushing to sumo")
    requests.post(url=SUMO_COLLECTOR_URL, data=json.dumps(node))

log.info("getting data for nodes")
pods = requests.get(url="{}/api/v1/pods".format(K8S_API_URL)).json()
for pod in pods["items"]:
    log.info("pushing to sumo")
    requests.post(url=SUMO_COLLECTOR_URL, data=json.dumps(pod))
