import datetime


class Publication:
    stationid: int = 0
    city: str = ""
    temp: int = 0
    rain: float = 0
    wind: int = 0
    direction: str = 0
    date: datetime.date = datetime.date.today()

    def __init__(self, stationid: int = 0, city: str = "", temp: int = 0, rain: float = 0, wind: int = 0,
                 direction: str = 0, date: datetime.date = datetime.date.today()):
        self.stationid = stationid
        self.city = city
        self.temp = temp
        self.rain = rain
        self.wind = wind
        self.direction = direction
        self.date = date

    def __str__(self):
        return "Publication(stationid=%s, city=%s, temp=%s, rain=%s, wind=%s, direction=%s, date=%s)" % \
               (str(self.stationid), self.city, str(self.temp), str(self.rain), str(self.wind), self.direction,
                str(self.date))

    def __repr__(self):
        return "Publication(stationid=%s, city=%s, temp=%s, rain=%s, wind=%s, direction=%s, date=%s)" % \
               (str(self.stationid), self.city, str(self.temp), str(self.rain), str(self.wind), self.direction,
                str(self.date))

    def to_csv_row(self) -> list:
        return [
            str(self.stationid), self.city, str(self.temp), str(self.rain), str(self.wind), self.direction,
            str(self.date)
        ]
