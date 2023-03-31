class Subscription:
    city: str = None
    city_operator: str = None
    temp: int = None
    temp_operator: str = None
    rain: float = None
    rain_operator: str = None
    wind: int = None
    wind_operator: str = None

    def __init__(self, city: str = None, city_operator: str = None,
                 temp: int = None, temp_operator: str = None,
                 rain: float = None, rain_operator: str = None,
                 wind: int = None, wind_operator: str = None):
        self.city = city
        self.city_operator = city_operator
        self.temp = temp
        self.temp_operator = temp_operator
        self.rain = rain
        self.rain_operator = rain_operator
        self.wind = wind
        self.wind_operator = wind_operator

    def to_row(self):
        values: [str] = []

        if self.city is not None:
            if self.city_operator is not None:
                values.append(f"(city, {self.city_operator}, \"{self.city}\")")
            else:
                values.append(f"(city, \"{self.city}\")")

        if self.temp is not None:
            if self.temp_operator is not None:
                values.append(f"(temp, {self.temp_operator}, {self.temp})")
            else:
                values.append(f"(temp, {self.temp})")

        if self.rain is not None:
            if self.rain_operator is not None:
                values.append(f"(rain, {self.rain_operator}, {self.rain})")
            else:
                values.append(f"(rain, {self.rain})")

        if self.wind is not None:
            if self.wind_operator is not None:
                values.append(f"(wind, {self.wind_operator}, {self.wind})")
            else:
                values.append(f"(wind, {self.wind})")

        text = ""
        for i in range(0, len(values) - 1):
            text += values[i] + ";"

        text += values[len(values) - 1]

        return "{" + text + "}"
