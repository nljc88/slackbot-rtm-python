

import requests
import json
import time
import datetime


apikey = 'apikey'

crontable = []
outputs = []

FILE = "plugins/weather/city_id"


def get_city(arg1):
    strcity = ' '.join(arg1)
    city = strcity.lower()
    return city


def get_cityID(arg2):
    searchfile = open(FILE, 'r')
    cities = []
    for line in searchfile:
        line = line.replace('[', "").replace(']', "").replace('\n', '').replace("u'", '').replace("'", "")
        newline = line.split(', ,')
        if arg2 == newline[0]:
            id = newline[1]
            return id
        elif arg2 in newline[0]:
            x = newline[0]
            cities.append(x)
    return cities
    searchfile.close()


def build_url(arg3, arg4, arg5=None):
    base_url = "http://api.openweathermap.org/data/2.5/%s?id=%s&APPID=%s"
    if arg3 == 'weather':
        refined_url = base_url % (arg3, arg4, apikey) + '&units=imperial'
        return refined_url
    elif arg3 == 'forecast' and not arg5:
        refined_url = base_url % (arg3, arg4, apikey) + '&units=imperial'
        return refined_url
    elif arg5:
        base_url2 = "http://api.openweathermap.org/data/2.5/%s/daily?id=%s&APPID=%s"
        refined_url = base_url2 % (arg3, arg4, apikey) + '&units=imperial' + '&cnt=%s' % arg5
        return refined_url


def get_data(arg6):
    results = ""
    results = requests.get(arg6)
    return results


def find_weather(arg7):
    data = json.loads(arg7.content)
    return data


def weather_current(arg8):
    print arg8
    name = arg8['name']
    dt = arg8['dt']
    tmp = arg8['main']['temp']
    min_tmp = arg8['main']['temp_min']
    max_tmp = arg8['main']['temp_max']
    humidity = arg8['main']['humidity']
    wind = arg8['wind']['speed']
    weather = arg8['weather']
    desc = [x['description'] for x in weather]
    description = str(desc[0])
    date = datetime.datetime.strptime(time.ctime(dt), "%a %b %d %H:%M:%S %Y")
    weather_result = "*City:* %s\n*Date:* %s\n*Temp:* %s F\n*Max Tmp:* %s F\n*Min Tmp:* %s F\n*Humidity:* %s%%\n*Wind:* %s mph\n*Description:* %s" % (name, date, tmp, max_tmp, min_tmp, humidity, wind, description)
    return weather_result


def weather_forecast(arg):
    dt_list = []
    temp_list = []
    humidity_list = []
    description_list = []
    for d in arg['list']:
        dt_list.append(d['dt'])
        temp_list.append(d['main']['temp'])
        humidity_list.append(d['main']['humidity'])
        description_list.append(d['weather'][0]['description'].encode("utf-8"))
    date = dt_time(dt_list)
    clean_date = []
    for item in date:
        if '00:00' in item:
            x = item.replace('00:00', '00')
            clean_date.append(x)
    temp = tempF(temp_list)
    humidity = humidity_percent(humidity_list)
    length = len(temp)
    list3 = []
    for x in range(0, length):
        a = clean_date[x]
        b = temp[x]
        c = humidity[x]
        d = description_list[x]
        string_val = "%s: %s %s %s" % (a, b, c, d)
        list3.append(string_val)
    weather_string = '\n'.join(list3)
    return weather_string


