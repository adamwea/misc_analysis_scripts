# Notes ===================================================================================================
'''
'''
# Imports ===================================================================================================
import os
import datetime
from RBS_network_models.sensitivity_analysis import run_sensitivity_analysis_v2, plot_sensitivity_analysis_v2
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
    'levels': 6,
    'upper_bound': 7.5,
    'lower_bound': 0.1,
    'conv_params': conv_params,
    'mega_params': mega_params,
    'evol_params': evol_params,
    'fitnessFuncArgs': fitnessFuncArgs,
    
    # runtime options  
    #'max_workers': 1,
    #'max_workers': 32,
    #'max_workers': 2,
    #'max_workers': 128,    
    'max_workers': 256,
    'run_parallel': True,
    #'try_loading': False,
    'try_load_sim_data': True, # try loading simulation data from sim_data_path instead of running new simulations
    'try_load_network_data': True, # check if network data plot is present, skip plotting if it is
    #'try_load_network_data': False, # check if network data plot is present, skip plotting if it is
    'try_load_network_summary': True, # check if network summary plot is present, skip plotting if it is
    #'try_load_network_summary': False, # check if network summary plot is present, skip plotting if it is
    'debug_mode': False,
    
    # Network analysis params
    'dtw_matrix': False, # cross compare all bursts with all bursts - takes a long time - includes parallelization
    'burst_sequencing': False, # sequence order of units participating in each burst - takes a long time - includes parallelization
    
    # simulation parameters
    'duration_seconds': 65,
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

def prep_output_dirs():
    # NOTES and Path Selection ===================================================================================================   
    '''
    # prior to aw 2025-03-02 15:21:01 - used mostly to develop
    # 'sim_data_path': os.path.join(data_dir, project_dir, batch_dir, 'gen_20/gen_20_cand_240_data.pkl'),
    # 'output_dir': os.path.join(data_dir, project_dir, 'sensitivity_analyses/'),
    
    # aw 2025-03-02 15:21:21 - running a different batch out of curiousity and also to finish developing output save locs
    # # define parent dirs
    # data_dir = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/'
    # project_dir = 'CDKL5/DIV21/' # NOTE: Apparently os.path doesnt like leading '/' in the path parts
    # batch_dir = 'batch_runs/batch_2025-02-09/'
    # ref_path = 'network_metrics/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/well005/network_metrics.npy'
    # cand_path = 'gen_26/gen_26_cand_71_data.pkl'
    '''
    '''
    # aw 2025-03-03 12:52:32 - /pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/2025-03-02_gen_26_cand_71_data_35s/propVelocity_3/propVelocity_3_data.pkl
    # this simulation showed faster hyper burst rate and tigher bursts like initially desired, great place to start for next sensitivity analysis.
    data_dir = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/'
    project_dir = 'CDKL5/DIV21/' # NOTE: Apparently os.path doesnt like leading '/' in the path parts
    ref_path = 'network_metrics/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/well005/network_metrics.npy'
    batch_dir = 'sensitivity_analyses/2025-03-02_gen_26_cand_71_data_35s/'
    cand_path = 'propVelocity_3/propVelocity_3_data.pkl'
    '''
    '''
    # aw 2025-03-05 14:37:17 - I'm going to try and generate a CDKL5 Model where the hyperburst rate is about 2-4 per 60 seconds...this is specifically for a meeting Roy has tomorrow. 
    # /pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/2025-03-04_propVelocity_3_data_35s/propVelocity_0/propVelocity_0_data.pkl
    # I'm going to extend the duration to 60 seconds and modulate the limits of levels
    # the starting point is the propVelocity_0 perm which has one big burst in 35 seconds
    # propVelocity_1 from the same SA is a little too fast.
    # I think If I constrict the levels a little bit, propVelocity_3 in the new SA will be about right.
    data_dir = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/'
    project_dir = 'CDKL5/DIV21/'
    ref_path = 'network_metrics/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/well005/network_metrics.npy'
    batch_dir = 'sensitivity_analyses/2025-03-04_propVelocity_3_data_35s/'
    cand_path = 'propVelocity_0/propVelocity_0_data.pkl'
    '''
    # aw 2025-03-05 16:03:07 - yup that worked. Now doing full SA for the propVelocity_3 data from the last run.
    # /pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/2025-03-05_propVelocity_0_data_65s/propVelocity_3/propVelocity_3_data.pkl
    data_dir = '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/'
    project_dir = 'CDKL5/DIV21/'
    ref_path = 'network_metrics/CDKL5-E6D_T2_C1_05212024/240611/M08029/Network/000091/well005/network_metrics.npy'
    batch_dir = 'sensitivity_analyses/2025-03-05_propVelocity_0_data_65s/'
    cand_path = 'propVelocity_3/propVelocity_3_data.pkl'
    # main ===================================================================================================
        
    # build paths
    output_dir = os.path.abspath(os.path.join(data_dir, project_dir, 'sensitivity_analyses/'))
    ref_path = os.path.abspath(os.path.join(data_dir, project_dir, ref_path))
    sim_data_path = os.path.abspath(os.path.join(data_dir, project_dir, batch_dir, cand_path))
    
    # Update kwargs
    kwargs['output_dir'] = output_dir
    kwargs['sim_data_path'] = sim_data_path
    kwargs['reference_data_path'] = ref_path
    
    # run_label
    # run_label = 'analysis_2_gen_20_cand_240_35s'
    # kwargs['output_dir'] = os.path.join(kwargs['output_dir'], run_label)     #update kwargs output_dir with additional dir for run_label
    # if not os.path.exists(kwargs['output_dir']): os.makedirs(kwargs['output_dir']) # create output_dir if it does not exist
    sim_data_path = kwargs.get('sim_data_path', None)
    base = os.path.basename(sim_data_path).replace('.pkl', '')
    
    # datetime YYYY-MM-DD HH:MM:SS
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # yesterdate = datetime.datetime.now() - datetime.timedelta(days=1)
    # date = yesterdate.strftime("%Y-%m-%d")
    
    duration = kwargs.get('duration_seconds', 35)
    kwargs['run_label'] = f'{date}_{base}_{duration}s'
    kwargs['output_dir'] = os.path.join(kwargs['output_dir'], kwargs['run_label'])     #update kwargs output_dir with additional dir for run_label
    if not os.path.exists(kwargs['output_dir']): os.makedirs(kwargs['output_dir']) # create output_dir if it does not exist
    #output_dir = kwargs['output_dir']
    print(f'output_dir: {kwargs["output_dir"]}')
    print(f'sim_data_path: {sim_data_path}')
    print(f'reference_data_path: {ref_path}')
    print(f'run_label: {kwargs["run_label"]}')

