from Binance import Binance
from SpotBot import SpotBot as bot


b = bot()


simbolos = ['ETHUSDT','SOLUSDT','ADAUSDT','XRPUSDT']
periodo ='15m'
num_compras = 2


b.Entrar(simbolos, periodo, num_compras)