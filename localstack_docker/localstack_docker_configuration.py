class LocalstackDockerConfiguration:
    pull_new_image = False
    randomize_ports = False
    image_name = None
    image_tag = None
    platform = None

    port_edge = '4566'
    port_elastic_search = '4571'
    external_hostname = 'localhost'
    environment_variables = {}
    port_mappings = {}
    bind_mounts = {}

    initialization_token = None
    use_dingle_docker_container = False
    ignore_docker_runerrors = False