# main ===================================================================================================
if __name__ == '__main__':
    
    # prep output directories
    prep_output_dirs() # NOTE: Review/Edit this to make sure inputs and outputs are correct for the current run
    
    # runtime options
    run_analysis = kwargs.get('run_analysis', False)
    plot_analysis = kwargs.get('plot_analysis', False)
    
    # # # force run_analysis to false if plot_analysis is false
    run_analysis = False
    
    # main analysis steps
    if run_analysis: run_sensitivity_analysis_v2(kwargs)  # run_analysis
    if plot_analysis: plot_sensitivity_analysis_v2(kwargs)  # plot sensitivity analysis

# perlmutter ===================================================================================================
# python command to run this script and save the output to output and error log files
'''
salloc -A m2043 -q interactive -C cpu -t 04:00:00 --nodes=1 --image=adammwea/axonkilo_docker:v7
module load conda
conda activate netsims_env
python /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/run_sensitivity_analysis.py \
    > /pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/2025-03-02_gen_26_cand_71_data_35s/_run_sensitivity_analysis_out.log \
    2> /pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/sensitivity_analyses/2025-03-02_gen_26_cand_71_data_35s/_run_sensitivity_analysis_err.log
'''

# '''
# cd */RBS_network_models
# python \ 
#     /RBS_network_models/RBS_network_models/tests/_4_test_sensitivity_analysis.py \
#     > /RBS_network_models/tests/outputs/test_sensitivity_analysis_levels/_test_sensitivity_analysis_levels_out.log \
#     2> /RBS_network_models/tests/outputs/test_sensitivity_analysis_levels/_test_sensitivity_analysis_levels_err.log
# '''