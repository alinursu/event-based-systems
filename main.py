import csv
import datetime
import random

from Publication import Publication

# =============================
# ======== CONFIGURARE ========
# =============================
# Numarul de publicatii & subscriptii care vor fi generate

number_of_pubs = 10000
number_of_subs = 0

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

# ========================
# ======== EXPORT ========
# ========================
# Publicatii in CSV
with open("publicatii.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["stationid", "city", "temp", "rain", "wind", "direction", "date"])
    writer.writerows([pub.to_csv_row() for pub in pubs])

# Subscriptii in CSV
