base='DOGE'
quote='USDT'
TF='1m'#Timeframe
start_date = '2024-01-01T00:00:00Z'
samples=100 #number of samples to downlowad
numberOfExchanges=1000
spreadThreshold=1 #valor umbral en % del spread
numberOfsamples=150 #numero de muestras que cumplen con el spreadThreshold 
N=20 #número de periodos para calcular el Zscore del spread
exchages_to_delete=[
'alpaca', #excepcion message": "forbidden."
'bigone',#fetchOHLCV() can only fetch ohlcvs for spot markets
'bitmart',#no llega bien la data
'bequant',#no llega bien la data
'bitcoincom',#no llega bien la data
'bitfinex2',#no llega bien la data
'binanceusdm', #es lo mismo que binance
'coinbase',#throws exception: coinbase requires "apiKey" credential
'deribit',#data congelada
'fmfwio',#no llega bien la data
'gateio',#es lo mismo que gate
'hitbtc',#no llega bien la data
'hitbtc3',#no llega bien la data
'lbank', #throws exception: Invalid Trading Pair






]
                 