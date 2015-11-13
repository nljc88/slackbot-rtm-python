
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
import itertools
import collections

crontable = []
outputs = []


class YouTube(object):

    API_SERVICE = 'youtube'
    API_VERSION = 'v3'
    API_KEY = 'API_KEY'

    def __init__(self):

        self.service = build(self.API_SERVICE,
                             self.API_VERSION,
                             developerKey=self.API_KEY)

    def video_search(self, query, results=1):
        link = 'https://www.youtube.com/watch?v=%s'
        url_results = list()
        title_list = list()

        params = dict()
        params['q'] = query
        params['type'] = 'video'
        params['part'] = 'id, snippet'
        params['maxResults'] = results
        params['videoEmbeddable'] = 'true'

        try:
            video_results = self.search(**params)
            for item in video_results['items']:
                video_url = link % item['id']['videoId'].encode('utf-8')
                url_results.append(video_url)
                titles = item['snippet']['title'].encode('ascii', 'ignore').decode('ascii')
                title_list.append(titles)
        except:
            # Add Log Event
            pass

        return url_results, title_list

    def search(self, **parameters):

        valid_params = ('part', 'forContentOwner', 'forDeveloper', 'forMine',
                        'relatedToVideoId', 'channelId', 'channelType',
                        'eventType', 'location', 'locationRadius',
                        'maxResults', 'onBehalfOfContentOwner', 'order',
                        'pageToken', 'publishedAfter', 'publishedBefore', 'q',
                        'regionCode', 'relevanceLanguage', 'safeSearch',
                        'topicId', 'type', 'videoCaption', 'videoCategoryId',
                        'videoDefinition', 'videoDimension', 'videoDuration',
                        'videoEmbeddable', 'videoLicense', 'videoSyndicated',
                        'videoType')

        required_params = ('part',)

        method = self.service.search()

        # Check all passsed parameters are valid ones
        for param in parameters:
            if param not in valid_params:
                # Add Log Event
                parameters.pop(param)

        # Ensure mandatory parameters are present
        if not all(param in parameters for param in required_params):
            raise AttributeError()

        response = method.list(**parameters).execute()
        return response


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'youtube':
        time.sleep(1)
        if alist[1] == 'list':
            alist = alist[2:]
            searchterm = ' '.join(alist)
            class_object = YouTube()
            results = class_object.video_search(searchterm, results=5)
            url_list = results[0]
            titles_list = results[1]
            cdict = collections.OrderedDict(itertools.izip(titles_list, url_list))
            for k, v in cdict.items():
                outputs.append([channel, "{}: \n{}\n".format(k, v)])
        else:
            alist = alist[1:]
            searchterm = ' '.join(alist)
            class_object = YouTube()
            results = class_object.video_search(searchterm)
            for item in results:
                url_list = results[0]
            outputs.append([channel, url_list[0]])
