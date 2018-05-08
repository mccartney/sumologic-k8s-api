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


class SumoAPILogger():

    def __init__(self):
        self.collector_url = None
        self.k8s_api_url = None
        self.headers = {}

    def get_headers(self):
        SUMO_HEADERS = ['X-Sumo-Name', 'X-Sumo-Host', 'X-Sumo-Category']
        for sh in SUMO_HEADERS:
            value = os.environ.get(sh, None)
            if value is not None:
                self.headers[sh] = value

    def run(self):
        self.collector_url = os.environ.get('SUMO_HTTP_URL', None)
        self.k8s_api_url = os.environ.get('K8S_API_URL', None)
        self.get_headers()

        if self.collector_url is None:
            log.error("NO Collector was Defined")
            sys.exit(os.EX_CONFIG)
        if os.environ.get('SUMO_HTTP_URL') is False:
            log.error("Collector was defined but is Empty")
            sys.exit(os.EX_CONFIG)
        if self.k8s_api_url is None:
            log.error("No Kubernetes API defined")
            sys.exit(os.EX_CONFIG)
        if self.k8s_api_url is False:
            log.error("K8s_API_URL was defined but is Empty")
            sys.exit(os.EX_CONFIG)

        log.info("getting data for nodes")
        nodes = requests.get(url="{}/api/v1/nodes".format(K8S_API_URL)).json()
        for node in nodes["items"]:
            log.info("pushing to sumo")
            requests.post(url=self.collector_url,
                          data=json.dumps(node),
                          headers=self.headers)

        log.info("getting data for nodes")
        pods = requests.get(url="{}/api/v1/pods".format(K8S_API_URL)).json()
        for pod in pods["items"]:
            log.info("pushing to sumo")
            requests.post(url=self.collector_url,
                          data=json.dumps(pod),
                          headers=self.headers)


if __name__ == '__main__':
    SumoAPILogger = SumoAPILogger()
    SumoAPILogger.run()
