import csv
import datetime
import random

import Subscription
from Publication import Publication

# =============================
# ======== CONFIGURARE ========
# =============================
# Numarul de publicatii & subscriptii care vor fi generate

number_of_pubs = 10000
number_of_subs = 10000

# Valori campuri publicatii
possible_values = {
    "stationid": [val for val in range(1, 11)],
    "city": ["Bucuresti", "Iasi", "Cluj-Napoca", "Constanta", "Brasov", "Braila", "Galati", "Suceava"],
    "direction": ["N", "NE", "E", "SE", "S", "SV", "V", "NV"],
    "date": [datetime.date(2023, 3, i) for i in range(1, 31)],
    "temp": {"min": -20, "max": 40},
    "rain": {"min": 0, "max": 1.0},
    "wind": {"min": 1, "max": 140}
}

# Valori operatori subscriptii
# possible_operators = {
#     "city": "=",
#     "direction": "=",
#     "date": [datetime.date(2023, 3, i) for i in range(1, 31)],
#     "temp": ["<", ">", "=", "<=", ">="],
#     "rain": ["<", ">", "=", "<=", ">="],
#     "wind": ["<", ">", "=", "<=", ">="]
# }


# Ponderea frecventelor campurilor din subscriptii

# ==========================
# ======== GENERARE ========
# ==========================
# Generarea publicatiilor
def generate_pub() -> Publication:
    stationid = random.choice(possible_values['stationid'])
    city = random.choice(possible_values['city'])
    direction = random.choice(possible_values['direction'])
    date = random.choice(possible_values['date'])
    temp = random.randint(possible_values['temp']['min'], possible_values['temp']['max'])
    rain = round(random.uniform(possible_values['rain']['min'], possible_values['rain']['max']), 2)
    wind = random.randint(possible_values['wind']['min'], possible_values['wind']['max'])
    return Publication(stationid, city, temp, rain, wind, direction, date)


pubs: [Publication] = []

for i in range(0, number_of_pubs):
    pubs.append(generate_pub())


# Generarea subscriptiilor
# adaugam si restul tipurilor?
def generate_sub(freq_city=None, freq_city_operator=None, freq_temp=None, freq_rain=None, freq_wind=None):
    freq_sum = 0
    freq_dict = {}

    # Verificam daca fiecare parametru este diferit de None si il adaugam la dictionar
    if freq_city:
        freq_dict['city'] = freq_city
        if freq_city_operator:
            freq_dict['city_operator'] = freq_city_operator
    else:
        freq_dict['city_operator'] = 0

    if freq_temp:
        freq_dict['temp'] = freq_temp

    if freq_rain:
        freq_dict['rain'] = freq_rain

    if freq_wind:
        freq_dict['wind'] = freq_wind

    freq_sum = sum(freq_dict.values()) - freq_city_operator

    if freq_sum > 0:
        # Normalizam fiecare frecventa
        for key, value in freq_dict.items():
            freq_dict[key] = round(value * number_of_subs / freq_sum)

    else:
        # Setam toate frecventele la 0 daca suma este 0
        freq_dict = {key: 0 for key in freq_dict}

    if freq_city & freq_city_operator:
        freq_dict['city_operator'] = round(freq_dict['city_operator'] * freq_dict['city'] / number_of_subs)

    #dictionarul cu frecventele normalizate
    print(freq_dict)


generate_sub(50, 1, 30, 20, None)


# ========================
# ======== EXPORT ========
# ========================
# Publicatii in CSV
with open("publicatii.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["stationid", "city", "temp", "rain", "wind", "direction", "date"])
    writer.writerows([pub.to_csv_row() for pub in pubs])

# Subscriptii in CSV
