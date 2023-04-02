import math
import random

from src.Subscription import Subscription
from src.config import freq_dict as freq_dict_config, possible_values
from src.utils import copy_dict


def is_valid_freq(freq_value: int) -> bool:
    """
    Verifica daca valoarea unei frecvente este valida: nu este None, este de tipul int si are o valoare pozitiva.

    :param freq_value: Valoarea frecventei, cea care va fi verificata.
    :return: True, daca indeplineste conditiie; False, altfel.
    """

    return freq_value is not None and type(freq_value) == int and freq_value >= 0


def check_freq_dict_params(freq_dict: dict):
    """
    Verifica daca parametrii din freq_dict sunt valizi. Daca sunt valizi (nu sunt None, sunt de tipul int si au valori
    pozitive), ii pastreaza; altfel, li se va seta valoarea 0.

    :param freq_dict: Dictionarul cu frecventele campurilor.
    """

    freq_dict = {
        'city': freq_dict['city'] if is_valid_freq(freq_dict['city']) else 0,
        'city_operator': freq_dict['city_operator'] if is_valid_freq(freq_dict['city']) and
                                                       is_valid_freq(freq_dict['city_operator']) else 0,
        'temp': freq_dict['temp'] if is_valid_freq(freq_dict['temp']) else 0,
        'temp_operator': freq_dict['temp_operator'] if is_valid_freq(freq_dict['temp']) and
                                                       is_valid_freq(freq_dict['temp_operator']) else 0,
        'rain': freq_dict['rain'] if is_valid_freq(freq_dict['rain']) else 0,
        'rain_operator': freq_dict['rain_operator'] if is_valid_freq(freq_dict['rain']) and
                                                       is_valid_freq(freq_dict['rain_operator']) else 0,
        'wind': freq_dict['wind'] if is_valid_freq(freq_dict['wind']) else 0,
        'wind_operator': freq_dict['wind_operator'] if is_valid_freq(freq_dict['wind']) and
                                                       is_valid_freq(freq_dict['wind_operator']) else 0,
    }


def normalize_frequency_dict(number_of_subs: int, freq_dict: dict):
    """
    Normalizeaza valorile dictionarului cu frecvente prin transformarea frecventelor din procente in numarul exact
    de subscriptii (de exemplu: daca totalul subscriptiilor este 10000, iar frecventa campului "city" este de 30%,
    atunci 30*10000/100 = 3000 de subscriptii vor avea acel camp).

    :param freq_dict: Dictionarul cu frecventele campurilor.
    :param number_of_subs: Numarul de subscriptii care vor fi generate
    """

    # Normalizam fiecare frecventa
    for key, value in freq_dict.items():
        freq_dict[key] = round(value * number_of_subs / 100)

    # Normalizam frecventa operatorilor
    freq_dict['city_operator'] = round(freq_dict['city_operator'] * freq_dict['city'] / number_of_subs)
    freq_dict['temp_operator'] = round(freq_dict['temp_operator'] * freq_dict['temp'] / number_of_subs)
    freq_dict['rain_operator'] = round(freq_dict['rain_operator'] * freq_dict['rain'] / number_of_subs)
    freq_dict['wind_operator'] = round(freq_dict['wind_operator'] * freq_dict['wind'] / number_of_subs)


def generate_sub_with_city(freq_dict: dict):
    """
    Genereaza o subscriptie care va avea valoare doar pe campul "city".

    :param freq_dict: Dictionarul cu frecventele campurilor.
    :return: Subscriptia generata.
    """

    city = random.choice(possible_values['city'])

    city_operator = None
    if freq_dict['city_operator'] > 0:
        city_operator = random.choice(possible_values['operators'])
        freq_dict['city_operator'] = freq_dict['city_operator'] - 1

    return Subscription(city=city, city_operator=city_operator)


