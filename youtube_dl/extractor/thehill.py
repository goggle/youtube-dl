# coding: utf-8
from __future__ import unicode_literals

from .brightcove import BrightcoveLegacyIE
from .common import InfoExtractor


class TheHillIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?thehill\.com/.+/(?P<id>[0-9]+)-.+'
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
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)

        regex = r'<param[^>]+name=["\']%s["\'][^>]+value=["\'](.+)["\']'
        video_player = self._search_regex(regex % '@videoPlayer', webpage, 'video player')
        player_key = self._search_regex(regex % 'playerKey', webpage, 'player key')
        brightcove_url = BrightcoveLegacyIE._FEDERATED_URL + '?playerKey=' + player_key + '&%40videoPlayer=' + video_player

        return self.url_result(brightcove_url, ie=BrightcoveLegacyIE.ie_key())
