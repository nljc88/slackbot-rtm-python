
import requests
import time
from bs4 import BeautifulSoup

crontable = []
outputs = []


def build_playername(arg):
    if len(arg) == 1:
        player_name_string = arg[0]
        return player_name_string
    else:
        name_a = arg[0]
        name_b = arg[1]
        if name_a[len(name_a)-1] == ",":
            player_name_string = name_a + "%20" + name_b
        else:
            player_name_string = name_b + ",%20" + name_a
        return player_name_string


def build_url(league, playername):
    base_url = 'http://www.rotoworld.com/content/playersearch.aspx?searchname=%s&sport=%s'
    refined_url = base_url % (playername, league)
    return refined_url


def get_data(url):
    response = requests.get(url)
    if '<h3>Search Results for:' in response.content:
        if '<table id="cp1_tblSearchResults"' in response.content:
            soup = BeautifulSoup(response.content, 'html.parser')
            table_tag = soup.find('table', {'id': 'cp1_tblSearchResults'})
            players_list1 = []
            for child in table_tag:
                if 'player' in str(child):
                    c = child.get_text().encode('utf-8')
                    d = ' '.join(c.split())
                    players_list1.append(d)
            players_list = []
            for item in players_list1:
                pl = item.split(' ')
                pl_str = "%s %s" % (pl[0], pl[1])
                players_list.append(pl_str)
            return players_list
    else:
        return response


def make_news_soup(arg):
    soup = BeautifulSoup(arg, 'html.parser')
    news = soup.find('div', {'class': 'playernews'})
    return news.text


def make_stats_soup(arg, sport):
    soup = BeautifulSoup(arg, 'html.parser')
    bs_data = soup.find('table', {'class': 'statstable'})
    header_list = []
    column_names = bs_data.find('tr', {'class': 'columnnames'}).find_all('td')
    for cols in column_names:
        z = cols.get_text()
        header_list.append(z.encode('ascii', 'ignore').decode('ascii'))
    season_stats_list = []
    if sport == 'hockey':
        col_data = bs_data.find_all('tr')[2]
    elif sport == 'football':
        col_data = bs_data.find_all('tr')[3]
    elif sport == 'basketball':
        col_data = bs_data.find_all('tr')[3]
    elif sport == 'baseball':
        col_data = bs_data.find_all('tr')[2]
    elif sport == 'golf':
        col_data = bs_data.find_all('tr')[3]
    stats = col_data.find_all('td')
    for stat in stats:
        row = stat.get_text()
        season_stats_list.append(row.encode('utf-8'))
    stats_list1 = []
    length1 = len(header_list)
    for x in range(0, length1):
        a = header_list[x]
        b = season_stats_list[x]
        string_vals = "%s: %s" % (a, b)
        stats_list1.append(string_vals)
    stats_string = '\n'.join(stats_list1)
    return stats_string


def make_statyear_soup(arg, year):
    soup = BeautifulSoup(arg, 'html.parser')
    bs_data = soup.find_all('table', {'class': 'statstable'})[1]
    header_list = []
    column_names = bs_data.find('tr', {'class': 'columnnames'}).find_all('td')
    for cols in column_names:
        z = cols.get_text()
        header_list.append(z)
    table = []
    trs = bs_data.find_all('tr')
    for tr in trs:
        tr_list = []
        tds = tr.find_all('td')
        for td in tds:
            x = td.get_text()
            tr_list.append(x)
        table.append(tr_list)
    stat_line = []
    for y in table:
        if str(year) in y:
            stat_line = y
    if not stat_line:
        statyear_string = "no results for that year"
        return statyear_string
    else:
        statyear_list1 = []
        length2 = len(header_list)
        for x in range(0, length2):
            a = header_list[x]
            b = stat_line[x]
            stats_vals = "%s: %s" % (a, b)
            statyear_list1.append(stats_vals)
        statyear_string = '\n'.join(statyear_list1)
        return statyear_string


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hockey' or alist[0] == 'football' or alist[0] == 'basketball' or alist[0] == 'baseball' or alist[0] == 'golf' or alist[0] == 'nascar':
        time.sleep(1)
        sport = alist.pop(0)
        if sport == 'hockey':
            league = 'nhl'
        elif sport == 'football':
            league = 'nfl'
        elif sport == 'basketball':
            league = 'nba'
        elif sport == 'baseball':
            league = 'mlb'
        elif sport == 'golf':
            league = 'gol'
        elif sport == 'nascar':
            league = 'nas'
        request = alist.pop(0)
        if request == 'news':
            playername = build_playername(alist)
            url = build_url(league, playername)
            response = get_data(url)
            if not response:
                outputs.append([channel, 'No player by that name found'])
            elif type(response) == list:
                players_str = '\n'.join(response)
                outputs.append([channel, "Were you looking for one of these players:\n%s" % (players_str)])
            else:
                news = make_news_soup(response.content)
                outputs.append([channel, news])
        elif request == 'stats':
            if sport == 'nascar':
                outputs.append([channel, 'only news events from nascar, no stats'])
            else:
                playername = build_playername(alist)
                url = build_url(league, playername)
                response = get_data(url)
                if not response:
                    outputs.append([channel, 'No player by that name found'])
                elif type(response) == list:
                    players_str = '\n'.join(response)
                    outputs.append([channel, "Were you looking for one of these players:\n%s" % (players_str)])
                else:
                    stats_string = make_stats_soup(response.content, sport)
                    outputs.append([channel, stats_string])
        elif request == 'statyear':
            try:
                year = int(alist.pop(-1))
            except ValueError:
                outputs.append([channel, "format your request: <sport> statyear <playername> <year>"])
            else:
                if sport == 'baseball' or sport == 'golf' or sport == 'nascar':
                    outputs.append([channel, 'no stats other than current year, use stats call'])
                else:
                    playername = build_playername(alist)
                    url = build_url(league, playername)
                    response = get_data(url)
                    if not response:
                        outputs.append([channel, 'No player by that name found'])
                    elif type(response) == list:
                        players_str = '\n'.join(response)
                        outputs.append([channel, "Were you looking for one of these players:\n%s" % (players_str)])
                    else:
                        statyear_results = make_statyear_soup(response.content, year)
                        outputs.append([channel, statyear_results])
