
import time
import requests
import json
from geopy.geocoders import Nominatim

client_id = 'client_id'
client_secret = 'secret'

crontable = []
outputs = []


def build_search_query(arg):
    query = ' '.join(arg)
    if ' ' in query:
        query1 = query.replace(' ', '+')
        return query1
    else:
        return query


def build_beer_search_url(arg):
    base_url = 'https://api.untappd.com/v4/search/beer?client_id=%s&client_secret=%s&q=%s&limit=10'
    refined_url = base_url % (client_id, client_secret, arg)
    return refined_url


def get_request(arg):
    response = requests.get(arg)
    return response


def make_json(arg):
    json_data = json.loads(arg.content)
    return json_data


def check_search_response(arg):
    count = arg['response']['beers']['count']
    if count == 0:
        return 'error1'
    elif count > 0:
        return 'good'


def beer_search_results(arg):
    beer_name_list = []
    beer_breweryname_list = []
    beer_style_list = []
    beer_abv_list = []
    beer_description_list = []
    beer_id = []
    for d in arg['response']['beers']['items']:
        beer_name_list.append(d['beer']['beer_name'].encode('utf-8'))
        beer_breweryname_list.append(d['brewery']['brewery_name'].encode('utf-8'))
        beer_style_list.append(d['beer']['beer_style'].encode('utf-8'))
        beer_abv_list.append(d['beer']['beer_abv'])
        beer_description_list.append(d['beer']['beer_description'].encode('ascii', 'ignore').decode('ascii'))
        beer_id.append(d['beer']['bid'])
    length = len(beer_name_list)
    search_list = []
    for x in range(0, length):
        a = beer_name_list[x]
        b = beer_breweryname_list[x]
        c = beer_style_list[x]
        d = beer_abv_list[x]
        e = beer_description_list[x]
        search_string_vals = "*Name:* %s\n*Brewery:* %s\n*Style:* %s\n*ABV:* %s%%\n*Description:* %s\n----------------------------------------" % (a, b, c, d, e)
        search_list.append(search_string_vals)
    search_string = '\n'.join(search_list)
    return search_string


def get_beer_review_ID(arg):
    beer_id = arg['response']['beers']['items'][0]['beer']['bid']
    return beer_id


def get_beer_review_json(arg):
    base_url = 'https://api.untappd.com/v4/beer/checkins/%s?client_id=%s&client_secret=%s&limit=10'
    refined_url = base_url % (arg, client_id, client_secret)
    response = requests.get(refined_url)
    json_data = json.loads(response.content)
    return json_data


def beer_review_results(arg):
    reviewed_beer_name = arg['response']['checkins']['items'][0]['beer']['beer_name'].encode('utf-8')
    checkin_time_list = []
    checkin_username_list = []
    checkin_comment_list = []
    checkin_rating_score_list = []
    for d in arg['response']['checkins']['items']:
        checkin_time_list.append(d['created_at'].encode('utf-8'))
        checkin_username_list.append(d['user']['user_name'].encode('utf-8'))
        checkin_comment_list.append(d['checkin_comment'].encode('utf-8'))
        checkin_rating_score_list.append(d['rating_score'])
    length1 = len(checkin_username_list)
    reviews_list = []
    for x in range(0, length1):
        a = checkin_time_list[x]
        b = checkin_username_list[x]
        c = checkin_rating_score_list[x]
        d = checkin_comment_list[x]
        review_string_vals = "*Time:* %s\n*Username:* %s\n*Rating:* %s\n*Comments:* %s\n----------------------------------------" % (a, b, c, d)
        reviews_list.append(review_string_vals)
    review_string = '\n'.join(reviews_list)
    return reviewed_beer_name, review_string


def build_brewery_search_url(arg):
    base_url = 'https://api.untappd.com/v4/search/brewery?client_id=%s&client_secret=%s&q=%s&limit=10'
    refined_url = base_url % (client_id, client_secret, arg)
    return refined_url


def check_brewery_response(arg):
    count = arg['response']['brewery']['count']
    if count == 0:
        return 'error1'
    elif count > 0:
        return 'good'


def brewery_search_results(arg):
    brewery_search_name = arg['response']['term'].encode('utf-8')
    brewery_name_list = []
    beer_count_list = []
    brewery_country_list = []
    for d in arg['response']['brewery']['items']:
        brewery_name_list.append(d['brewery']['brewery_name'].encode('utf-8'))
        beer_count_list.append(d['brewery']['beer_count'])
        brewery_country_list.append(d['brewery']['country_name'].encode('utf-8'))
    length2 = len(brewery_name_list)
    brewery_search_list = []
    for x in range(0, length2):
        a = brewery_name_list[x]
        b = beer_count_list[x]
        c = brewery_country_list[x]
        brewery_search_string_vals = "*Brewery Name:* %s\n*Beer Count:* %s\n*Location:* %s\n----------------------------------------" % (a, b, c)
        brewery_search_list.append(brewery_search_string_vals)
    brewery_search_string = '\n'.join(brewery_search_list)
    return brewery_search_name, brewery_search_string


