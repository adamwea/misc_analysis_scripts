# bin/bash

module load conda
#conda create -n my_mpi4py_env python=3.8
conda activate my_mpi4py_env
module swap PrgEnv-${PE_ENV,,} PrgEnv-gnu
# MPICC="cc -shared" pip install --force-reinstall --no-cache-dir --no-binary=mpi4py mpi4py
# python -m pip install --upgrade pip

# # requirements
# # pip install numpy
# pip install /pscratch/sd/a/adammwea/workspace/RBS_network_models
# pip install /pscratch/sd/a/adammwea/workspace/MEA_Analysis
# # pip install scipy
# # python -m pip install matplotlib
# # pip install tdqm
# # pip install pandas
# # pip install h5py
# # pip install spikeinterface==0.100.4
# # pip install neuron
# # #pip install netpyne
# pip install /pscratch/sd/a/adammwea/workspace/netpyne

# update for new repo location # aw 2025-04-08 12:12:24
# pip install -e ~/workspace/repos/RBS_network_models
# pip install -e ~/workspace/repos/MEA_Analysis
# pip install -e ~/workspace/repos/netpyne

#pip install scikit-learn
#pip install fastdtw

datetime=$(date '+%Y_%m_%d_%H_%M_%S')
#echo "printing outputs to workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/logs/${datetime}_test_batch_opt_DIV21_WT_interact_node.log" # send outputs and errors to file
#mkdir -p workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/logs/
#python -u workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_opt_DIV21_WT_interact.py > workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/logs/${datetime}_test_batch_opt_DIV21_WT_interact_node.log 2>&1 # send outputs and errors to file

# send outputs and errors to file - comment this or the other out as needed
#echo "printing outputs to workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/logs/${datetime}_test_batch_config_interact.log" # send outputs and errors to file
#python -u workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_config_interact.py > workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/logs/${datetime}_test_batch_config_interact.log 2>&1 # send outputs and errors to file

# send outputs and errors to console
#python -u workspace/RBS_network_models/scripts/CDKL5/DIV21_WT/test_batch_opt_DIV21_WT_interact.py

#update for organoid
# echo "printing outputs to workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/batch_runs/logs/${datetime}_test_batch_config_interact.log" # send outputs and errors to file
# python -u workspace/RBS_network_models/scripts/Organoid_RTT_R270X/DIV112_WT/test_batch_config_interact.py > workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/batch_runs/logs/${datetime}_test_batch_config_interact.log 2>&1 # send outputs and errors to file

#send outputs and errors to console - useful for debugging
#python -u ~/workspace/aw_scripts/network_model_development/Organoid_RTT_R270X/DIV112_WT/test_batch_config_interact.py
python -u ~/workspace/aw_scripts/network_model_development/Organoid_RTT_R270X/DIV112_WT/run_batch_login.py