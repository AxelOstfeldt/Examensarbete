import matplotlib.pyplot as plt
import numpy as np
import math

PlotNr = 61

#
#PlotNr 1. Bar plot for RiceCoding original input

#Shorten plots
#PlotNr 11. Bar plot for Shorten best k and m values, grouped by sound
#PlotNr 12. Bar plot for times using shorten with rice and golomb codes
#PlotNr 13. Bar plot for compression rate over an array of mics using Shorten and rice codes (modifed k-value) (with meta data)
#PlotNr 14. Bar plot comparing rice and golomb but groupen by order not sound

#Lpc plots
#PlotNr 21. Bar plot for LPC best k and m values, grouped by sound
#PlotNr 22. Bar plot for times using LPC with rice and golomb codes
#PlotNr 23. Bar plot for compression rate over an array of mics using LPC and rice codes (modifed k-value) (with meta data)
#PlotNr 24. Bar plot for LPC b or m, grouped by order


#FLAC plots
#PlotNr 31. Bar plot for compression rate for full array of mics using FLAC (max order lpc 32)
#PlotNr 32. Timing for recreate original values using FLAC (max order lpc 32)

#Adjacent plots
#PlotNr 41. Bar plot for Adjacent best k and m values, grouped by sound
#PlotNr 42. Bar plot for Adjacent time to recreate values
#PlotNr 43. Test adjacent compression rate for all samples of an array (modifed k-values)

#FLAC modified plots
#PlotNr 51. Bar plot for time to recreate values using FLAC modified
#PlotNr 52. Bar plot for compression rate using FLAC modified

#DoubleCompression plots
#PlotNr 61. Bar plot for time to recreate vales using DoubleCompression
#PlotNr 62. Bar plot for compression rate using DoubleCompression


if PlotNr == 1:
    fig, ax = plt.subplots(layout='constrained')

    title = ['1 k Hz tone', 'Drone sound', 'Static noise', 'Silence', 'Loud']
    counts = [0.739, 0.809, 0.808, 0.125, 0.784]
    bar_labels = ['Mic#79', '_Mic#79', '_Mic#79', 'Mic#20', 'Mic#217']
    bar_colors = ['tab:red', 'tab:red', 'tab:red', 'tab:blue', 'tab:green']
    for i in range(len(counts)):
        rects = ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])
        ax.bar_label(rects, fontsize = 45)


    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.legend(loc = 'upper left', fontsize = 40, ncol = 3)
    plt.ylim(0,1.1)
    
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.show()


if PlotNr == 11:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 0", "Order 1", "Order 2", "Order 3")

    #1 k Hz tone

    cr = {
        'Rice code using theortical ideal k-value': (0.745, 0.580, 0.592, 0.619),
        'Rice code using best k-value': (0.692, 0.572, 0.558, 0.592),
        'Golomb code using best m-value': (0.691, 0.573, 0.557, 0.592),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 12","k = 10","k = 9","k = 10"],["k = 14","k = 11","k = 10","k = 11"],["m = 13957","m = 1954","m = 1216","m = 2207"]]

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


    #Silent mic

    cr = {
        'Rice code using theortical ideal k-value': (0.125, 0.125, 0.125, 0.125),
        'Rice code using best k-value': (0.125, 0.125, 0.125, 0.125),
        'Golomb code using best m-value': (0.125, 0.125, 0.125, 0.125),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 1","k = 1","k = 1","k = 1"],["k = 1","k = 1","k = 1","k = 1"],["m = 1","m = 1","m = 1","m = 1"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()

    #Drone sound

    cr = {
        'Rice code using theortical ideal k-value': (0.823, 0.824, 0.806, 0.863),
        'Rice code using best k-value': (0.775, 0.776, 0.790, 0.817),
        'Golomb code using best m-value': (0.774, 0.774, 0.787, 0.814),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 14","k = 14","k = 15","k = 15"],["k = 16","k = 16","k = 16","k = 17"],["m = 47059","m = 48331","m = 65461","m = 93953"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()


    #Static noise

    cr = {
        'Rice code using theortical ideal k-value': (0.804, 0.827, 0.887, 0.885),
        'Rice code using best k-value': (0.789, 0.800, 0.823, 0.850),
        'Golomb code using best m-value': (0.788, 0.799, 0.821, 0.848),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 15","k = 15","k = 15","k = 16"],["k = 16","k = 16","k = 17","k = 17"],["m = 65085","m = 68518","m = 118484","m = 164989"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)

    plt.show()


if PlotNr == 12:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 0", "Order 1", "Order 2", "Order 3")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.163, 0.086, 0.100, 0.115),
        'Drone sound': (0.231, 0.231, 0.241, 0.261),
        'Static noise': (0.229, 0.207, 0.281, 0.276),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    barTopText = [["0.163s", "0.086s", "0.100s", "0.115s"],["0.231s", "0.231s", "0.241s", "0.261s"],["0.229s", "0.207s", "0.281s", "0.276s"]]
    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 22)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 30, ncol = 3)
    ax.set_ylim(0, 0.35)
    plt.yticks(fontsize=35)
    
    plt.show()

    #Golomb codes

    cr = {
        '1 k Hz tone': (0.958, 0.156, 0.163, 0.217),
        'Drone sound': (8.827, 7.530, 10.278, 22.130),
        'Static noise': (12.000, 18.245, 28.046, 62.389),
    }

    barTopText = [["0.958s","0.156s","0.163s", "0.217s"],["8.827s","7.530s","10.278s", "22.130s"],["12.000s","18.245s","28.046s","62.389s"]]

    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ],fontsize = 22)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 30, ncol = 3)
    #ax.set_ylim(0, 0.35)
    plt.yticks(fontsize=35)
    
    plt.show()


