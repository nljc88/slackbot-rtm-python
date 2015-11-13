
import time
import requests

crontable = []
outputs = []


def get_threatcrowd_data(type1, query):
    if type1 == 'domain':
        base_url = 'http://www.threatcrowd.org/searchApi/v1/api.php?type=%s&query=%s&displayDates=true'
        refined_url = base_url % (type1, query)
        response = requests.get(refined_url)
        return response
    else:
        base_url = 'http://www.threatcrowd.org/searchApi/v1/api.php?type=%s&query=%s'
        refined_url = base_url % (type1, query)
        response = requests.get(refined_url)
        return response


def get_results_from_data(response):
    list1 = response.split('\n')
    md5_list = []
    domain_list = []
    ip_list = []
    email_list = []
    for item in list1:
        if 'MD5' in item:
            md5_list.append(item)
        if 'DOMAIN' in item:
            domain_list.append(item)
        if 'IP' in item:
            ip_list.append(item)
        if 'EMAIL' in item:
            email_list.append(item)

    hashes_list = []
    analysis_list = []
    for items in md5_list:
        mid_list = []
        x = items.split(',')
        mid_list.append(x)
        for item1 in mid_list:
            hashes_list.append(item1[1])
            analysis_list.append(item1[2])
    length1 = len(hashes_list)
    md5_hash_list = []
    for x in range(0, length1):
        a = hashes_list[x]
        b = analysis_list[x]
        string_vals = "*md5*: %s\n*Analysis:* %s\n" % (a, b)
        md5_hash_list.append(string_vals)
    hash_string = '\n'.join(md5_hash_list)
    just_domains_list = []
    for item2 in domain_list:
        mid_list = []
        y = item2.split(',')
        mid_list.append(y)
        for item3 in mid_list:
            just_domains_list.append(item3[1])
    domain_vals_list = []
    for item in just_domains_list:
        string_vals = "  %s\n" % item
        domain_vals_list.append(string_vals)
    domain_string = "".join(domain_vals_list)
    just_ip_list = []
    for item in ip_list:
        mid_list = []
        z = item.split(',')
        mid_list.append(z)
        for item2 in mid_list:
            just_ip_list.append(item2[1])
    ip_vals_list = []
    for item in just_ip_list:
        string_vals = "  %s\n" % item
        ip_vals_list.append(string_vals)
    ip_string = ''.join(ip_vals_list)

    just_email_list = []
    for item in email_list:
        mid_list = []
        x = item.split(',')
        mid_list.append(x)
        for item2 in mid_list:
            just_email_list.append(item2[1])
    email_vals_list = []
    for item in just_email_list:
        string_vals = "  %s\n" % item
        email_vals_list.append(string_vals)
    email_string = ''.join(email_vals_list)

    threatcrowd_results = "*HASHES:*\n%s\n----------------------------------------\n*DOMAINS:*\n%s\n----------------------------------------\n*IPs:*\n%s\n----------------------------------------\n*EMAILS:*\n%s" % (hash_string, domain_string, ip_string, email_string)
    return threatcrowd_results


def clean_list_for_query(blist):
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
    if alist[0] == '!threatcrowd':
        time.sleep(1)
        alist = alist[1:]
        blist = clean_list_for_query(alist)
        response = get_threatcrowd_data(blist[0], blist[1])
        threatcrowd_results = get_results_from_data(response.content)
        outputs.append([channel, threatcrowd_results])
