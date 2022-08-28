import hashlib
import Configuracion
import requests
import json
import hmac
from datetime import datetime

class Binance:

    apiKey = ""
    secretKey = ""
    url = ""     

    def __init__(self):
        self.apiKey     = Configuracion.API_KEY
        self.secretKey  = Configuracion.SECRET_KEY
        self.url        = "https://api.binance.com"

    def ObtenerFechaServer(self) -> int:
        endPoint = self.url + "/api/v3/time"
        r = requests.get(endPoint)
        resp = r.json()
        return resp['serverTime']

    def Firmar(self, parametros:str) -> str:
        m = hmac.new(self.secretKey.encode('utf-8'), parametros.encode('utf-8'), hashlib.sha256)
        return parametros + "&signature=" + m.hexdigest()

    def Encabezados(self) -> dict:
        if self.apiKey:
            assert self.apiKey
            headers = {
                'X-MBX-APIKEY': self.apiKey
            }
        return headers
    
    def InformacionExchange(self, simbolo: str):
        endPoint = self.url + "/api/v3/exchangeInfo"
        parametro = "symbol=" + simbolo.upper()
        r = requests.get(endPoint, parametro)
        return r.json()
        
    
    def Log(self, texto: str):
        f = open("Ordenes.log", "a")  
        f.write(datetime.now().strftime("%d/%m/%Y  %H:%M:%S")+ " ->" + texto + "\n")
        f.close()
