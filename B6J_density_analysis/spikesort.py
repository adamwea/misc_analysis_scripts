# imports ==========================================================================================
import sys
import os
import argparse
from axon_reconstructor.axon_reconstructor import AxonReconstructor
from MEA_Analysis.MEAProcessingLibrary import mea_processing_library as MPL
import traceback

# helper functions =================================================================================
def get_h5_files(project_dirs):
    import pprint
    h5_files = []
    for project_dir in project_dirs:
        # if project_dir is a single h5 file
        if project_dir.endswith('.h5'):
            h5_files.append(project_dir)
            continue       
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.h5'):
                    if 'AxonTracking' in root:
                        h5_files.append(os.path.join(root, file))
    print("H5 files found:")
    pprint.pprint(h5_files)
    #import sys
    #sys.exit()
    return h5_files

def parse_arguments():
    print("Parsing arguments...")
    print(sys.argv)
    parser = argparse.ArgumentParser(description="Run the axon reconstruction pipeline for a single well.")
    return parser.parse_args()

# INPUTS and OUTPUTS =================================================================================
output_dir = "/global/homes/a/adammwea/pscratch/zoutputs"
input_dirs = [
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/241004",
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/241010",
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR",
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/241004/M06804/ActivityScan/000001/data.raw.h5",
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/241004/M08029/AxonTracking/000007/data.raw.h5", # too short?
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/241007/M08029/AxonTracking/000023/data.raw.h5",
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/B6J_DensityTest_10012024_AR/241004/M08029/AxonTracking/000007/data.raw.h5"
    
    # aw 2025-03-31 05:52:45 - ok its working now
    #"/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/B6J_DensityTest_10012024_AR/241004",
    # "/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/B6J_DensityTest_10012024_AR/241007",
    "/global/homes/a/adammwea/pscratch/zinputs/B6J_DensityTest_10012024_AR/B6J_DensityTest_10012024_AR",
    ]

