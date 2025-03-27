global PROGRESS_SLIDES_PATH, SIMULATION_RUN_PATH, REFERENCE_DATA_NPY, CONVOLUTION_PARAMS, DEBUG_MODE
#from workspace.RBS_neuronal_network_models.optimizing.CDKL5_DIV21.scripts_dep.sim_helper import *
#from DIV21.utils.sim_helper import *
from netpyne import sim
import os
from RBS_network_models.sim_analysis import process_simulation_v3
# ===================================================================================================
#load network metric npy
npy_path = (
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/'
    'network_metrics/CDKL5-E6D_T2_C1_05212024_240611_M08029_Network_000091_network_metrics_well001.npy'
)
# ===================================================================================================

# get configured simConfig and netParams
#from DIV21.src import init
from RBS_network_models.CDKL5.DIV21.src import init # NOTE this will create, run and analyze a simulation
                                                    # param edits prior to sim need to be done in init.py or cfg.py
                                                    # Duration is set to 1 second by default in cfg.py

# post simulation saving and analysis
print('Simulation successfully ran!')
#set paths
sim.cfg.filename = 'test_single_run'
saveFolder = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/test_single_run'
sim.cfg.saveFolder = os.path.abspath(saveFolder)
filename = sim.cfg.filename

#save cfg and netParams to file
netParamsPath = os.path.join(saveFolder, filename+'_netParams.pkl')
netParamsPath = os.path.abspath(netParamsPath)
sim.net.params.save(netParamsPath)
sim.saveData()
print('Data saved successfully!')

# test typical simulation analysis - including fitness function
sim_data_path = os.path.join(sim.cfg.saveFolder, sim.cfg.filename + '_data.pkl')
reference_data_path = npy_path

#from RBS_network_models.utils.cfg_helper import import_module_from_path
from RBS_network_models.CDKL5.DIV21.src.conv_params import conv_params, mega_params
feature_path = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features/20250204_features.py'
#feature_module = import_module_from_path(feature_path)
#fitnessFuncArgs = feature_module.fitnessFuncArgs

kwargs = {
    'sim_data_path': sim_data_path,
    'reference_data_path': reference_data_path,
    'conv_params': conv_params,
    'mega_params': mega_params,
    #'fitnessFuncArgs': fitnessFuncArgs,
    'DEBUG_MODE': False,
}

process_simulation_v3(kwargs)
#print('Parameters are selected randomly here, if neither E nor I cells are firing, try running again.') #TODO: I need a config that I reliably know will work for testing purposes.