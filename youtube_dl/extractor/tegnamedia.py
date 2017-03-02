# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    parse_duration,
    str_or_none,
    unified_timestamp,
)


class TegnaMediaIE(InfoExtractor):
    _VALID_URL = r'''(?x)
                    https?://
                        (?:www\.)?
                        (?P<channel>
                            (?:thv11|todaysthv)\.com|
                            12news\.com|
                            # tucsonnewsnow\.com| This one is different
                            (?:abc10|news10)\.com|
                            9news\.com|
                            wusa9\.com|
                            firstcoastnews\.com|
                            wtsp\.com|
                            # myatltv\.com| # Does this one work?
                            11alive\.com|
                            13wmaz\.com|
                            ktvb\.com|
                            whas11\.com|
                            (?:wwltv|wupltv)\.com|
                            wlbz2\.com|
                            wcsh6\.com|
                            wzzm13\.com|
                            kare11\.com|
                            ksdk\.com|
                            wcnc\.com|
                            wfmynews2\.com|
                            wgrz\.com|
                            wkyc\.com|
                            kgw\.com|
                            wltx\.com|
                            kvue\.com|
                            12newsnow\.com|
                            kagstv\.com|
                            kiiitv\.com|
                            wfaa\.com|
                            khou\.com|
                            myfoxzone\.com|
                            kens5\.com|
                            cbs19\.tv|
                            kcentv\.com|
                            (?:13newsnow|wvec)\.com|
                            king5\.com|
                            krem\.com|
                            spokanescw22\.com # Does this work?
                        )
                        /.+?/
                        (?P<id>[0-9]+)$
                    '''
    _SUBSCRIPTION_KEYS = {
        'thv11.com': 'd8d2110b71e5490f8652a270ef1cc8c2',
        'todaysthv.com': 'd8d2110b71e5490f8652a270ef1cc8c2',
        '12news.com': 'd721cdf2210c493cb8a194d1e53b4ef5',
        'abc10.com': '18b00432d8f34c77a8eb4d0fab784d9b',
        'news10.com': '18b00432d8f34c77a8eb4d0fab784d9b',
        '9news.com': 'ae1d3e46c9914e9b87757fead91d7654',
        'wusa9.com': '7460415cfdd548c7bcc9b3910cf540be',
        'firstcoastnews.com': '31adc5f926f54d8eab0e3fa4ae463783',
        'wtsp.com': '8a2be5f0fd7a4dd2a5588e3d053ee04a',
        '11alive.com': 'd2305405b1804d90a074e434c75900fd',
        '13wmaz.com': '8581efc654d8472bafc47b126724ebf8',
        'ktvb.com': '08a28e05f0cf442290e2d1a22e3743ef',
        'whas11.com': '01782147ad8a4be485c5c0078d886f09',
        'wwltv.com': '17675484a9b249d0970256b52ffdf916',
        'wlbz2.com': 'f2ebcb9f9a2a4ebf8bdb6df29e673227',
        'wcsh6.com': 'e7bde2553fa842fcbc9845e81baf5c42',
        'wzzm13.com': 'ce255d82695c4515961f06fd628de155',
        'kare11.com': '889d9f26fb804ab2aef4165db4a3e6f6',
        'ksdk.com': '29ef605dc92345708f6da324ff5c637f',
        'other': 'ae1d3e46c9914e9b87757fead91d7654',
    }

    def _real_extract(self, url):
        channel, show_id = re.match(self._VALID_URL, url).groups()
        webpage = self._download_webpage(url, show_id)

        player_info = self._html_search_regex(
            r'<div[^>]+class="js-jwloader"(?P<info>[^>]+)', webpage, 'player info')
        data_id = self._search_regex(
            r'data-id="(?P<id>\d+)"', player_info, 'video id')
        data_site = self._search_regex(
            r'data-site="(?P<data_site>\d+)"', player_info, 'data site')

        api_url = 'http://api.tegna-tv.com/video/v2/getAllVideoPathsById/%s/%s?subscription-key=%s' % (data_id,
            data_site, self._SUBSCRIPTION_KEYS['other'])
        video_json = self._download_json(api_url, show_id)

        video_id = str_or_none(video_json['Id'])
        title = str_or_none(video_json['Title'])
        description = str_or_none(video_json.get('Description'))
        thumbnail = str_or_none(video_json.get('Image'))

        duration = parse_duration(str_or_none(video_json.get('VideoLength')))
        timestamp = unified_timestamp(str_or_none(video_json.get('DateCreated')))

        formats = []
        for elem in video_json.get('Sources'):
            path = str_or_none(elem['Path'])
            if elem.get('Format') == 'MP4':
                formats.append(
                    {
                        'url': path,
                        'format_id': 'mp4-' + str_or_none(elem['EncodingRate']),
                        'vbr': int_or_none(elem['EncodingRate']),
                    }
                )
            elif elem.get('Format') == 'HLS':
                forms = self._extract_m3u8_formats(
                    path, video_id, ext='mp4', entry_protocol='m3u8_native')
                formats += forms
            elif elem.get('Format') == 'HDS':
                path += '/manifest.f4m?hdcode'
                forms = self._extract_akamai_formats(path, video_id)
                formats += forms

        self._sort_formats(formats)
        return {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'duration': duration,
            'timestamp': timestamp,
            'formats': formats,
        }


# class NineNewsIE(TegnaMediaIE):
#     _VALID_URL = r'https?://(?:www\.)?9news\.com/.+/(?P<id>[0-9]+)'
#     SUBSCRIPTION_KEY = 'ae1d3e46c9914e9b87757fead91d7654'
#
#     _TEST = {
#         'url': 'http://www.9news.com/news/local/father-worries-about-immigration-status/408808900',
#         'md5': 'e367c89e52eed4ff3bcc696d664e4f4b',
#         'info_dict': {
#             'id': '2512310',
#             'ext': 'mp4',
#             'title': 'Father worries about immigration status',
#             'description': '9NEWS @ 9. 2/15/2017',
#             'thumbnail': 'http://kusa-download.edgesuite.net/video/2512310/2512310_Still.jpg',
#             'duration': 96.0,
#             'timestamp': 1487218434,
#             'upload_date': '20170216',
#         }
#     }
#
#     def _real_extract(self, url):
#         return super(NineNewsIE, self)._real_extract(url)
#
#
# class TwelveNewsIE(TegnaMediaIE):
#     _VALID_URL = r'https?://(?:www\.)?12news\.com/.+/(?P<id>[0-9]+)'
#     SUBSCRIPTION_KEY = 'd721cdf2210c493cb8a194d1e53b4ef5'
#
#     _TEST = {
#         'url': 'http://www.12news.com/news/local/valley/dps-stops-wrong-way-driver-after-several-miles/408864874',
#         'info_dict': {
#             'id': '2514219',
#             'ext': 'mp4',
#             'title': '''Megan Melanson's initial court appearance''',
#             'description': 'md5:24188e754669c29700e8dd6d19e4943b',
#             'timestamp': 1487360943,
#             'upload_date': '20170217',
#         },
#         'params': {
#             'skip_download': True,
#         }
#     }
#
#     def _real_extract(self, url):
#         return super(TwelveNewsIE, self)._real_extract(url)
#
#
# class THVElevenIE(TegnaMediaIE):
#     _VALID_URL = r'https?://(?:www\.)?thv11\.com/.+/(?P<id>[0-9]+)'
#     SUBSCRIPTION_KEY = 'd8d2110b71e5490f8652a270ef1cc8c2'
#
#     def _real_extract(self, url):
#         return super(THVElevenIE, self)._real_extract(url)