if PlotNr == 13:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 0", "Order 1", "Order 2", "Order 3")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.671, 0.557, 0.553, 0.590),
        'Drone sound': (0.772, 0.767, 0.780, 0.808),
        'Static noise': (0.787, 0.795, 0.816, 0.842),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fontsize = 25)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 35, ncol = 3)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


if PlotNr == 14:

    

    SoundFiles = ("1 k Hz tone", "Silent (mic 20)", "Drone sound", "Static noise")

    
    
    

    
    #Add some text for labels, title and custom x-axis tick labels, etc.
    #Order 0
    cr = {
        'Rice code using theortical ideal k-value': (0.745, 0.125,0.823,0.804),
        'Rice code using best k-value': (0.692, 0.125,0.775,0.789),
        'Golomb code using best m-value': (0.691, 0.125,0.774,0.788),
    }

    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 12","k = 1","k = 14","k = 15"],["k = 14","k = 1","k = 16","k = 16"],["m = 13957","m = 1","m = 47059","m = 65085"]]
    
    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


    #Order 1

    cr = {
        'Rice code using theortical ideal k-value': (0.580, 0.125,0.824,0.827),
        'Rice code using best k-value': (0.572, 0.125,0.776,0.800),
        'Golomb code using best m-value': (0.573, 0.125,0.774,0.799),
    }



    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 10","k = 1","k = 14","k = 15"],["k = 11","k = 1","k = 16","k = 16"],["m = 1954","m = 1","m = 48331","m = 68518"]]
    


    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()

    #Order 2

    cr = {
        'Rice code using theortical ideal k-value': (0.592, 0.125,0.806,0.887),
        'Rice code using best k-value': (0.558, 0.125,0.790,0.823),
        'Golomb code using best m-value': (0.557, 0.125,0.787,0.821),
    }
   



    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 9","k = 1","k = 15","k = 15"],["k = 10","k = 1","k = 16","k = 17"],["m = 1216","m = 1","m = 65461","m = 118484"]]
    


    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()


    #Order 3
    cr = {
        'Rice code using theortical ideal k-value': (0.619, 0.125,0.863,0.885),
        'Rice code using best k-value': (0.592, 0.125,0.817,0.850),
        'Golomb code using best m-value': (0.592, 0.125,0.814,0.848),
    }



    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 10","k = 1","k = 15","k = 16"],["k = 11","k = 1","k = 17","k = 17"],["m = 2207","m = 1","m = 93953","m = 164989"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)

    plt.show()


