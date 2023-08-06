import datetime
import json
import random
import sqlite3
import time
from random import choice

import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

headers ={
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}

url = 'https://www.meteonova.ru/hourly/36052-pogoda-Gorno-Altaisk.htm'

class HelloWorld(Resource):
    def get(self):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        hours = soup.find_all('td', class_=('tod dnmd','tod dnmn'))
        value = soup.find_all('img', width='50', height='80')
        tempera = soup.find_all('td', class_='temper')

        #HOURS
        hours_2 = []
        num = 0

        for x in range(0, len(hours)):
            d = hours[x].text.split(':')
            d = int(d[0])
            if d > num:
                num = d
                hours_2.append(hours[x].text)

        hours = hours_2

        #VALUE
        value_2 = []
        for i in range(0, len(value)):
            
            result = value[i].__str__().split('"')

            value_2.append(result[1])

        value = value_2

        #TEMPERA
        tempera_2 = []
        for x in tempera:
            tempera_2.append(x.text)

        tempera = tempera_2

        tempera.pop(0)

        week = time.ctime(time.time())
        week = week.split(' ')
        week = f'{week[0]}, {week[3]} {week[1]}'

        mes =f'{week}\n'

        for i in range(0, len(hours)):
            mes += f'{hours[i]}, {value[i]}, {tempera[i]}\n'

        return {'hello': mes}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

