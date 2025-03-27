# this test script is for testing typical use case of extract_features.py
# Notes ===================================================================================================
# NOTE: this works...on login node in NERSC.
#       But I think I remember that it didn't work on local machine. laptop.
#       TODO: test on local machine.

# Import necessary libraries ==========================================================================================
import os
import glob
from RBS_network_models import extract_features as ef
from RBS_network_models.CDKL5.DIV21.src.conv_params import conv_params, mega_params

# main ===========================================================================================================
# =============================================================================
# NOTE: this is a list of paths to raw data files that you want to extract features from
#      this is useful for batch processing.
#      Also, NOTE: if parent dirs are provided, each path will be searched recursively for .h5 files
raw_data_parent_paths = [
    '/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02242025_PVSandCA'
]
raw_data_paths = [
    path for parent_path in raw_data_parent_paths
    for path in glob.glob(os.path.join(parent_path, '**', '*.h5'), recursive=True)
    if 'Network' in path
]
sorted_data_dir = glob.glob('**/misc_scripts/data/sorted', recursive=True)[0]
# =============================================================================
'''main'''
#conv_params = CDKL5.DIV21.src.conv_params
network_metrics_output_dir = os.path.join(os.path.dirname(sorted_data_dir), 'network_metrics')
network_metrics_output_dir = os.path.abspath(network_metrics_output_dir)
sorted_data_dir = os.path.abspath(sorted_data_dir)
feature_data = ef.analyze_network_data(
    raw_data_paths,
    sorted_data_dir=sorted_data_dir,
    output_dir = network_metrics_output_dir,
    stream_select=None,
    conv_params=conv_params,
    mega_params=mega_params,
    limit_seconds = None, # Specify some limit in seconds to only plot a portion of the data
    plot_wfs = True, # plot waveforms while classifying neurons
    # plot=True,
    )
print("Network metrics saved.")