def get_brewery_id(arg):
    brewery_id = arg['response']['brewery']['items'][0]['brewery']['brewery_id']
    return brewery_id


def get_brewery_info_json(arg):
    base_url = 'https://api.untappd.com/v4/brewery/info/%s?client_id=%s&client_secret=%s'
    refined_url = base_url % (arg, client_id, client_secret)
    response = requests.get(refined_url)
    json_data = json.loads(response.content)
    return json_data


def get_brewery_info_from_json(arg):
    brewery_name = arg['response']['brewery']['brewery_name'].encode('utf-8')
    brewery_website = arg['response']['brewery']['contact']['url'].encode('ascii', 'ignore').decode('ascii')
    brewery_address = arg['response']['brewery']['location']['brewery_address'].encode('utf-8')
    brewery_city = arg['response']['brewery']['location']['brewery_city'].encode('utf-8')
    brewery_state = arg['response']['brewery']['location']['brewery_state'].encode('utf-8')
    brewery_rating = arg['response']['brewery']['rating']['rating_score']
    brewery_description = arg['response']['brewery']['brewery_description'].encode('ascii', 'ignore').decode('ascii')
    brewery_info = "*%s*\n%s\n%s\n%s, %s\n*Rating:* %s\n\n%s" % (brewery_name, brewery_website, brewery_address, brewery_city, brewery_state, brewery_rating, brewery_description)
    return brewery_info


def get_beer_list_from_brewery_json(arg):
    brewery_name = arg['response']['brewery']['brewery_name'].encode('utf-8')
    beer_name_list = []
    for d in arg['response']['brewery']['beer_list']['items']:
        beer_name_list.append(d['beer']['beer_name'].encode('utf-8'))
    beer_name_string = '\n'.join(beer_name_list)
    return brewery_name, beer_name_string


def get_beer_info_json(arg):
    base_url = 'https://api.untappd.com/v4/beer/info/%s?client_id=%s&client_secret=%s'
    refined_url = base_url % (arg, client_id, client_secret)
    response = requests.get(refined_url)
    json_data = json.loads(response.content)
    return json_data


def get_beer_info_from_json(arg):
    beer_name = arg['response']['beer']['beer_name'].encode('utf-8')
    beer_style = arg['response']['beer']['beer_style'].encode('utf-8')
    beer_abv = arg['response']['beer']['beer_abv']
    beer_ibu = arg['response']['beer']['beer_ibu']
    beer_rating = arg['response']['beer']['rating_score']
    beer_description = arg['response']['beer']['beer_description'].encode('ascii', 'ignore').decode('ascii')
    brewer = arg['response']['beer']['brewery']['brewery_name'].encode('utf-8')
    beer_info_string = "*Name:* %s\n*Style:* %s\n*ABV:* %s%%\n*IBU:* %s ppm\n*Rating:* %s\n*Brewery:* %s\n%s" % (beer_name, beer_style, beer_abv, beer_ibu, beer_rating, brewer, beer_description)
    return beer_info_string


def get_local_geocodes(arg):
    location_arg = ' '.join(arg)
    geolocator = Nominatim()
    location = geolocator.geocode(location_arg)
    try:
        lat = location.latitude
        lng = location.longitude
        return lat, lng
    except AttributeError:
        return 'error1'


def build_the_pub_search_get_json(arg1, arg2):
    base_url = 'https://api.untappd.com/v4/thepub/local?client_id=%s&client_secret=%s&lat=%s&lng=%s&radius=5'
    refined_url = base_url % (client_id, client_secret, arg1, arg2)
    response = requests.get(refined_url)
    json_data = json.loads(response.content)
    return json_data


