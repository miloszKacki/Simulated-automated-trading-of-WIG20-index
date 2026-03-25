## Simulated automated trading of WIG20 using MACD indicator

This project is a simulation of Automated trading, based off of the MACD and Signal trade indicators.
The behaviour and performance of the automated wallet was analysed. The results are in a different .md [file](TODO)

This project was an assignment for the Numerical Methods class on the Gdańsk University of Technology.

## How does it work

MACD and Signal are trade indicators, that are supposed to reveal shifts in the strrength and direction of a stock's trend. They are calculated using Exponential moving averages(EMAs).

### MACD = EMA(12) - EMA(26), Signal = EMA(19)

Exponential moving averages are a type of Generalized means, where weights of earlier prices are decreased exponentially.

The wallet is set to buy when the MACD indicator overtakes Signal in value, and sell when the Signal overtakes the MACD

More info on MACD, and how It's calculated can be found on [wikipedia](https://en.wikipedia.org/wiki/MACD)

## About the data

The historical data used for this task consists of the closing values of the WIG20 index for the period from March 17, 2021, to March 14, 2025. This data was obtained from the website [stooq.com](https://stooq.com/).
