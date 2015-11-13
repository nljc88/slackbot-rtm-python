
import time
import requests
import json

crontable = []
outputs = []

apikey = 'apikey'


def build_report_params(arg1, arg2):
    params = {arg1: arg2, "apikey": apikey}
    return params


def submit_url_scan_and_get_response(arg1, arg2):
    base_url = 'https://www.virustotal.com/vtapi/v2/%s'
    refined_url = base_url % arg1
    response = requests.post(refined_url, params=arg2)
    json_data = json.loads(response.content)
    return json_data


def get_post_results_from_json(arg):
    if arg['response_code'] == 0:
        verbose_msg = arg['verbose_msg'].encode('utf-8')
        return verbose_msg
    elif arg['response_code'] == 1:
        verbose_msg = arg['verbose_msg'].encode('utf-8')
        scan_date = arg['scan_date'].encode('utf-8')
        permalink = arg['permalink'].encode('utf-8')
        post_results = "%s\n%s\n%s" % (verbose_msg, scan_date, permalink)
        return post_results


def get_vt_json_data(arg1, arg2):
    base_url = 'https://www.virustotal.com/vtapi/v2/%s'
    refined_url = base_url % arg1
    response = requests.get(refined_url, params=arg2)
    json_data = json.loads(response.content)
    return json_data


def get_vt_file_report_from_json(arg):
    if arg['response_code'] == 0:
        verbose_msg = arg['verbose_msg'].encode('utf-8')
        return verbose_msg
    elif arg['response_code'] == 1:
        scan_date = arg['scan_date']
        av_hits = arg['positives']
        sha256 = arg['sha256']
        sha1 = arg['sha1']
        md5 = arg['md5']
        av_engine_list = []
        result_list = []
        for k, v in arg.iteritems():
            if type(v) == dict:
                for subkey, subvalue in v.iteritems():
                    if subvalue['detected'] == True:
                        av_engine_list.append(subkey.encode('utf-8'))
                        result_list.append(subvalue['result'].encode('utf-8'))
        av_engine_hit_list = []
        if av_engine_list:
            length1 = len(av_engine_list)
            for x in range(0, length1):
                a = av_engine_list[x]
                b = result_list[x]
                av_string_vals = "%s: %s\n" % (a, b)
                av_engine_hit_list.append(av_string_vals)
        else:
            no_av_hits_string = 'No AV Engines hit on the hash'
            av_engine_hit_list.append(no_av_hits_string)
        av_hit_string = ''.join(av_engine_hit_list)
        vt_results = "*Scan Date:* %s\n*AV-Hits:* %s\n*Sha256:* %s\n*Sha1:* %s\n*md5:* %s\n\n----------------------------------------\n*AV Engines:*\n%s" % (scan_date, av_hits, sha256, sha1, md5, av_hit_string)
        return vt_results


def get_vt_url_report_from_json(arg):
    if arg['response_code'] == 0:
        verbose_msg = arg['verbose_msg'].encode('utf-8')
        return verbose_msg
    elif arg['response_code'] == 1:
        scan_date = arg['scan_date']
        av_hits = arg['positives']
        av_engine_list = []
        result_list = []
        for k, v in arg.iteritems():
            if type(v) == dict:
                for subkey, subvalue in v.iteritems():
                    if subvalue['detected'] == True:
                        av_engine_list.append(subkey.encode('utf-8'))
                        result_list.append(subvalue['result'].encode('utf-8'))
        av_engine_hit_list = []
        if av_engine_list:
            length1 = len(av_engine_list)
            for x in range(0, length1):
                a = av_engine_list[x]
                b = result_list[x]
                av_string_vals = "%s: %s\n" % (a, b)
                av_engine_hit_list.append(av_string_vals)
        else:
            no_av_hits_string = 'No AV Engines hit on the hash'
            av_engine_hit_list.append(no_av_hits_string)
        av_hit_string = ''.join(av_engine_hit_list)
        vt_results = "*Scan Date:* %s\n*AV-Hits:* %s\n\n*AV Engines:*\n%s" % (scan_date, av_hits, av_hit_string)
        return vt_results


def get_vt_ip_report_from_json(arg):
    if arg['response_code'] == 0:
        verbose_msg = arg['verbose_msg'].encode('utf-8')
        return verbose_msg
    elif arg['response_code'] == 1:
        asn = arg['asn']
        country = arg['country'].encode('utf-8')
        detected_urls_list = []
        detected_urls_scan_date_list = []
        for d in arg['detected_urls']:
            detected_urls_list.append(d['url'].encode('utf-8'))
            detected_urls_scan_date_list.append(d['scan_date'].encode('utf-8'))
        url_list = []
        if detected_urls_list:
            length2 = len(detected_urls_list)
            for x in range(0, length2):
                a = detected_urls_scan_date_list[x]
                b = detected_urls_list[x]
                detected_url_string_vals = "*Scan Date:* %s\n*url:* %s\n\n" % (a, b)
                url_list.append(detected_url_string_vals)
        else:
            no_det_urls = 'No URLs detected'
            url_list.append(no_det_urls)
        detected_url_string = ''.join(url_list)
        resolv_date_list = []
        resolv_hostname_list = []
        for e in arg['resolutions']:
            resolv_date_list.append(e['last_resolved'].encode('utf-8'))
            resolv_hostname_list.append(e['hostname'].encode('utf-8'))
        resolv_list = []
        if resolv_date_list:
            length3 = len(resolv_date_list)
            for x in range(0, length3):
                a = resolv_date_list[x]
                b = resolv_hostname_list[x]
                resolv_host_string_vals = "*Last Resolved:* %s\n*hostname:* %s\n\n" % (a, b)
                resolv_list.append(resolv_host_string_vals)
        else:
            no_resolv_hostnames = 'No hostnames resolved'
            resolv_list.append(no_resolv_hostnames)
        resolv_host_string = ''.join(resolv_list)
        vt_results = "*ASN:* %s\n*Country:* %s\n\n*Detected URLs:*\n%s\n\n----------------------------------------\n*Resolutions:*\n%s" % (asn, country, detected_url_string, resolv_host_string)
        return vt_results


