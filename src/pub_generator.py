import random

from src.Publication import Publication
from src.config import possible_values


def generate_pub() -> Publication:
    """
    Genereaza un obiect Publication prin alegerea unor valori random, folosing distributia uniform, din valorile predefinite in src.config.possible_values.

    :return: Publicatia generata.
    """

    stationid = round(random.uniform(possible_values['stationid'][0], possible_values['stationid'][-1]))
    city = random.choice(possible_values['city'])
    direction = random.choice(possible_values['direction'])
    date = random.choice(possible_values['date'])
    temp = round(random.uniform(possible_values['temp']['min'], possible_values['temp']['max']))
    rain = round(random.uniform(possible_values['rain']['min'], possible_values['rain']['max']), 2)
    wind = round(random.uniform(possible_values['wind']['min'], possible_values['wind']['max']))

    return Publication(stationid, city, temp, rain, wind, direction, date)
