import numpy as np
import matplotlib.pyplot as plt

class Simulation:

    def __init__(self,commodity_price_history,signal,MACD,crossings,time_skip = 0,owned_commodity = 1000,owned_money=0):

        self.commodity_price_history = commodity_price_history
        self.signal = signal
        self.MACD = MACD
        self.crossings = crossings
        self.funds_liquid = owned_money
        self.funds_commodity = owned_commodity

        self.moment_in_time = time_skip
        self.time_skip = time_skip

        self.networth_history = []
        #trade history is a list of pairs [day_of_trade, buy_or_sell]
        self.trade_history = []

        return

    def Buy(self):

        buy_ammount = self.funds_liquid // self.commodity_price_history[self.moment_in_time]

        #add bought commodity to "wallet"
        self.funds_commodity += buy_ammount

        #deduct funds from "wallet"
        self.funds_liquid -= buy_ammount * self.commodity_price_history[self.moment_in_time]

        return

    def Sell(self):

        self.funds_liquid += self.funds_commodity * self.commodity_price_history[self.moment_in_time]

        self.funds_commodity = 0

        return

    def Simulate(self):

        #begin the simulation
        print("Starting the simulation")
        print(f"Money: {self.funds_liquid}.")
        print(f"Ammount of asset: {self.funds_commodity}.")
        print(f"Networth: {self.Networth()}")

        #loop of the simulation
        while(self.moment_in_time < len(self.commodity_price_history)):

            #sell when signal crosses over MACD
            if(self.crossings[self.moment_in_time] == 1):
                self.Buy()
                self.trade_history.append([self.moment_in_time-self.time_skip,"bought"])

            elif(self.crossings[self.moment_in_time] == -1):
                self.Sell()
                self.trade_history.append([self.moment_in_time-self.time_skip,"sold"])

            self.networth_history.append(self.Networth())

            self.moment_in_time += 1

        #print the simulation outcome, set time to check last days price
        self.moment_in_time -= 1
        print("Simulation ended")
        print(f"Money: {self.funds_liquid}.")
        print(f"Ammount of asset: {self.funds_commodity}.")
        print(f"Networth: {self.Networth()}")

    def Networth(self):
        #return money + value of funds
        return (self.funds_liquid +
                self.funds_commodity * self.commodity_price_history[self.moment_in_time])