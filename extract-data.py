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

    def config_error(self, err_msg):
        log.error(err_msg)
        sys.exit(os.EX_CONFIG)

    def get_error(self, err_msg):
        log.error(err_msg)
        log.error("using k8s api url: %s", self.k8s_api_url)
        sys.exit(os.EX_DATAERR)

    def push_error(self, err_msg):
        log.error(err_msg)
        log.error("using collector_url: %s", self.collector_url)
        sys.exit(os.EX_DATAERR)

    def run(self):
        self.collector_url = os.environ.get('SUMO_HTTP_URL', None)
        self.k8s_api_url = os.environ.get('K8S_API_URL', None)
        self.get_headers()

        if self.collector_url is None:
            self.config_error("NO Collector was Defined")
        if self.collector_url is False:
            self.config_error("Collector was defined but is Empty")
        if self.k8s_api_url is None:
            self.config_error("No Kubernetes API defined")
        if self.k8s_api_url is False:
            self.config_error("K8s_API_URL was defined but is Empty")

        log.info("getting data for nodes")
        r = requests.get(url="{}/api/v1/nodes".format(self.k8s_api_url))
        if r.status_code != 200:
            self.get_error("error getting data.  Received status code: {}".format(r.status_code))
        nodes = r.json()
        for node in nodes["items"]:
            log.info("pushing node data to sumo")
            r = requests.post(url=self.collector_url,
                          data=json.dumps(node),
                          headers=self.headers)
            if r.status_code != 200:
                self.push_error("error pushing to sumo.  Received status code: {}".format(r.status_code))

        log.info("getting data for pods")
        r = requests.get(url="{}/api/v1/pods".format(self.k8s_api_url))
        if r.status_code != 200:
            self.get_error("error getting data.  Received status code: {}".format(r.status_code))
        pods = r.json()
        for pod in pods["items"]:
            log.info("pushing pod data to sumo")
            r = requests.post(url=self.collector_url,
                          data=json.dumps(pod),
                          headers=self.headers)
            if r.status_code != 200:
                self.push_error("error pushing to sumo.  Received status code: {}".format(r.status_code))

if __name__ == '__main__':
    SumoAPILogger = SumoAPILogger()
    SumoAPILogger.run()