if PlotNr == 21:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 1", "Order 2", "Order 3", "Order 4", "Order 5")

    #1 k Hz tone

    cr = {
        'Rice code using theortical ideal k-value': (0.580, 0.582, 0.560, 0.575, 0.575),
        'Rice code using best k-value': (0.573, 0.552, 0.542, 0.526, 0.526),
        'Golomb code using best m-value': (0.573, 0.552, 0.542, 0.525, 0.525),
    }




    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 10","k = 9","k = 9","k = 8", "k = 8"],["k = 11","k = 10","k = 10","k = 10", "k = 10"],["m = 1943","m = 1125","m = 1030","m = 781","m = 748"]]

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


    #Silent mic



    cr = {
        'Rice code using theortical ideal k-value': (0.125, 0.125, 0.125, 0.125, 0.125),
        'Rice code using best k-value': (0.125, 0.125, 0.125, 0.125, 0.125),
        'Golomb code using best m-value': (0.125, 0.125, 0.125, 0.125, 0.125),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 1","k = 1","k = 1","k = 1","k = 1"],["k = 1","k = 1","k = 1","k = 1","k = 1"],["m = 1","m = 1","m = 1","m = 1", "m = 1"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()

    #Drone sound

    cr = {
        'Rice code using theortical ideal k-value': (0.799, 0.778, 0.773, 0.771, 0.755),
        'Rice code using best k-value': (0.765, 0.754, 0.752, 0.751, 0.743),
        'Golomb code using best m-value': (0.762, 0.753, 0.750, 0.749, 0.742),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 14","k = 14","k = 14","k = 14", "k = 14"],["k = 15","k = 15","k = 15","k = 15", "k = 15"],["m = 38898","m = 32786","m = 32788","m = 32725","m = 32277"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()


    #Static noise

    cr = {
        'Rice code using theortical ideal k-value': (0.797, 0.830, 0.827, 0.805, 0.799),
        'Rice code using best k-value': (0.785, 0.777, 0.777, 0.768, 0.756),
        'Golomb code using best m-value': (0.785, 0.777, 0.775, 0.767, 0.757),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 15","k = 14","k = 14","k = 14", "k = 14"],["k = 16","k = 16","k = 16","k = 15", "k = 15"],["m = 64612","m = 53542","m = 51011","m = 43993","m = 34679"]]



    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)

    plt.show()


if PlotNr == 22:



    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 1", "Order 2", "Order 3", "Order 4", "Order 5")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.086, 0.088, 0.115, 0.096, 0.120),
        'Drone sound': (0.235, 0.243, 0.249, 0.272, 0.281),
        'Static noise': (0.184, 0.220, 0.129, 0.144, 0.142),
    }

    barTopText = [["0.086s","0.088s","0.115s","0.096s","0.120s"],["0.235s","0.243s","0.249s","0.272s","0.281s"],["0.184s","0.220s","0.129s","0.144s","0.142s"]]

    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 21)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 30, ncol = 3)
    ax.set_ylim(0, 0.35)
    plt.yticks(fontsize=35)
    
    plt.show()

    #Golomb codes

    cr = {
        '1 k Hz tone': (0.165, 0.200, 0.162, 0.183, 0.151),
        'Drone sound': (5.936, 4.844, 4.993, 4.496, 5.009),
        'Static noise': (11.230, 8.445, 9.115, 7.898, 6.041),
    }

    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    barTopText = [["0.165s","0.200s","0.162s","0.183s","0.151s"],["5.936s","4.844s","4.993s","4.496s","5.009s"],["11.230s","8.445s","9.115s","7.898s","6.041s"]]
    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 21)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 30, ncol = 3)
    ax.set_ylim(0, 13.5)
    plt.yticks(fontsize=35)
    
    plt.show()


if PlotNr == 23:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 1", "Order 2", "Order 3", "Order 4", "Order 5")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.558, 0.547, 0.542, 0.528, 0.525),
        'Drone sound': (0.758, 0.754, 0.754, 0.752, 0.751),
        'Static noise': (0.785, 0.778, 0.779, 0.769, 0.767),
    }


    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fontsize = 21)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 35, ncol = 3)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


