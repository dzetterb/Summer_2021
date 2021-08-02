def yieldvrxnmult(filenames, figurename = 'None'):
    import plot_rxn_ratio as prr
    import numpy as np
    import matplotlib.pyplot as plt
    
    plt.figure(1)
    color_list = ['b', 'r', 'g', 'y', 'c', 'k']
    
    for counter in np.arange(len(filenames)):
        data = np.genfromtxt(filenames[counter], dtype = str)
        names = data[:, 0]
        rxn_list = []
        for row in names:
            rxn_list.append(prr.find_rxn_rate(row))
        
        mass_str = data[:, 1]
        
        mass = mass_str.astype('float64')
        
        plt.plot(rxn_list, mass, c = color_list[counter], marker = 'd', linestyle = '--')
        
    
    labels_list = ["high neutrino trajectory", "low neutrino trajectory"]
    plt.legend(loc = 'upper right', fontsize = 20, labels = labels_list)
    plt.xlabel('Reaction Rate Multipler', fontsize = 20)
    plt.ylabel('Mass Yield of $^{10}$Be', fontsize = 20)
    plt.xscale('log')
    plt.grid(True)
    
    
    #Save or show figure
    if figurename == 'None':
        plt.show()
        print("Plot shown.")
    else:
        plt.savefig(figurename, bbox_inches = 'tight')
        print("Plot saved.")
        