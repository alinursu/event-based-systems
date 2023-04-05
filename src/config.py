import datetime

# Numarul de publicatii & subscriptii care vor fi generate
number_of_pubs = 100000
number_of_subs = 100000

# Numarul de thread-uri care vor fi folosite pentru generarea datelor
number_of_threads = 4

# Valori posibile pentru fiecare camp
possible_values = {
    "stationid": [val for val in range(1, 11)],
    "city": ["Bucuresti", "Iasi", "Cluj-Napoca", "Constanta", "Brasov", "Braila", "Galati", "Suceava"],
    "direction": ["N", "NE", "E", "SE", "S", "SV", "V", "NV"],
    "date": [datetime.date(2023, 3, i) for i in range(1, 31)],
    "temp": {"min": -20, "max": 40},
    "rain": {"min": 0, "max": 1.0},
    "wind": {"min": 1, "max": 140},
    "operators": ['>', '>=', '<', '<=', '=']
}

# Ponderea frecventelor campurilor din subscriptii
freq_dict = {
    'city': 50,
    'city_operator': 10,
    'temp': 35,
    'temp_operator': 5,
    'rain': 20,
    'rain_operator': 3,
    'wind': 40,
    'wind_operator': 30
}
