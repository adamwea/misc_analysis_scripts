from RBS_network_models.CDKL5.DIV21.src.batch import batchEvol
from mpi4py import MPI
kwargs = {
    #'feature_path' : '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features/20250204_features.py',
    'feature_path' : '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features/20250207_features.py',    
    'mpiCommand' :             
            'srun'
            ' --nodes=1' # number of nodes
            # bind to socket
            #' --cpu-bind=verbose,cores'
            #' --hint=multithread' # enable multithreading on each core
            #' --cores-per-task=4' # set number of cores per task
            ,
    'nrnCommand': 
        'shifter --image=adammwea/netsims_docker:v1 '
        'nrniv',
    'seed_dir': "/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/seeds"
    }

batchEvol(**kwargs)

'''
# run everything in interactive node - run each script, one at a time

# step 1:
bash /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_config_interact_allocate.sh

# step 2:
bash /pscratch/sd/a/adammwea/workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_config_interact_run.sh
'''

# Use this script to run the batch optimization in interactive node and test if parallelized simulations work properly.