def generate_sub_with_temp(freq_dict: dict):
    """
    Genereaza o subscriptie care va avea valoare doar pe campul "temp".

    :param freq_dict: Dictionarul cu frecventele campurilor.
    :return: Subscriptia generata.
    """

    temp = random.randint(possible_values['temp']['min'], possible_values['temp']['max'])

    temp_operator = None
    if freq_dict['temp_operator'] > 0:
        temp_operator = random.choice(possible_values['operators'])
        freq_dict['temp_operator'] = freq_dict['temp_operator'] - 1

    return Subscription(temp=temp, temp_operator=temp_operator)


def generate_sub_with_rain(freq_dict: dict):
    """
    Genereaza o subscriptie care va avea valoare doar pe campul "rain".

    :param freq_dict: Dictionarul cu frecventele campurilor.
    :return: Subscriptia generata.
    """

    rain = round(random.uniform(possible_values['rain']['min'], possible_values['rain']['max']), 2)

    rain_operator = None
    if freq_dict['rain_operator'] > 0:
        rain_operator = random.choice(possible_values['operators'])
        freq_dict['rain_operator'] = freq_dict['rain_operator'] - 1

    return Subscription(rain=rain, rain_operator=rain_operator)


def generate_sub_with_wind(freq_dict: dict):
    """
    Genereaza o subscriptie care va avea valoare doar pe campul "wind".

    :param freq_dict: Dictionarul cu frecventele campurilor.
    :return: Subscriptia generata.
    """

    wind = random.randint(possible_values['wind']['min'], possible_values['wind']['max'])

    wind_operator = None
    if freq_dict['wind_operator'] > 0:
        wind_operator = random.choice(possible_values['operators'])
        freq_dict['wind_operator'] = freq_dict['wind_operator'] - 1

    return Subscription(wind=wind, wind_operator=wind_operator)


