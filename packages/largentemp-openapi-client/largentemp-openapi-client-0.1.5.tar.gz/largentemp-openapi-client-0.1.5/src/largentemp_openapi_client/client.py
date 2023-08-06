'''client.py
Innehåller LargenTemps API-klient.
'''
import requests, logging
from .models import *
from .exceptions import *

class Client:
    def __init__(self):
        '''Initierar en LargenTemp API-klient.'''
        #Skapa en logger
        self.logger = logging.getLogger(__name__)

    def get_data(self):
        '''Hämtar temperaturdata från LargenTemp.'''
        request = requests.get("https://largentemp.pythonanywhere.com/openapi",
                                   headers={
                                       "User-Agent": "Python/LargenTempClient"
                                   })
        self.logger.debug(f"Förfrågning till LargenTemp skickad. Svar: {request.content}")
        #Konvertera till svar
        if request.status_code == 200:
            server_response = ServerResponse()
            server_response.from_json(request.json())
            self.logger.debug("Svar hanterat. Returnerar...")
            return server_response
        elif request.status_code == 429:
            raise RateLimitedException("Ett fel inträffade: du har blivit förfrågningslimiterad (rate-limited) från API:et.")
        else:
            raise UnknownAPIResponse(f"Ett fel inträffade: ohanterad statuskod från API-et returnerades ({request.status_code})")
