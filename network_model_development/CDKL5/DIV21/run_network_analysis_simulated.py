'''
This script uses the extract_network_features module to perform network analyis on a targeted simulated data.
'''
# Notes: =====================================================================

# Imports =====================================================================
import os
import glob
from RBS_network_models import extract_features as ef
from RBS_network_models.CDKL5.DIV21.src.conv_params import conv_params, mega_params
from netpyne import sim
from MEA_Analysis.NetworkAnalysis.awNetworkAnalysis.network_analysis import compute_network_metrics
import numpy as np

# Paths =============================================================================
sim_data_path = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/2025-03-05_propVelocity_3_data_65s/_propVelocity_3/_propVelocity_3_data.pkl'

# Parallelism =============================================================================
'''check available cores'''
print("Number of cores available: ", os.cpu_count())
#max_workers = 128 # aw 2025-02-24 04:07:33 - I got an odd error trying to use 256 cores... just going to use 128 for now.

# Main =============================================================================
'''main'''
source = 'simulated'
sim.clearAll()
sim.load(sim_data_path)

#unpack tkwargs

nkwargs = {
    'simData': sim.allSimData,
    'popData': sim.net.allPops,
    'cellData': sim.net.allCells,
    'run_parallel': True,
    'debug_mode': False,
    'max_workers': 16, 
    'sim_data_path': sim_data_path,
    'burst_sequencing': False,
    'dtw_matrix': False,
}
network_data = compute_network_metrics(conv_params, mega_params, source, **nkwargs)
#perm_dir = os.path.dirname(path)
#remove the .pkl extension
perm_dir = sim_data_path.replace('_data.pkl', '')
if not os.path.exists(perm_dir): os.makedirs(perm_dir)
perm_path = os.path.join(perm_dir, 'network_data.npy')
np.save(perm_path, network_data)
print(f'Computed network metrics for {sim_data_path}')
print(f'Saved network metrics to {perm_path}')
print("Network Analysis Complete.")

# Perlmutter =============================================================================
'''
salloc -A m2043 -q interactive -C cpu -t 04:00:00 --nodes=1 --image=adammwea/axonkilo_docker:v7
module load conda
conda activate netsims_env
mkdir -p /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/
python /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/run_network_analysis.py
'''