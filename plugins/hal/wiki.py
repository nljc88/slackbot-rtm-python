
import wikipedia
import time

crontable = []
outputs = []


def build_keywords(arg1):
    keywords = ' '.join(arg1)
    return keywords


def wiki_summary(arg2):
    try:
        summary = wikipedia.summary(arg2)
        summary_encoded = str(summary.encode('ascii', 'ignore').decode('ascii'))
        return summary_encoded
    except wikipedia.exceptions.PageError:
        return 'error1'


def wiki_search(arg3):
    search_results_list = wikipedia.search(arg3, results=10, suggestion=False)
    return search_results_list


def wiki_page(arg4):
    try:
        page = wikipedia.page(arg4)
        return page
    except wikipedia.exceptions.PageError:
        return 'error1'


def wiki_random():
    random = wikipedia.random(pages=10)
    return random


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    text = str(text)
    string1 = text.lower()
    alist = string1.split(' ')
    if alist[0] == 'hal' and alist[1] == 'wiki':
        time.sleep(1)
        del alist[0]
        del alist[0]
        if 'summary' in string1:
            command = alist.index('summary')
            del alist[command]
            keywords = build_keywords(alist)
            summary = wiki_summary(keywords)
            if summary == 'error1':
                outputs.append([channel, "Page id '%s' does not match any pages. Try another id!" % keywords])
            else:
                outputs.append([channel, summary])
        elif 'search' in string1:
            command = alist.index('search')
            del alist[command]
            keywords = build_keywords(alist)
            search_results_list = wiki_search(keywords)
            if not search_results_list:
                outputs.append([channel, "no results, try again"])
            else:
                string = '\n'.join(search_results_list)
                outputs.append([channel, "Wikipedia Search Results:\n%s" % string])
        elif 'url' in string1:
            command = alist.index('url')
            del alist[command]
            keywords = build_keywords(alist)
            page = wiki_page(keywords)
            if page == 'error1':
                outputs.append([channel, "Page id '%s' does not match any pages. Try another id!" % keywords])
            else:
                url = page.url
                outputs.append([channel, url])
        elif 'references' in string1:
            command = alist.index('references')
            del alist[command]
            keywords = build_keywords(alist)
            page = wiki_page(keywords)
            if page == 'error1':
                outputs.append([channel, "Page id '%s' does not match any pages. Try another id!" % keywords])
            else:
                references = page.references
                if len(references) > 10:
                    short_references = references[:10]
                    string = '\n'.join(short_references)
                    outputs.append([channel, "Wikipedia References for %s:\n%s" % (keywords, string)])
                else:
                    string = '\n'.join(references)
                    outputs.append([channel, "Wikipedia References for %s:\n%s" % (keywords, string)])
        elif 'random' in string1:
            command = alist.index('random')
            del alist[command]
            keywords = build_keywords(alist)
            random_list = wiki_random()
            string = '\n'.join(random_list)
            outputs.append([channel, "Random Wikipedia Articles:\n%s" % string])
