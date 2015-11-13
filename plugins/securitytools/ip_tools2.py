
import requests
import pythonwhois
import dns.resolver
import dns.reversename
import geoip2.database
from collections import OrderedDict

crontable = []
outputs = []

geolocation_database = "plugins/securitytools/GeoLite2-City.mmdb"


def clean_list_for_query(arg):
    blist = arg
    if '|' in blist[0]:
        blist = [y for x in blist for y in x.split('|')]
        del blist[0]
    if '>' or '<' in blist[0]:
        x = blist[0].replace('>', "").replace('<', '')
        blist[0] = x
    return blist


def build_resolver(query, recordtype=None):
    myResolver = dns.resolver.Resolver()
    answer_list = []
    try:
        answers = myResolver.query(query, recordtype)
        for rdata in answers:
            print rdata
            if recordtype == 'A':
                answer_list.append(rdata.address)
            elif recordtype == 'MX':
                answer_list.append(str(rdata.exchange))
            elif recordtype == 'NS':
                answer_list.append(str(rdata))
            elif recordtype == 'PTR':
                answer_list.append(str(rdata))
        answer = '\n'.join(answer_list)
        return "*%s* Resolved the Following:\n%s" % (query, answer)
    except dns.resolver.NXDOMAIN:
        return "NX Domain"
    except dns.resolver.Timeout:
        return "Query Timeout"
    except dns.resolver.NoAnswer:
        return "No Answer"
    except dns.resolver.NoNameservers:
        return "No Name Server"
    except Exception:
        return "Unexpected error"


def get_geoip(ip):
    reader = geoip2.database.Reader(geolocation_database)
    try:
        response = reader.city(ip)
        results = OrderedDict({"city": response.city.name,
                               "province": response.subdivisions.most_specific.name,
                               "country": response.country.name})
        province = results['province'].encode('utf-8')
        city = results['city'].encode('utf-8')
        country = results['country'].encode('utf-8')
        results = "*Searched IP:* %s\n*Province:* %s\n*City:* %s\n*Country:* %s" % (ip, province, city, country)
        return results
    except ValueError:
        return "Invalid IP address passed"

    except geoip2.errors.AddressNotFoundError:
        return "IP address not found in database"

    except Exception as unexpected_error:
        return "Unexpected error %s" % unexpected_error


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'tools':
        alist = alist[1:]
        if alist[0] == 'whois':
            blist = clean_list_for_query(alist[1:])
            searchterm = blist[0]
            response = pythonwhois.get_whois(searchterm)
            record_list = response.pop('raw', None)
            record = record_list[0].encode('utf-8')
            outputs.append([channel, record])
        elif alist[0] == 'dnslookup' and alist[1] == 'ip':
            blist = clean_list_for_query(alist[2:])
            query = blist[0]
            recordtype = 'A'
            results = build_resolver(query, recordtype)
            outputs.append([channel, results])
        elif alist[0] == 'dnslookup' and alist[1] == 'mx':
            blist = clean_list_for_query(alist[2:])
            query = blist[0]
            recordtype = 'MX'
            results = build_resolver(query, recordtype)
            outputs.append([channel, results])
        elif alist[0] == 'dnslookup' and alist[1] == 'ns':
            blist = clean_list_for_query(alist[2:])
            query = blist[0]
            recordtype = 'NS'
            results = build_resolver(query, recordtype)
            outputs.append([channel, results])
        elif alist[0] == 'reversedns':
            blist = clean_list_for_query(alist[1:])
            ip = blist[0]
            addr = dns.reversename.from_address(ip)
            recordtype = 'PTR'
            results = build_resolver(addr, recordtype)
            outputs.append([channel, results])
        elif alist[0] == 'geolocate':
            ip = alist[1]
            results = get_geoip(ip)
            outputs.append([channel, results])
