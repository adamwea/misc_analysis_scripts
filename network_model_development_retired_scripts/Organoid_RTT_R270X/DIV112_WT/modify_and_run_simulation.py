from netpyne import sim
import os
from datetime import datetime as dt
import json
from RBS_network_models.sim_analysis import process_simulation_v3
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params
from RBS_network_models.sensitivity_analysis import prepare_permuted_sim_v2
# Notes ===================================================================================================

# aw 2025-03-13 16:30:23 - I am going to modify the propVelocity parameter in the simConfig and run the simulation
# TODO: handle all this preprocessing in a function that can be called with a single line
# reference_data_path = ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics' #load reference data for fitness function
#                        '/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy')
# sim_data_path = ("/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/" # load pkl file of previously run simulation
#                  "2025-03-13_gen_20_cand_4_data_65s_overrideWT_1/propVelocity_3/propVelocity_3_data.pkl")
# saveParentFolder = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/modified_simulations/'
# dt_now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
# run_label = 'slower_propVelocity_'
# run_label_dt = run_label + dt_now
# saveFolder = os.path.join(saveParentFolder, run_label_dt)
# saveFolder = os.path.abspath(saveFolder)
# sim.load(sim_data_path) # load simulation data
# og_value = sim.cfg.propVelocity
# sim.cfg.propVelocity = sim.cfg.propVelocity * 0.9 # modify propVelocity # HACK, 
# #TODO: update the prepare_permuted_sim_v2 function so I don't need to do the previous two lines directly 
# modification_json = {
#     'src': sim_data_path,
#     'mods':{
#         'propVelocity': sim.cfg.propVelocity * 0.9
#         }
# }
# os.makedirs(saveFolder, exist_ok=True)
# mod_json_path = os.path.join(saveFolder, 'modification.json')
# with open(mod_json_path, 'w') as f:
#     json.dump(modification_json, f, indent=4)
    
# # aw 2025-03-14 09:23:00    
# reference_data_path = ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics' #load reference data for fitness function
#                        '/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy')
# sim_data_path = ("/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/"
#                  "weightIE_5/weightIE_5_data.pkl")
# saveParentFolder = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/modified_simulations/'
# dt_now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
# run_label = 'faster_prop_with_increased_weightIE'
# run_label_dt = run_label + dt_now
# saveFolder = os.path.join(saveParentFolder, run_label_dt)
# saveFolder = os.path.abspath(saveFolder)
# sim.load(sim_data_path) # load simulation data
# og_value = sim.cfg.propVelocity
# sim.cfg.propVelocity = sim.cfg.propVelocity * 1.5 # modify propVelocity # HACK, 
# #TODO: update the prepare_permuted_sim_v2 function so I don't need to do the previous two lines directly 
# modification_json = {
#     'src': sim_data_path,
#     'mods':{
#         'propVelocity': sim.cfg.propVelocity * 1.5
#         }
# }
# os.makedirs(saveFolder, exist_ok=True)
# mod_json_path = os.path.join(saveFolder, 'modification.json')
# with open(mod_json_path, 'w') as f:
#     json.dump(modification_json, f, indent=4)

# # aw 2025-03-14 13:17:45 - adding plotting, removing mods - MUT data for Organoid Grant    
# reference_data_path = ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics' #load reference data for fitness function
#                        '/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy')
# sim_data_path = ("/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/"
#                  "weightIE_5/weightIE_5_data.pkl")
# saveParentFolder = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/modified_simulations/'
# dt_now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
# run_label = 'faster_prop_with_increased_weightIE'
# run_label_dt = run_label + dt_now
# saveFolder = os.path.join(saveParentFolder, run_label_dt)
# saveFolder = os.path.abspath(saveFolder)
# sim.load(sim_data_path) # load simulation data
# og_value = sim.cfg.propVelocity
# sim.cfg.propVelocity = sim.cfg.propVelocity * 1.5 # modify propVelocity # HACK,
# sim.cfg.analysis['plotTraces'] = {
#     #'include': 'all', 
#     'oneFigPer': 'cell', 
#     'saveFig': True,
#  	'showFig': False,
#     'figSize': (12,8), 'timeRange': [0, sim.cfg.duration]}
# sim.cfg.analysis['plot2Dnet'] = {'saveFig': True}                                                # plot 2D cell positions and connections
# sim.cfg.analysis['plotConn'] = {'saveFig': True}                                                 # plot connectivity matrix
# #TODO: update the prepare_permuted_sim_v2 function so I don't need to do the previous two lines directly 
# modification_json = {
#     'src': sim_data_path,
#     'mods':{
#         'propVelocity': sim.cfg.propVelocity
#         }
# }
# os.makedirs(saveFolder, exist_ok=True)
# mod_json_path = os.path.join(saveFolder, 'modification.json')
# with open(mod_json_path, 'w') as f:
#     json.dump(modification_json, f, indent=4)
    