def get_vt_domain_report_from_json(arg):
    if arg['response_code'] == 0:
        verbose_msg = arg['verbose_msg'].encode('utf-8')
        return verbose_msg
    elif arg['response_code'] == 1:
        bitdefender_cat = arg['BitDefender category']
        whois_info = arg['whois']
        websense_threatseeker_cat = arg['Websense ThreatSeeker category']
        webutation_verdict = arg['Webutation domain info']['Verdict']
        detected_urls_list = []
        detected_urls_scan_date_list = []
        for d in arg['detected_urls']:
            detected_urls_list.append(d['url'].encode('utf-8'))
            detected_urls_scan_date_list.append(d['scan_date'].encode('utf-8'))
        url_list = []
        if detected_urls_list:
            length2 = len(detected_urls_list)
            for x in range(0, length2):
                a = detected_urls_scan_date_list[x]
                b = detected_urls_list[x]
                detected_url_string_vals = "*Scan Date:* %s\n*url:* %s\n\n" % (a, b)
                url_list.append(detected_url_string_vals)
        else:
            no_det_urls = 'No URLs detected'
            url_list.append(no_det_urls)
        detected_url_string = ''.join(url_list)
        resolv_date_list = []
        resolv_ip_list = []
        for e in arg['resolutions']:
            resolv_date_list.append(e['last_resolved'].encode('utf-8'))
            resolv_ip_list.append(e['ip_address'].encode('utf-8'))
        resolv_list = []
        if resolv_date_list:
            length3 = len(resolv_date_list)
            for x in range(0, length3):
                a = resolv_date_list[x]
                b = resolv_ip_list[x]
                resolv_ip_string_vals = "*Last Resolved:* %s\n*IP:* %s\n\n" % (a, b)
                resolv_list.append(resolv_ip_string_vals)
        else:
            no_resolv_ips = 'No IPs resolved'
            resolv_list.append(no_resolv_ips)
        resolv_ip_string = ''.join(resolv_list)
        vt_results = "*BitDefender:* %s\n*Whois:*\n%s\n----------------------------------------\n\n*Websense Threatseeker:* %s\n*Webutation Verdict:* %s\n\n----------------------------------------\n*Detected URLs:*\n%s----------------------------------------\n*Resolved IPs:*\n%s" % (bitdefender_cat, whois_info, websense_threatseeker_cat, webutation_verdict, detected_url_string, resolv_ip_string)
        return vt_results


def clean_list_for_query(arg):
    blist = arg
    if '|' in blist[0]:
        blist = [y for x in blist for y in x.split('|')]
        del blist[0]
    if '>' or '<' in blist[0]:
        x = blist[0].replace('>', "").replace('<', '')
        blist[0] = x
    return blist


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == '!vt' and alist[1] == 'hash':
        time.sleep(1)
        alist = alist[2:]
        param_key = 'resource'
        params = build_report_params(param_key, alist[0])
        query = 'file/report'
        json_data = get_vt_json_data(query, params)
        vt_results = get_vt_file_report_from_json(json_data)
        outputs.append([channel, vt_results])
    elif alist[0] == '!vt' and alist[1] == 'url':
        time.sleep(1)
        alist = alist[2:]
        blist = clean_list_for_query(alist)
        param_key = 'resource'
        params = build_report_params(param_key, blist[0])
        query = 'url/report'
        json_data = get_vt_json_data(query, params)
        vt_results = get_vt_url_report_from_json(json_data)
        outputs.append([channel, vt_results])
    elif alist[0] == '!vt' and alist[1] == 'url-scan':
        time.sleep(1)
        alist = alist[2:]
        blist = clean_list_for_query(alist)
        param_key = 'url'
        params = build_report_params(param_key, blist[0])
        query = 'url/scan'
        post_json_data = submit_url_scan_and_get_response(query, params)
        vt_results = get_post_results_from_json(post_json_data)
        outputs.append([channel, vt_results])
    elif alist[0] == '!vt' and alist[1] == 'ip':
        time.sleep(1)
        alist = alist[2:]
        param_key = 'ip'
        params = build_report_params(param_key, alist[0])
        query = 'ip-address/report'
        json_data = get_vt_json_data(query, params)
        vt_results = get_vt_ip_report_from_json(json_data)
        string1 = alist[0]
        outputs.append([channel, '*Searched IP:* %s\n%s' % (string1, vt_results)])
    elif alist[0] == '!vt' and alist[1] == 'domain':
        time.sleep(1)
        alist = alist[2:]
        blist = clean_list_for_query(alist)
        param_key = 'domain'
        params = build_report_params(param_key, blist[0])
        query = 'domain/report'
        json_data = get_vt_json_data(query, params)
        vt_results = get_vt_domain_report_from_json(json_data)
        outputs.append([channel, vt_results])