def weather_numDay(arg):
    dt_list = []
    min_temp_list = []
    max_temp_list = []
    humidity_list = []
    description_list = []
    for d in arg['list']:
        dt_list.append(d['dt'])
        min_temp_list.append(d['temp']['min'])
        max_temp_list.append(d['temp']['max'])
        humidity_list.append(d['humidity'])
        description_list.append(d['weather'][0]['description'].encode("utf-8"))
    date = dt_time(dt_list)
    clean_date = []
    for item in date:
        if '00:00' in item:
            x = item.replace('00:00', '00')
            clean_date.append(x)
    min_temp = tempF(min_temp_list)
    max_temp = tempF(max_temp_list)
    humidity = humidity_percent(humidity_list)
    length = len(min_temp)
    list3 = []
    for x in range(0, length):
        a = clean_date[x]
        b = max_temp[x]
        c = min_temp[x]
        d = humidity[x]
        e = description_list[x]
        string_val = "%s: Max: %s  Min: %s  %s  %s" % (a, b, c, d, e)
        list3.append(string_val)
    weather_string = '\n'.join(list3)
    return weather_string


def dt_time(arg):
    date = []
    for item in arg:
        x = datetime.datetime.strptime(time.ctime(item), "%a %b %d %H:%M:%S %Y")
        y = str(x)
        date.append(y)
    return date


def tempF(arg):
    temp = []
    for item in arg:
        t = "%sF" % item
        temp.append(t)
    return temp


def humidity_percent(arg):
    humidity = []
    for item in arg:
        h = "%s%%H" % item
        humidity.append(h)
    return humidity


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower().encode('utf-8')
    alist = string.split(' ')
    if alist[0] == '!weather' and alist[1] != 'forecast':
        time.sleep(1)
        alist = alist[1:]
        city = get_city(alist)
        var2 = get_cityID(city)
        if type(var2) is list and len(var2) > 0:
            string = '\n'.join(var2)
            outputs.append([channel, "Which city are you looking for?\n%s" % string])
        elif not var2:
            outputs.append([channel, "try that again, this time with correct spelling"])
        elif type(var2) is str:
            wvar = 'weather'
            refined_url = build_url(wvar, var2)
            results = get_data(refined_url)
            data = find_weather(results)
            weather_result = weather_current(data)
            outputs.append([channel, weather_result])
    elif alist[0] == '!weather-current':
        time.sleep(1)
        alist = alist[1:]
        city = get_city(alist)
        var2 = get_cityID(city)
        if type(var2) is list and len(var2) > 0:
            string = '\n'.join(var2)
            outputs.append([channel, "Which city are you looking for?\n%s" % string])
        elif not var2:
            outputs.append([channel, "Derp! check spelling of your city"])
        elif type(var2) is str:
            wvar = 'weather'
            refined_url = build_url(wvar, var2)
            results = get_data(refined_url)
            data = find_weather(results)
            weather_result = weather_current(data)
            outputs.append([channel, weather_result])
    elif alist[0] == '!weather-forecast':
        time.sleep(1)
        alist = alist[1:]
        city = get_city(alist)
        var2 = get_cityID(city)
        if type(var2) is list and len(var2) > 0:
            string = '\n'.join(var2)
            outputs.append([channel, "Which city are you looking for?\n%s" % string])
        elif not var2:
            outputs.append([channel, "check your map and spell the city correctly"])
        elif type(var2) is str:
            fvar = 'forecast'
            refined_url = build_url(fvar, var2)
            results = get_data(refined_url)
            data = find_weather(results)
            weather_forecast_results = weather_forecast(data)
            outputs.append([channel, weather_forecast_results])
    elif alist[0] == '!weather' and alist[1] == 'forecast':
        time.sleep(1)
        alist = alist[2:]
        if 'day' in alist[0]:
            cnt = int(filter(str.isdigit, alist[0]))
            del alist[0]
        else:
            cnt = 10
        city = get_city(alist)
        var2 = get_cityID(city)
        if type(var2) is list and len(var2) > 0:
            string = '\n'.join(var2)
            outputs.append([channel, "Which city are you looking for?\n%s" % string])
        elif not var2:
            outputs.append([channel, "where did you learn to spell. try your city again"])
        elif type(var2) is str:
            fvar = 'forecast'
            refined_url = build_url(fvar, var2, cnt)
            results = get_data(refined_url)
            data = find_weather(results)
            weather_10day_results = weather_numDay(data)
            outputs.append([channel, weather_10day_results])
