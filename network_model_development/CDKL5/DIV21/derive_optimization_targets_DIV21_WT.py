# New Fitness Targets
#from workspace.RBS_neuronal_network_models.optimizing.CDKL5_DIV21.scripts_dep.sim_helper import *
#from RBS_network_models.network_analysis import build_network_metric_targets_dict, save_network_metric_dict_with_timestamp
from MEA_Analysis.NetworkAnalysis.awNetworkAnalysis.network_analysis import save_network_metric_dict_with_timestamp
from RBS_network_models.feature_struct import build_network_metric_targets_dict_v2
import numpy as np
#load network metric npy
npy_path = (
    # "/pscratch/sd/a/adammwea/workspace/RBS_neuronal_network_models/optimization_projects/"
    # "CDKL5_DIV21/_config/experimental_data_features/network_metrics/"
    # "CDKL5-E6D_T2_C1_05212024_240611_M06844_Network_000076_network_metrics_well000.npy"
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/'
    'network_metrics/CDKL5-E6D_T2_C1_05212024_240611_M08029_Network_000091_network_metrics_well001.npy'
)

#
#output_dir = '/pscratch/sd/a/adammwea/workspace/RBS_neuronal_network_models/optimization_projects/CDKL5_DIV21/_config/experimental_data_features'
output_dir = (
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features'
)
#==============================================================================

# derive initial optimization targets, save as .py script mean to be edited and annotated as needed.
# feature scripts are saved in data/CDKL5/DIV21/features and annotated with the date they were created.
network_metrics = np.load(npy_path, allow_pickle=True).item()
network_metrics_targets = build_network_metric_targets_dict_v2(network_metrics)
save_network_metric_dict_with_timestamp(network_metrics, network_metrics_targets, output_dir)

# calibrate against fitness function
from  RBS_network_models.fitnessFunc import fitnessFunc
kwargs = {
    'targets': network_metrics_targets,
    'network_metrics': network_metrics,
}
#kwargs = network_metrics
average_fitness = fitnessFunc(**kwargs, mode='experimental')

  