# -*- coding: utf-8 -*-

import json
import urllib3
import argparse
from math import sin, cos, asin

DATA_MOS_API_KEY = 'cd16cc87e94f1bfce95ed5c26d769a2a'

"""
http://data.mos.ru/opendata/7710881420-bary
Требуется скачать спиок московских баров в формате json и написать скрипт, который рассчитает:
    самый большой бар;
    самый маленький бар;
    самый близкий бар (текущие gps-координаты ввести с клавиатуры).
"""

"""
лишние файлы в репозитории, почитай доку по git

оставь в коде ссылку на описание алгоритма расчета расстояния

Используй встроенные функции Python. Документация. (min max для поиска всех трех баров).
"""


def load_data(filepath):
    http = urllib3.PoolManager()
    response = http.request('GET', filepath).data.decode('utf-8')
    return json.loads(response)


def get_biggest_bar(data):
    biggest_bar = max(data, key=lambda bar: bar['Cells']['SeatsCount'])
    return biggest_bar['Cells']['Name']


def get_smallest_bar(data):
    smallest_bar = min(data, key=lambda bar: bar['Cells']['SeatsCount'])
    return smallest_bar['Cells']['Name']


def get_closest_bar(data, longitude, latitude):
    earth_radius = 6371  # Earth's radius
    distance = float('inf')  # Формула гаверсинуса en.wikipedia.org/wiki/Haversine_formula
    name = ''
    for bar in data:
        lng1 = bar['Cells']['geoData']['coordinates'][0]
        lat1 = bar['Cells']['geoData']['coordinates'][1]
        sin1 = sin((lat1 - latitude) / 2)
        sin2 = sin((lng1 - longitude) / 2)
        curr_distance = 2 * earth_radius * asin((sin1 ** 2 + sin2 ** 2 * cos(lat1) * cos(latitude)) ** 0.5)
        if curr_distance < distance:
            name = bar['Cells']['Name']
            distance = curr_distance
    return name


if __name__ == '__main__':
    bars = load_data('http://api.data.mos.ru/v1/datasets/1796/rows?')

    print('Самый большой бар - {0}'.format(get_biggest_bar(bars)))
    print('Самый маленький бар - {0}'.format(get_smallest_bar(bars)))

    parser = argparse.ArgumentParser(description='Выводит самый больший и маленький бары,'
                                                 'при введении долготы и широты выводит ближайший бар')
    parser.add_argument('-lng', '--longitude',
                        type=float,
                        help='Долгота')

    parser.add_argument('-lat', '--latitude',
                        type=float,
                        help='Широта')

    args = parser.parse_args()

    lng = args.longitude  # 55.0000
    lat = args.latitude   # 37.4000

    print('Ближайший бар - {0}'.format(get_closest_bar(bars, lng, lat)))
