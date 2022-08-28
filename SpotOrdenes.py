from Binance import Binance
from SpotConsultas import SpotConsultas as Consultas
import requests
import json

class SpotOrdenes(Binance):
    def __init__(self):
        Binance.__init__(self)

    def ComprarMarket(self, simbolo: str, inversion: float):
            
        endPoint = self.url + "/api/v3/order"
        simbolo = simbolo.upper()
        
        c = Consultas()
        precio = c.ObtenerPrecio(simbolo)
        
        if simbolo == "ETHUSDT":    
            cantidad = round(inversion/float(precio),4)
        if simbolo == "SOLUSDT":
            cantidad = round(inversion/float(precio),2)
        if simbolo == "ADAUSDT":
            cantidad = round(inversion/float(precio),1)
        if simbolo == "XRPUSDT":
            cantidad = round(inversion/float(precio),0)
        if simbolo == "BTCUSDT":
            cantidad = round(inversion/float(precio),5)        
            
        parametro = "symbol=" + simbolo
        parametro += "&side=BUY"
        parametro += "&type=MARKET"
        parametro += "&quantity=" + str(cantidad)
        parametro += "&timestamp=" + str(self.ObtenerFechaServer())
        
        parametro = self.Firmar(parametro)
        h = self.Encabezados()
        
        r = requests.post(endPoint, params=parametro, headers=h)
        return r.json()

    def VenderMarket(self, simbolo:str, cantidad:float) -> dict:
        
        endPoint = self.url + "/api/v3/order"
        parametro = "timestamp=" + str(self.ObtenerFechaServer())
        parametro += "&symbol=" + simbolo.upper() 
        parametro += "&side=SELL"
        parametro += "&type=MARKET"
        parametro += "&quantity=" + str(cantidad)

        parametro = self.Firmar(parametro)
        h = self.Encabezados()
        
        r = requests.post(endPoint, params=parametro, headers=h)
        return r.json()
