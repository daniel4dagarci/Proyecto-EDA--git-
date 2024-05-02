import ccxt
import time 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import functions as fun
import cons
import datetime
from datetime import datetime
import os
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import backtrader as bt
import vectorbt as vbt

#create an instance of the CCXT class for each exchange on our list
binance = ccxt.binance() 
bybit=ccxt.bybit()
bitfinex = ccxt.bitfinex() 
bittrex = ccxt.bitmex() 
poloniex = ccxt.poloniex() 
kraken=ccxt.krakenfutures()
ace=ccxt.ace()
ascendex=ccxt.ascendex()
bitrue=ccxt.bitrue()
kucoinfutures=ccxt.kucoinfutures()
digifinex=ccxt.digifinex()



#getting the ticker for each exchange
'''binance_ticker = binance.fetch_ticker(‘BTC/USDT’) 
bitfinex_ticker = bitfinex.fetch_ticker(‘BTC/USDT’) 
bittrex_ticker = bittrex.fetch_ticker(‘BTC/USDT’) 
poloniex_ticker = poloniex.fetch_ticker(‘BTC/USDT’) '''

# Crea una instancia de Binance Futures
exchange = ccxt.binance({
    'apiKey': 'f2u7KyXup2pTpsi1XNBScnpAx4nEPIwgasAP88GjrxWg6IaHotOtzBfLKEcpwuQr',
    'secret': '41U4e362AhK1A7ipenNCgCCJp7jVAi5FmPDUtHvx700qWnYjPel38k6fzplveZIO',
    'enableRateLimit': True,
    'options': {
        'defaultType': 'swap',  # Configura el tipo como 'future'
    },
})

#1.CARGAR LOS DATASETS DEL PAR PARA CADA EXCHANGE, GUARDÁNDOLOS EN FICHEROS .CSV

#QUITAR EL COMENTARIO DE ESTO, FUNCIONA BIEN!
'''
# Carga los mercados disponibles
markets = binance.load_markets()
exchanges_with_swaps=fun.get_exchanges_with_swaps()
#print(f"Hay {len(exchanges_with_swaps)} exchanges con swap de un total de {len(ccxt.exchanges)} exchanges")
print(f"Listado de exchanges con swap: {exchanges_with_swaps}")
#print(f"Listado de markets para binanceusdm swap: {exchanges_with_swaps['binanceusdm']}")
'''


#Paja, igual borrar
'''
btc_usdt = binance.fetch_ohlcv('WOO/USDT:USDT', timeframe=cons.TF, limit=cons.samples) 

# Crear un DataFrame a partir de los datos
df_btc_usdt = pd.DataFrame(btc_usdt, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df_btc_usdt['timestamp'] = pd.to_datetime(df_btc_usdt['timestamp'], unit='ms')
print(df_btc_usdt)

  # Obtiene una lista de todos los exchanges disponibles
print (f"Listado de todos los exchanges: {ccxt.exchanges}")
#print (f"Listado de todos los mercados en binance: {binance.load_markets()}")
'''

#2.CARGAR EN UN DICCIONARIO DE DATAFRAMES LOS FICHEROS .CSV DE LOS EXCHANGES PARA CADA PAR Y CREAR LOS FICHEROS .CSV DE LOS SPREADS

#QUITAR EL COMENTARIO DE ESTO, FUNCIONA BIEN!
'''
# Llama a la función para cargar los archivos del par especificado y almacenarlos en un diccionario
exchange_dataframes = fun.load_exchange_files()

# Imprime las claves del diccionario (nombres de las carpetas)
print("Archivos BTCUSDT cargados desde las siguientes carpetas:")
for folder_name in exchange_dataframes.keys():
    print(folder_name)
    print(exchange_dataframes[folder_name])

fun.merge_and_process_dataframes(exchange_dataframes)
'''

#3.ANALIZAR EL SPREAD

#QUITAR EL COMENTARIO DE ESTO, FUNCIONA BIEN!
'''
path = os.path.dirname(os.path.abspath(__file__))+"\\src\\data\\spreads\\BNBUSDT\\TEST.csv"
df = pd.read_csv(path,sep=";")
fun.spread_analysis(df)
'''

#4.BACKTESTEAR EL SPREAD

#QUITAR EL COMENTARIO DE ESTO, FUNCIONA BIEN!
'''
path = os.path.dirname(os.path.abspath(__file__))+"\\src\\data\\spreads\\BNBUSDT\\TEST.csv"
df = pd.read_csv(path,sep=";")

#Ploteo el spread vs el Zscore del spread
fun.plot_zscore(df)
'''







#69.MÁS PRUEBAS
'''
# Set up the exchange
exchange = ccxt.bitrue()  # Replace with your desired exchange

# Define the symbol and timeframe
symbol_0 = 'ETH'  # Replace with your desired trading pair
symbol_1 = 'USDT'

timeframe = '1m'  # Replace with your desired timeframe (e.g., '1m', '5m', '1h', '1d')

n_days = 10  # Replace with how far back you'd like to look

# Set the start and end dates
end_date = '2024-01-01T00:00:00Z'
start_date = '2024-01-20T00:00:00Z'


# Fetch OHLCV data for the specified date range
token_0 = fun.fetch_historical_prices(exchange, symbol_0+'USDT', timeframe, start_date, end_date)
print(token_0)
'''