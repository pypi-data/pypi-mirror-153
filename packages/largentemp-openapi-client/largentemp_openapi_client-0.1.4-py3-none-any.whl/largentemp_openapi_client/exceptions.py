'''exceptions.py
Innehåller anpassade modeller för felmeddelanden.
'''
class TemperatureDataNotFoundException(Exception):
    pass

class RateLimitedException(Exception):
    pass

class UnknownAPIResponse(Exception):
    pass
