import os
from MEA_Analysis.NetworkAnalysis.awNetworkAnalysis.run_sorter import run_sorter
import glob

# prepare paths =============================================================================
input_dir = '/global/homes/a/adammwea/pscratch/zinputs/' #dir where all raw data are stored in pscratch (data should be copied here from long term storage before running for optimal I/O)
raw_data_path = 'CDKL5-E6D_T2_C1_05212024/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/data.raw.h5' # path to raw data within inputs_dir
output_dir = '/global/homes/a/adammwea/pscratch/zoutputs/' #dir where all analyzed data are stored in pscratch (use data transfer bash script to copy to long term storage as needed)
input_path = os.path.join(input_dir, raw_data_path) # absolute path to raw data
sorted_output_dir = os.path.join(output_dir, os.path.dirname(raw_data_path), 'sorted') # path to sorted data within outputs_dir
waveform_output_dir = os.path.join(output_dir, os.path.dirname(raw_data_path), 'waveforms') # path to waveform data within outputs_dir

# print paths
print()
print(f"Targeted paths:")
print(f"input_path: {input_path}")
print(f"sorted_output_dir: {sorted_output_dir}")
print(f"waveform_output_dir: {waveform_output_dir}")

# create output directories if they don't exist
os.makedirs(sorted_output_dir, exist_ok=True)
os.makedirs(waveform_output_dir, exist_ok=True)

# =============================================================================
run_sorter(
    #raw_data_path,
    input_path,
    sorted_output_dir,
    waveform_output_dir,
    use_docker=False,   # NOTE: Default is True. Comment out this line to use docker.
                        #       If running on NERSC, you'll need to run without docker and with shifter.
                        #       see below for shifter command to run on NERSC
    try_load = False,   # NOTE: Default is True. Comment out this line to try loading the sorted data.
    )

# bash commands =============================================================================

# bash commands to run kilosort2 on NERSC
#  to run spikesorting as needed in interactive node with gpu:
'''
salloc -A m2043_g -q interactive -C gpu -t 04:00:00 --nodes=4 --gpus=4 --image=adammwea/axonkilo_docker:v7
salloc -A m2043_g -q interactive -C gpu -t 04:00:00 --nodes=1 --gpus=1 --image=adammwea/axonkilo_docker:v7
'''

# after salloc, run the following command: # NOTE: replace path to script as needed.
'''
# run shifter and install editable packages as needed
shifter --image=adammwea/axonkilo_docker:v7 /bin/bash
pip install -e /pscratch/sd/a/adammwea/workspace/RBS_network_models
pip install -e /pscratch/sd/a/adammwea/workspace/MEA_Analysis
'''

'''
# run without saving output to log file
python /global/homes/a/adammwea/workspace/aw_scripts/Organoid_RTT_R270X_models/DIV112_WT/spikesort.py
'''

# '''
# # run and save output to log file
# python /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/spikesort.py \
#     > /pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sorted/logs/test_spikesort.log 2>&1
# '''