## This script ensures bidirectional syncing between a local Synology NAS directory and the NERSC pscratch workspace over NERSC recommended globus service.
## WARNING: Files stored on pscratch are routinely deleted by NERSC. Run this script routinely to avoid loss of data.
# Steps to follow:

# (Optional) Stop and remove any existing Docker container named "linux-env" as needed. Skip steps if comfortable re-starting existing container.
sudo docker stop linux-env
sudo docker rm linux-env

## Start a new Docker container with a Debian environment:
# if running on laptop locally instead of NAS, use the following command:
sudo docker run -it -d --name linux-env -v /mnt/c/Users/adamm:/Users/adamm  debian:latest

#NOTE: if the docker exists and is running, you can just attach to it with the following command:
sudo docker attach linux-env ## attach to the container to interact with it

#NOTE: if the docker already exitsts but is stopped - just start it with the following command:
sudo docker start linux-env

# ====================== INSIDE DOCKER CONTAINER ======================

# Update package lists and install required dependencies
apt-get update && apt-get install -y python3 python3-pip python3-venv passwd sudo

# Install pipx and ensure it's in the PATH
pip install --no-cache-dir --break-system-packages pipx # Install pipx using pip
pipx ensurepath
source ~/.bashrc # Add pipx to PATH for the current session

# Install Globus Connect Personal - required for setting up local endpoint
apt-get update && apt-get install -y wget
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
tar -xvzf globusconnectpersonal-latest.tgz

# ======================= SETUP GLOBUS USER =======================

# create a new user for globus - globus connect does not support running as root.
adduser globususer # follow prompts to set password and other details - enter whatever you want.

# permissions laptop
mkdir -p /Users/adamm/gdrive_amwe
chown -R globususer:globususer /Users/adamm/gdrive_amwe
chmod -R 777 /Users/adamm/gdrive_amwe --verbose

# add globususer to root and sudo groups
usermod -aG root globususer
usermod -aG sudo globususer

#check permissions after changing permissions
ls -ld /Users/adamm/gdrive_amwe

#login as globususer
su - globususer

# re-ensure pipx path with globuser
pipx ensurepath --force
source ~/.bashrc ## source updated bashrc
pipx install globus-cli # more info at # https://docs.globus.org/cli/

# ================== SETUP SYNC BETWEEEN LOCAL AND NERSC ==================

# login to globus
globus login --no-local-server
    # follow link and prompts after this command to login to globus

#cd back to root dir then to globusconnectpersonal dir, then run the setup script
cd globusconnectpersonal-*
./globusconnectpersonal -setup # follow prompts

#export
export laptop_end_point='ef02202c-f3d0-11ef-a7d6-0e26ca329435'

# start globus connect personal and check status to ensure it's running
./globusconnectpersonal -start -restrict-paths rw/Users/adamm &
./globusconnectpersonal -status

# get NERSC DTN collection ID from globus: https://app.globus.org/file-manager/collections/9d6d994a-6d04-11e5-ba46-22000b92c6ec/overview
export NERSC_DTN_endpoint="9d6d994a-6d04-11e5-ba46-22000b92c6ec"

# test access
globus ls "$NERSC_DTN_endpoint"
# probably prompted to run something like this: (can skip to this if NERSC endpoint hasnt changed)
globus session consent 'urn:globus:auth:scope:transfer.api.globus.org:all[*https://auth.globus.org/scopes/9d6d994a-6d04-11e5-ba46-22000b92c6ec/data_access]' --no-local-server
    #follow prompts to allow access.

# test access again
globus ls "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace" #check that you can access the workspace on NERSC


## OPTIONAL SYNC COMMANDS (NERSC -> Laptop) ======================

#prioritize spike_sorted data - mtime and better label
# Sync analysis outputs from NERSC to Local - misc_scripts/helping_hk_seker_lab to Local - use modified time instead of checksum
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/misc_scripts/helping_hk_seker_lab/data/sorted" \
"$laptop_end_point:/Users/adamm/gdrive_amwe/aw_spikesort_and_analysis/data/sorted" \
--sync-level mtime --notify failed,inactive,succeeded \
--label "Sync sorting data first by mtime NERSC to Local - $now" --verbose

#then send the rest of the project and data folder to the local machine
# Sync analysis outputs from NERSC to Local - misc_scripts/helping_hk_seker_lab to Local - use modified time instead of checksum 
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/misc_scripts/helping_hk_seker_lab" \
"$laptop_end_point:/Users/adamm/gdrive_amwe/aw_spikesort_and_analysis" \
--sync-level mtime --notify failed,inactive,succeeded \
--label "Sync analysis by mtime NERSC to Local - $now" --verbose

