from netpyne import sim
import os
from RBS_network_models.sim_analysis import process_simulation_v3
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params
# ===================================================================================================
#load network metric npy
npy_path = (
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics'
    '/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy'
)
# ===================================================================================================

# run simulation
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src import init # NOTE this will create, run and analyze a simulation

# post simulation saving and analysis
print('Simulation successfully ran!')
#set paths
sim.cfg.filename = 'test_single_run'
saveFolder = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/test_single_run'
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

kwargs = {
    'sim_data_path': sim_data_path,
    'reference_data_path': reference_data_path,
    'conv_params': conv_params,
    'mega_params': mega_params,
    #'fitnessFuncArgs': fitnessFuncArgs,
    'DEBUG_MODE': False,
}


# TODO: broken , fix later # aw 2025-03-20 21:49:56
process_simulation_v3(kwargs)
# print('Parameters are selected randomly here, if neither E nor I cells are firing, try running again.') #TODO: I need a config that I reliably know will work for testing purposes.