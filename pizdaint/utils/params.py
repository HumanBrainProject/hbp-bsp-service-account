# PIZDAINT parameters

import json


# Defining parameters
N_CORES = 'core_number'
N_NODES = 'node_number'
RUNTIME = 'runtime'
COMMAND = 'command'

# Defining parameters limit
MIN_CORES = 12
MIN_NODES = 1
#MAX_RUNTIME = 48


def check_payload(payload):
    for k in payload.keys():
        if k == N_CORES and int(payload[k]) < MIN_CORES:
            raise ValueError
        if k == N_NODES and int(payload[k]) < MIN_NODES:
            raise ValueError
    return True


def transform_payload(payload):
    p = {}
    r = {'NodeConstraints': 'mc'}
    for k in payload.keys():
        if k == N_CORES:
            r.update({'CPUsPerNode': payload[k]})
        if k == N_NODES:
            r.update({'Nodes': payload[k]})
        if k == RUNTIME:
            runtime = str(int(float(payload['runtime']) * 60)) + 'm'
            r.update({'Runtime': runtime})
        if k == COMMAND:
            p.update({'Executable': payload[k]})
    p.update({'Resources': json.dumps(r)})
    return p

