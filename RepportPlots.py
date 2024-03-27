import matplotlib.pyplot as plt
import numpy as np
import math

PlotNr = 44

#
#PlotNr 1. Bar plot for RiceCoding original input

#Shorten plots
#PlotNr 11. Bar plot for Shorten best k and m values, grouped by sound
#PlotNr 12. Bar plot for times using shorten with rice and golomb codes
#PlotNr 13. Bar plot for compression rate over an array of mics using Shorten and rice codes (modifed k-value) (with meta data, 20 bits for decimals)
#PlotNr 14. Bar plot comparing rice and golomb but groupen by order not sound
#PlotNr 15. Scatter plot for different m and k values using Shorten, save in test 13

#Lpc plots
#PlotNr 21. Bar plot for LPC best k and m values, grouped by sound
#PlotNr 22. Bar plot for times using LPC with rice and golomb codes
#PlotNr 23. Bar plot for compression rate over an array of mics using LPC and rice codes (modifed k-value) (with meta data)
#PlotNr 24. Bar plot for LPC b or m, grouped by order
#PlotNr 25. Scatter plot for different m and k values using LPC, save in test 24


#FLAC plots
#PlotNr 31. Bar plot for compression rate for full array of mics using FLAC (max order lpc 32)
#PlotNr 32. Timing for recreate original values using FLAC (max order lpc 32)

#Adjacent plots
#PlotNr 41. Bar plot for Adjacent best k and m values, grouped by sound
#PlotNr 42. Bar plot for Adjacent time to recreate values
#PlotNr 43. Test adjacent compression rate for all samples of an array (modifed k-values)
#PlotNr 44. Scatter plot for different m and k values using Adjacent, save in test 44

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
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 19)
        
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
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ],fontsize = 19)
        
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