# aw 2025-03-14 13:17:45 - adding plotting, removing mods - WT data for Organoid Grant
reference_data_path = ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics' #load reference data for fitness function
                       '/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy')
# sim_data_path = ("/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/"
#                  "weightIE_5/weightIE_5_data.pkl")
sim_data_path = "workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/_propVelocity_3_slower_propVelocity_/_propVelocity_3_slower_propVelocity__data.pkl"
saveParentFolder = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/modified_simulations/'
dt_now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
run_label = 'WT_data_for_Organoid_Grant'
run_label_dt = run_label + dt_now
saveFolder = os.path.join(saveParentFolder, run_label_dt)
saveFolder = os.path.abspath(saveFolder)
sim.load(sim_data_path) # load simulation data
og_value = sim.cfg.propVelocity
sim.cfg.propVelocity = sim.cfg.propVelocity * 1.5 # modify propVelocity # HACK,
sim.cfg.analysis['plotTraces'] = {
    #'include': 'all', 
    'oneFigPer': 'cell', 
    'saveFig': True,
 	'showFig': False,
    'figSize': (12,8), 'timeRange': [0, sim.cfg.duration]}
sim.cfg.analysis['plot2Dnet'] = {'saveFig': True}                                                # plot 2D cell positions and connections
sim.cfg.analysis['plotConn'] = {'saveFig': True}                                                 # plot connectivity matrix
#TODO: update the prepare_permuted_sim_v2 function so I don't need to do the previous two lines directly 
modification_json = {
    'src': sim_data_path,
    'mods':{
        'propVelocity': sim.cfg.propVelocity
        }
}
os.makedirs(saveFolder, exist_ok=True)
mod_json_path = os.path.join(saveFolder, 'modification.json')
with open(mod_json_path, 'w') as f:
    json.dump(modification_json, f, indent=4)

# Main ===================================================================================================
# prep permuted simulation
pkwargs = {
    'sim_data_path': sim_data_path,
    'cfg': sim.cfg.__dict__,
    'cfg_param': 'propVelocity', # parameter to permute
    'cfg_val': og_value, # original value of parameter
    
}
prepare_permuted_sim_v2(pkwargs)
sim.runSim()
sim.gatherData()
sim.analyze()

allCells = sim.net.allCells
cell_data_for_table = {}
for cell in allCells:
    cell_label = cell['tags']['cellType']
    conns = cell['conns']
    num_conns = len(conns)
    num_inhb_cons = len([conn for conn in conns if conn['sec'] == 'soma' and conn['synMech'] == 'exc'])
    num_exc_cons = len([conn for conn in conns if conn['sec'] == 'soma' and conn['synMech'] == 'inh'])
    cell_data_for_table[cell_label] = {
        'num_conns': num_conns,
        'num_inhb_cons': num_inhb_cons,
        'num_exc_cons': num_exc_cons,
        'conns': [conn['preGid'] for conn in conns]
    }
    
# use pandas to create a csv file and a nice table
import pandas as pd

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(cell_data_for_table, orient='index')

# Save the DataFrame to a CSV file
csv_path = os.path.join(saveFolder, 'cell_data.csv')
df.to_csv(csv_path)

print('Cell data saved to csv file: ' + csv_path)

# post simulation saving and analysis
print('Simulation successfully ran!')
sim.cfg.filename = run_label
sim.cfg.saveFolder = saveFolder
sim.cfg.simLabel = sim.cfg.simLabel + '_' + run_label

#save cfg and netParams to file
netParamsPath = os.path.join(saveFolder, sim.cfg.filename+'_netParams.pkl')
netParamsPath = os.path.abspath(netParamsPath)
sim.net.params.save(netParamsPath)
sim.saveData()
print('Data saved successfully!')

# test typical simulation analysis - including fitness function
sim_data_path = os.path.join(sim.cfg.saveFolder, sim.cfg.filename + '_data.pkl')

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