# print out the structure of a folder in terminal.

import os

def print_structure_of_folder(folder_path, indent=0, exclude_folders=[]):
    for item in os.listdir(folder_path):
        
        #if .git folder, skip it
        if item == '.git':
            continue
        
        # if item is a file, not a folder, skip it
        if os.path.isfile(os.path.join(folder_path, item)) and not item.endswith('__init__.py'):
            continue
        
        if os.path.isdir(os.path.join(folder_path, item)):
            print(' ' * indent + item + '/')
            if item not in exclude_folders:
                print_structure_of_folder(os.path.join(folder_path, item), indent + 4, exclude_folders=exclude_folders)
        else:
            print(' ' * indent + item)
            
#print_structure_of_folder('/pscratch/sd/a/adammwea/workspace/RBS_network_models')
print_structure_of_folder('/pscratch/sd/a/adammwea/workspace/MEA_Analysis',
                          exclude_folders=[     '.git',
                                                'build',
                                                'dist',
                                                'venv',
                                                'env',
                                                'Archive',
                                                'outputs',
                                                'output',                                                
                            
                                           ]
                          )
print('done')