if PlotNr == 15:
    k_plot = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    #Values from testing sine sound, k= 11-15 for order 0, k=8-15 order 1, k = 8-15 for order 2, k = 8-15 order 3
    Sine_order0 = [0.88515625, 0.7446940104166666, 0.6957600911458334, 0.691748046875, 0.7091064453125]
    Sine_order1 = [0.7937744140625, 0.6391438802083333, 0.5803059895833333, 0.5723795572916666, 0.58974609375, 0.6253743489583334, 0.6668212890625002, 0.7083577473958335]
    Sine_order2 = [0.6918619791666667, 0.5924886067708333, 0.5577067057291667, 0.5619140624999999, 0.5873860677083333, 0.6258138020833334, 0.6670003255208333, 0.7083984375000002]
    Sine_order3 = [0.9262125651041668, 0.7160400390625001, 0.6189046223958334, 0.5917643229166667, 0.6001627604166668, 0.6279134114583333, 0.6674235026041667, 0.7085693359375]
    #Values from testing silent (mic 20), k = 1-8
    Silent_order0 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order1 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order2 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order3 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    #Values from testing Drone, k = 13-20 for all orders but 3 wich is k= 14-20
    Drone_order0 =  [0.9572916666666667, 0.8228434244791666, 0.7768636067708334, 0.77548828125, 0.7971842447916666, 0.8335286458333334, 0.875, 0.9166666666666667]
    Drone_order1 = [0.9583170572916666, 0.8236083984375, 0.7773030598958333, 0.7756266276041667, 0.7973714192708334, 0.8336018880208333, 0.875, 0.9166666666666667]
    Drone_order2 =  [1.0740071614583333, 0.8810791015625001, 0.8058430989583334, 0.7895426432291667, 0.8037353515625, 0.8348551432291668, 0.875048828125, 0.9166666666666667]
    Drone_order3 =[0.9959472656250001, 0.8629313151041668, 0.8175862630208334, 0.8169677734375, 0.8393717447916668, 0.8754964192708332, 0.9166666666666667]
    #Values from testing static noise, k = 13-20 order 0, k= 14-20 for order 1 and order 2, k= 15-20 for order 3
    Static_order0 = [1.0679524739583335, 0.8781494140625, 0.8041178385416666, 0.7887207031250001, 0.8031575520833332, 0.8342936197916666, 0.875, 0.9166666666666667]
    Static_order1 = [0.9243652343750002, 0.827392578125, 0.800244140625, 0.8084879557291668, 0.8358154296875, 0.8750162760416667, 0.9166666666666667]
    Static_order2 = [1.0432942708333335, 0.8866048177083332, 0.8293619791666667, 0.8226725260416667, 0.8415852864583332, 0.8756266276041667, 0.9166666666666667]
    Static_order3 = [0.9977783203125001, 0.8848958333333332, 0.8495035807291667, 0.853662109375, 0.8788574218749998, 0.9167724609375]
    
    plt.figure("Test13_fixed_values", layout = 'constrained')

    #Plot sine
    plt.plot(k_plot[10:15], Sine_order0, 'yo', markersize = 25,label='1k Hz tone, Order 0')
    plt.plot(k_plot[7:15], Sine_order1, 'yv', markersize = 25, label='1k Hz tone, Order 1')
    plt.plot(k_plot[7:15], Sine_order2, 'ys', markersize = 25, label='1k Hz tone, Order 2')
    plt.plot(k_plot[7:15], Sine_order3, 'y*', markersize = 25, label='1k Hz tone, Order 3')

    #plot silent
    plt.plot(k_plot[0:8], Silent_order0, 'ro', markersize = 25, label='Silent mic, Order 0')
    plt.plot(k_plot[0:8], Silent_order1, 'rv', markersize = 25, label='Silent mic, Order 1')
    plt.plot(k_plot[0:8], Silent_order2, 'rs', markersize = 25, label='Silent mic, Order 2')
    plt.plot(k_plot[0:8], Silent_order2, 'r*', markersize = 25, label='Silent mic, Order 3')

    #plot drone
    plt.plot(k_plot[12:20], Drone_order0, 'bo', markersize = 25, label='Drone sound, Order 0')
    plt.plot(k_plot[12:20], Drone_order1, 'bv', markersize = 25, label='Drone sound, Order 1')
    plt.plot(k_plot[12:20], Drone_order2, 'bs', markersize = 25, label='Drone sound, Order 2')
    plt.plot(k_plot[13:20], Drone_order3, 'b*', markersize = 25, label='Drone sound, Order 3')

    #plot Static oise
    plt.plot(k_plot[12:20], Static_order0, 'go', markersize = 25, label='Static noise, Order 0')
    plt.plot(k_plot[13:20], Static_order1, 'gv', markersize = 25, label='Static noise, Order 1')
    plt.plot(k_plot[13:20], Static_order2, 'gs', markersize = 25, label='Static noise, Order 2')
    plt.plot(k_plot[14:20], Static_order3, 'g*', markersize = 25, label='Static noise, Order 3')

    #plt.plot(k_array, cr_2, 'bo', label='Order 2')
    #plt.plot(k_array, cr_3, 'go', label='Order 3')
    #plt.title("Comparison of comression ratio for differente orders")
    plt.yticks(fontsize=25)
    plt.xticks(fontsize=25)
    plt.xlabel("k-value", fontsize=30)
    plt.ylabel("Average compression ratio", fontsize=30)
    plt.legend(fontsize=20)
    plt.xticks(np.arange(0, 21, 1.0))
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
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 18)
        
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
        ax.bar_label(rects, labels =[i for i in barTopText[multiplier] ], fontsize = 18)
        
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
        '1 k Hz tone': (0.560, 0.553, 0.548, 0.533, 0.533),
        'Drone sound': (0.762, 0.757, 0.759, 0.761, 0.761),
        'Static noise': (0.786, 0.781, 0.784, 0.778, 0.776),
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