def get_venue_info_from_json(arg):
    venue_name_list = []
    venue_address_list = []
    venue_city_list = []
    venue_state_list = []
    for d in arg['response']['checkins']['items']:
        venue_name_list.append(d['venue']['venue_name'].encode('utf-8'))
        venue_address_list.append(d['venue']['location']['venue_address'].encode('utf-8'))
        venue_city_list.append(d['venue']['location']['venue_city'].encode('utf-8'))
        venue_state_list.append(d['venue']['location']['venue_state'].encode('utf-8'))
    length3 = len(venue_name_list)
    venue_search_list = []
    for x in range(0, length3):
        a = venue_name_list[x]
        b = venue_address_list[x]
        c = venue_city_list[x]
        d = venue_state_list[x]
        venue_string_vals = "*%s*\n%s, %s, %s\n----------------------------------------" % (a, b, c, d)
        venue_search_list.append(venue_string_vals)
    no_dups_venue_list = set(venue_search_list)
    venue_search_string = '\n'.join(no_dups_venue_list)
    return venue_search_string


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'beer' and alist[1] == 'search':
        time.sleep(1)
        alist = alist[2:]
        query = build_search_query(alist)
        refined_url = build_beer_search_url(query)
        response = get_request(refined_url)
        json_data = make_json(response)
        check = check_search_response(json_data)
        if check == 'error1':
            outputs.append([channel, 'The search did not return any beers, try spelling it right'])
        elif check == 'good':
            search_results = beer_search_results(json_data)
            outputs.append([channel, search_results])
    elif alist[0] == 'beer' and alist[1] == 'info':
        time.sleep(1)
        alist = alist[2:]
        query = build_search_query(alist)
        refined_url = build_beer_search_url(query)
        response = get_request(refined_url)
        json_data = make_json(response)
        check = check_search_response(json_data)
        if check == 'error1':
            outputs.append([channel, 'The search did not return any beers, try spelling it right'])
        elif check == 'good':
            beer_id = get_beer_review_ID(json_data)
            json_data = get_beer_info_json(beer_id)
            beer_info = get_beer_info_from_json(json_data)
            outputs.append([channel, beer_info])
    elif alist[0] == 'beer' and alist[1] == 'reviews':
        time.sleep(1)
        alist = alist[2:]
        query = build_search_query(alist)
        refined_url = build_beer_search_url(query)
        response = get_request(refined_url)
        json_data = make_json(response)
        check = check_search_response(json_data)
        if check == 'error1':
            outputs.append([channel, 'The search did not return any beers, try spelling it right'])
        elif check == 'good':
            beer_id = get_beer_review_ID(json_data)
            json_data = get_beer_review_json(beer_id)
            review_results = beer_review_results(json_data)
            reviewed_beer_name = review_results[0]
            review_string = review_results[1]
            outputs.append([channel, '*Reviewed Beer:* %s\n\n%s\n' % (reviewed_beer_name, review_string)])
    elif alist[0] == 'brewery' and alist[1] == 'search':
        time.sleep(1)
        alist = alist[2:]
        query = build_search_query(alist)
        refined_url = build_brewery_search_url(query)
        response = get_request(refined_url)
        json_data = make_json(response)
        check = check_brewery_response(json_data)
        if check == 'error1':
            outputs.append([channel, 'The search did not return any breweries, try spelling it right'])
        elif check == 'good':
            brewery_results = brewery_search_results(json_data)
            brewery_search_name = brewery_results[0]
            breweries_found = brewery_results[1]
            outputs.append([channel, "*Brewery Searched:* %s\n\n%s" % (brewery_search_name, breweries_found)])
    elif alist[0] == 'brewery' and alist[1] == 'info':
        time.sleep(1)
        alist = alist[2:]
        query = build_search_query(alist)
        refined_url = build_brewery_search_url(query)
        response = get_request(refined_url)
        json_data = make_json(response)
        check = check_brewery_response(json_data)
        if check == 'error1':
            outputs.append([channel, 'The search did not return any breweries, try spelling it right'])
        elif check == 'good':
            brewery_id = get_brewery_id(json_data)
            json_data = get_brewery_info_json(brewery_id)
            brewery_info = get_brewery_info_from_json(json_data)
            outputs.append([channel, brewery_info])
    elif alist[0] == 'brewery' and alist[1] == 'beerlist':
        time.sleep(1)
        alist = alist[2:]
        query = build_search_query(alist)
        refined_url = build_brewery_search_url(query)
        response = get_request(refined_url)
        json_data = make_json(response)
        check = check_brewery_response(json_data)
        if check == 'error1':
            outputs.append([channel, 'The search did not return any breweries, try spelling it right'])
        elif check == 'good':
            brewery_id = get_brewery_id(json_data)
            json_data = get_brewery_info_json(brewery_id)
            brewery_list = get_beer_list_from_brewery_json(json_data)
            brewery_name = brewery_list[0]
            brewery_beers = brewery_list[1]
            outputs.append([channel, "*Brewery: %s*\n\nBeer List (Top 15):\n%s" % (brewery_name, brewery_beers)])
    elif alist[0] == 'local' and alist[1] == 'search':
        time.sleep(1)
        alist = alist[2:]
        geocode = get_local_geocodes(alist)
        if geocode == 'error1':
            outputs.append([channel, 'try another address, that one did not work'])
        else:
            lat = geocode[0]
            lng = geocode[1]
            json_data = build_the_pub_search_get_json(lat, lng)
            venue_info = get_venue_info_from_json(json_data)
            outputs.append([channel, venue_info])
