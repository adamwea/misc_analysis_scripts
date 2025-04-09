#from RBS_network_models.CDKL5.DIV21.src.batch import batchEvol
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.batch import batchEvol_v2 as batchEvol
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.evol_params import params
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import mega_params
try:
    from mpi4py import MPI
except ImportError:
    print("WARNING: mpi4py not installed, running in single process mode")
    print("this is fine if debugging in login node, but not for batch jobs")
    pass

# main ========================================================================================
kwargs = {
    
    # login
    #'mpiCommand': '',
    #'nrnCommand': '',
    
    # interactive or queue
    # 'mpiCommand' :             
    #         'srun'
    #         ' --nodes=1' # number of nodes
    #         # bind to socket
    #         #' --cpu-bind=verbose,cores'
    #         #' --hint=multithread' # enable multithreading on each core
    #         #' --cores-per-task=4' # set number of cores per task
    #         ,
    # 'nrnCommand': 
    #     'shifter --image=adammwea/netsims_docker:v1 '
    #     'nrniv',
    'parameter_space': params,
    'batchFolder': (
        '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/batch_runs'
        ),
    'reference_data_paths': { # for fitting against
        #'/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics/Organoid_RTT_R270X_pA_pD_B1_d91_250107_M07297_Network_000028_network_metrics_well005.npy',
        #'~/cfs_m2043/roybens/ben-shalom_nas/analysis/2025/adamm/old_data_pre-27Mar2025/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics/Organoid_RTT_R270X_pA_pD_B1_d91_250107_M07297_Network_000028_network_metrics_well005.npy'
        '/global/homes/a/adammwea/cfs_m2043/roybens/ben-shalom_nas/analysis/2025/adamm/old_data_pre-27Mar2025/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/network_metrics/Organoid_RTT_R270X_pA_pD_B1_d91/250107/M07297/Network/000028/well005/network_metrics.npy'
        },
    'runCfg_script_path': '/pscratch/sd/a/adammwea/workspace/RBS_network_models/RBS_network_models/Organoid_RTT_R270X/DIV112_WT/src/init.py',
    #'seed_dir': "/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/seeds"
    "conv_params": conv_params,
    "mega_params": mega_params,
    }

batchEvol(**kwargs)

# '''
# # run everything in interactive node - run each script, one at a time

# # step 1:
# bash /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_config_interact_allocate.sh

# # step 2:
# bash /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_config_interact_run.sh
# '''

'''
# run in login node for testing/debugging

shifter --image=adammwea/netsims_docker:v1 bash

'''


'''
# run everything in interactive node - run each script, one at a time

# step 1:
bash ~/workspace/aw_scripts/network_model_development/Organoid_RTT_R270X/DIV112_WT/test_batch_config_interact_allocate.sh

# step 2:
bash ~/workspace/aw_scripts/network_model_development/Organoid_RTT_R270X/DIV112_WT/test_batch_config_interact_run.sh

'''

# Use this script to run the batch optimization in interactive node and test if parallelized simulations work properly.