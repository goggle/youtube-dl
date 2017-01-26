# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    sanitized_Request,
    urlencode_postdata,
)


class QuicklineBaseIE(InfoExtractor):
    _LOGIN_URL = 'https://mobiltv.quickline.com/login'
    _LOGIN_URL = 'https://mobiltv.quickline.com/zapi/v2/account/login'
    _LOGIN_URL2 = 'https://mobiltv.quickline.com/autofill-dummy.html'
    _WATCH_URL = 'http://mobiltv.quickline.com/zapi/watch'
    _USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

    def _login(self):
        (username, password) = self._get_login_info()
        if username is None:
            return

        login_form = {
            'login': username,
            'password': password,
            'remember': 'true',
        }

        request = sanitized_Request(
            self._LOGIN_URL, urlencode_postdata(login_form))
        request.add_header('Referer', 'https://mobiltv.quickline.com/login')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.add_header('User-Agent', self._USER_AGENT)
        request.add_header('X-Requested-With', 'XMLHttpRequest')

        login_form2 = {
            'login': username,
            'password': password,
        }
        request2 = sanitized_Request(
            self._LOGIN_URL2, urlencode_postdata(login_form2))
        request2.add_header('Referer', 'https://mobiltv.quickline.com/login')
        request2.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request2.add_header('User-Agent', self._USER_AGENT)


        response = self._download_webpage(
            request2, None, 'Logging in as %s' % username)

        # print(response)
        # response = self._download_json(request, None)
        print('RESPONSE: {}'.format(response))
        self.report_login()



    def _real_initialize(self):
        self._login()


class QuicklineLiveIE(QuicklineBaseIE):
    _VALID_URL = r'https?://mobiltv\.quickline\.com/watch/(?P<id>[^/]+)$' # TODO: Fix that

    _TEST = {
        'url': 'http://yourextractor.com/watch/42',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '42',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        # webpage = self._download_webpage(url, video_id)
        # print('WEBPAGE {}'.format(webpage))
        #
        # # TODO more code goes here, for example ...
        # title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')

        form = {
            'cid': 'sf-2',
            'stream_type': 'dash',
            'timeshift': '10800',
        }

        request = sanitized_Request(
            self._WATCH_URL, urlencode_postdata(form))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.add_header('Referer', 'http://mobiltv.quickline.com/watch/srf_zwei')
        request.add_header('User-Agent', self._USER_AGENT)
        request.add_header('X-Requested-With', 'XMLHttpRequest')



        # response = self._download_webpage(
        #     request, None, 'Logging in as %s' % username)
        response = self._download_json(request, video_id)
        print(response)


        return {
            'id': video_id,
            'title': 'No title',
            # 'description': self._og_search_description(webpage),
            # 'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }


class QuicklineVideoIE(QuicklineBaseIE):
    _VALID_URL = r'https?://mobiltv\.quickline\.com/watch/(?P<channel>.+)/(?P<id>[0-9]+)-.+/(?P<id2>[0-9]+)/(?P<id3>[0-9]+)'

    def _real_extract(self, url):
        print('YO BITCHES')
        formats = self._extract_mpd_formats('http://zba2-1-dash-pvr.zahs.tv/HD_rtl_schweiz/1484773800/1484778900/manifest.mpd?z32=OVZWK4S7NFSD2MRTGM3DEMBWGMTG22LOOJQXIZJ5GATG2YLYOJQXIZJ5GATHG2LHHVSDAZRUGQYDSZLEGE4DSOLFMI4GCOBQME2TMZDEMZTGGODCGU4DKJTDONUWIPJRGQ4UIMJVGU3TMOKFIRCDGQZSFU3EKMZXGEZDINZUHEZUCOBVIY3SM2LONF2GSYLMOJQXIZJ5GA', None)
        return {
            'title': 'jungle',
            'id': '1223',
            'formats': formats

        }
