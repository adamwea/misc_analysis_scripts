# ============================================================================================
reference_data_path = (
    # "/pscratch/sd/a/adammwea/workspace/RBS_neuronal_network_models/optimization_projects/"
    # "CDKL5_DIV21/_config/experimental_data_features/network_metrics/"
    # "CDKL5-E6D_T2_C1_05212024_240611_M06844_Network_000076_network_metrics_well000.npy"
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/'
    'network_metrics/CDKL5-E6D_T2_C1_05212024_240611_M08029_Network_000091_network_metrics_well001.npy'
)
feature_path = (
    #'/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features/20250204_features.py'
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/features/20250207_features.py'
    )
batch_dir = (
    #'/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/batch_2025-02-07'
    '/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/CDKL5/DIV21/batch_runs/batch_2025-02-09'
    )

v2 = True # turned on for now
if v2: # v2 ============================================================================================
    import os
    import pandas as pd
    import json
    import multiprocessing
    from netpyne import sim
    from RBS_network_models.sim_analysis import process_simulation
    from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params
    from RBS_network_models.utils.cfg_helper import import_module_from_path

    def get_penultimate_generation(batch_dir):
        for root, dirs, _ in os.walk(batch_dir):
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            
            # Sort directories by generation number
            dirs.sort(key=lambda x: int(x.split('_')[1]), reverse=True)
            
            if len(dirs) < 2:
                raise ValueError("Not enough generations to find a penultimate directory.")
            
            return os.path.join(root, dirs[1])  # Skip latest generation
        
        raise ValueError("No valid generations found.")

    def get_x_generation(batch_dir,x):
        for root, dirs, _ in os.walk(batch_dir):
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            
            # Sort directories by generation number
            #dirs.sort(key=lambda x: int(x.split('_')[1]), reverse=True)
            dirs.sort(key=lambda x: int(x.split('_')[1]), reverse=False)
            
            if len(dirs) < 2:
                raise ValueError("Not enough generations to find a penultimate directory.")
            
            #return os.path.join(root, dirs[1])  # Skip latest generation
            return os.path.join(root, dirs[x])  # Skip latest generation
        
        raise ValueError("No valid generations found.")

    def get_fitness_stats(batch_dir):
        for root, _, files in os.walk(batch_dir):
            for file in files:
                if file.endswith('_stats.csv'):
                    csv_path = os.path.join(root, file)
                    df = pd.read_csv(csv_path, delimiter=' ', skipinitialspace=True)
                    
                    if df.empty:
                        raise ValueError("CSV file is empty or improperly formatted.")
                    
                    min_fitness, max_fitness = df.iloc[-1, 2], df.iloc[-1, 3]
                    return min_fitness, max_fitness
        
        raise FileNotFoundError("No stats CSV file found in batch directory.")

    def collect_sorted_data_paths(penultimate_dir):
        data_paths = {}
        
        for root, _, files in os.walk(penultimate_dir):
            for file in files:
                if file.endswith('_data.pkl'):
                    fitness_path = os.path.join(root, file.replace('_data.pkl', '_fitness.json'))
                    
                    try:
                        with open(fitness_path, 'r') as f:
                            fitness = json.load(f)
                        
                        fit = fitness.get('average_fitness')
                        if fit is not None:
                            data_paths[fit] = {
                                'data_path': os.path.join(root, file),
                                'fitness_path': fitness_path,
                            }
                    except Exception as e:
                        print(f"Skipping {fitness_path} due to error: {e}")
                        continue
        
        return dict(sorted(data_paths.items()))

    def process_simulation_parallel(path, reference_data_path, feature_path):
        sim_data_path = path['data_path']
        
        try:
            sim.clearAll()
        except Exception:
            pass
        
        print(f"Processing: {sim_data_path}")
        
        #slide_paths = []        
        try:
            #feature_path = os.path.join(os.path.dirname(sim_data_path), 'feature_module.py')
            feature_module = import_module_from_path(feature_path)
            fitnessFuncArgs = feature_module.fitnessFuncArgs
            
            comparison_summary_slide_paths = process_simulation(
                sim_data_path, 
                reference_data_path,
                DEBUG_MODE=False,
                conv_params=conv_params,
                mega_params=mega_params,
                fitnessFuncArgs=fitnessFuncArgs,
            )
            #slide_paths.extend(comparison_summary_slide_paths)
            return comparison_summary_slide_paths
        except Exception as e:
            print(f"Error processing {sim_data_path}: {e}")
            return None
            
        #return slide_paths
        #return comparison_summary_slide_paths
            
    def process_top_simulations(data_paths, reference_data_path, feature_path, top_n=25):
        top_data_paths = list(data_paths.values())[:top_n]
        
        with multiprocessing.Pool(processes=min(top_n, multiprocessing.cpu_count())) as pool:
            results = pool.starmap(process_simulation_parallel, [(path, reference_data_path, feature_path) for path in top_data_paths])
            
        gen_pdfs = []
        for result in results:
            if result:
                gen_pdfs.extend(result)
        
        # remove any .png files from gen_pdfs
        gen_pdfs = [pdf for pdf in gen_pdfs if pdf.endswith('.pdf')]
                
        print(f"Processed top {top_n} simulations.")
        
        return gen_pdfs

    # Main execution
    pdf_path_dict = {}
    try:
        penultimate_dir = get_penultimate_generation(batch_dir)
        gen = int(penultimate_dir.split('gen_')[1].split('/')[0]) #get gen # from path. look for gen_, get the number afterwards
        min_fitness, max_fitness = get_fitness_stats(batch_dir)
        for i in range(0, gen):
            gen_dir = get_x_generation(batch_dir,i)
            data_paths = collect_sorted_data_paths(gen_dir)
            gen_pdfs = process_top_simulations(data_paths, reference_data_path, feature_path, top_n=25)
            pdf_path_dict[i] = gen_pdfs
            
            #break
    except Exception as e:
        print(f"Execution failed: {e}")

    import os
    import glob
    from PyPDF2 import PdfReader, PdfWriter

    def compile_pdfs(output_dir, pdf_path_dict):
        """Compiles PDF files from different generations into single PDFs per generation."""
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for gen, pdf_files in pdf_path_dict.items():
            output_pdf = os.path.join(output_dir, f'compiled_pdfs_gen_{gen}.pdf')
            pdf_writer = PdfWriter()

            for pdf_file in pdf_files:
                try:
                    with open(pdf_file, 'rb') as f:
                        pdf_reader = PdfReader(f)
                        for page in pdf_reader.pages:  # Corrected method usage
                            pdf_writer.add_page(page)
                except Exception as e:
                    print(f"Skipping {pdf_file} due to error: {e}")
                    continue

            with open(output_pdf, 'wb') as out_f:
                pdf_writer.write(out_f)

            print(f"Compiled PDF saved: {output_pdf}")
    # Example usage
    output_dir = batch_dir.replace('batch_runs', 'batch_analysis')
    compile_pdfs(output_dir, pdf_path_dict)