if PlotNr == 24:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    SoundFiles = ("1 k Hz tone", "Silent (mic 20)", "Drone sound", "Static noise")


    #Order 1
    cr = {
        'Rice code using theortical ideal k-value': (0.580, 0.125,0.799,0.797),
        'Rice code using best k-value': (0.573, 0.125,0.765,0.785),
        'Golomb code using best m-value': (0.573, 0.125,0.762,0.785),
    }

    k_values = [["k = 10","k = 1","k = 14","k = 15"],["k = 11","k = 1","k = 15","k = 16"],["m = 1943","m = 1","m = 38898","m = 64612"]]
    

    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


    #Order 2
    cr = {
        'Rice code using theortical ideal k-value': (0.582, 0.125,0.778,0.830),
        'Rice code using best k-value': (0.552, 0.125,0.754,0.777),
        'Golomb code using best m-value': (0.552, 0.125,0.753,0.777),
    }



    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 9","k = 1","k = 14","k = 14"],["k = 10","k = 1","k = 15","k = 16"],["m = 1125","m = 1","m = 32786","m = 53542"]]
    


    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()

    #Order 3
    cr = {
        'Rice code using theortical ideal k-value': (0.560, 0.125,0.773,0.827),
        'Rice code using best k-value': (0.542, 0.125,0.752,0.777),
        'Golomb code using best m-value': (0.542, 0.125,0.750,0.775),
    }



    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 9","k = 1","k = 14","k = 14"],["k = 10","k = 1","k = 15","k = 16"],["m = 1030","m = 1","m = 32788","m = 51011"]]
    


    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)


    plt.show()


    #Order 4
    cr = {
        'Rice code using theortical ideal k-value': (0.575, 0.125,0.771,0.805),
        'Rice code using best k-value': (0.526, 0.125,0.751,0.768),
        'Golomb code using best m-value': (0.525, 0.125,0.749,0.767),
    }



    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 8","k = 1","k = 14","k = 14"],["k = 10","k = 1","k = 15","k = 15"],["m = 781","m = 1","m = 32725","m = 43993"]]
    


    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)

    plt.show()


    #Order 5
    cr = {
        'Rice code using theortical ideal k-value': (0.575, 0.125,0.755,0.799),
        'Rice code using best k-value': (0.526, 0.125,0.743,0.756),
        'Golomb code using best m-value': (0.525, 0.125,0.742,0.757),
    }

    x = np.arange(len(SoundFiles))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 8","k = 1","k = 14","k = 14"],["k = 10","k = 1","k = 15","k = 15"],["m = 748","m = 1","m = 32277","m = 34679"]]


    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 13)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, SoundFiles, fontsize=35)
    ax.legend(loc="upper left", fontsize = 22)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)

    plt.show()


if PlotNr == 31:
    fig, ax = plt.subplots(layout = 'constrained')

    title = ['1 k Hz tone', 'Drone sound', 'Static noise']
    counts = [0.564, 0.781, 0.800]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    for i in range(len(counts)):
        rects = ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])
        ax.bar_label(rects, fontsize = 45)


    ax.set_ylabel('Average compression rate', fontsize=45)
    #ax.legend(loc="upper left", fontsize = 35, ncol = 3)
    plt.ylim(0,1)
    
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.show()


if PlotNr == 32:
    fig, ax = plt.subplots(layout = 'constrained')

    title = ['1 k Hz tone', 'Drone sound', 'Static noise']
    counts = [0.198, 0.265, 0.332]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    barTopText = [["0.198s"],["0.265s"],["0.332s"]]
    for i in range(len(counts)):
        rects = ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])
        ax.bar_label(rects, labels = [j for j in barTopText[i]], fontsize = 45)


    ax.set_ylabel('Average time [s]', fontsize=45)
    #ax.legend(loc="upper left", fontsize = 35, ncol = 3)
    plt.ylim(0,0.4)
    
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.show()


