def get_tickers():
    '''Devuelve una serie con los simbolos de tickers que cotizan en ARG
    '''
    import pandas as pd
    df = pd.read_csv('Tickers yfinance.csv')
    return df['Symbol']

def get_data(symbols, *args, **kwargs):
    '''
    Devuelve un dataframe con la serie de tiempo de los precios de los tickers. 
    Para ver los tickers que cotizan en ARG, usar get_tickers().
    Se puede usar para tickers no argentinos.
    
    La moneda depende del ticker según Yahoo Finance, revisar el ticker en https://finance.yahoo.com/.
    
    Parametros:
        @symbols : string, objeto tipo array (list, tuple, Series), o DataFrame. Símbolo de uno o varios tickers en string (se pueden separar por ","), lista o Serie.
    
    Kwargs:
        @start : string, int, date, datetime, Timestamp
            Fecha de inicio de la serie. Acepta distintos formatos (i.e., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980'). 
            Default: fecha de inicio del ticker
        @end : string, int, date, datetime, Timestamp
            Fecha de final de la serie. Acepta distintos formatos (i.e., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980').
            Default: última fecha del ticker
        @interval : string, default 'd'. Intervalo de tiempo, ('d' para diario, 'w' para semanal, 'm' para mensual)
        @get_actions : bool, default False
            Si es True, agrega las columnas 'Dividend' y 'Split' al dataframe.
        @adjust_dividends: bool, default True
            Si es True, ajusta los dividendos según los splits.
        @adjust_price : bool, default False.
            Si es True, ajusta todos los precios ('Open', 'High', 'Low', 'Close') basándose en 'Adj Close'. Agrega la columna 'Adj_Ratio' y dropea 'Adj Close'.
    '''
    import yfinance as yf
    import pandas_datareader as pdr
    yf.pdr_override()
    
    data = pdr.get_data_yahoo(symbols, *args, **kwargs)
    return data