import json
import urllib3
import argparse
from math import sin, cos, asin


def load_data(url):
    if url is None:
        return None
    http = urllib3.PoolManager()
    response = http.request('GET', url).data.decode('utf-8')
    return json.loads(response)


def get_biggest_bar(data):
    biggest_bar = max(data, key=lambda bar: bar['Cells']['SeatsCount'])
    return biggest_bar['Cells']['Name']


def get_smallest_bar(data):
    smallest_bar = min(data, key=lambda bar: bar['Cells']['SeatsCount'])
    return smallest_bar['Cells']['Name']


def get_closest_bar(data, longitude, latitude):
    earth_radius = 6371
    closest_distance = float('inf')
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


def main(longitude, latitude):
    bars = load_data('http://api.data.mos.ru/v1/datasets/1796/rows?')
    print('Самый большой бар - {0}'.format(get_biggest_bar(bars)))
    print('Самый маленький бар - {0}'.format(get_smallest_bar(bars)))
    print('Ближайший бар - {0}'.format(get_closest_bar(bars, longitude, latitude)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Выводит самый больший и маленький бары,'
                                                 'при введении долготы и широты выводит ближайший бар')

    parser.add_argument('-lng', '--longitude',  # 55.0000
                        type=float,
                        help='Долгота',
                        required=True)

    parser.add_argument('-lat', '--latitude',  # 37.4000
                        type=float,
                        help='Широта',
                        required=True)

    args = parser.parse_args()
    main(args.longitude, args.latitude)
