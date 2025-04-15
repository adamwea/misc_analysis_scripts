from RBS_network_models.CDKL5.DIV21.src.batch import batchEvol

kwargs = {
    'feature_path' : '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features/20250204_features.py',
    'mpiCommand' : '',
    }

batchEvol(**kwargs)

# Use this script to run the batch optimization in login node and test if fitness function works properly.