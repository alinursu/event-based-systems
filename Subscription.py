class Subscription:
    city: str = None
    city_operator = None
    temp: int = None
    rain: float = None
    wind: int = None

    def __init__(self, city: str = None, city_operator: str = None, temp: int = 0, rain: float = None,
                 wind: int = None):
        self.city = city
        self.city_operator = city_operator
        self.temp = temp
        self.rain = rain
        self.wind = wind
