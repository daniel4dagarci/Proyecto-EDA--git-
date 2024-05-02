import ccxt
import functions as fun
import cons
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from scipy.stats import shapiro

def get_exchanges_with_swaps():

    # Initialize a list to store exchanges with swaps
    exchanges_with_swaps = []
    selected_exchanges = {}

    # Get a list of all available exchanges
    all_exchanges = ccxt.exchanges
    all_exchanges = all_exchanges[:cons.numberOfExchanges]

    # Iterate over each exchange
    for exchange_name in all_exchanges:
        try:
            # Initialize the exchange object
            exchange = getattr(ccxt, exchange_name)()
           


            #print (f"Exchange: {exchange_name}")

            '''
            if 'swap' in exchange.options['accountsByType']:
                exchanges_with_swaps.append(exchange_name)
                print (f"El exchange {exchange_name} tiene swap")
            else: print (f"El exchange {exchange_name} NO tiene swap")
            '''


            # Obtener la lista de mercados disponibles
            markets = exchange.load_markets()

            #all_exchanges[exchange_name] = markets

            # Crear una lista de símbolos con "swap"=True
            #swap_symbols = [symbol for symbol, market in markets.items() if market.get('swap') and market.get('base') == cons.base and market.get('quote') == cons.quote]
            #swap_symbols = [symbol for symbol, market in markets.items() if market.get('swap') and market.get('base') in market and market.get('quote') in market]

            swap_symbols = []

            # Itera sobre cada símbolo y mercado en el diccionario 'markets'
            for symbol, market in markets.items():
                # Verifica si el mercado tiene la clave 'swap' y si las claves 'base' y 'quote' coinciden con las propiedades de 'cons'
                if market.get('swap') and market.get('base') ==cons.base and market.get('quote') == cons.quote:
                    # Agrega el símbolo a la lista swap_symbols
                    swap_symbols.append(symbol)

            #if len(swap_symbols)>0 and exchange_name not in cons.exchages_to_delete:
            if len(swap_symbols)>0 and exchange_name in ['ascendex','binance','bingx','bitget','bitmex','bybit','delta','gate','htx','huobi','okx','phemex']:
                selected_exchanges[exchange_name]=swap_symbols


                #EMPIEZA


                # Lista para almacenar las muestras
                all_samples = []
                start_date=cons.start_date
                cont=0

                # Consulta iterativa de datos
                
                while True:
                    try:
                        # Consulta los datos
                        #OHLC = exchange.fetch_ohlcv(swap_symbols[0], timeframe=cons.TF, since=exchange.parse8601(start_date), limit=cons.samples)
                        OHLC = exchange.fetch_ohlcv(swap_symbols[0], timeframe=cons.TF, since=exchange.parse8601(start_date),limit=None)

                        if len(OHLC) == 0:
                            break  # No hay más datos
                        all_samples.extend(OHLC)
                        # Actualiza la fecha de inicio para la siguiente consulta
                        start_date = exchange.iso8601(OHLC[-1][0] + 60000)  # Agrega 1 minuto al último timestamp
                        time.sleep(1)  # Espera 1 segundo para evitar exceder el límite de solicitudes
                        cont+=1
                        print (f"Contador: {cont}")
                    except Exception as e:
                        print(f"Error al obtener datos: {e}")
                        break

                #ACABA

                #time.sleep(30)
                # Crear un DataFrame a partir de los datos
                df= pd.DataFrame(all_samples, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.drop(columns=['open', 'high', 'low', 'volume'],inplace=True)
                df.rename(columns={'close':'close'+'_'+exchange_name},inplace=True)
                print (f"El exchange {exchange_name} tiene los siguientes mercados: {swap_symbols}")
                print(df)         

                            
                # Ruta donde se guardará el archivo CSV
                #Fget the path for the directory of the script being run:
                path = os.path.dirname(os.path.abspath(__file__))+"\\src\\data\\exchanges\\"+exchange_name
               

              

                # Crear la carpeta si no existe
                if not os.path.exists(path):
                    os.makedirs(path)

                # Guardar el DataFrame en un archivo CSV llamado "datos.csv"
                archivo_csv = os.path.join(path, cons.base+cons.quote+".csv")
                #archivo_csv = os.path.join(path,exchange_name+".csv")
                df.to_csv(archivo_csv, index=False, sep=";")

                print(f"El DataFrame se ha guardado exitosamente en {archivo_csv}")


        except Exception as e:
            # Handle any exceptions (e.g., unsupported exchanges)
            print(f"Exchange {exchange_name} throws exception: {e}")
            #Borro del diccionaro el exchange que ha dado excepción
            if exchange_name in selected_exchanges: del selected_exchanges[exchange_name]
            pass


    #return exchanges_with_swaps
    return selected_exchanges

def get_markets_by_exchange():
    # Inicializa un diccionario vacío para almacenar los mercados por exchange
    markets_by_exchange = {}

    # Obtiene una lista de todos los exchanges disponibles
    '''if allExchanges:
        exchange_names = ccxt.exchanges
    else: exchange_names=fun.selected_exchanges'''
    exchange_names=ccxt.exchanges

    # Inicializa los objetos de intercambio
    for exchange_name in exchange_names:
        try:
            exchange = getattr(ccxt, exchange_name)()

             # Obtener la lista de mercados disponibles
            markets = exchange.load_markets()

            # Crear una lista de símbolos con "swap"=True
            #swap_symbols = [symbol for symbol, market in markets.items() if market.get('swap') and market.get('quote') == cons.quote and market.get('base') == cons.base]
            swap_symbols = [symbol for symbol, market in markets.items() if market.get('swap') and market.get('quote') == 'USDT']



            markets_by_exchange[exchange_name] = swap_symbols
        
        except Exception as e:
            # Maneja cualquier excepción (por ejemplo, exchanges no compatibles)
            print(f"El exchange {exchange_name} ha arrojado la excepción {e}")
            pass

    return markets_by_exchange


def load_exchange_files():

    path = os.path.dirname(os.path.abspath(__file__))+"\\src\\data\\exchanges"

    # Inicializa un diccionario vacío para almacenar los dataframes
    dataframes_dict = {}
    
    # Itera sobre todos los subdirectorios en la ruta dada
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            # Comprueba si el directorio contiene un archivo llamado 'par.csv'
            btcusdt_file = os.path.join(root, dir_name, cons.base+cons.quote+'.csv')
            if os.path.exists(btcusdt_file):
                # Carga el archivo en un dataframe de pandas
                df = pd.read_csv(btcusdt_file,sep=";")
                # Almacena el dataframe en el diccionario con el nombre de la carpeta como clave
                dataframes_dict[dir_name] = df
    
    return dataframes_dict


def merge_and_process_dataframes(exchange_dataframes):
    """
    Combines dataframes from the exchange_dataframes dictionary and performs the specified operations.
    Saves resulting dataframes as CSV files in separate folders based on the dictionary keys.
    """
    



    '''
    for exchange, df in exchange_dataframes.items():
        merged_df = df.copy()

        # Merge with other dataframes
        for other_exchange, other_df in exchange_dataframes.items():
            if other_exchange != exchange:
                merged_df = pd.merge(merged_df, other_df, on="timestamp", suffixes=("", f"_{other_exchange}"))

        # Calculate spread
        for col in merged_df.columns:
            if col.startswith("column"):
                merged_df[f"spread_{col}"] = merged_df[col] - merged_df[f"{col}_{exchange}"]

        # Calculate arbitrage
        for col in merged_df.columns:
            if col.startswith("spread"):
                avg_col = (merged_df[col] + merged_df[f"{col}_{exchange}"]) / 2
                merged_df[f"arbitrage_{col}"] = (abs(merged_df[col]) / avg_col) * 100 >= cons.spreadThreshold

        # Save to CSV if any row has arbitrage
        if merged_df[[col for col in merged_df.columns if col.startswith("arbitrage")]].any().any():
            output_file = os.path.join(path, f"{cons.base+cons.quote}.csv")
            merged_df.to_csv(output_file, index=False)
            print(f"Saved {exchange} data to {output_file}")
    '''
    # Ruta donde se guardará el archivo CSV
    path = os.path.dirname(os.path.abspath(__file__))+"\\src\\data\\spreads\\"+cons.base+cons.quote
               
    # Crear la carpeta si no existe
    if not os.path.exists(path):
        os.makedirs(path)

    # Inicializar un diccionario para almacenar los dataframes combinados
    combined_dataframes = {}

    # Obtener las claves del diccionario para iterar
    keys = list(exchange_dataframes.keys())

    # Iterar sobre las claves para combinar los dataframes
    for i, key1 in enumerate(keys):
        for j in range(i+1, len(keys)):
            key2 = keys[j]
            
            # Combinar los dataframes
            #combined_df = pd.merge(exchange_dataframes[key1], exchange_dataframes[key2], how='outer', on='timestamp')  
            combined_df = pd.merge(exchange_dataframes[key1], exchange_dataframes[key2], on='timestamp')  

             # Creo las columnas "spread"
            combined_df["spread"] = combined_df["close_"+key1] - combined_df["close_"+key2]
            combined_df["spread_percent"] = (abs(combined_df["spread"]) / ((combined_df["close_"+key1] + combined_df["close_"+key2])/2))*100
            
            # Guardar el dataframe combinado en el diccionario con una clave única
            combined_key = f"{key1}_{key2}"
            combined_dataframes[combined_key] = combined_df
            
            # Guardar el DataFrame en un archivo CSV llamado "datos.csv"
            #if combined_df["spread_percent"].gt(cons.spreadThreshold).any():
            if (combined_df["spread_percent"]>cons.spreadThreshold).sum() > cons.numberOfsamples:
                archivo_csv = os.path.join(path, combined_key+".csv")
                combined_df.to_csv(archivo_csv, index=False, sep=";")    

def spread_analysis(df):

    # Realiza la prueba ADF
    estacionaria=False
    spread_series = df["spread"]
    result = adfuller(spread_series)
    print("ADF Statistic:", result[0])
    print("p-value:", result[1])
    print("Critical Values:", result[4])

    # Interpreta los resultados de la prueba ADF
    if result[1] < 0.05:
        estacionaria=True
    if estacionaria:
        print("La serie temporal de spread es estacionaria (rechazamos la hipótesis nula).")
    else:
        print("La serie temporal de spread no es estacionaria (no rechazamos la hipótesis nula).")

    if estacionaria:
    
        # Plot the time series of both spreads
        plt.figure(figsize=(10, 6))
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=df.columns[1], color="blue")
        plt.plot(df.iloc[:, 0], df.iloc[:, 2], label=df.columns[2], color="orange")
        plt.xlabel("Timestamp (min)")
        plt.ylabel("Price (USDT)")
        plt.title(f"Time Series: {df.columns[1]} vs {df.columns[2]}")
        plt.legend()
        plt.show()  
    
        # Plot a histogram of the "spread" column
        plt.figure(figsize=(8, 6))
        plt.hist(df.iloc[:, 4], bins=20, color="skyblue", edgecolor="black")
        plt.xlabel("Spread Percent")
        plt.ylabel("Frequency")
        plt.title("Histogram of Spread Percent")
        plt.grid(True)
        plt.show()
    


    

   