if PlotNr == 25:
    #Values from testing sine sound, k= 8-16 for order 1, k=7-16 order 2, k = 7-16 for order 3, k = 7-16 order 4, k = 7-16 for order 5
    Sine_order1 = [0.7995198567708334, 0.6397867838541667, 0.58076171875, 0.5725748697916667, 0.5897460937500001, 0.6253417968749999, 0.666796875, 0.7083658854166668, 0.75]

    Sine_order2 = [0.9288818359375, 0.6835774739583332, 0.5820475260416667, 0.5524739583333333, 0.5596923828125, 0.586181640625, 0.6255452473958333, 0.6668701171874999, 0.7083740234375001, 0.75]

    Sine_order3 = [0.8458658854166666, 0.6416259765625, 0.5608479817708333, 0.5417968750000001, 0.5546793619791667, 0.5852213541666667, 0.6255777994791667, 0.6668375651041667, 0.7083740234375001, 0.75]
    Sine_order4 = [0.7119547526041666, 0.5751871744791667, 0.5279947916666667, 0.5262125651041667, 0.5483317057291667, 0.5848063151041667, 0.6255777994791666, 0.666845703125, 0.7083740234375001, 0.75]
    Sine_order5 = [0.7107747395833334, 0.5746744791666667, 0.5276936848958333, 0.5258382161458333, 0.5481526692708334, 0.584814453125, 0.6255289713541667, 0.6668294270833333, 0.7083740234375001, 0.75]

    #Values from testing silent (mic 20), k = 1-8 for all
    Silent_order1 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order2 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order3 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order4 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
    Silent_order5 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]

    #Values from testing Drone, k = 12-20 for all
    Drone_order1 =  [1.1723307291666667, 0.9091634114583333, 0.7989420572916666, 0.764892578125, 0.7698974609374999, 0.7954264322916667, 0.8334147135416667, 0.875, 0.9166666666666667]

    Drone_order2 = [1.0881510416666664, 0.8672119140625, 0.7778727213541666, 0.7544514973958333, 0.7651448567708333, 0.7940022786458335, 0.8333984375000002, 0.875, 0.9166666666666667]

    Drone_order3 = [1.0695393880208333, 0.8576416015625, 0.7733072916666667, 0.752490234375, 0.7640380859375, 0.7938802083333334, 0.8333984375000002, 0.875, 0.9166666666666667] 
    Drone_order4 = [1.06240234375, 0.8544026692708332, 0.7717692057291667, 0.7512125651041666, 0.7636881510416667, 0.7936686197916667, 0.8333902994791668, 0.875, 0.9166666666666667]

    Drone_order5 = [0.99404296875, 0.8203938802083334, 0.7546630859375, 0.7431396484375, 0.7598225911458334, 0.7926920572916666, 0.8333577473958333, 0.875, 0.9166666666666667]

    #Values from testing static noise, k = 13-20 for all
    Static_order1 = [1.038134765625, 0.8631022135416666, 0.7969401041666667, 0.7851318359375, 0.8017008463541666, 0.8340087890625, 0.875, 0.9166666666666667]

    Static_order2 = [0.9714192708333332, 0.8300211588541668, 0.7802571614583333, 0.7771728515625, 0.7982666015625, 0.8336344401041667, 0.875, 0.9166666666666667]

    Static_order3 = [0.9663818359375, 0.8274332682291666, 0.7792073567708333, 0.7765055338541667, 0.798046875, 0.8336669921875, 0.875, 0.9166666666666667]

    Static_order4 = [0.9208984375, 0.8046549479166665, 0.7679361979166667, 0.7709879557291667, 0.7954833984375, 0.8334147135416667, 0.875, 0.9166666666666667]

    Static_order5 = [0.8694905598958332, 0.7792236328125, 0.7555094401041667, 0.7656331380208332, 0.7939127604166666, 0.8333902994791668, 0.875, 0.9166666666666667]

    plt.figure("Test24_fixed_values", layout = 'constrained')

    ms = 23 #Variable for marker size

    #Plot sine
    plt.plot(list(range(8,17)), Sine_order1, 'yv', markersize = ms, label='1k Hz tone, Order 1')
    plt.plot(list(range(7,17)), Sine_order2, 'ys', markersize = ms, label='1k Hz tone, Order 2')
    plt.plot(list(range(7,17)), Sine_order3, 'y*', markersize = ms, label='1k Hz tone, Order 3')
    plt.plot(list(range(7,17)), Sine_order4, 'yo', markersize = ms, label='1k Hz tone, Order 4')
    plt.plot(list(range(7,17)), Sine_order5, 'y^', markersize = ms, label='1k Hz tone, Order 5')

    #plot silent
    plt.plot(list(range(1,9)), Silent_order1, 'ro', markersize = ms, label='Silent mic, Order 1')
    plt.plot(list(range(1,9)), Silent_order2, 'rv', markersize = ms, label='Silent mic, Order 2')
    plt.plot(list(range(1,9)), Silent_order3, 'rs', markersize = ms, label='Silent mic, Order 3')
    plt.plot(list(range(1,9)), Silent_order4, 'r*', markersize = ms, label='Silent mic, Order 4')
    plt.plot(list(range(1,9)), Silent_order5, 'r^', markersize = ms, label='Silent mic, Order 5')

    #plot drone
    plt.plot(list(range(12,21)), Drone_order1, 'bo', markersize = ms, label='Drone sound, Order 1')
    plt.plot(list(range(12,21)), Drone_order2, 'bv', markersize = ms, label='Drone sound, Order 2')
    plt.plot(list(range(12,21)), Drone_order3, 'bs', markersize = ms, label='Drone sound, Order 3')
    plt.plot(list(range(12,21)), Drone_order4, 'b*', markersize = ms, label='Drone sound, Order 4')
    plt.plot(list(range(12,21)), Drone_order5, 'b^', markersize = ms, label='Drone sound, Order 5')

    #plot Static oise
    plt.plot(list(range(13,21)), Static_order1, 'go', markersize = ms, label='Static noise, Order 1')
    plt.plot(list(range(13,21)), Static_order2, 'gv', markersize = ms, label='Static noise, Order 2')
    plt.plot(list(range(13,21)), Static_order3, 'gs', markersize = ms, label='Static noise, Order 3')
    plt.plot(list(range(13,21)), Static_order4, 'g*', markersize = ms, label='Static noise, Order 4')
    plt.plot(list(range(13,21)), Static_order5, 'g^', markersize = ms, label='Static noise, Order 5')

    #plt.plot(k_array, cr_2, 'bo', label='Order 2')
    #plt.plot(k_array, cr_3, 'go', label='Order 3')
    #plt.title("Comparison of comression ratio for differente orders")
    plt.yticks(fontsize=25)
    plt.xticks(fontsize=25)
    plt.xlabel("k-value", fontsize=30)
    plt.ylabel("Average compression ratio", fontsize=30)
    plt.legend(fontsize=17)

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


