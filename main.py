import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Simulation as sim

def Ema_reku(range,index,data):
    if (index <= 0 ): return data[0]

    alpha = 2/(range + 1)

    return (  (data[index] * alpha) + ((1-alpha) * Ema_reku(range,index-1,data)))

def Ema_reku_array_supported(range,index,data,ema_list):

    if (index == 0): return data[0]
    if (ema_list[index] != 0): return ema_list[index]

    alpha = 2/(range + 1)

    ret_value =((  data[index]
                * alpha)
                + ((1-alpha)
                * Ema_reku_array_supported(range,index-1,data,ema_list)))

    ema_list[index] = ret_value
    return ret_value

def Create_ema_array(data,ema_n):

    output_array = np.zeros(len(data))

    for i in range(len(data)):
        output_array[i] = Ema_reku_array_supported(ema_n,i,data,output_array)

    return output_array

def Create_Macd(data,n1,n2):

    ema1 = Create_ema_array(data,n1)
    ema2 = Create_ema_array(data,n2)

    return np.subtract(ema1, ema2)

def Find_datas_crossings_by_id(data_1,data_2):

    output_table = np.zeros(len(data_1))

    for i in range(1,len(data_1)):
        if ( (data_1[i] >= data_2[i]) != (data_1[i-1] > data_2[i-1])):
            output_table[i] = 1 if (data_1[i-1] < data_2[i-1]) else -1

    #0s where there is no crossing, 1 when data_1 surpases data_2 and -1 when data_2 surpases data_1
    return output_table

def Plot_Trends(trends,colors):
    for i in range(len(trends)):
        plt.plot(trends[i],color=colors[i])

def Plot_wig20(wig20_values_daily):
    #plt.title("Wartości wig20 w czasie")
    plt.title("wig20 value in time")
    plt.plot(wig20_values_daily, color="black")
    #plt.ylabel("Wartość")
    plt.ylabel("Value")
#    plt.xlabel("Dni od początku obserwowanego okresu")
    plt.xlabel("Days since the start of the observation process")
    plt.show()
    plt.cla()

def Plot_macd_vs_signal(signal,MACD,crossings):
#    plt.title("Wskazniki MACD vs SIGNAL")
    plt.title("Indicators: MACD vs SIGNAL")
    plt.plot(signal, color="blue")
    plt.plot(MACD, color="purple")
#    plt.ylabel("Wartość wskaźnika")
    plt.ylabel("Indicator value")
    #plt.xlabel("Dni od początku obserwowanego okresu")
    plt.xlabel("Days since the start of the observation process")

    for i in range(len(MACD)):
        if (crossings[i] == 1):
            plt.scatter(i, MACD[i], color='red', s=100)
        elif (crossings[i] == -1):
            plt.scatter(i, MACD[i], color='green', s=100)

    plt.show()
    plt.cla()

def Plot_wig20_with_transactions(crossings,wig20):

    #plt.title("Wartości wig20 zestawione z tranzakcjami")
    plt.title("wig20 values and transactions")
    plt.plot(wig20, color="black")
    plt.ylabel("Value")
    #plt.xlabel("Dni od początku obserwowanego okresu")
    plt.xlabel("Days since the start of the observation process")

    for i in range(len(wig20)):
        if (crossings[i] == 1):
            plt.scatter(i, wig20[i], color='red', s=100)
        elif (crossings[i] == -1):
            plt.scatter(i, wig20[i], color='green', s=100)

    plt.show()
    plt.cla()

def Plot_partial_macd_vs_signal(sigal,MACD,crossings,wig20,start,end):
    part_of_signal = signal[start:end]
    part_of_MACD = MACD[start:end]
    part_of_crossings = crossings[start:end]
    part_of_wig20 = wig20[start:end]

    Plot_macd_vs_signal(part_of_signal,part_of_MACD,part_of_crossings)
    Plot_wig20_with_transactions(part_of_crossings,part_of_wig20)

def Plot_MACD_and_wig20(wig20,networths):
    #plt.title("Historia wartości portfela w symulacji vs wartość wig20")
    plt.title("Wallet value history vs wig20 value")
    #plt.ylabel("Wartości w jednostkach pieniędzy")
    plt.ylabel("Values in money units")
    #plt.xlabel("Dni od początku obserwowanego okresu")
    plt.xlabel("Days since the start of the observation process")

    plt.plot(networths, color="green")
    plt.plot(wig20,color="black")

    plt.show()
    plt.cla()

def Analyze_sim_history(networth_history,trade_history):

    #plt.title("Historia wartości portfela w symulacji")
    plt.title("Wallet value history")

    plt.plot(test_sim.networth_history, color="green")

    #plt.ylabel("Wartość portfela")
    plt.ylabel("Wallet value")
    #plt.xlabel("Dni od początku obserwowanego okresu")
    plt.xlabel("Days since the start of the observation process")

    plt.show()
    plt.cla()

    print(trade_history)

    positive_transactions = 0
    capital_losses = 0
    negative_transactions = 0
    capital_gains = 0

    for i in range(1,len(trade_history)):
        if (trade_history[i][1] == "sold"):
            #print(i)
            if(networth_history[trade_history[i][0]] < networth_history[trade_history[i-1][0]]):
                negative_transactions += 1
                capital_losses += networth_history[trade_history[i-1][0]] - networth_history[trade_history[i][0]]

            else:
                positive_transactions += 1
                capital_gains += networth_history[trade_history[i][0]] - networth_history[trade_history[i-1][0]]

    print(f"Made {positive_transactions} positive trades yealding total of {capital_gains} profits, and {negative_transactions} negative trades resulting in {capital_losses} in losses.")




data = pd.read_csv('data/wig20_d.csv')

wig20_values_daily = np.array(data.get("Close"))


MACD = Create_Macd(wig20_values_daily,26,12)
signal = Create_ema_array(MACD,9)
crossings = Find_datas_crossings_by_id(signal, MACD)


#test_sim = sim.Simulation(wig20_values_daily,signal,MACD,crossings,26)
#test_sim.Simulate()

#Plot_MACD_and_wig20(wig20_values_daily,test_sim.networth_history)

#Plot_wig20_with_transactions(crossings,wig20_values_daily)

Plot_macd_vs_signal(signal,MACD,crossings)
Plot_wig20(wig20_values_daily)


#Plot_partial_macd_vs_signal(signal,MACD,crossings,wig20_values_daily,200,300)
#Plot_partial_macd_vs_signal(signal,MACD,crossings,wig20_values_daily,600,675)

#Analyze_sim_history(test_sim.networth_history,test_sim.trade_history)

#print(wig20_values_daily)