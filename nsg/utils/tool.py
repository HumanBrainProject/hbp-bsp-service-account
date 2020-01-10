# Defining NSG tools
BLUE_PY_OPT = 'BLUEPYOPT_TG'
BRIAN = 'BRIAN_TG'
C_PIPELINE = 'CPIPELINE_TG'
EE_GLAB = 'EEGLAB_TG'
FREE_SURFER = 'FREESURF_TG'
MOOSE = 'MOOSE_TG'
NEST_PY = 'NEST_PY_TG'
NEST = 'NEST_TG'
NEURON_73 = 'NEURON73_PY_TG'
NEURON_74 = 'NEURON74_PY_TG'
NEURON_75 = 'NEURON75_TG'
NEURON_77 = 'NEURON77_TG'
OSB_PY_NEURON_74 = 'OSBPYNEURON74'
P_GENESIS = 'PGENESIS_TG'
PY_NN = 'PYNN_TG'
PYTHON = 'PY_TG'
SINGULARITY_HNN = 'SINGULARITY_HNN_TG'


def get_tool_list():
    return [
        BLUE_PY_OPT,
        BRIAN,
        C_PIPELINE,
        EE_GLAB,
        FREE_SURFER,
        MOOSE,
        NEST_PY,
        NEST,
        NEURON_73,
        NEURON_74,
        NEURON_75,
        NEURON_77,
        OSB_PY_NEURON_74,
        P_GENESIS,
        PY_NN,
        PYTHON,
        SINGULARITY_HNN
    ]
