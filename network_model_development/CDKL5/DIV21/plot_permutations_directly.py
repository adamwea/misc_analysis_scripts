# Notes ===================================================================================================
'''
'''
# Imports ===================================================================================================
from RBS_network_models.sensitivity_analysis import run_sensitivity_analysis_v2, plot_sensitivity_analysis
from RBS_network_models.CDKL5.DIV21.src.conv_params import conv_params
from RBS_network_models.CDKL5.DIV21.src.conv_params import mega_params
from RBS_network_models.CDKL5.DIV21.src.fitness_targets import fitnessFuncArgs
from RBS_network_models.CDKL5.DIV21.src.evol_params import params as evol_params
# globals ===================================================================================================
#global PROGRESS_SLIDES_PATH, SIMULATION_RUN_PATH, REFERENCE_DATA_NPY, CONVOLUTION_PARAMS, DEBUG_MODE
# kwargs ===================================================================================================
kwargs = {
    
    # runtime options
    'run_analysis': True,
    'plot_analysis': True,
    
    # analysis parameters
    'sim_data_path': ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/batch_2025-02-09/gen_20/gen_20_cand_240_data.pkl'),
    'output_dir': ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analysis/'),
    'reference_data_path': ('/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/network_metrics/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/well005/network_metrics.npy'),
    'levels': 6,
    'upper_bound': 1.8,
    'lower_bound': 0.2,
    'conv_params': conv_params,
    'mega_params': mega_params,
    'evol_params': evol_params,
    'fitnessFuncArgs': fitnessFuncArgs,
    #'max_workers': 32,
    'max_workers': 128,
    'run_parallel': True,
    'try_loading': False,
    'debug_mode': False,
    
    # simulation parameters
    'duration_seconds': 15,
    'verbose': False,
    'use_coreneuron': False,
    'validateNetParams': True,
    'saveJson': False,
    'savePickle': True,
    'cvode_active': False,
    
    #remove recordCells if present
    'remove_recordCells': True,
    
    # plot options
    'plot_permutations': True, # plot simulation permutation summary plots (i,e. bursting plots and comparisons to reference data) during run_permutation_v2()
    'plot_grid': False, # Old and deprecated
    'plot_heatmaps': True, # plot heatmaps of sensitivity analysis results in plot_sensitivity_analysis()
}
# main ===================================================================================================
if __name__ == '__main__':
    # runtime options
    #run_analysis = kwargs.get('run_analysis', False)
    #plot_analysis = kwargs.get('plot_analysis', False)
    
    # main analysis steps
    #if run_analysis: run_sensitivity_analysis_v2(kwargs)  # run_analysis
    #if plot_analysis: plot_sensitivity_analysis(kwargs)  # plot sensitivity analysis
    from RBS_network_models.sensitivity_analysis import plot_permutations
    #sim_data_path = kwargs.get('sim_data_path', None)
    output_dir = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analysis/'
    list_of_pkls_in_dir = []
    # walk through the directory and get all the pkl files
    import os
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".pkl"):
                list_of_pkls_in_dir.append(os.path.join(root, file))
    
    # load pickles and plot
    perm_network_data = []
    import pickle
    for pkl in list_of_pkls_in_dir:
        with open(pkl, 'rb') as f:
            data = pickle.load(f)
            perm_network_data.append(data)
            print(f"Loaded {pkl}")
            list_len = len(perm_network_data)
            if list_len == 10:
                break
    pkwargs = kwargs.copy()
    pkwargs['perm_network_data'] = perm_network_data
    plot_permutations(perm_network_data, pkwargs)

        
    

# perlmutter ===================================================================================================
# python command to run this script and save the output to output and error log files
'''
cd */RBS_network_models
python \ 
    /RBS_network_models/RBS_network_models/tests/_4_test_sensitivity_analysis.py \
    > /RBS_network_models/tests/outputs/test_sensitivity_analysis_levels/_test_sensitivity_analysis_levels_out.log \
    2> /RBS_network_models/tests/outputs/test_sensitivity_analysis_levels/_test_sensitivity_analysis_levels_err.log
'''