def normalize_subs_to_match_set_total_number(subs_with_city: [Subscription], subs_with_temp: [Subscription],
                                             subs_with_rain: [Subscription], subs_with_wind: [Subscription],
                                             number_of_subs: int, freq_dict: dict) \
        -> [Subscription]:
    """
    Normalizeaza subscriptiile generate astfel incat numarul total va fi egal cu numarul total setat in
    src.config.number_of_subs.

    In cazul in care am generat mai multe subscriptii decat trebuia, atunci voi calcula numarul extra de subscriptii,
    le voi extrage din liste si le voi combina cu alte subscriptii care nu au deja setate valori pentru acel camp (spre
    exemplu, daca am o subscriptie cu o valoare setata pentru campul "city", nu o voi combina cu o alta subscriptie
    care are o valoare setata pentru campul "city" deoarece se vor suprascrie una pe cealalta).

    La final, combina listele primite ca si parametru intr-o singura lista cu subscriptii.

    :param subs_with_city: Lista cu subscriptii care au setate campul "city".
    :param subs_with_temp: Lista cu subscriptii care au setate campul "temp".
    :param subs_with_rain: Lista cu subscriptii care au setate campul "rain".
    :param subs_with_wind: Lista cu subscriptii care au setate campul "wind".
    :param number_of_subs: Numarul total de subscriptii care (ar trebui) sa fi fost generate.
    :param freq_dict: Dictionarul cu frecventele campurilor.
    :return: Lista agregata de subscriptii.
    """

    total_generated_subs = len(subs_with_city) + len(subs_with_temp) + len(subs_with_rain) + len(subs_with_wind)
    if total_generated_subs > number_of_subs:
        # Daca numarul total de subscriptii generate depaseste numarul setat de subscriptii, atunci trebuie sa
        # le combin

        # Calculez numarul de subscriptii extra din fiecare lista
        difference = total_generated_subs - number_of_subs

        number_of_sub_attributes_with_freq = 0
        if freq_dict['city'] > 0:
            number_of_sub_attributes_with_freq += 1

        if freq_dict['temp'] > 0:
            number_of_sub_attributes_with_freq += 1

        if freq_dict['rain'] > 0:
            number_of_sub_attributes_with_freq += 1

        if freq_dict['wind'] > 0:
            number_of_sub_attributes_with_freq += 1

        extra_subs_in_each_list = math.ceil(difference / number_of_sub_attributes_with_freq)

        # Extrag subscriptiile extra intr-o lista noua
        extra_subs: [Subscription] = []

        extra_subs.extend(subs_with_city[:extra_subs_in_each_list])
        subs_with_city = subs_with_city[extra_subs_in_each_list:]

        extra_subs.extend(subs_with_temp[:extra_subs_in_each_list])
        subs_with_temp = subs_with_temp[extra_subs_in_each_list:]

        extra_subs.extend(subs_with_rain[:extra_subs_in_each_list])
        subs_with_rain = subs_with_rain[extra_subs_in_each_list:]

        extra_subs.extend(subs_with_wind[:extra_subs_in_each_list])
        subs_with_wind = subs_with_wind[extra_subs_in_each_list:]

        # Agregarea listelor
        subs: [Subscription] = []
        subs.extend(subs_with_city)
        subs.extend(subs_with_temp)
        subs.extend(subs_with_rain)
        subs.extend(subs_with_wind)

        # Combinarea subscriptiilor
        for index, sub in enumerate(extra_subs):
            left_extra_subs = len(extra_subs) - index
            total_subs_if_all_extra_subs_would_be_uncombined = len(subs) + left_extra_subs

            if total_subs_if_all_extra_subs_would_be_uncombined == number_of_subs:
                # Daca numarul total de subscriptii actuale (din toate listele) este egal cu numarul tinta de
                # subscriptii, opresc procesul de combinare
                subs.extend(extra_subs[index:])
                break

            # Aleg o subscriptie in care voi insera datele
            sub_to_insert_into = None
            while sub_to_insert_into is None:
                sub_to_insert_into = random.choice(subs)

                if (sub.city is not None and sub_to_insert_into.city is not None) or \
                        (sub.temp is not None and sub_to_insert_into.temp is not None) or \
                        (sub.rain is not None and sub_to_insert_into.rain is not None) or \
                        (sub.wind is not None and sub_to_insert_into.wind is not None):
                    # Cazul in care as suprascrie valoarea din subscriptie
                    sub_to_insert_into = None

            # Combin cele doua subscriptii intr-una singura
            subs.remove(sub_to_insert_into)
            if sub.city is not None:
                sub_to_insert_into.city = sub.city

            if sub.temp is not None:
                sub_to_insert_into.temp = sub.temp

            if sub.rain is not None:
                sub_to_insert_into.rain = sub.rain

            if sub.wind is not None:
                sub_to_insert_into.wind = sub.wind

            subs.append(sub_to_insert_into)

        return subs
    else:
        # Agregarea listelor
        subs: [Subscription] = []
        subs.extend(subs_with_city)
        subs.extend(subs_with_temp)
        subs.extend(subs_with_rain)
        subs.extend(subs_with_wind)
        return subs


def generate_subs(number_of_subs: int) -> [Subscription]:
    """
    Genereaza o lista de subscriptii in functie de parametrii setati in src.config.freq_dict.

    :param number_of_subs: Numarul de subscriptii care vor fi generate.
    :return: Lista de subscriptii generata.
    """

    freq_dict = copy_dict(freq_dict_config)

    # Verificam parametrii din freq_dict
    check_freq_dict_params(freq_dict)

    # Normalizam valorile din freq_dict
    normalize_frequency_dict(number_of_subs, freq_dict)

    # Afisarea dictionarului de frecvente
    # print(freq_dict)

    # Generarea subscriptiilor
    subs_with_city: [Subscription] = [generate_sub_with_city(freq_dict) for i in range(0, freq_dict['city'])]
    subs_with_temp: [Subscription] = [generate_sub_with_temp(freq_dict) for i in range(0, freq_dict['temp'])]
    subs_with_rain: [Subscription] = [generate_sub_with_rain(freq_dict) for i in range(0, freq_dict['rain'])]
    subs_with_wind: [Subscription] = [generate_sub_with_wind(freq_dict) for i in range(0, freq_dict['wind'])]

    # Intercalarea subscriptiilor (daca suma frecventelor initiale ale campurilor este > 100)
    subs = normalize_subs_to_match_set_total_number(
        subs_with_city, subs_with_temp, subs_with_rain, subs_with_wind, number_of_subs, freq_dict
    )

    return subs
