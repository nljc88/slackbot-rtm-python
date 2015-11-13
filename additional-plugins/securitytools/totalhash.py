
import time
import requests
import json
import hashlib
import hmac
import xmltodict
from math import ceil

crontable = []
outputs = []

apikey = 'apikey'
userid = 'username'


def build_sign(arg):
    sign = hmac.new(apikey, msg=arg, digestmod=hashlib.sha256).hexdigest()
    return sign


def build_url(request, sign, query1=None, page=None):
    if page:
        base_url = 'http://api.totalhash.com/%s/%s&id=%s&sign=%s&start=%s'
        refined_url = base_url % (request, query1, userid, sign, page)
        return refined_url
    elif (request == 'search' or request == 'analysis') and not page:
        base_url = 'http://api.totalhash.com/%s/%s&id=%s&sign=%s'
        refined_url = base_url % (request, query1, userid, sign)
        return refined_url
    elif request == 'usage':
        base_url = 'http://api.totalhash.com/%s/id=%s&sign=%s'
        refined_url = base_url % (request, userid, sign)
        return refined_url


def get_th_data(arg):
    response = requests.get(arg, verify=False)
    return response


def get_json_from_response(arg):
    json_string = json.dumps(xmltodict.parse(arg))
    json_dict = json.loads(json_string)
    return json_dict


def get_analysis_from_json(arg):
    sha1 = arg['analysis']['@sha1']
    md5 = arg['analysis']['@md5']
    scan_date = arg['analysis']['@time']
    magic = arg['analysis']['static']['magic']['@value'].encode('utf-8')
    pehash_list = []
    packer_list = []
    av_scanner_list = []
    av_signature_list = []
    dns_domain_list = []
    dns_ip_list = []
    flows_dest_ip_list = []
    flows_dest_port_list = []
    http_request_type_list = []
    http_request_text_list = []
    for k, v in arg.iteritems():
        if type(v) == dict:
            for subkey, subvalue in v.iteritems():
                if type(subvalue) == dict:
                    for subkey2, subvalue2 in subvalue.iteritems():
                        if type(subvalue2) == dict:
                            if subkey2 == 'pehash':
                                pehash_list.append(subvalue2['@value'])
                            elif subkey2 == 'packer':
                                packer_list.append(subvalue2['@value'])
                            elif subkey2 == 'av':
                                av_scanner_list.append(subvalue2['@scanner'].encode('utf-8'))
                                av_signature_list.append(subvalue2['@signature'].encode('utf-8'))
                            elif subkey2 == 'dns':
                                dns_domain_list.append(subvalue2['@rr'].encode('utf-8'))
                                dns_ip_list.append(subvalue2['@ip'].encode('utf-8'))
                            elif subkey2 == 'flows':
                                flows_dest_ip_list.append(subvalue2['@dst_ip'])
                                flows_dest_port_list.append(subvalue2['@dst_port'])
                            elif subkey2 == 'http':
                                http_request_type_list.append(subvalue2['@type'].encode('utf-8'))
                                http_request_text_list.append(subvalue2['#text'].encode('ascii', 'ignore').decode('ascii'))
                        if type(subvalue2) == list:
                            for d in subvalue2:
                                if subkey2 == 'pehash':
                                    pehash_list.append(d['@value'])
                                elif subkey2 == 'packer':
                                    packer_list.append(d['@value'])
                                elif subkey2 == 'av':
                                    av_scanner_list.append(d['@scanner'].encode('utf-8'))
                                    av_signature_list.append(d['@signature'].encode('utf-8'))
                                elif subkey2 == 'dns':
                                    if '@rr' in d:
                                        dns_domain_list.append(d['@rr'].encode('utf-8'))
                                    else: 
                                        dns_domain_list.append('null')
                                    if '@ip' in d:
                                        dns_ip_list.append(d['@ip'].encode('utf-8'))
                                    else:
                                        dns_ip_list.append('null')
                                elif subkey2 == 'flows':
                                    flows_dest_ip_list.append(d['@dst_ip'])
                                    flows_dest_port_list.append(d['@dst_port'])
                                elif subkey2 == 'http':
                                    http_request_type_list.append(d['@type'].encode('utf-8'))
                                    http_request_text_list.append(d['#text'].encode('ascii', 'ignore').decode('ascii'))
    file_info_string = "*sha1:* %s\n*md5:* %s\n*magic:* %s\n*Scan Date:* %s\n" % (sha1, md5, magic, scan_date)
    if pehash_list:
        pehash_string = ''.join(pehash_list)
    else:
        pehash_string = "NULL"
    if packer_list:
        packer_string = ''.join(packer_list)
    else:
        packer_string = 'NULL'
    av_list = []
    if av_scanner_list:
        length1 = len(av_scanner_list)
        for x in range(0, length1):
            a = av_scanner_list[x]
            b = av_signature_list[x]
            av_string_vals = "%s :%s\n" % (a, b)
            av_list.append(av_string_vals)
    else:
        no_av_hits_string = 'NULL\n'
        av_list.append(no_av_hits_string)
    av_string = ''.join(av_list)
    dns_list = []
    if dns_domain_list:
        length2 = len(dns_domain_list)
        for x in range(0, length2):
            a = dns_domain_list[x]
            b = dns_ip_list[x]
            dns_string_vals = "%s\n%s\n\n" % (a, b)
            dns_list.append(dns_string_vals)
    else:
        no_dns_string = 'NULL\n'
        dns_list.append(no_dns_string)
    dns_string = ''.join(dns_list)
    flows_list = []
    if flows_dest_ip_list:
        length3 = len(flows_dest_ip_list)
        for x in range(0, length3):
            a = flows_dest_ip_list[x]
            b = flows_dest_port_list[x]
            flow_string_vals = "dst_ip: %s:%s\n" % (a, b)
            flows_list.append(flow_string_vals)
    else:
        no_flow_string = 'NULL\n'
        flows_list.append(no_flow_string)
    flows_string = ''.join(flows_list)
    http_list = []
    if http_request_type_list:
        length4 = len(http_request_type_list)
        for x in range(0, length4):
            a = http_request_type_list[x]
            b = http_request_text_list[x]
            http_string_vals = "*Request Type:* %s\n%s\n\n" % (a, b)
            http_list.append(http_string_vals)
    else:
        no_http_string = 'NULL\n'
        http_list.append(no_http_string)
    http_string = ''.join(http_list)
    analysis_results = "%s\n*pehash:* %s\n*packer:* %s\n\n----------------------------------------\n*AV Hits:*\n%s\n----------------------------------------\n*DNS:*\n%s----------------------------------------\n*Flow Results:*\n%s\n----------------------------------------\n*HTTP Results:*\n%s" % (file_info_string, pehash_string, packer_string, av_string, dns_string, flows_string, http_string)
    return analysis_results


