from logging import warning

try:
    from . import ENGHo
    from . import Series
    from . import EPH
    from . import BancoMundial
    from . import YahooFinance
except ImportError:
    import ENGHo
    import Series
    import EPH
    import BancoMundial
    import YahooFinance

class INDECError(Exception):
    pass

class WaveError(Exception):
    pass

class TrimesterError(Exception):
    pass

class YearError(Exception):
    pass

class AdvertenciaINDEC(Warning):
    pass

class AdvertenciaRegion(Warning):
    pass


eph = EPH
ENGHO = ENGHo
engho = ENGHo
series = Series
TimeSeries = Series
SeriesDeTiempo = Series
series_de_tiempo = Series
time_series = Series
timeseries = Series
BM = BancoMundial
WB = BancoMundial
WorldBank = BancoMundial
banco_mundial = BancoMundial
world_bank = BancoMundial
yfinance = YahooFinance
yf = YahooFinance
YF = YahooFinance
yahoo_finance = YahooFinance



        
