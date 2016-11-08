# Бары!

Бары! - это скрипт, определяющий самый большой и самый маленький бары в 
Москве, основываясь на открытых данных с сайта http://data.mos.ru/.

При введении Ваших текущих gps-координат будет выведен ближайший бар.

Пример использования:
```sh
cd 3_bars
usage: bars.py [-h] [-lng LONGITUDE] [-lat LATITUDE]

Выводит самый больший и маленький бары,при введении долготы и широты выводит
ближайший бар

optional arguments:
  -h, --help            show this help message and exit
  -lng LONGITUDE, --longitude LONGITUDE
                        Долгота
  -lat LATITUDE, --latitude LATITUDE
                        Широта
```
