## This script ensures bidirectional syncing between a local Synology NAS directory and the NERSC pscratch workspace over SSH.
## WARNING: Files stored on pscratch are routinely deleted by NERSC. Run this script routinely to avoid loss of data.

# Steps to follow:

# 1. Open terminal on the Synology NAS.
ping Ben-Shalom_NAS # check if the NAS is reachable on the network
#use CTRL+C to exit the ping command
ssh adamm@Ben-Shalom_NAS # Log in to the Synology NAS using SSH.
# follow the prompts to log in.

# 2. Run this command to start a Docker container with a Debian environment:

# if the docker was already running - you can skip this step or do the following:
sudo docker stop linux-env
sudo docker rm linux-env

## Start a new Docker container with a Debian environment:
sudo docker run -it --rm --name linux-env -v /volume1:/volume1 debian bash

# 3. Install necessary tools inside the container:
apt-get update
apt-get install rsync -y
apt-get install openssh-client -y
apt-get install unison -y ## Optional: Install Unison for bidirectional sync if needed - try this out later.


#3.5 setup ssh key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
ssh-copy-id adammwea@perlmutter-p1.nersc.gov
# test the ssh connection
ssh adammwea@perlmutter-p1.nersc.gov

# 4. Perform bidirectional sync using rsync.


### Option 1 - Using two separate rsync commands for bidirectional sync:

#check dry-run before running the actual sync:
#sync FROM Synology TO NERSC
rsync -avz --progress -e "ssh" \
/volume1/MEA_Backup/analysis/adamm_pscratch_workspace/ \
adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/ \
--dry-run \

rsync -avz --progress -e "ssh" \
adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/ \
/volume1/MEA_Backup/analysis/adamm_pscratch_workspace/ \
--dry-run

# Create a script to run both directions together:

# TODO: Not currently sure how to do this in a single command due to OTP. So I'll do one at a time.
# I'll sync from synology to NERSC first, then from NERSC to Synology on a different day. # aw 2025-01-22 16:02:37

cat << 'EOF' > /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/sync_workspace.sh
#!/bin/bash

# Sync FROM Synology TO NERSC
rsync -avz --progress -e "ssh" \
/volume1/MEA_Backup/analysis/adamm_pscratch_workspace/ \
adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/ \
> /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/rsync_synology_to_pscratch.log 2>&1

# Sync FROM NERSC TO Synology
rsync -avz --progress -e "ssh" \
adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/ \
/volume1/MEA_Backup/analysis/adamm_pscratch_workspace/ \
> /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/rsync_pscratch_to_synology.log 2>&1

# Print completion message
echo "Bidirectional sync completed. Check logs for details."
EOF

# 5. Make the script executable:
chmod +x /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/sync_workspace.sh

# 6. Run the script to execute both syncs in one command:
bash /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/sync_workspace.sh

### Option 2 - Using Unison for bidirectional sync (optional):


### Option 3 - set up syncthing in terminal for bidirectional sync (optional):


# 7. Detach from the Docker container and allow the sync to continue:
# Press Ctrl+P, then Ctrl+Q to detach from the container.

# 8. Walk away and let the sync complete. Repeat this process regularly to avoid losing data on pscratch.
