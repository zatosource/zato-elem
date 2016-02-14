# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# stdlib
from json import loads
from unittest import TestCase

# Zato
from zato.elem import Elem

# ################################################################################################################################

class ToJSON(TestCase):
    """ Tests .to_json serialization.
    """
    def setUp(self):
        self.maxDiff = None

    def test_to_json(self):
        """ Based on https://dev.twitter.com/rest/reference/get/statuses/show/:id
        All .to_json does is calling .dumps on output from .to_dict thus the majority
        of test cases are actually in test_to_dict.py.
        """
        doc = Elem()

        doc.coordinates = None
        doc.favorited = False
        doc.truncated = False
        doc.created_at = 'Wed Jun 06 20:07:10 +0000 2012'
        doc.id_str = '210462857140252672'
        doc.entities.urls[0].expanded_url = 'https://dev.twitter.com/terms/display-guidelines'
        doc.entities.urls[0].url = 'https://t.co/Ed4omjYs'
        doc.entities.urls[0].indices = [76, 97]
        doc.entities.urls[0].display_url = 'dev.twitter.com/terms/display-\u2026'
        doc.entities.hashtags[0].text = 'Twitterbird'
        doc.entities.hashtags[0].indices = [19, 31]
        doc.entities.user_mentions = []
        doc.in_reply_to_user_id_str = 2
        doc.contributors = [14927800]
        doc.text = "Along with our new #Twitterbird, we've also updated our Display Guidelines: https://t.co/Ed4omjYs  ^JC"
        doc.retweet_count = 66
        doc.in_reply_to_status_id_str = None
        doc.id = 210462857140252672
        doc.geo = None
        doc.retweeted = True
        doc.possibly_sensitive = False
        doc.in_reply_to_user_id = None
        doc.place = None
        doc.user.profile_sidebar_fill_color = 'DDEEF6'
        doc.user.profile_sidebar_border_color = 'C0DEED'
        doc.user.profile_background_tile = False
        doc.user.name = 'Twitter API'
        doc.user.profile_image_url = 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png'
        doc.user.created_at = 'Wed May 23 06:01:13 +0000 2007'
        doc.user.location = 'San Francisco, CA'
        doc.user.follow_request_sent = False
        doc.user.profile_link_color = '0084B4'
        doc.user.is_translator = False
        doc.user.id_str = '6253282'
        doc.user.entities.url.urls[0].expanded_url = None
        doc.user.entities.url.urls[0].url = 'http://dev.twitter.com'
        doc.user.entities.url.urls[0].indices = [0, 22]
        doc.user.entities.description.urls = []
        doc.user.default_profile = True
        doc.user.contributors_enabled = True
        doc.user.favourites_count = 24
        doc.user.url = 'http://dev.twitter.com'
        doc.user.profile_image_url_https = 'https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png'
        doc.user.utc_offset = -28800
        doc.user.id = 6253282
        doc.user.profile_use_background_image = True
        doc.user.listed_count = 10774
        doc.user.profile_text_color = '333333'
        doc.user.lang = 'en'
        doc.user.followers_count = 1212963
        doc.user.protected = False
        doc.user.notifications = None
        doc.user.profile_background_image_url_https = 'https://si0.twimg.com/images/themes/theme1/bg.png'
        doc.user.profile_background_color = 'C0DEED'
        doc.user.verified = True
        doc.user.geo_enabled = True
        doc.user.time_zone = 'Pacific Time (US & Canada)'
        doc.user.description = 'The Real Twitter API.'
        doc.user.default_profile_image = False
        doc.user.profile_background_image_url = 'http://a0.twimg.com/images/themes/theme1/bg.png'
        doc.user.statuses_count = 3333
        doc.user.friends_count = 31
        doc.user.following = True
        doc.user.show_all_inline_media = False
        doc.user.screen_name = 'twitterapi'
        doc.in_reply_to_screen_name = None
        doc.source = 'web'
        doc.in_reply_to_status_id = None

        expected = {
            'coordinates': None,
            'favorited': False,
            'truncated': False,
            'created_at': 'Wed Jun 06 20:07:10 +0000 2012',
            'id_str': '210462857140252672',

            'entities': {
                'urls': [
                    {'expanded_url': 'https://dev.twitter.com/terms/display-guidelines',
                     'url': 'https://t.co/Ed4omjYs',
                     'indices': [76, 97],
                     'display_url': 'dev.twitter.com/terms/display-\u2026'}
                ],
                'hashtags': [
                    {'text': 'Twitterbird',
                     'indices': [19, 31]}
                ],
                'user_mentions': []
            },
            'in_reply_to_user_id_str': 2,

            'contributors': [
                14927800
                ],
            'text': "Along with our new #Twitterbird, we've also updated our Display Guidelines: https://t.co/Ed4omjYs  ^JC",
            'retweet_count': 66,
            'in_reply_to_status_id_str': None,
            'id': 210462857140252672,
            'geo': None,
            'retweeted': True,
            'possibly_sensitive': False,
            'in_reply_to_user_id': None,
            'place': None,

            'user': {
                'profile_sidebar_fill_color': 'DDEEF6',
                'profile_sidebar_border_color': 'C0DEED',
                'profile_background_tile': False,
                'name': 'Twitter API',
                'profile_image_url': 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
                'created_at': 'Wed May 23 06:01:13 +0000 2007',
                'location': 'San Francisco, CA',
                'follow_request_sent': False,
                'profile_link_color': '0084B4',
                'is_translator': False,
                'id_str': '6253282',
                'entities': {
                    'url': {
                        'urls': [
                            {'expanded_url': None,
                             'url': 'http://dev.twitter.com',
                             'indices': [0, 22]
                            }
                        ]
                    },
                    'description': {'urls': []}
                    },
                'default_profile': True,
                'contributors_enabled': True,
                'favourites_count': 24,
                'url': 'http://dev.twitter.com',
                'profile_image_url_https': 'https://si0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
                'utc_offset': -28800,
                'id': 6253282,
                'profile_use_background_image': True,
                'listed_count': 10774,
                'profile_text_color': '333333',
                'lang': 'en',
                'followers_count': 1212963,
                'protected': False,
                'notifications': None,
                'profile_background_image_url_https': 'https://si0.twimg.com/images/themes/theme1/bg.png',
                'profile_background_color': 'C0DEED',
                'verified': True,
                'geo_enabled': True,
                'time_zone': 'Pacific Time (US & Canada)',
                'description': 'The Real Twitter API.',
                'default_profile_image': False,
                'profile_background_image_url': 'http://a0.twimg.com/images/themes/theme1/bg.png',
                'statuses_count': 3333,
                'friends_count': 31,
                'following': True,
                'show_all_inline_media': False,
                'screen_name': 'twitterapi'
                },
            'in_reply_to_screen_name': None,
            'source': 'web',
            'in_reply_to_status_id': None
        }

        out = loads(doc.to_json())
        self.assertDictEqual(expected, out)
