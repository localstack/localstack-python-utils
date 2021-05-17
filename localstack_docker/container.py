import logging
import re
import docker
from time import sleep

LOCALSTACK_NAME = "localstack/localstack";
LOCALSTACK_TAG = "latest";
LOCALSTACK_PORT_EDGE = "4566";
LOCALSTACK_PORT_ELASTICSEARCH = "4571";

MAX_PORT_CONNECTION_ATTEMPTS = 10;
MAX_LOG_COLLECTION_ATTEMPTS = 120;
POLL_INTERVAL = 1;
NUM_LOG_LINES = 10;

ENV_DEBUG = "DEBUG";
ENV_USE_SSL = "USE_SSL";
ENV_DEBUG_DEFAULT = "1";
LOCALSTACK_EXTERNAL_HOSTNAME = "HOSTNAME_EXTERNAL"
DEFAULT_CONTAINER_ID = "localstack_main"

DOCKER_CLIENT = docker.from_env()

class Container:

    @staticmethod
    def create_localstack_container(external_hostname, pull_new_image, randomize_ports, image_name, image_tag, port_edge, port_elasticsearch, environment_variables, port_mappings, bind_mounts, platform):

        environment_variables = {} if environment_variables == None else environment_variables
        bind_mounts = {} if bind_mounts == None else bind_mounts
        port_mappings = {} if port_mappings == None else port_mappings
        image_name_or_default = LOCALSTACK_NAME if image_name == None else image_name 
        image_exists = True if len(DOCKER_CLIENT.images.list(name=image_name_or_default)) else False
        
        fullPortEdge = {(LOCALSTACK_PORT_EDGE if port_edge == None else port_edge) : (LOCALSTACK_PORT_EDGE)}

        if pull_new_image or not image_exists:
            logging.info("Pulling latest image")
            DOCKER_CLIENT.images.pull(image_name_or_default, image_tag)
        
        return DOCKER_CLIENT.containers.run(image_name_or_default, ports=fullPortEdge, environment=environment_variables, detach=True)
    
    @staticmethod
    def waitForReady(container, pattern):
        attemps = 0
        
        while True:
            logs = container.logs(tail=NUM_LOG_LINES).decode('utf-8')
            if re.search(pattern, logs):
                return;
            
            sleep(POLL_INTERVAL)
            attemps += 1

            if attemps >= MAX_LOG_COLLECTION_ATTEMPTS:
                raise "Could not find token: " +pattern.toString()+ "in logs"
