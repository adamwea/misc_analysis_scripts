'''
This script uses the extract_network_features module to perform network analyis on a targeted raw data file and then extract features from the network to later pass to batch simulations.
'''
# Notes: =====================================================================
'''
    # before # aw 2025-02-26 11:52:29
    # - NOTE: this works...on login node in NERSC.
    # -- But I think I remember that it didn't work on local machine. laptop.
    # -- TODO: test on local machine.
    # - [about raw_data_paths list of paths]
    # -- NOTE: this is a list of paths to raw data files that you want to extract features from this is useful for batch processing.
    # -- NOTE: Also, if parent dirs are provided, each path will be searched recursively for .h5 files
'''

# Imports =====================================================================
import os
import glob
from RBS_network_models import extract_features as ef
#from RBS_network_models.CDKL5.DIV21.src.conv_params import conv_params, mega_params
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params

# Paths =============================================================================
raw_data_paths = [
    #'/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5-E6D_T2_C1_05212024/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/data.raw.h5'
    '/pscratch/sd/a/adammwea/workspace/_raw_data/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/data.raw.h5',
]
sorted_data_dir = (
    #'**/data/CDKL5/DIV21/sorted'   #syntax for glob.glob
    '**/data/Organoid_RTT_R270X/DIV112_WT/sorted'
)
sorted_data_dir = glob.glob(sorted_data_dir, recursive=True)[0]

# Parallelism =============================================================================
'''check available cores'''
print("Number of cores available: ", os.cpu_count())
#max_workers = 128 # aw 2025-02-24 04:07:33 - I got an odd error trying to use 256 cores... just going to use 128 for now.

# Main =============================================================================
'''main'''
#conv_params = CDKL5.DIV21.src.conv_params
# network_metrics_output_dir = os.path.join(os.path.dirname(sorted_data_dir), 'network_metrics')
# network_metrics_output_dir = os.path.abspath(network_metrics_output_dir)
network_analysis_output_dir = os.path.join(os.path.dirname(sorted_data_dir), 'network_analysis')
network_analysis_output_dir = os.path.abspath(network_analysis_output_dir)
sorted_data_dir = os.path.abspath(sorted_data_dir)
feature_data = ef.analyze_network_data(
    raw_data_paths,
    sorted_data_dir=sorted_data_dir,
    output_dir = network_analysis_output_dir,
    stream_select=None,
    conv_params=conv_params,
    mega_params=mega_params,
    limit_seconds = None, # Specify some limit in seconds to only plot a portion of the data
    #plot_wfs = False, # plot waveforms while classifying neurons
    plot_wfs = True, # plot waveforms while classifying neurons
    
    max_workers = 100, # number of parallel processes to use
    #max_workers = os.cpu_count(), # use all available cores
    #max_workers = max_workers, # use all available cores
    # plot=True,
    #debug_mode=True, #default is False, set to True to reduce units and bursts processed for quicker debugging
    )
#print("Network metrics saved.")
print("Network Analysis Complete.")

# Perlmutter =============================================================================
'''
salloc -A m2043 -q interactive -C cpu -t 04:00:00 --nodes=1 --image=adammwea/axonkilo_docker:v7
module load conda
conda activate netsims_env
mkdir -p /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/
python /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/run_network_analysis.py
'''