v1 = False # turned off for now
if v1: # v1 ============================================================================================
    # get penultimate gen dir

    for root, dirs, files in os.walk(batch_dir):
            #dirs.sort(reverse=True)
            # sort by number in dir name preceeded by 'gen_'
            # skip pycache
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            print(dirs)
            dirs.sort(key=lambda x: int(x.split('_')[1]), reverse=True)
                    
            
            ultimate_dir = os.path.join(root, dirs[0])
            penultimate_dir = os.path.join(root, dirs[1])
            break
    print(ultimate_dir)
    print(penultimate_dir)

    # load csv, get lowest and highest fitness from 3rd and 4th columns respectively from last row
    import pandas as pd
    for root, dirs, files in os.walk(batch_dir):
        for file in files:
            if file.endswith('_stats.csv'):
                csv_path = os.path.join(root, file)
                df = pd.read_csv(csv_path, delimiter=' ', skipinitialspace=True)
                print(df.head())
                print("DataFrame Shape:", df.shape)

                
                # print(df.iloc[:,:])
                # print(df.iloc[0,0])
                
                min_fitness = df.iloc[-1, 2]
                max_fitness = df.iloc[-1, 3]
                print('min fitness: ', min_fitness)
                print('max fitness: ', max_fitness)
                break
            
    # collect a list of all sim data paths, fitness data paths. Sort by fitness.
    data_paths = {}
    for root, dirs, files in os.walk(penultimate_dir):
            # skip pycache
            #print(files)
            
            for file in files:
                if file.endswith('_data.pkl'):
                    try:                    
                        data_path = os.path.join(root, file)
                        fitness_path = os.path.join(root, file.replace('_data.pkl', '_fitness.json'))
                        import json
                        with open(fitness_path, 'r') as f:
                            fitness = json.load(f)
                        fit = fitness['average_fitness']
                        #print(fit)
                        data_paths[fit] = {
                            'data_path': data_path,
                            'fitness_path': fitness_path,
                        }
                        #print(data_paths[fit])
                    except Exception as e:                    
                        #print(e)
                        continue
                    
            # sort by numeric values of keys
            data_paths = dict(sorted(data_paths.items()))
            # print(data_paths)
            # import sys
            # sys.exit()
            
    # collect the top 10 data_paths
    top_10_data_paths = {}
    for i, (k, v) in enumerate(data_paths.items()):
        if i < 10:
            top_10_data_paths[k] = v
        else:
            break
        
    print(top_10_data_paths)
    # import sys
    # sys.exit()

    # walk through penultimate dir and plot each sim
    #for root, dirs, files in os.walk(penultimate_dir):
            # skip pycache
            #print(files)
    from netpyne import sim
    for path in top_10_data_paths.values():
        # data_path = path['data_path']
        # file = data_path
        file = path['data_path']
        
        # if needed clear sim before runnning process_simulation
        try:
            sim.clearAll()
        except:
            pass
            
            #for file in files:
        if file.endswith('_data.pkl'):
            #data_path = os.path.join(root, file)
            #print(data_path)
            print(file)
            # plot sim
            from RBS_network_models.sim_analysis import process_simulation
            from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params
            from RBS_network_models.utils.cfg_helper import import_module_from_path
            feature_module = import_module_from_path(feature_path)
            fitnessFuncArgs = feature_module.fitnessFuncArgs
            #sim_data_path = data_path
            sim_data_path = file
            #reference_data_path = os.path.join(ultimate_dir, 'best_data.pkl')
            try:
                process_simulation(
                sim_data_path, 
                reference_data_path,
                DEBUG_MODE=False,
                conv_params = conv_params,
                mega_params = mega_params,
                fitnessFuncArgs = fitnessFuncArgs,
                )        
                #break
            except Exception as e:
                print(e)
                continue