#Sacado de: https://gist.github.com/liquiditygoblin/e8053cb6c3ae62b23f3b1c7bb302b19b
def fetch_historical_prices(exchange, symbol, timeframe, start_date, end_date):
    # Convert start_date and end_date to timestamps
    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)
    
    # Initialize an empty list to store the fetched OHLCV data
    ohlcv_data = []
    
    # Set up the progress bar
    #progress_bar = tqdm(total=end_timestamp - start_timestamp, desc='Fetching Data')

    # Fetch OHLCV data
    current_timestamp = start_timestamp
    while current_timestamp < end_timestamp:
        # Fetch OHLCV data
        data = exchange.fetch_ohlcv(symbol, timeframe, current_timestamp)
        if len(data) < 1:
            break
        # Append the fetched data to the overall list
        ohlcv_data += data
        # Update the current timestamp and progress bar
        #progress_bar.update(data[-1][0] + 1 - current_timestamp)

        current_timestamp = data[-1][0] + 1  # Set the next timestamp to fetch as the last timestamp in the current data + 1 millisecond
    
    # Close the progress bar
    #progress_bar.close()
    
    # Convert the data into a DataFrame
    columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(ohlcv_data, columns=columns)
    
    # Convert the timestamp to a readable format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    
    # Set the Timestamp column as the DataFrame's index
    df.set_index('Timestamp', inplace=True)
    
    return df

