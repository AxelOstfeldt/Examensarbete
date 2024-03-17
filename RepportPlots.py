import matplotlib.pyplot as plt
import numpy as np
import math

PlotNr = 21

#
#PlotNr 1. Bar plot for RiceCoding original input

#Shorten plots
#PlotNr 11. Bar plot for Shorten best k and m values
#PlotNr 12. Bar plot for times using shorten with rice and golomb codes
#PlotNr 13. Bar plot for compression rate over an array of mics using Shorten and rice codes (modifed k-value) (with meta data)


#Lpc plots
#PlotNr 21. Bar plot for LPC best k and m values
#PlotNr 22. Bar plot for times using LPC with rice and golomb codes
#PlotNr 23. Bar plot for compression rate over an array of mics using LPC and rice codes (modifed k-value) (with meta data)



if PlotNr == 1:
    fig, ax = plt.subplots()

    title = ['1 k Hz tone', 'Drone sound', 'Static noise', 'Silence (Mic 20)', 'Large magnitude (Mic 217)']
    counts = [0.739, 0.809, 0.808, 0.125, 0.784]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise', 'Silence (Mic 20)', 'Large magnitude (Mic 217)']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple']
    for i in range(len(counts)):
        ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])

    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.legend(fontsize = 20)
    plt.ylim(0,1)
    
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=17)
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
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)
    
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
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left",fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)


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
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left",fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)


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
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left",fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)

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

    
    fig, ax = plt.subplots(layout='constrained')
    
    for attribute, measurement in cr.items():

        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    #ax.set_ylim(0, 0.4)
    plt.yticks(fontsize=20)
    
    plt.show()

    #Golomb codes

    cr = {
        '1 k Hz tone': (0.958, 0.156, 0.163, 0.217),
        'Drone sound': (8.827, 7.530, 10.278, 22.130),
        'Static noise': (12.000, 18.245, 28.046, 62.389),
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
        ax.bar_label(rects, fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    #ax.set_ylim(0, 0.4)
    plt.yticks(fontsize=20)
    
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
        ax.bar_label(rects, fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)
    
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
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)
    
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
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left",fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)


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
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left",fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)


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
        ax.bar_label(rects, labels =[i for i in k_values[multiplier] ], fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average compression rate', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left",fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)

    plt.show()


if PlotNr == 22:

    print("Redo golom and rice for LPC 1 and 5")

    #Add some text for labels, title and custom x-axis tick labels, etc.

    Order = ("Order 1", "Order 2", "Order 3", "Order 4", "Order 5")

    #Rice Codes

    cr = {
        '1 k Hz tone': (0.168, 0.088, 0.115, 0.096, 0.120),
        'Drone sound': (0.235, 0.243, 0.249, 0.272, 0.281),
        'Static noise': (0.184, 0.220, 0.129, 0.144, 0.1423),
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
        ax.bar_label(rects, fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    #ax.set_ylim(0, 0.4)
    plt.yticks(fontsize=20)
    
    plt.show()

    #Golomb codes

    cr = {
        '1 k Hz tone': (0.165, 0.200, 0.162, 0.183, 0.139),
        'Drone sound': (5.936, 4.844, 4.993, 4.496, 5.009),
        'Static noise': (11.230, 8.445, 9.115, 7.898, 6.041),
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
        ax.bar_label(rects, fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    #ax.set_ylim(0, 0.4)
    plt.yticks(fontsize=20)
    
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
        ax.bar_label(rects, fontsize = 15)
        
        multiplier += 1
        

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average time [s]', fontsize=25)
    ax.set_xticks(x + width, Order, fontsize=20)
    ax.legend(loc="upper left", fontsize = 20)
    ax.set_ylim(0, 1)
    plt.yticks(fontsize=20)
    
    plt.show()
