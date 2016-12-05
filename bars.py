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
    closest_distance = float('inf')  # Формула гаверсинуса en.wikipedia.org/wiki/Haversine_formula
    bar_name = ''
    for bar in data:
        bar_longitude = bar['Cells']['geoData']['coordinates'][0]
        bar_latitude = bar['Cells']['geoData']['coordinates'][1]
        sin1 = sin((bar_latitude - latitude) / 2)
        sin2 = sin((bar_longitude - longitude) / 2)
        curr_bar_distance = 2 * earth_radius * asin((sin1 ** 2 + sin2 ** 2 * cos(bar_latitude) * cos(latitude)) ** 0.5)
        if curr_bar_distance < closest_distance:
            bar_name = bar['Cells']['Name']
            closest_distance = curr_bar_distance
    return bar_name


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

    current_longitude = args.longitude  # 55.0000
    current_latitude = args.latitude   # 37.4000

    print('Ближайший бар - {0}'.format(get_closest_bar(bars, current_longitude, current_latitude)))
