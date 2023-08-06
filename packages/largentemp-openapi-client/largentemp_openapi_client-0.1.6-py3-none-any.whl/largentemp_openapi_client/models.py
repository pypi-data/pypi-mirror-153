'''models.py
Innehåller modeller (klasser) för temperaturdata, statistik, etc. från API:et.
'''
import datetime, pytz

def datetime_to_human_readable(datetime_obj)->str:
    '''Konverterar en datetime till en sträng som är mänskligt läsbar.'''
    if type(datetime_obj) == datetime.datetime:
        return datetime_obj.strftime("%Y-%M-%d %H:%M")
    else: #Om datumsträngen är None så fångar vi upp det här för att underlätta konvertering etc.
        return "--"

class Timestamp:
    def __init__(self, local_timestamp, server_timestamp, string_timestamp):
        '''Ett objekt som representerar en tidsstämpel för data.'''
        self.local_timestamp = local_timestamp
        self.server_timestamp = server_timestamp
        self.string_timestamp = string_timestamp

class TemperatureData:
    def __init__(self, reading:float, reading_rounded:float, timestamp:Timestamp):
        self.reading = reading
        self.reading_rounded = reading_rounded
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.reading_rounded} grader (uppmätt: {datetime_to_human_readable(self.timestamp.local_timestamp)})"

class Statistics:
    def __init__(self, today_high:TemperatureData, today_low:TemperatureData, today_mean, today_median, value_count_today):
        self.today_high = today_high
        self.today_low = today_low
        self.today_mean = today_mean
        self.today_median = today_median
        self.value_count_today = value_count_today

    def __str__(self):
        return f"""
        Högsta värde för idag: {self.today_high} (uppmätt: {self.today_high.timestamp.local_timestamp})
        Lägsta värde för idag: {self.today_low} (uppmätt: {self.today_low.timestamp.local_timestamp})
        Medianvärde idag: {self.today_median}
        Medelvärde idag: {self.today_mean}
        Antal värden idag: {self.value_count_today}
        """

class ServerResponse:
    def __init__(self, temperaturedata:TemperatureData=None, statistics:Statistics=None, json_data=None):
        '''Huvudklassen för ett serversvar.'''
        self.temperaturedata = temperaturedata
        self.statistics = statistics
        self.json_data = None

    def from_json(self, json_data:dict):
        '''Konverterar JSON från LargenTemp-servern till en temperaturdata-klass.

        :param json_data: JSON-data som en dict såsom den mottagits från servern.

        :returns: Ett ServerResponse-objekt med data ifyllt.'''
        #Hämta först temperaturdata
        self.json_data = json_data
        reading = self.parse_returned_value(json_data["temperaturedata"])
        reading_rounded = round(reading, 1) if reading != None else None
        latest_updated = json_data["latestupdated"]
        reading_local_timestamp = datetime.datetime.fromisoformat(latest_updated["local"]).astimezone(tz=pytz.timezone("Europe/Stockholm"))
        reading_server_timestamp = datetime.datetime.fromisoformat(latest_updated["server"])
        reading_human_readable_timestamp = latest_updated["string"]
        reading_timestamp = Timestamp(reading_local_timestamp,
                                      reading_server_timestamp,
                                      reading_human_readable_timestamp)
        self.temperaturedata = TemperatureData(
            reading,
            reading_rounded,
            reading_timestamp
        )
        #Hämta sedan statistik
        statistics = json_data["statistics"]
        today_high = self.parse_returned_value(statistics["today_high"])
        today_low = self.parse_returned_value(statistics["today_low"])
        today_high_ts = datetime.datetime.fromisoformat(statistics["today_high_ts"]) if today_high != None else None
        today_low_ts = datetime.datetime.fromisoformat(statistics["today_low_ts"]) if today_low != None else None
        today_high_timestamp = Timestamp(
            today_high_ts,
            self.local_time_to_server_time(today_high_ts) if today_high_ts != None else None,
            datetime_to_human_readable(today_high_ts) if today_high_ts != None else None
        )
        today_high_object = TemperatureData(
            today_high,
            round(today_high, 1) if today_high != None else today_high,
            today_high_timestamp
        )
        today_low_timestamp = Timestamp(
            today_low_ts,
            self.local_time_to_server_time(today_low_ts) if today_low_ts != None else None,
            datetime_to_human_readable(today_low_ts) if today_low_ts != None else None
        )
        today_low_object = TemperatureData(
            today_low,
            round(today_low, 1) if today_low != None else today_low,
            today_low_timestamp
        )
        #Hämta övriga statistikvärden
        today_mean = self.parse_returned_value(statistics["today_mean"]) #Medelvärde för dagen
        today_median = self.parse_returned_value(statistics["today_median"]) #Medianvärde för dagen
        today_value_count = self.parse_returned_value(statistics["value_count_today"]) #Antal inrapporterade temperaturvärden för dagen

        self.statistics = Statistics(
            today_high_object,
            today_low_object,
            today_mean,
            today_median,
            today_value_count
        )
        return self

    def parse_returned_value(self, string):
        '''LargenTemps API returnerar antingen "--" eller data
        som har med statistik att göra. Vi skapar därför en funktion
        som klarar av de gångerna då statistik inte finns tillgänglig än
        utan LargenTemps API istället returnerar "--".'''
        if string == "--":
            return None
        elif type(string) != float: #Hantera typkonverteringar
            return float(string)
        else:
            return string

    def local_time_to_server_time(self, datetime_obj:datetime.datetime)->datetime.datetime:
        '''Konverterar en datetime som är i lokal tid till servertid (servertid som i tiden som LargenTemps server har).
        Detta eftersom alla delar av API:et inte returnerar det. (Servern har tidszonen UTC)

        :param datetime_obj: Datetime-objektet att konvertera.'''
        return datetime_obj.astimezone(tz=pytz.timezone("UTC"))

    def __str__(self):
        return f"{self.temperaturedata}\n{self.statistics}"
