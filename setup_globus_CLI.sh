## This script ensures bidirectional syncing between a local Synology NAS directory and the NERSC pscratch workspace over NERSC recommended globus service.
## WARNING: Files stored on pscratch are routinely deleted by NERSC. Run this script routinely to avoid loss of data.
# Steps to follow:

# Open terminal on the Synology NAS.
ping Ben-Shalom_NAS # check if the NAS is reachable on the network, #use CTRL+C to exit the ping command
ssh adamm@Ben-Shalom_NAS # Log in to the Synology NAS using SSH. # follow the prompts to log in.

# (Optional) Stop and remove any existing Docker container named "linux-env" as needed. Skip steps if comfortable re-starting existing container.
sudo docker stop linux-env
sudo docker rm linux-env

## Start a new Docker container with a Debian environment:
#sudo docker run -it -d --name linux-env -v /volume1:/volume1 debian bash # start detatched and interactive
sudo docker run -it -d --name linux-env -v /volume1/MEA_Backup:/volume1/MEA_Backup debian bash

#if running on lab server instead of NAS, use the following command:
sudo docker run -it -d --name linux-env -v /mnt/ben-shalom_nas/:/mnt/ben-shalom_nas debian bash


#NOTE: if the docker exists and is running, you can just attach to it with the following command:
sudo docker attach linux-env ## attach to the container to interact with it

#NOTE: if the docker already exitsts but is stopped - just start it with the following command:
sudo docker start linux-env

# ====================== INSIDE DOCKER CONTAINER ======================

# Update package lists and install required dependencies
apt-get update && apt-get install -y python3 python3-pip python3-venv
apt-get update && apt-get install -y passwd sudo
#apt-get update && apt-get install -y acl #needed for changing permissions of volume1

# Install pipx and ensure it's in the PATH
pip install --no-cache-dir --break-system-packages pipx # Install pipx using pip
pipx ensurepath

# Add pipx to PATH for the current session
source ~/.bashrc

# Install Globus Connect Personal - required for setting up local endpoint
apt-get update && apt-get install -y wget
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
tar -xvzf globusconnectpersonal-latest.tgz

# ======================= SETUP GLOBUS USER =======================

# create a new user for globus - globus connect does not support running as root.
adduser globususer # follow prompts to set password and other details - enter whatever you want.

# ====================== SETUP PERMISSIONS AND INSTALL GLOBUS CLI ======================

# check permissions after changing permissions
ls -ld /volume1/MEA_Backup/analysis/adamm/workspace_perlmutter
chown -R globususer:globususer /volume1/MEA_Backup/analysis/adamm/ --verbose
chmod -R 777 /volume1/MEA_Backup/analysis/adamm/ --verbose

# server version
ls -ld /mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter
chown -R globususer:globususer /mnt/ben-shalom_nas/analysis/adamm/ --verbose
chmod -R 777 /mnt/ben-shalom_nas/analysis/adamm/ --verbose

# add globususer to root and sudo groups
usermod -aG root globususer
usermod -aG sudo globususer

# check permissions after changing permissions
ls -ld /volume1/MEA_Backup/analysis/adamm/workspace_perlmutter
# server version
ls -ld /mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter

#3.

#login as globususer
su - globususer

# re-ensure pipx path with globuser
pipx ensurepath --force
source ~/.bashrc ## source updated bashrc
pipx install globus-cli # more info at # https://docs.globus.org/cli/

# ================== SETUP SYNC BETWEEEN LOCAL AND NERSC ==================

globus login --no-local-server

# follow link and prompts.

#cd back to root dir then to globusconnectpersonal dir, then run the setup script
cd globusconnectpersonal-*
./globusconnectpersonal -setup # follow prompts

#export local_endpoint="f79f4d40-daa0-11ef-a1f9-798072df7d18" #replace with the actual ID of your local Globus Connect Personal endpoint
#export local_endpoint=" 28936af4-e266-11ef-9cb8-33056a2963dc"
# export local_endpoint="f6011104-e26a-11ef-9cb8-33056a2963dc"
export local_endpoint="a3bad8b6-ea4d-11ef-a25f-0219042cd421"
export lab_server_endpoint="beb53322-eaff-11ef-b59e-0affe48c30b5"

#./globusconnectpersonal -start & ## Start Globus Connect Personal in the background
./globusconnectpersonal -start -restrict-paths rw/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter &
# lab server version
./globusconnectpersonal -start -restrict-paths rw/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter &

#check status
./globusconnectpersonal -status

## follow the prompts to set up Globus Connect Personal

#globus ls "$local_endpoint"

# get NERSC DTN collection ID from globus: https://app.globus.org/file-manager/collections/9d6d994a-6d04-11e5-ba46-22000b92c6ec/overview
export NERSC_DTN_endpoint="9d6d994a-6d04-11e5-ba46-22000b92c6ec"

# test access
globus ls "$NERSC_DTN_endpoint"

# probably prompted to run something like this:
globus session consent 'urn:globus:auth:scope:transfer.api.globus.org:all[*https://auth.globus.org/scopes/9d6d994a-6d04-11e5-ba46-22000b92c6ec/data_access]' --no-local-server

#follow prompts to allow access.

# test access again
#globus ls "$NERSC_DTN_endpoint"
globus ls "$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace" #check that you can access the workspace on NERSC

#check local endpoint one more time
#ln -s /volume1/MEA_Backup/analysis/adamm/workspace_perlmutter ~/workspace_perlmutter
globus ls "$local_endpoint:/volume1/MEA_Backup/analysis/adamm/workspace_perlmutter" #check that you can access the workspace on your local endpoint

# server version
globus ls "$lab_server_endpoint:/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter" #check that you can access the workspace on your local endpoint

## OPTIONAL SYNC COMMANDS (NERSC -> Laptop) ======================


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
