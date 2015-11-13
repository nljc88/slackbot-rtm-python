
import requests
import json

api_key = 'api_key'
secret = 'shared_secret'

crontable = []
outputs = []


def clean_list_for_query(arg):
    blist = arg
    if '|' in blist[0]:
        blist = [y for x in blist for y in x.split('|')]
        del blist[0]
    if '>' or '<' in blist[0]:
        x = blist[0].replace('>', "").replace('<', '')
        blist[0] = x
    return blist[0]


def get_censys(endpoint, index, query):
    auth = (api_key, secret)
    if endpoint == 'search':
        url = "https://www.censys.io/api/v1/%s/%s" % (endpoint, index)
        response = requests.post(url, data=query, auth=auth)
        return response
    else:
        url = "https://www.censys.io/api/v1/%s/%s/%s" % (endpoint, index, query)
        response = requests.get(url, auth=auth)
        return response


def parse_censys_view(json_data):
    date = json_data['updated_at']
    searched_query = ''
    try:
        searched_query = json_data['ip']
    except KeyError:
        pass
    try:
        searched_query = json_data['domain']
    except KeyError:
        pass
    province = json_data['location']['province'].encode('utf-8')
    city = json_data['location']['city'].encode('utf-8')
    country = json_data['location']['country'].encode('utf-8')
    registered_country = json_data['location']['registered_country_code'].encode('utf-8')
    asn_name = json_data['autonomous_system']['name'].encode('utf-8')
    route_prefix = json_data['autonomous_system']['routed_prefix']
    organization = json_data['autonomous_system']['organization']
    asn_number_list = []
    for d in json_data['autonomous_system']['path']:
        asn_number_list.append(str(d))
    asn_numbers = '\n  '.join(asn_number_list)
    protocols_list = []
    for d in json_data['protocols']:
        protocols_list.append(d.encode('utf-8'))
    protocols = '\n  '.join(protocols_list)
    info_string = "*Searched:* %s\n*Last Updated:* %s\n*Province:* %s\n*City:* %s\n*Country:* %s\n*Registered Country:* %s\n*ASN Name:* %s\n*Organization:* %s" % (searched_query, date, province, city, country, registered_country, asn_name, organization)
    ip_info_string = "*Route Prefix:* %s\n*ASN Numbers:*\n  %s\n*Protocols:*\n  %s" % (route_prefix, asn_numbers, protocols)

    website = ''
    try:
        website = json_data['80']['http']['get']['headers']['location'].encode('utf-8')

    except KeyError:
        pass

    dns_resolves_list = []
    try:
        for d in json_data['443']['https']['tls']['certificate']['parsed']['extensions']['subject_alt_name']['dns_names']:
            dns_resolves_list.append(d.encode('utf-8'))
    except KeyError:
        pass

    dns_string = ''
    if dns_resolves_list:
        dns_string = '\n  '.join(dns_resolves_list)
    dns_info_string = "*Website:* %s\n*DNS Resolves:*\n  %s" % (website, dns_string)
    results = "%s\n----------------------------------------\n%s\n----------------------------------------\n%s" % (info_string, ip_info_string, dns_info_string)
    return results


def parse_censys_view_cert(json_data):
    date = json_data['updated_at']
    searched_query = ''
    try:
        searched_query = json_data['parsed']['fingerprint_sha256']
    except KeyError:
        pass
    dns_resolves_list = []
    try:
        for d in json_data['parsed']['extensions']['subject_alt_name']['dns_names']:
            dns_resolves_list.append(d.encode('utf-8'))
    except KeyError:
        pass
    dns_string = ''
    if dns_resolves_list:
        dns_string = '\n  '.join(dns_resolves_list)
    issuer_cn = []
    issuer_country = []
    issuer_org = []
    try:
        for d in json_data['parsed']['issuer']['common_name']:
            issuer_cn.append(d.encode('utf-8'))
    except KeyError:
        issuer_cn.append('NULL')
    try:
        for d in json_data['parsed']['issuer']['country']:
            issuer_country.append(d.encode('utf-8'))
    except KeyError:
        issuer_country.append('NULL')
    try:
        for d in json_data['parsed']['issuer']['organization']:
            issuer_org.append(d.encode('utf-8'))
    except KeyError:
        issuer_org.append('NULL')
    issuer_list = []
    if issuer_cn:
        length = len(issuer_cn)
        for x in range(0, length):
            a = issuer_cn[x]
            b = issuer_country[x]
            c = issuer_org[x]
            issuer_string_vals = "*Issuer:*\n  *Common Name:* %s\n  *Country:* %s\n  *Organization:* %s" % (a, b, c)
            issuer_list.append(issuer_string_vals)
    issuer_string = '\n'.join(issuer_list)
    results = "*Searched:* %s\n*Last Updated:* %s\n*DNS Resolves:*\n  %s\n----------------------------------------\n%s" % (searched_query, date, dns_string, issuer_string)
    return results


