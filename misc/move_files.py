import os
import subprocess

# Define the second-layer target directory
#base_dir = "/pscratch/sd/a/adammwea/workspace/_raw_data/B6J_DensityTest_10012024_AR"
#base_name = 'B6J_DensityTest_10012024_AR'

# Define the second-layer target directory
# base_dir = "/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5_R59X_100112024_PS"
# base_dir = '/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5_R59X_10112024_PS'
# base_name = 'CDKL5_R59X_10112024_PS'

def get_deepest_dirs(base):
    """Find directories nested inside target_dir"""
    all_dirs = []
    for root, dirs, files in os.walk(base, topdown=False):  # Walk from deepest to shallowest
        if root != target_dir:  # Ignore the second-layer directory itself
            all_dirs.append(root)
    return sorted(all_dirs, key=lambda x: x.count('/'), reverse=True)  # Sort by depth

def get_all_dirs_in_base_dir():
    """Get all files in the base directory"""
    #all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            #all_files.append(os.path.join(root, directory))
            all_dirs.append(os.path.join(root, directory))
        #for file in files:
        #    all_files.append(os.path.join(root, file))
        
    # Remove all empty directories
    for directory in all_dirs:
        current_dir = directory
        # Remove empty directories in the current directory
        if os.path.isdir(current_dir):
            try:
                subprocess.run(["find", current_dir, "-type", "d", "-empty", "-delete"], check=True)
                #print(f"Removed empty directories in: {current_dir}")
                #print(f"Removed empty directory: {current_dir}")
            except:
                #print(f"Error: {current_dir}")
                continue
    
    # update all_dirs
    all_dirs = []
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            all_dirs.append(os.path.join(root, directory))
    
    return all_dirs

def move_files_up():
    """Moves files from the deepest directories to their parent"""
    while True:
        
        # Get the deepest directories
        all_dirs = get_all_dirs_in_base_dir()
        print(len(all_dirs))
        
        #counts = []
        #removal_attempts = 0
        to_be_removed = []
        for i, directory in enumerate(all_dirs):
            count = directory.count(base_name)
            if count == 2:
                #all_dirs.remove(directory)
                to_be_removed.append(directory)
                #removal_attempts += 1
            else:
                print(f"Error: {directory}")
                continue
            #counts.append(count)
            
        for directory in to_be_removed:
            all_dirs.remove(directory)
        
        print(len(all_dirs))
        if not all_dirs:
            print("No more directories to process.")
            break

        # for dir_path in deepest_dirs:
        for directory in all_dirs:
            # init
            current_dir = directory
            
            # count the number of base_name copies in the directory
            count = directory.count(base_name)
            
            # if there is any number other than 2 base_name copies, replace those basenames with two copies in target_dir
            if count != 2:
                template_copies = f'/{base_name}' * count
                target_dir = current_dir.replace(template_copies, f'/{base_name}/{base_name}')
                if target_dir.endswith('/'):
                    target_dir = target_dir[:-1]
            else:
                continue                
            
            # set current and target directories
            try:
                assert target_dir != current_dir, "Target directory is the same as the current directory."
                assert target_dir.count(base_name) == 2, "Target directory does not contain two copies of the base name."  
            except:
                print(f"Error: {target_dir}")
                continue
            
            # skip directories end in base_name to avoid recursion
            if current_dir.endswith(base_name) and target_dir.endswith(base_name):
                #continue
                pass
            else:          
            
                # Rsync command to move files up one level
                rsync_cmd = [
                    "rsync", "-a", "--size-only", "--remove-source-files", "--progress",
                    f"{current_dir}/",  # Source directory
                    f"{target_dir}/"  # Destination
                ]
                
                print()
                print(f"Moving files from:\n\t{current_dir} → \n\t{target_dir}")
                print()
                subprocess.run(rsync_cmd, check=True)

def move_files_down():
    """Moves any remaining files from base_dir (1st layer) to target_dir (2nd layer), avoiding recursion."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # Ensure the second-layer directory exists

    # Rsync to move only files and directories EXCEPT the second-layer directory itself
    rsync_cmd = [
        "rsync", "-a", "--size-only", "--remove-source-files", "--progress",
        "--exclude", f"{os.path.basename(target_dir)}/",  # Exclude the second-layer directory
        f"{base_dir}/",  # Source (1st layer)
        f"{target_dir}/"  # Destination (2nd layer)
    ]

    print(f"Moving remaining files from {base_dir} → {target_dir}, excluding {target_dir}")
    subprocess.run(rsync_cmd, check=True)

    # Remove empty directories in the base layer, but NOT the target directory itself
    subprocess.run(["find", base_dir, "-mindepth", "1", "-type", "d", "-empty", "-delete"], check=True)

if __name__ == "__main__":
    # Define the second-layer target directory
    base_dir = '/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5-E6D_T1_C1_05152024'
    base_name = 'CDKL5-E6D_T1_C1_05152024'
    
    move_files_up()
    
    # Define the second-layer target directory
    base_dir = '/pscratch/sd/a/adammwea/workspace/_raw_data/CDKL5-E6D_T2_C1_05212024'
    base_name = 'CDKL5-E6D_T2_C1_05212024'
    
    move_files_up()
    
    # Define the second-layer target directory
    base_dir = '/pscratch/sd/a/adammwea/workspace/_raw_data/FolicAcid_T3_10222024_PS'
    base_name = 'FolicAcid_T3_10222024_PS'
    
    move_files_up()
    
    # Define the second-layer target directory
    base_dir = '/pscratch/sd/a/adammwea/workspace/_raw_data/Human_E_Neurons_T1_06072024'
    base_name = 'Human_E_Neurons_T1_06072024'
    
    move_files_up()
    
    # Define the second-layer target directory
    base_dir = '/pscratch/sd/a/adammwea/workspace/_raw_data/Organoid_RTT_R270X_pA_pD_B1_d91'
    base_name = 'Organoid_RTT_R270X_pA_pD_B1_d91'
    
    move_files_up() 
