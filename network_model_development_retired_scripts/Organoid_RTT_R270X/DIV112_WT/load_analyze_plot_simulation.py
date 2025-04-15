from netpyne import sim
import os
from datetime import datetime as dt
import json
from RBS_network_models.sim_analysis import process_simulation_v3
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params
from RBS_network_models.sensitivity_analysis import prepare_permuted_sim_v2
# Notes ===================================================================================================
reference_data_path = ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics' #load reference data for fitness function
                       '/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy')
sim_data_path = "workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/_propVelocity_3_slower_propVelocity_/_propVelocity_3_slower_propVelocity__data.pkl"
sim.load(sim_data_path) # load simulation data
saveFolder = sim.cfg.saveFolder # get save folder from sim.cfg

kwargs = {
    'sim_data_path': sim_data_path,
    'reference_data_path': reference_data_path,
    'conv_params': conv_params,
    'mega_params': mega_params,
    'simData': sim.allSimData,
    'popData': sim.net.allPops,
    'cellData': sim.net.allCells,
    'output_dir': saveFolder,
    #'fitnessFuncArgs': fitnessFuncArgs,
    'DEBUG_MODE': False,
}

process_simulation_v3(kwargs)
#print('Parameters are selected randomly here, if neither E nor I cells are firing, try running again.') #TODO: I need a config that I reliably know will work for testing purposes.