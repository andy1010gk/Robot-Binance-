from SpotConsultas import SpotConsultas as Consultas
from SpotOrdenes import SpotOrdenes as Ordenes
from Binance import Binance
from Estrategia import Estrategia
import pandas as pd
import json

class SpotBot(Binance):
    
    orden = ""
    ticker = ""
    
    def __init__(self):
        Binance.__init__(self)
        
    def ObtenerComando(self, texto: str):
        compra = ["comprar", "compra", "buy", "long"]
        venta = ["vender", "venta", "sell", "short"]
        
        if texto.lower() in compra:
            return "Comprar"
        if texto.lower() in venta:
            return "Vender"
        
        
    def ObtenerTicker(self, texto: str) -> str:
        ticker = texto.upper()
        if "PERP" in ticker:
            ticker = ticker.replace('PERP', '')
        if "USDT" not in ticker:
            ticker += "USDT"
        return ticker
        
        
    def Desglozar(self, mensaje: str) -> list:
        x = mensaje.split()
        self.orden = self.ObtenerComando(x[0])
        self.ticker = self.ObtenerTicker(x[1])
        
        
    def ObtenerInversiones(self, ticker: str) -> float:
        f = open("Cantidades.json", "r")
        inversiones = json.load(f)
        f.close()
        
        if ticker in inversiones:
            return inversiones[ticker]
        if ticker not in inversiones:
            return 0.0

    def Entrar(self, simbolos:list, lengh:str ,num_compras:int) -> bool:
        
        e = Estrategia()
        mensajes = e.Mensajes(simbolos, lengh)
        
        # Se crea una base de datos que contiene todas las ordenes
        ordenes = pd.DataFrame([],columns=['simbolo','precio','cantidad','inversion']) 
        
        for i in range(0,len(mensajes)):
                     
            #Desglozar el mensaje
            self.Desglozar(mensajes[i])
            
            #Obtener la cantidad a operar según el ticket
            inversion = self.ObtenerInversiones(self.ticker)
            
            #Se obtiene la máximo cantidad de inversión posible
            max_inversion = inversion*num_compras
            
            o = Ordenes()
            c = Consultas()
                
            # Se configura la estrategia
            if self.orden == "Comprar" and ordenes.loc[ordenes['simbolo'] == self.ticker, 'inversion'].sum() <=max_inversion:
                compra = o.ComprarMarket(self.ticker, inversion)
                self.Log("Se compra" + self.ticker + " Cant:" + str(inversion))
                    
                # Se extrae el precio, cantidad y simbolo de la transacción.
                precio_compra = float(compra['fills'][0]['price'])
                cantidad_compra = float(compra['fills'][0]['qty'])
                ordenes = ordenes.append(pd.DataFrame([self.ticker,precio_compra, cantidad_compra,inversion],columns=['simbolo','precio','cantidad','inversion']))
                    
                    
            if self.orden == "Vender":
                    
                for j in range(0,len(ordenes)):
                    if self.ticker == ordenes.iloc[j]['simbolo'] and c.ObtenerPrecio(self.ticker) > ordenes.iloc[j]['precio']:
                        o.VenderMarket(self.ticker, ordenes.iloc[j]['cantidad'])
                        self.Log("Se vende" + self.ticker + " Cant:" + str(ordenes.iloc[j]['cantidad']))
                     