if PlotNr == 41:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("1 k Hz tone", "Drone sound", "Static noise")

    #1 k Hz tone

    cr = {
        'Rice code using theortical ideal k-value': (0.594, 0.759, 0.804),
        'Rice code using best k-value': (0.580, 0.746,  0.768),
        'Golomb code using best m-value': (0.57808, 0.74402, 0.766781),
    }




    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc
    k_values = [["k = 10","k = 14","k = 14"],["k = 11","k = 15","k = 15"],["m = 2046","m = 32755","m = 44514"]]

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 22)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 30)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=35)
    
    plt.show()


if PlotNr == 42:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("1 k Hz tone", "Drone sound", "Static noise")

    #1 k Hz tone

    cr = {
        'Using Rice codes': (0.111, 0.163, 0.179),
        'Using Golomb codes': (0.101, 0.101,  0.146)
    }

    barTopText = [["0.111s","0.163s","0.179s"],["0.101s","0.101s","0.146s"]]


    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
 
    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ],fontsize = 35)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=45)
    ax.set_xticks(x + width, Order, fontsize=35)
    ax.legend(loc="upper left", fontsize = 35)
    ax.set_ylim(0, 0.2)
    plt.yticks(fontsize=35)
    
    plt.show()


if PlotNr == 43:
    fig, ax = plt.subplots(layout='constrained')

    title = ['1 k Hz tone', 'Drone sound', 'Static noise']
    counts = [0.583, 0.749, 0.771]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    for i in range(len(counts)):
        rects = ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])
        ax.bar_label(rects, fontsize = 45)

    ax.set_ylabel('Average compression rate', fontsize=45)
    #ax.legend(loc = 'upper left', fontsize = 35, ncol = 3)
    plt.ylim(0,1.1)
    
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.show()


if PlotNr == 51:

    fig, ax = plt.subplots(layout='constrained')

    title = ['1 k Hz tone', 'Drone sound', 'Static noise']
    counts = [0.106, 0.146, 0.096]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    barTopText = [["0.106s"],["0.146s"],["0.096s"]]
    for i in range(len(counts)):
        rects = ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])
        ax.bar_label(rects, labels =[j for j in barTopText[i] ], fontsize = 45)

    ax.set_ylabel('Average time [s]', fontsize=45)
    #ax.legend(loc="upper left", fontsize = 20)
    plt.ylim(0,0.2)
    
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.show()


if PlotNr == 52:
    fig, ax = plt.subplots(layout='constrained')

    title = ['1 k Hz tone', 'Drone sound', 'Static noise']
    counts = [0.529, 0.709, 0.730]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    for i in range(len(counts)):
        rects = ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])
        ax.bar_label(rects, fontsize = 45)

    ax.set_ylabel('Average compression rate', fontsize=45)
    #ax.legend(loc="upper left", fontsize = 20)
    plt.ylim(0,1)
    
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.show()


if PlotNr == 61:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 0", "Order 1", "Order 2", "Order 3", "Order 4")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.085, 0.115, 0.257, 0.127, 0.249),
        'Drone sound': (0.178,  0.300, 0.359, 0.321, 0.332),
        'Static noise': (0.214, 0.305, 0.294, 0.329, 0.319),
    }

    barTopText = [["0.085s", "0.115s", "0.257s", "0.127s", "0.249s"],["0.178s", "0.300s", "0.359s", "0.321s", "0.332s"],["0.214s", "0.305s", "0.294s", "0.329s", "0.319s"]]

    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 21)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=70)
    ax.set_xticks(x + width, Order, fontsize=50)
    ax.legend(loc="upper left", fontsize = 33)
    #ax.set_ylim(0, 0.4)
    plt.yticks(fontsize=30)
    
    plt.show()


if PlotNr == 62:
    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 0", "Order 1", "Order 2", "Order 3", "Order 4")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.550, 0.521, 0.554, 0.589, 0.623),
        'Drone sound': (0.713, 0.725, 0.745, 0.772, 0.801),
        'Static noise': (0.732, 0.753, 0.775, 0.804, 0.832),
    }



    x = np.arange(len(Order))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    
    #First array for theoretical ideal, second for rice with best k, last for Golomb best m.
    #First value in each array for order 0, second for order 1, etc

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fontsize = 21)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=55)
    ax.set_xticks(x + width, Order, fontsize=50)
    ax.legend(loc="upper left", fontsize = 33)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=30)
    
    plt.show()