# prioritize spike_sorted data
# Sync analysis outputs from NERSC to Local - misc_scripts/helping_hk_seker_lab to Local - use size instead of checksum for faster syncing
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/misc_scripts/helping_hk_seker_lab/data/sorted" \
"$laptop_end_point:/Users/adamm/gdrive_amwe/aw_spikesort_and_analysis/data/sorted" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync NERSC to Local - $now" --verbose

#then send the rest of the project and data folder to the local machine
# Sync analysis outputs from NERSC to Local - misc_scripts/helping_hk_seker_lab to Local - use size instead of checksum for faster syncing
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/misc_scripts/helping_hk_seker_lab" \
"$laptop_end_point:/Users/adamm/gdrive_amwe/aw_spikesort_and_analysis" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync NERSC to Local - $now" --verbose


## OPTIONAL SYNC COMMANDS (Lab Server -> NERSC) ======================

# Sync Raw Data from lab server to NERSC - use size instead of checksum for faster syncing - specific folder
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter/_raw_data/hk_data_to_spikesort" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/hk_data_to_spikesort" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync server to NERSC - $now" --verbose

# Sync Raw Data from lab server to NERSC - use size instead of checksum for faster syncing - specific folder
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter/_raw_data/MEASlices_02122025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02122025_PVSandCA" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync server to NERSC - $now" --verbose

# Sync Raw Data from lab server to NERSC - use size instead of checksum for faster syncing - specific folder
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter/_raw_data/MEASlices_02032025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02032025_PVSandCA" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync server to NERSC - $now" --verbose

# sync all _raw_data from lab server to NERSC - use size instead of checksum for faster syncing
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter/_raw_data" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync server to NERSC - $now" --verbose


## OPTIONAL SYNC COMMANDS (Synology -> NERSC) ======================

# Sync Raw Data from Local to NERSC - use size instead of checksum for faster syncing - specific folder 
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter/_raw_data/hk_data_to_spikesort" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/hk_data_to_spikesort" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync workspace to NERSC - $now" --verbose

# Sync Raw Data from Local to NERSC - use size instead of checksum for faster syncing - specific folder 
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter/_raw_data/MEASlices_02122025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02122025_PVSandCA" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync workspace to NERSC - $now" --verbose

# Sync Raw Data from Local to NERSC - use size instead of checksum for faster syncing - specific folder 
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter/_raw_data/MEASlices_02032025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02032025_PVSandCA" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync workspace to NERSC - $now" --verbose

# Sync Raw Data from Local to NERSC - use size instead of checksum for faster syncing
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter/_raw_data" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data" \
--sync-level size --notify failed,inactive,succeeded \
--label "Sync workspace to NERSC - $now" --verbose

# Sync Raw Data from Local to NERSC
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter/_raw_data" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data" \
--sync-level checksum --notify failed,inactive,succeeded \
--label "Sync workspace to NERSC - $now" --verbose

# Sync Local → NERSC
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace" \
--sync-level checksum --notify failed,inactive,succeeded \
--label "Sync workspace to NERSC - $now" --verbose

# Sync NERSC → Local
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace" \
"$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter" \
--sync-level checksum --notify failed,inactive,succeeded \
--label "Sync workspace to Local - $now" --verbose

#allow globus to run in the background, if for some reason you're unable to type anything in the terminal because the globus command is taking over the terminal
# because the original docker command was run with -it and -d, you should be able to just close the terminal and the globus command will continue to run in the background. I think. # aw 2025-01-24 14:30:41


# Set up timers to use in perpetuity
# ====================== SETUP TIMERS ======================
globus timer create transfer \
"$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace" \
--interval 1d \
--start "$(date +'%Y-%m-%dT%H:%M:%S')" \
--sync-level checksum \
--notify failed,inactive,succeeded \
--name "Daily Local->NERSC Sync" \
--label "Sync workspace to NERSC"

globus timer create transfer \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace" \
"$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter" \
--interval 1d \
--start "$(date +'%Y-%m-%dT%H:%M:%S')" \
--sync-level checksum \
--notify failed,inactive,succeeded \
--name "Daily NERSC->Local Sync" \
--label "Sync workspace to Local"


# ====================== POST SETUP ======================
# # after setting up the timers, you can exit the docker container
# exit # exit the globususer shell
# exit # exit the docker container

# detatch from the docker container and keep it running in the background with globaluser logged in:


# very

## verify that postgreSQL is running and permissions are set correctly
sudo systemctl status pgsql-adapter.service
sudo -u postgres psql -c "SELECT version();"
