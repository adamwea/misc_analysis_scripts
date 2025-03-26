# this test script is for testing typical use case of extract_features.py
import os
import glob
from RBS_network_models import extract_features as ef

# NOTE: this works...on login node in NERSC.
#       But I think I remember that it didn't work on local machine. laptop.
#       TODO: test on local machine.
from RBS_network_models.CDKL5.DIV21.src.conv_params import conv_params, mega_params
# =============================================================================
#script_path = os.path.abspath(__file__)
#os.chdir(os.path.dirname(script_path))
raw_data_paths = [ 
    # NOTE: this is a list of paths to raw data files that you want to extract features from
    #      this is useful for batch processing.
    #      Also, NOTE: if parent dirs are provided, each path will be searched recursively for .h5 files
    #'/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/data.raw.h5',
    #'/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5-E6D_T2_C1_05212024/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/data.raw.h5'
    '/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02032025_PVSandCA/MEASlices_02032025_PVSandCA/250203/M06804/Network/000013/data.raw.h5'
]
sorted_data_dir = (
    # this should be the parent directory of all sorted data files, ideally following proper data structure, naming conventions
    #'../data/CDKL5/DIV21/sorted'
    '**/data/slice/sorted'   #syntax for glob.glob
    #'**'
)
sorted_data_dir = glob.glob(sorted_data_dir, recursive=True)[0]
# =============================================================================
'''main'''
#conv_params = CDKL5.DIV21.src.conv_params
network_metrics_output_dir = os.path.join(os.path.dirname(sorted_data_dir), 'network_metrics')
network_metrics_output_dir = os.path.abspath(network_metrics_output_dir)
sorted_data_dir = os.path.abspath(sorted_data_dir)
feature_data = ef.extract_network_features_v2(
    raw_data_paths,
    sorted_data_dir=sorted_data_dir,
    output_dir = network_metrics_output_dir,
    stream_select=None,
    conv_params=conv_params,
    mega_params=mega_params,
    limit_seconds = None, # Specify some limit in seconds to only plot a portion of the data
    plot_wfs = False, # plot waveforms while classifying neurons
    # plot=True,
    )
print("Network metrics saved.")