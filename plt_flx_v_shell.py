def match_flx_to_mass_shell(directory_files, properties_file, output_file, flx_index_list, rxn_name_list):
        '''This will be a function that goes through every shell file and writes the flx data for a specific reaction into a new file
           It will be written very similar to match_abundance_to_mass_shell
           directory_files = list of ts files to run through
           properties_file = file with mass coordinate properties
           output_file = file to be written to
           flx_index_list = list of flux indicies to run through (find indecies through code in Jupyter notebook, and then confirm in vim
           rxn_name_list = list of names of reaction fluxes
        '''
        
        
        import numpy as np
        import read_ts_file as rtf
        import glob as g
        
        #Open the output file
        f = open(output_file, 'w')
        
        #Initialize a counter to make the header print only once.
        counter = 1
        
        #Create a list of all desired files in the given directory.
        number_of_files = len(directory_files)
        print(number_of_files)
        
        if number_of_files > 1:
                files = g.glob(directory_files)
        
        else: 
                files = directory_files
        
        #Read in Properties File
        col_headers = ["Shell_Number", "Radius(cm)", "Mass_coord(M_sun)", "dm(g)"]
        properties = np.genfromtxt(properties_file, names = col_headers)

        for datafile in files:
                #i wont use the find file type code because i can just do ts_* to make it run faster
                print(datafile)
                #Add mass shell data from Properties File 
                print ("%s" % counter)
                mass_shell = datafile[-3] + datafile[-2] + datafile[-1]
                mass_shell_int = int(mass_shell)
        
                mass_shell_properties = properties[mass_shell_int - 2]
        
                #read in ts file
                zz, aa, xmf, time, temperature, density, timestep, edot, flx_end, flx = rtf.read_ts_file(datafile)
        
                #Set certain parameters based on the size of the data.
                timesteps_total = np.shape(time)
                
                #Write header with column headers and species names as a first line.
                if counter == 1:
                        # set size of padding based on first filename
                        padding = len(datafile) + 5
                        
                        line = "Shell_Number" + "   " + "Radius(cm)" + "   " + 
                               "Mass_coord(M_sun)" + "   " + "dm(g)" + "   " + 
                               "filename" + "   " + "total_flux_" 
                        
                        #pass in rxn_list to rxn_namer
                        for counter in rxn_name_list:
                                line = line + counter
                        
                        f.write(line + '\n')
                        
                #total flux of reaction
                flx_write_list = []
                for counter in flx_index_list:
                        flx_write = np.sum(flx[:, counter])
                        flx_write_list.append(flx_write)
                        
                
                #Create 'line' variable with mass shell properties for each file
                #idk, but i might need to declare variable outside of the scope of each for loop
                for item in mass_shell_properties:
                        line = str("%.5e" % item).ljust(14)
                padding = len(datafile) + 3
                line = datafile.ljust(padding)
                        
                #add integrated flux to 'line' variable
                for counter in flx_write_list:
                        line = line + str("%.5e" % counter).ljust(14)
                        
                #write line to file
                f.writelines(line + "\n")
                        
                counter +=1
        
        f.close()
        #did some revamping of the code, will test it when Cori is back up


def plot_flxvshell (inputfiles, listoflabels, xmin_max, ymin_max, figurename = 'None'):
        '''This will be a function that takes the output of match_flx_to_mass_shell and plots it against shell
           inputfiles = list of files with fluxes to be plotted, files are output of match_flx_to_mass_shell
           listoflabels = list of reaction flux names (list of lists)
           figurename = name of figure to be saved as pdf
           xmin_max = min and max of x axis of figure (will find appropriate default later)
           ymin_max = min and max of y axis of figure (will find appropriate default later)
        '''
         
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        
        #create figures
        plt.figure(1)
        ax1 = plt.subplot(1, 1, 1)
        
        
        for counter1 in np.arange(len(inputfiles)):
                #read in data
                data = pd.read_csv(inputfiles(counter1), engine = 'python', skipfooter = 1, sep = '\s+')
                
                #order data in dataframe
                ordered_data = data.sort_values(by = 'Shell_Number')
                print(inputfiles(counter1) + " file read")
                
                for counter2 in np.arange(len(listoflabels[:,counter1])):
                        ordered_data.plot(x = "Mass_coord(M_sun)", 
                                          y = "total_flux_" + listoflabels[counter2, counter1],
                                          kind = 'line', 
                                          ax = ax1,
                                          logy = True,
                                          grid = True)
                
                print(inputfiles(counter1) + " plotted")
        
        plt.xlabel(r'Mass_coord ($M_\odot\$)')
        plt.ylabel(r'Total Flux')
        plt.title(r'Flux vs Mass Coordinate')
        ax1.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        
        if figurename == 'None':
            plt.show()
            print("Plot shown.")
        else:
            plt.savefig(figurename, bbox_inches = "tight")
            print("Plot saved.")
            
        