def parse_search_results(json_data, searchtype):
    if searchtype == 'ip' or searchtype == 'domain':
        domain_list = []
        reg_country_code_list = []
        date_list = []
        for d in json_data['results']:
            domain_list.append(d[searchtype].encode('utf-8'))
            for key, value in d.iteritems():
                if key == 'location.registered_country_code':
                    reg_country_code_list.append(value[0].encode('utf-8'))
                if key == 'updated_at':
                    date_list.append(value[0].encode('utf-8'))
        domain_results_list = []
        length = len(domain_list)
        for x in range(0, length):
            a = domain_list[x]
            b = reg_country_code_list[x]
            c = date_list[x]
            search_str_vals = "*Domain:* %s\n    *Last Updated:* %s\n    *Country Code:* %s\n" % (a, b, c)
            domain_results_list.append(search_str_vals)
        domain_results_string = '\n'.join(domain_results_list)
        page = json_data['metadata']['page']
        tpages = json_data['metadata']['pages']
        query = json_data['metadata']['query']
        results = "*Searched:* %s\n*Page* %s *of* %s\n----------------------------------------\n%s" % (query, page, tpages, domain_results_string)
        return results

    elif searchtype == 'certificates':
        date_list = []
        dns_names_list = []
        ip_list = []
        cn_name_list = []
        country_list = []
        province_list = []
        for d in json_data['results']:
            try:
                value = d['parsed.issuer.common_name']
                for sublistitem in value:
                    cn_name_list.append(sublistitem.encode('utf-8'))
            except KeyError:
                cn_name_list.append('None')
            try:
                value = d['parsed.issuer.country']
                for sublistitem in value:
                    country_list.append(sublistitem.encode('utf-8'))
            except KeyError:
                country_list.append('None')
            try:
                value = d['parsed.issuer.province']
                for sublistitem in value:
                    province_list.append(sublistitem.encode('utf-8'))
            except KeyError:
                province_list.append('None')
            try:
                value = d['parsed.extensions.subject_alt_name.dns_names']
                for sublistitem in value:
                    dns_names_list.append(sublistitem.encode('utf-8'))
            except KeyError:
                dns_names_list.append('None')
            try:
                value = d['parsed.extensions.subject_alt_name.ip_addresses']
                for sublistitem in value:
                    ip_list.append(sublistitem.encode('utf-8'))
            except KeyError:
                ip_list.append('None')
            try:
                value = d['updated_at']
                for sublistitem in value:
                    date_list.append(sublistitem.encode('utf-8'))
            except KeyError:
                date_list.append('None')
        page = json_data['metadata']['page']
        tpages = json_data['metadata']['pages']
        query = json_data['metadata']['query']
        cert_string = "    *Common Name:* %s\n    *Province:* %s\n    *Country:* %s" % (cn_name_list[0], province_list[0], country_list[0])
        dns_info_string = '\n    '.join(dns_names_list)
        ip_info_string = '\n    '.join(ip_list)
        results = "*Searched:* %s\n*Last Update:* %s\n*Page* %s *of* %s\n----------------------------------------\n*Issuer Info:*\n%s\n----------------------------------------\n*DNS Names:*\n    %s\n----------------------------------------\n*IPs:*\n    %s\n" % (query, date_list[0], page, tpages, cert_string, dns_info_string, ip_info_string)
        return results


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'censys':
        if alist[1] == 'view':
            endpoint = alist[1]
            index = alist[2]
            query_list = []
            query_list.append(alist[3])
            query = clean_list_for_query(query_list)
            response = get_censys(endpoint, index, query)
            if response.status_code != 200:
                outputs.append([channel, "something went wrong. prob user error\nformat:\ncensys view (ipv4|websites|certificates) <(ip|website|sha256)>"])
            else:
                json_data = json.loads(response.content)
                if index == 'ipv4' or index == 'websites':
                    results = parse_censys_view(json_data)
                    outputs.append([channel, results])
                elif index == 'certificates':
                    results = parse_censys_view_cert(json_data)
                    outputs.append([channel, results])
        elif alist[1] == 'search':
            endpoint = alist[1]
            index = alist[2]
            query_list = []
            query_list.append(alist[3])
            searchterm = clean_list_for_query(query_list)
            field = []
            if index == 'ipv4':
                field = ['ip',
                         'updated_at',
                         'location.registered_country_code'
                         ]
                searchtype = 'ip'
            elif index == 'websites':
                field = ["domain",
                         "updated_at",
                         "location.registered_country_code"
                         ]
                searchtype = 'domain'
            elif index == 'certificates':
                field = ["updated_at",
                         "parsed.extensions.subject_alt_name.dns_names",
                         "parsed.extensions.subject_alt_name.ip_addresses",
                         "parsed.issuer.province",
                         "parsed.issuer.country",
                         "parsed.issuer.common_name"
                         ]
                searchtype = 'certificates'
            query = json.dumps({"query": searchterm,
                                "fields": field})
            response = get_censys(endpoint, index, query)
            if response.status_code != 200:
                outputs.append([channel, "something went wrong. prob user error\nformat:\ncensys search (ipv4|websites|certificates) <(ip|website|sha256)>"])
            else:
                json_data = json.loads(response.content)
                results = parse_search_results(json_data, searchtype)
                outputs.append([channel, results])
