from Binance import Binance
import requests
import pandas as pd
import json

class SpotConsultas(Binance):

    def __init__(self):
        Binance.__init__(self)

    def ObtenerOperaciones(self, simbolo: str, limite: int =500):
        endPoint = self.url + "/api/v3/trades"
        parametro = "symbol=" + simbolo.upper()
        if limite != 500 and limite <= 1000 and limite > 0:
            parametro += "&limit=" + str(limite)
        r = requests.get(endPoint, parametro)
        return r.json()

    def ObtenerInfoVelas(self, simbolo: str, periodo: str, limite: int = 500):
        endPoint = self.url + "/api/v3/klines"
        parametro = "symbol=" + simbolo.upper()
        parametro += "&interval=" + periodo
        if limite != 500 and limite <= 1000 and limite > 0:
            parametro += "&limit=" + str(limite) 
        r = requests.get(endPoint, parametro)
        r = r.json()

        # Se expresa en una base de datos

        df = pd.DataFrame(r, columns= ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time','Quote asset volume',
        'Number of trades','Taker volume', 'Maker volume', 'Ignore'])

        df = df.drop(['Ignore','Open time'],1)

        # Se da formato de los datos
        df['DateTime'] = pd.DatetimeIndex(pd.to_datetime(df['Close time'], unit='ms', utc=True))
        df['Open'] = df['Open'].astype('float')
        df['High'] = df['High'].astype('float')
        df['Low'] = df['Low'].astype('float')
        df['Close'] = df['Close'].astype('float')
        df['Volume'] = df['Volume'].astype('float')
        df['Close time'] = pd.DatetimeIndex(pd.to_datetime(df['Close time'], unit='ms', utc=True))
        df['Quote asset volume'] = df['Quote asset volume'].astype('float')
        df['Number of trades'] = df['Number of trades'].astype('float')
        df['Taker volume'] = df['Taker volume'].astype('float')
        df['Maker volume'] = df['Maker volume'].astype('float')

        df = df.set_index('DateTime')
        return df

    def ObtenerPrecio(self, simbolo: str)-> float:
        o = self.ObtenerOperaciones(simbolo.upper(), 1)
        return float(o[0]["price"])

    def ObtenerCuenta(self):
        endPoint = self.url + "/api/v3/account"
        parametro = "timestamp=" + str(self.ObtenerFechaServer())
        parametro = self.Firmar(parametro)
        h = self.Encabezados()
        r = requests.get(endPoint, params=parametro, headers= h)
        return r.json()

    def ObtenerOrdenes(self, simbolo: str):
        endPoint = self.url + "/api/v3/allOrders"
        parametro = "timestamp=" + str(self.ObtenerFechaServer())
        parametro += "&symbol=" + simbolo.upper() 
        parametro = self.Firmar(parametro)
        h = self.Encabezados()
        r = requests.get(endPoint, params=parametro, headers= h)
        return r.json()