# Main =================================================================================
def run_pipeline_on_project_dirs(project_dirs, output_dir):
    # subfunction to build kwargs for AxonReconstructor
    def build_kwargs():
        ''' Parameters '''
        # Reconstructor parameters
        kwargs = {
            # runtime options
            'sorting_params': {
                'allowed_scan_types': ['AxonTracking'],
                'load_existing_sortings': True,
                'keep_good_only': False,
                #'use_gpu': False,
            },
            'te_params': {
                'load_merged_templates': True,
                'save_merged_templates': True,
                'time_derivative': True,
            },
            'av_params': {
                # 'upsample': 2,  # Upsampling factor to better capture finer details (unitless). Higher values increase temporal resolution.
                # 'min_selected_points': 20,  # Minimum number of selected points to include more potential signals (unitless). Determines the minimum dataset size for analysis.
                # 'verbose': False,  # Verbosity flag for debugging (boolean). If True, additional logs are printed.

                # # Channel selection
                # 'detect_threshold': 0.01,  # Threshold for detecting signals, sensitive to smaller amplitudes (relative or absolute units, depending on 'detection_type'). Works with 'detection_type'.
                # 'detection_type': 'relative',  # Type of detection threshold ('relative' or 'absolute'). Determines if 'detect_threshold' is a relative or absolute value.
                # 'kurt_threshold': 0.2,  # Kurtosis threshold for noise filtering (unitless, kurtosis measure). Lower values allow more channels through noise filtering.
                # 'peak_std_threshold': 0.5,  # Peak time standard deviation threshold (milliseconds). Filters out channels with high variance in peak times.
                # 'init_delay': 0.05,  # Initial delay threshold to include faster signals (milliseconds). Minimum delay for considering a channel.
                # 'peak_std_distance': 20.0,  # Distance for calculating peak time standard deviation (micrometers). Defines the neighborhood for peak time calculation.
                # 'remove_isolated': True,  # Flag to remove isolated channels (boolean). If True, only connected channels are kept for analysis.

                # # Graph
                # 'init_amp_peak_ratio': 0.2,  # Ratio between initial amplitude and peak time (unitless). Used to sort channels for path search.
                # 'max_distance_for_edge': 150.0,  # Maximum distance for creating graph edges (micrometers). Defines the maximum allowed distance between connected channels.
                # 'max_distance_to_init': 300.0,  # Maximum distance to initial channel for creating edges (micrometers). Determines the initial connectivity range.
                # #'max_distance_to_init': 4000.0,  # Maximum distance to initial channel for creating edges (micrometers). Determines the initial connectivity range.
                # 'n_neighbors': 9,  # Maximum number of neighbors (edges) per channel (unitless). Enhances connectivity by increasing the number of edges.
                # 'distance_exp': 1.5,  # Exponent for distance calculation (unitless). Adjusts the influence of distance in edge creation.
                # 'edge_dist_amp_ratio': 0.2,  # Ratio between distance and amplitude for neighbor selection (unitless). Balances the importance of proximity and amplitude in selecting edges.

                # # Axonal reconstruction
                # 'min_path_length': 80.0,  # Minimum path length to include shorter paths (micrometers). Ensures that only significant paths are considered.
                # 'min_path_points': 3,  # Minimum number of channels in a path (unitless). Defines the minimum size of a valid path.
                # 'neighbor_radius': 80.0,  # Radius to include neighboring channels (micrometers). Defines the search radius for neighbors.
                # 'min_points_after_branching': 2,  # Minimum points after branching to keep paths (unitless). Ensures that branches have enough data points.

                # # Path cleaning/velocity estimation
                # 'mad_threshold': 10.0,  # Median Absolute Deviation threshold for path cleaning (unitless). Higher values allow more variability in the path.
                # 'split_paths': True,  # Flag to enable path splitting (boolean). If True, paths can be split for better velocity fit.
                # 'max_peak_latency_for_splitting': 0.7,  # Maximum peak latency jump for splitting paths (milliseconds). Allows capturing more variations by splitting paths at significant jumps.
                'r2_threshold': 0.5,  # R-squared threshold for velocity fit (unitless). Lower values include more paths with less perfect fits.
                # 'r2_threshold_for_outliers': 0.95,  # R-squared threshold for outlier detection (unitless). Defines the threshold below which the algorithm looks for outliers.
                # 'min_outlier_tracking_error': 40.0,  # Minimum tracking error to consider a channel as an outlier (micrometers). Sets the error tolerance for tracking outliers.
            },
            'analysis_options': {
                'generate_animation': True,
                'generate_summary': False,
            },
            'save_reconstructor_object': True,
            'reconstructor_save_options': {
                'recordings': True, 
                'multirecordings': True, 
                'sortings': True,
                'waveforms': True,
                'templates': True,
            },
            'reconstructor_load_options': {
                'load_reconstructor': True,
                
                #Only relevant if load_reconstructor is True:
                'load_multirecs': True,
                'load_sortings': True,
                'load_wfs': False,
                'load_templates': False,
                'load_templates_bypass': False,  # This is a new parameter that allows the user to bypass pre-processing steps and load the templates directly. 
                                                # Useful if there isn't any need to reprocess the templates.
                'restore_environment': False,
            },
            'verbose': True,
            'debug_mode': True,
            'n_jobs': 64,
            #'n_jobs': 256,
            #'max_workers': 64,
            'logger_level': 'DEBUG',
            'run_lean': True,
        }
        
        kwargs['project_name'] = None # Use project name to create subdirectories, if true the paths below can be relative
        kwargs['output_dir'] = output_dir # Output directory for the reconstructions when running on NERSC
        kwargs['mode'] = 'lean'
        kwargs['stream_select'] = stream_select

        # Process a single well file
        print(f"Processing plate {plate_file} stream {stream_select}...")
        h5_files = [plate_file]
        h5_file = plate_file
        #continue
        #return None, None
        
        h5_details = MPL.extract_recording_details(h5_file)
        date = h5_details[0]['date']
        chipID = h5_details[0]['chipID']
        runID = h5_details[0]['runID']
        scanType = h5_details[0]['scanType']
        
        projectName = h5_details[0]['projectName']
        reconstructorID = f'{date}_{chipID}_{runID}_well00{stream_select}'

        wellID = f'well00{stream_select}'
        well_path = f'{kwargs["output_dir"]}/{projectName}/{date}/{chipID}/{scanType}/{runID}/{wellID}'
        kwargs['log_file'] = f'{well_path}/{wellID}_axon_reconstruction.log'
        kwargs['error_log_file'] = f'{well_path}/{wellID}_axon_reconstruction_error.log'
        kwargs['recordings_dir'] = os.path.join(well_path, 'recordings')
        kwargs['sortings_dir'] = os.path.join(well_path, 'sortings')
        kwargs['waveforms_dir'] = os.path.join(well_path, 'waveforms')
        kwargs['templates_dir'] = os.path.join(well_path, 'templates')
        kwargs['recon_dir'] = os.path.join(well_path, 'reconstructions')
        kwargs['reconstructor_dir'] = well_path
        
        return kwargs, reconstructorID    
    
    # main ========================================================================    
    h5_file_paths = get_h5_files(project_dirs)
    args = parse_arguments()
    
    # loop through each h5 file and streams
    for plate_file in h5_file_paths:
        for stream_select in [0, 1, 2, 3, 4, 5]:
            try:
                kwargs, reconstructorID = build_kwargs()
                print("\n--------------------------------------------------")
                print(f'Starting reconstruction for {reconstructorID}...')
                print(f'Log file: {kwargs["log_file"]}')
                print(f'Error log file: {kwargs["error_log_file"]}')
                print(f'Recordings dir: {kwargs["recordings_dir"]}')
                print(f'Sortings dir: {kwargs["sortings_dir"]}')
                print(f'Waveforms dir: {kwargs["waveforms_dir"]}')
                print(f'Templates dir: {kwargs["templates_dir"]}')
                print(f'Reconstructions dir: {kwargs["recon_dir"]}')
                print(f'Reconstructor dir: {kwargs["reconstructor_dir"]}')
                
                #kwargs switches
                kwargs['reconstructor_load_options']['load_reconstructor'] = False
                kwargs['reconstructor_load_options']['load_templates_bypass'] = False
                kwargs['concatenate_switch'] = True
                kwargs['sort_switch'] = True
                #kwargs['only_load_sortings'] = True
                kwargs['only_load_sortings'] = False  # set to False to run the full pipeline
                kwargs['waveform_switch'] = False
                kwargs['template_switch'] = False
                kwargs['recon_switch'] = False
                h5_file_list = [plate_file] #   NOTE: in this case, always a list of one file
                                            #   but AxonReconstructor expects a list of h5 files
                reconstructor = AxonReconstructor(h5_file_list, **kwargs)
                #reconstructor = AxonReconstructor(h5_file_paths, **kwargs)
                reconstructor.run_pipeline(**kwargs)
            except Exception as e:
                print(f"Error processing plate {plate_file} stream {stream_select}: {e}")
                traceback.print_exc()
                continue
            
            #sys.exit()  # exit after processing the first file for testing purposes

if __name__ == "__main__":
    run_pipeline_on_project_dirs(input_dirs, output_dir)
    
#to run in login node:
'''
shifter --image=adammwea/axonkilo_docker:v7 /bin/bash
pip install numpy==1.26.4 # need an older version of numpy for spikinginterface==0.100.4
pip install -e /global/homes/a/adammwea/workspace/repos/MEA_Analysis
'''

#to run spikesorting as needed in interactive node with gpu:
'''
salloc -A m2043_g -q interactive -C gpu -t 04:00:00 --nodes=4 --gpus=4 --image=adammwea/axonkilo_docker:v7
salloc -A m2043_g -q interactive -C gpu -t 04:00:00 --nodes=1 --gpus=1 --image=adammwea/axonkilo_docker:v7
'''