def check_param(arg):
    keys = ['dns', 'email', 'filename', 'hash', 'ip', 'url', 'av', 'mutex', 'pdb', 'registry', 'useragent', 'version']
    if arg[0] not in keys:
        return 'error1'
    if len(arg) == 1:
        return 'error1'


def build_query(arg):
    if arg[0] == 'dns':
        arg[0] = 'dnsrr'
        query = ':'.join(arg)
        return query
    else:
        query = ':'.join(arg)
        return query


def get_search_results_from_json(arg):
    number_found = arg['response']['result']['@numFound']
    if number_found == 0:
        search_results = 'error2'
        return search_results
    else:
        page_number = arg['response']['result']['@start']
        x = float(number_found) / 10
        of_page = int(ceil(x))
        text_list = []
        for k, v in arg.iteritems():
            if type(v) == dict:
                for subkey, subvalue in v.iteritems():
                    for subkey2, subvalue2 in subvalue.iteritems():
                        if type(subvalue2) == list:
                            for d in subvalue2:
                                if subkey2 == 'doc':
                                    text_list.append(d['str']['#text'])
                        elif type(subvalue2) == dict:
                            if subkey2 == 'doc':
                                text_list.append(subvalue2['str']['#text'])
        sha1_string = '\n'.join(text_list)
        search_results = "*Number of Results Found:* %s\n*Page:* %s *of* %s\n\n*sha1 hashes:*\n%s" % (number_found, page_number, of_page, sha1_string)
        return search_results


def clean_list_for_query(arg):
    blist = arg
    if '|' in blist[1]:
        blist = [y for x in blist for y in x.split('|')]
        del blist[1]
    if '>' or '<' in blist[1]:
        x = blist[1].replace('>', "").replace('<', '')
        blist[1] = x
    return blist


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'totalhash' and alist[1] == 'analysis':
        time.sleep(1)
        alist = alist[2:]
        sign = build_sign(alist[0])
        request = 'analysis'
        refined_url = build_url(request, sign, alist[0])
        response = get_th_data(refined_url)
        if response.status_code == 404:
            outputs.append([channel, '404: The requested resource could not be found but may be available again in the future. Subsequent requests by the client are permissible.'])
        elif response.status_code == 200:
            json_data = get_json_from_response(response.content)
            analysis_results = get_analysis_from_json(json_data)
            outputs.append([channel, analysis_results])
    if alist[0] == 'totalhash' and alist[1] == 'search':
        time.sleep(1)
        alist = alist[2:]
        blist = clean_list_for_query(alist)
        if 'page=' in alist[-1]:
            page = int(filter(str.isdigit, blist[-1]))
            del blist[-1]
        else:
            page = 0
        check = check_param(blist)
        if check == 'error1':
            outputs.append([channel, "incorrect search parameter, try:\ntotalhash search (dns|email|filename|hash|ip|url|av|mutex|pdb|registry|useragent|version|) <searchitem>\nsee https://totalhash.cymru.com/api-documentation/ for help formatting searchitem"])
        else:
            query = build_query(blist)
            sign = build_sign(query)
            request = 'search'
            refined_url = build_url(request, sign, query, page)
            response = get_th_data(refined_url)
            json_data = get_json_from_response(response.content)
            search_results = get_search_results_from_json(json_data)
            if search_results == 'error2':
                outputs.append([channel, 'No results found'])
            else:
                outputs.append([channel, search_results])
    elif alist[0] == 'totalhash' and alist[1] == 'usage':
        time.sleep(1)
        sign = build_sign(alist[1])
        refined_url = build_url(alist[1], sign)
        response = get_th_data(refined_url)
        if response.status_code == 404:
            outputs.append([channel, '404: The requested resource could not be found but may be available again in the future. Subsequent requests by the client are permissible.'])
        elif response.status_code == 200:
            outputs.append([channel, response.content])