if PlotNr == 44:

    #K values for sine: 2 = k 8-16
    Sine_2 = [0.8500504811604804, 0.6653977711995446, 0.5942123413085907, 0.5801274617513004, 0.5951808929443353, 0.6281656901041665, 0.667703755696605, 0.708484268188506, 0.75]

    #K values for Drone: 2 = k 12-20
    Drone_2 =[1.0085985819498702, 0.8280771891276049, 0.7590602874755846, 0.7461541493733703, 0.7623184204101547, 0.7942623138427689, 0.8335726420085013, 0.8750035603841146, 0.9166666666666524]

    #K values for static: 2 = k 13-20
    Static_2 = [0.9175244649251315, 0.8035437266031901, 0.7679500579833974, 0.7721909840901684, 0.7975072224934917, 0.8339841206868762, 0.8750086466471352, 0.9166666666666524]

    ms = 30#set marker size

    plt.figure("Test44_fixed_values", layout = 'constrained')

    #Plot sine
    plt.plot(list(range(8,17)), Sine_2, 'yo', markersize = ms, label='1k Hz tone')


    #plot drone
    plt.plot(list(range(12,21)), Drone_2, 'bo', markersize = ms, label='Drone sound')


    #plot Static oise
    plt.plot(list(range(13,21)), Static_2, 'go', markersize = ms, label='Static noise')


        
    #plt.title("Comparison of comression ratio for differente orders")
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)
    plt.xlabel("k-value", fontsize=45)
    plt.ylabel("Average compression ratio", fontsize=45)
    plt.legend(fontsize=35, loc = 'upper left')

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
    plt.yticks(fontsize=35)
    
    plt.show()
