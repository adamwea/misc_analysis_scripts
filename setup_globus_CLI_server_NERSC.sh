## This script ensures bidirectional syncing between a local Synology NAS directory and the NERSC pscratch workspace over NERSC recommended globus service.
## WARNING: Files stored on pscratch are routinely deleted by NERSC. Run this script routinely to avoid loss of data.
# Steps to follow:
# Open terminal on the Synology NAS.
ping Ben-Shalom_NAS # check if the NAS is reachable on the network, #use CTRL+C to exit the ping command
ssh adamm@Ben-Shalom_NAS # Log in to the Synology NAS using SSH. # follow the prompts to log in.
sudo docker run -it -d --name globus-docker -v /mnt/ben-shalom_nas/:/mnt/ben-shalom_nas debian bash #if running on lab server instead of NAS, use the following command:

# options if docker already exists in some state
sudo docker stop globus-docker # (Optional) Stop and remove any existing Docker container named "linux-env" as needed. Skip steps if comfortable re-starting existing container.
sudo docker rm globus-docker
sudo docker attach globus-docker #NOTE: if the docker exists and is running, you can just attach to it
sudo docker start globus-docker #NOTE: if the docker already exitsts but is stopped - just start it

# ====================== INSIDE DOCKER CONTAINER ======================
# Update package lists and install required dependencies
apt-get update && apt-get install -y python3 python3-pip python3-venv passwd sudo
pip install --no-cache-dir --break-system-packages pipx # Install pipx using pip # Install pipx and ensure it's in the PATH
pipx ensurepath
source ~/.bashrc # Add pipx to PATH for the current session
apt-get update && apt-get install -y wget # Install Globus Connect Personal - required for setting up local endpoint
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
tar -xvzf globusconnectpersonal-latest.tgz

# ======================= SETUP GLOBUS USER =======================
# create a new user for globus - globus connect does not support running as root.
adduser globususer # follow prompts to set password and other details - enter whatever you want.
#ls -ld /mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter
# chown -R globususer:globususer /mnt/ben-shalom_nas/analysis/adamm/ --verbose
# chmod -R 777 /mnt/ben-shalom_nas/analysis/adamm/ --verbose
usermod -aG root globususer # add globususer to root and sudo groups
usermod -aG sudo globususer
# ls -ld /mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter
su - globususer #login as globususer

# ================== SETUP SYNC BETWEEEN LOCAL AND NERSC ==================
# set up sync between local and NERSC
pipx ensurepath --force # re-ensure pipx path with globuser
source ~/.bashrc ## source updated bashrc
pipx install globus-cli # more info at # https://docs.globus.org/cli/
globus login --no-local-server # follow link and prompts after running this command

cd / #cd back to root dir then to globusconnectpersonal dir, then run the setup script
cd globusconnectpersonal-3.2.6 # or whatever version you have
./globusconnectpersonal -setup # follow prompts and copy the endpoint ID for the next step

export lab_server_endpoint="0f0b7790-f3dd-11ef-901c-0e26ca329435" #export local_endpoint="f79f4d40-daa0-11ef-a1f9-798072df7d18" #replace with the actual ID of your local Globus Connect Personal endpoint
#./globusconnectpersonal -start -restrict-paths rw/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter & # lab server version
./globusconnectpersonal -start -restrict-paths rw/mnt/ben-shalom_nas & # so I can access raw_data files
./globusconnectpersonal -status #check status

# get NERSC DTN collection ID from globus: https://app.globus.org/file-manager/collections/9d6d994a-6d04-11e5-ba46-22000b92c6ec/overview
export NERSC_DTN_endpoint="9d6d994a-6d04-11e5-ba46-22000b92c6ec"
globus ls "$NERSC_DTN_endpoint"  # test access # probably prompted to run something like this:
globus session consent 'urn:globus:auth:scope:transfer.api.globus.org:all[*https://auth.globus.org/scopes/9d6d994a-6d04-11e5-ba46-22000b92c6ec/data_access]' --no-local-server #follow prompts to allow access.

#test access
globus ls $NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace #check that you can access the workspace on NERSC
globus ls $lab_server_endpoint:/mnt/ben-shalom_nas/raw_data #check that you can access the workspace on your local endpoin

# ====================== List of Projects to Sync Raw Data From ======================
# /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/Organoid_RTT_R270X_pA_pD_B1_d91
# Sync Raw Data from Local to NERSC - use size mtimes of files instead of checksum for faster syncing - use descriptive label for tracking
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/Organoid_RTT_R270X_pA_pD_B1_d91" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/Organoid_RTT_R270X_pA_pD_B1_d91" \
--sync-level mtime --notify failed,inactive,succeeded \
--label "Sync Organoid_RTT_R270X_pA_pD_B1_d91 to NERSC - $now" --verbose

# /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02032025_PVSandCA
# Sync Raw Data from Local to NERSC - use size mtimes of files instead of checksum for faster syncing - use descriptive label for tracking
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02032025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02032025_PVSandCA" \
--sync-level mtime --notify failed,inactive,succeeded \
--label "Sync MEASlices_02032025_PVSandCA to NERSC - $now" --verbose

# /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02122025_PVSandCA
# Sync Raw Data from Local to NERSC - use size mtimes of files instead of checksum for faster syncing - use descriptive label for tracking
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02122025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02122025_PVSandCA" \
--sync-level mtime --notify failed,inactive,succeeded \
--label "Sync MEASlices_02122025_PVSandCA to NERSC - $now" --verbose

# /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02242025_PVSandCA
# Sync Raw Data from Local to NERSC - use size mtimes of files instead of checksum for faster syncing - use descriptive label for tracking
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02242025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02242025_PVSandCA" \
--sync-level mtime --notify failed,inactive,succeeded \
--label "Sync MEASlices_02242025_PVSandCA to NERSC - $now" --verbose

# checksum version
# /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02242025_PVSandCA
# Sync Raw Data from Local to NERSC - use size mtimes of files instead of checksum for faster syncing - use descriptive label for tracking
now=$(date +'%Y-%m-%d %H:%M:%S')
globus transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02242025_PVSandCA" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_raw_data/MEASlices_02242025_PVSandCA" \
--sync-level checksum --notify failed,inactive,succeeded \
--label "Sync MEASlices_02242025_PVSandCA to NERSC - $now" --verbose

## ====================== List of Timers to Sync Analysis Data From ======================
# /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk24tbvol1/MEASlices_02242025_PVSandCA
# Sync Raw Data from Local to NERSC - use size mtimes of files instead of checksum for faster syncing - use descriptive label for tracking
# Define Variables
now=$(date +'%Y-%m-%d %H:%M:%S')
export TZ="America/Los_Angeles"
today=$(date +'%Y-%m-%d')
start_time=$(date -u -d "$today 17:00:00 PST" +'%Y-%m-%dT%H:%M:%SZ')
globus timer create transfer "$lab_server_endpoint:/mnt/ben-shalom_nas/analysis/adamm/workspace_perlmutter/2022-03-01_2022-03-31" \
"$NERSC_DTN_endpoint:/pscratch/sd/a/adammwea/workspace/_analysis_data/2022-03-01_2022-03-31" \
--start "$start_time" \
--label "Scheduled Sync MEASlices_02242025_PVSandCA to NERSC - $now" \
--sync-level mtime \
--notify failed,inactive,succeeded \
--verbose \
--stop-after-runs=1
