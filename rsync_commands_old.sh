rsync -avz --progress -e "ssh -p <HPC_SSH_PORT>" \
    --include '*/' \
    --include '*/AxonTracking/**' \
    --exclude '*' \
    /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/CDKL5*/ \
    adammwea@login28:/pscratch/sd/a/adammwea/workspace/xInputs/xRBS_input_data/

rsync -avz --progress --dry-run -e "ssh" \
    --include '*/' \
    --include '*/AxonTracking/**' \
    --exclude '*' \
    /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/CDKL5*/ \
    adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/xInputs/xRBS_input_data/
    
rsync -avz --progress --prune-empty-dirs --dry-run -e "ssh" \
    --include '*/' \
    --include '*/AxonTracking/**' \
    --exclude '*' \
    /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/CDKL5*/ \
    adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/xInputs/xRBS_input_data/

rsync -avz --progress --prune-empty-dirs -e "ssh" \
    --include '*/' \
    --include '*/AxonTracking/**' \
    --exclude '*' \
    /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/CDKL5*/ \
    adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/xInputs/xRBS_input_data/ \
    --dry-run \  # Uncomment this line to enable dry-run mode
    > /home/adamm/rsync_to_perlmutter.log 2>&1 &

#protocol
sudo docker run -it --rm --name linux-env debian bash

#install screen if necessary
apt-get update
#apt-get install screen -y
apt-get install rsync -y

#install ssh
apt-get install openssh-client -y

#screen #in the future, skip this screen step and just run the rsync command in docker

#use dry run to test, then run without dry run
#rsync -avz --progress --prune-empty-dirs -e "ssh" --include '*/' --include '*/AxonTracking/**' --exclude '*' /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/CDKL5*/ adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/xInputs/xRBS_input_data/ --dry-run

## options
# rsync specific folder
rsync -avz --progress --prune-empty-dirs -e "ssh" /volume1/MEA_Backup/analysis/_to_adamm_pscratch/ adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/_from_synology/ --dry-run

# rsync the entire workspace folder
rsync -avz --progress -e "ssh" /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/ adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/ --dry-run > /volume1/MEA_Backup/analysis/adamm_pscratch_workspace/rsync_synology_pscratch.log 2>&1 &



#detatch from screen
#Ctrl+A, D # in the future, skip this screen step and just run the rsync command in docker

#detatch from docker
#Ctrl+P, Q

#  > /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/rsync_to_perlmutter.log 2>&1 && scp /volume1/MEA_Backup/raw_data/rbs_maxtwo_desktop/harddisk20tb/rsync_to_perlmutter.log adammwea@perlmutter-p1.nersc.gov:/pscratch/sd/a/adammwea/workspace/xInputs/xRBS_input_data/
