# sumologic-k8s-api
Dockerized python script to extract information from the Kubernetes API and forward to SumoLogic.

## Usage

This script can be run standalone or as a container.  A Dockerfile has been provided should you wish to enhance.  An example deployment YAML has also been provided.

### Create a hosted collector and HTTP source in Sumo

In this step you create, on the Sumo service, an HTTP endpoint to receive your logs. This process involves creating an HTTP source on a hosted collector in Sumo. In Sumo, collectors use sources to receive data.

1. If you don’t already have a Sumo account, you can create one by clicking the **Free Trial** button on https://www.sumologic.com/.
2. Create a hosted collector, following the instructions on [Configure a Hosted Collector](https://help.sumologic.com/Send-Data/Hosted-Collectors/Configure-a-Hosted-Collector) in Sumo help. (If you already have a Sumo hosted collector that you want to use, skip this step.)  
3. Create an HTTP source on the collector you created in the previous step. For instructions, see [HTTP Logs and Metrics Source](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/HTTP-Source) in Sumo help. 
4. When you have configured the HTTP source, Sumo will display the URL of the HTTP endpoint. Make a note of the URL. You will use it when you configure the script to send data to Sumo. 

### Deploy the script as you want to
The script can be configured with the following environment variables:

| Variable        | Description                                            | Required | DEFAULT VALUE |
| --------        | -----------                                            | -------- | ------------- |
| `SUMO_HTTP_URL` | The URL for the HTTP source created in the first step. | YES      |               |
| `K8S_API_URL`   | The URL for the Kubernetes API                         | YES      |               | 

### Run On Node

You can simply add the script to one of your nodes and set it up via cron.  However, if the node dies so does your script unless baked into the image.

### Run As CronJob

An example cronjob file has been provided. This deployment runs a sidecar container that starts `kubectl proxy` with the default port of 8001.  The cronjob has a default schedule of running every 5 minutes, you can tune as needed.  The `K8S_API_URL` variable has been set based on the `kubectl` sidecar container.

## License
Released under Apache 2.0 License.
