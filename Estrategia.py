from Binance import Binance
from SpotConsultas import SpotConsultas as Consultas
import tti


class Estrategia(Binance):
    def __init__(self):
        Binance.__init__(self)
        
    def Mensajes(self, simbolos: list, lengh: str):
        
        c = Consultas()
        mensajes = []
        
        for i in range(0,len(simbolos)):
                     
            # Se consulta información de velas
            velas = c.ObtenerInfoVelas(simbolos[i],lengh)
            
            #-----------------------------------------------------------------#            
            # Se obtiene indicadores financieros
            #-----------------------------------------------------------------#
           
            # Se muestra el indicador EMA200 
            ema200 = tti.indicators.MovingAverage(input_data=velas, period=200, ma_type='exponential').getTiData()
            
            '''
            # Se identifica un patron de subida/bajada/horizontal
            patron = pd.DataFrame(data=[velas.iloc[-15:]['low'],ema200.iloc[-15:]['ma-exponential']]).transpose()
            patron.columns = ['precios_low','emas200']
            patron['dif'] = patron['precios_low']-patron['emas200']
            
            patron.loc[patron.dif >= 0, 'ind_patron'] = 1
            patron.loc[patron.dif < 0, 'ind_patron'] = 0
            '''
        
            # Bandas de Bollinger
            bandas_bolinger = tti.indicators.BollingerBands(input_data=velas).getTiData()
            
            # Estocastico 
            estocastico = tti.indicators.StochasticOscillator(input_data=velas, k_slowing_periods = 3).getTiData()

            # Se crea las señales de compra y venta
            k = estocastico.iloc[-1,0]
            d = estocastico.iloc[-1,1]
            min_precio =  velas["low"].iloc[-1]
            max_precio =  velas["high"].iloc[-1]
            bandas_upper = bandas_bolinger["upper_band"].iloc[-1]
            bandas_lower = bandas_bolinger["lower_band"].iloc[-1]
            
            # Orden de compra
            if k == d and k < 20 and d < 20 and min_precio == bandas_lower:
                
                mensaje_temp = 'Compra ' + simbolos[i] 
                mensajes.append(mensaje_temp) 
            
            # Orden de venta
            if k == d and k > 80 and d > 80 and max_precio == bandas_upper:
                
                mensaje_temp = 'Vender ' + simbolos[i] 
                mensajes.append(mensaje_temp)           
        
        return mensajes
        