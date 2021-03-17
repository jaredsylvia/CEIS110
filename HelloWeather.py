# -*- coding: utf-8 -*-
"""
Jared's Hello World script.

"""
import json
import requests

zcodeapiKey = 'INSERTZIPCODEAPIKEYHERE'
zcodeFormat = 'json' #also accepts xml or csv
zcodeUnits = 'degrees' #also accepts radials

owmapiKey = 'INSERTOPENWEATHERMAPKEYHERE'
headers = { 'Content-Type': "application/x-www-form-urlencoded", 'cache-control': "no-cache" }

name = input('Who am I speaking with? ')
zipCode = input('What is your Zip code? ')

zcodebaseURL = 'https://www.zipcodeapi.com/rest/'
zcodeFullURL = zcodebaseURL + zcodeapiKey + '/info.' + zcodeFormat + '/' + zipCode + '/' + zcodeUnits




zcodeResults = requests.get(zcodeFullURL, headers=headers)
zcodeResultsJSON = json.dumps(zcodeResults.json())
zcodeResultsParsed = json.loads(zcodeResultsJSON)
city = zcodeResultsParsed['city']
state = zcodeResultsParsed['state']

owmbaseURL = 'https://api.openweathermap.org/data/2.5/weather?zip='
owmFullURL = owmbaseURL + zipCode + '&appid=' + owmapiKey + '&units=imperial'
owmResults = requests.get(owmFullURL, headers=headers)
owmResultsJSON = json.dumps(owmResults.json())
owmResultsParsed = json.loads(owmResultsJSON)
owmWeather = owmResultsParsed['weather'][0]['main']
owmTemp = str(round(owmResultsParsed['main']['temp']))

print("Hello " + name + "! From " + city + ", " + state + '.', end='\n')
print("The weather is currently: " + owmWeather, end='\n')
print("And it is currently " + owmTemp + ' degrees.')