def plot_zscore(df):
    # Calcula el Z-score del spread para N periodos
    rolling_mean = df["spread"].rolling(window=cons.N).mean()
    rolling_std = df["spread"].rolling(window=cons.N).std()
    df["zscore"] = (df["spread"] - rolling_mean) / rolling_std
    df.dropna(subset=["zscore"], inplace=True)


    # Realiza la prueba de Shapiro-Wilk al Zscore del spread para ver si sigue una distribucion nornmal
    normal=False
    # Realiza la prueba de Shapiro-Wilk
    p_value = shapiro(df["spread"].dropna())[1]
    if p_value > 0.05:
        print(f"Los datos pueden seguir una distribución normal con un valor p_value de {p_value}.")
    else:
        print(f"Los datos no siguen una distribución normal con un valor p_value de {p_value}.")

    # Crea una figura y un eje
    fig, ax = plt.subplots(figsize=(10, 6))

    # Grafica el spread
    ax.plot(df["timestamp"], df["spread"], label="Spread", color="blue")

    # Grafica las líneas de Z-score
    ax.axhline(y=0, color="green", linestyle="--", label="Z-score = 0")
    ax.axhline(y=2, color="orange", linestyle="--", label="Z-score = 2")
    ax.axhline(y=-2, color="red", linestyle="--", label="Z-score = -2")

    # Etiquetas y título
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Valor")
    ax.set_title("Spread VS Z-score del Spread")

    # Leyenda
    ax.legend()

    # Muestra el gráfico
    plt.show()