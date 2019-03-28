# NSG submitted job parameters
from nsg.utils.tool import get_tool_list


# Defining parameters
TOOL = 'tool'
N_CORES = 'core_number'
N_NODES = 'node_number'
N_GENERATION = 'generation_number'
OFFSPRING_SIZE = 'offspring_size'
RUNTIME = 'runtime'
START_FILE = 'init_file'
SINGLE_LAYER = 'single_layer'
PYTHON_OPTION = 'python_option'
EMAIL_NOTIFICATION = 'email_notification'
EMAIL_ADDRESS = 'email_address'


# Defining parameters limit
MAX_CORES = 24
MAX_GENERATION = 60
MAX_NODES = 72
MAX_RUNTIME = 48


def check_payload(payload):
    for k in payload.keys():
        if k == N_CORES and int(payload[k]) > MAX_CORES:
            raise ValueError
        if k == N_NODES and int(payload[k]) > MAX_NODES:
            raise ValueError
        if k == N_GENERATION and int(payload[k]) > MAX_GENERATION:
            raise ValueError
        if k == RUNTIME and float(payload[k]) > MAX_RUNTIME:
            raise ValueError
        if k == TOOL and payload[k] not in get_tool_list():
            raise ValueError
    return True


def transform_payload(payload):
    p = {}
    for k in payload.keys():
        if k == TOOL:
            p.update({'tool': payload[k]})
        if k == RUNTIME:
            p.update({'vparam.runtime_': payload[k]})
        if k == N_CORES:
            p.update({'vparam.number_cores_': payload[k]})
        if k == N_NODES:
            p.update({'vparam.number_nodes_': payload[k]})
        if k == PYTHON_OPTION:
            p.update({'vparam.pythonoption_': payload[k]})
        if k == SINGLE_LAYER:
            p.update({'vparam.singlelayer_': payload[k]})
        if k == START_FILE:
            p.update({'vparam.filename_': payload[k]})
        if k == EMAIL_NOTIFICATION:
            p.update({'metadata.statusEmail': payload[k]})
        if k == EMAIL_ADDRESS:
            p.update({'metadata.emailAddress': payload[k]})
    return p
