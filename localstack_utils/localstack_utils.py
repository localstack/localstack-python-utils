import re
import sys
import docker
import logging
from localstack_utils.container import Container
from localstack_utils.localstack_docker_configuration import LocalstackDockerConfiguration
from localstack_utils.localstack_logger import LocalstackLogger

ENV_CONFIG_USE_SSL = "USE_SSL"
ENV_CONFIG_EDGE_PORT = "EDGE_PORT"
INIT_SCRIPTS_PATH = "/docker-entrypoint-initaws.d"
TMP_PATH = "/tmp/localstack"
READY_TOKEN = re.compile("Ready\\.")
DEFAULT_EDGE_PORT = 4566
PORT_CONFIG_FILENAME = "/opt/code/localstack/.venv/lib/python3.8/site-packages/localstack_client/config.py"
# DEFAULT_PORT_PATTERN = re.compile("'(\\w+)'\\Q: '{proto}://{host}:\\E(\\d+)'")

localstack_instance = None
logging.basicConfig(level=logging.INFO, format='%(message)s')

class Localstack:
    
    localstack_container = None
    service_to_map = {}
    locked = False

    @staticmethod
    def INSTANCE():
        return Localstack()

    external_hostName = '' 

    def startup(self, docker_configuration) :
        if self.locked:
            raise Exception("A docker instance is starting or already started.")
        self.locked = True
        self.external_hostname = docker_configuration.external_hostname

        try:
            self.localstack_container = Container.create_localstack_container(
                docker_configuration.external_hostname,
                docker_configuration.pull_new_image,
                docker_configuration.randomize_ports,
                docker_configuration.image_name,
                docker_configuration.image_tag,
                docker_configuration.port_edge,
                docker_configuration.port_elastic_search,
                docker_configuration.environment_variables,
                docker_configuration.port_mappings,
                docker_configuration.bind_mounts,
                docker_configuration.platform
            )

            self.setup_logger()

            Container.waitForReady(self.localstack_container, READY_TOKEN)

        except docker.errors.APIError as error:
            if not docker_configuration.ignore_docker_runerrors:
                raise "Unable to start docker"

        except:
            raise sys.exc_info()


    def stop(self):
        self.localstack_container.stop()

    
    def setup_logger(self):
        localstack_logger = LocalstackLogger(self.localstack_container)
        localstack_logger.start()

def startup_localstack(port=4566, services=[], ignore_docker_errors = False):
    global localstack_instance
    localstack_instance = Localstack.INSTANCE()
    config = LocalstackDockerConfiguration()

    if len(services):
        config.envirement_variables.update({'SERVICES': ','.join(services)})
    if port != 4566:
        config.port_edge = str(port)
    config.ignore_docker_runerrors = ignore_docker_errors

    localstack_instance.startup(config)

def stop_localstack():
    if localstack_instance:
        localstack_instance.stop()
