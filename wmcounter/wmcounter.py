#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014-2017 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import hashlib
import os
import random
import re
import time
import urllib
from twython import Twython

def read_keys():
    f = open('%s/.twitter_keys' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    APP_KEY = re.findall(r'(?im)^APP_KEY\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    APP_SECRET = re.findall(r'(?im)^APP_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return APP_KEY, APP_SECRET

def read_tokens():
    f = open('%s/.twitter_tokens' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    OAUTH_TOKEN = re.findall(r'(?im)^OAUTH_TOKEN\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    OAUTH_TOKEN_SECRET = re.findall(r'(?im)^OAUTH_TOKEN_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    gap = 1000000
    response = urllib.request.urlopen('https://tools.wmflabs.org/wmcounter/wmcounter.data.js')
    raw = response.readall().decode('utf-8')
    if re.search(r"(?im)var editinit = (\d+)", raw):
        current_count = int(re.findall(r"(?im)var editinit = (\d+)", raw)[0].strip())
        f = open('%s/wmcounter.log' % (os.path.dirname(os.path.realpath(__file__))), 'r')
        previous_count = int(f.read().strip())
        f.close()
        if current_count and previous_count and previous_count > 3000000000 and current_count >= previous_count + gap:
            current_count_round = current_count - (current_count % gap)
            
            number = '{:,}'.format(current_count_round)
            hashtags = ['#wikipedia', '#wikimedia', '#wikidata', '#commons', '#wikisource', '#wiktionary', '#wikibooks', '#wikiversity', '#wikivoyage']
            htl = 5
            
            #en
            random.shuffle(hashtags)
            status = '%s edits - Watch it live! https://tools.wmflabs.org/wmcounter/ %s' % (number, ' '.join(hashtags[:htl]))
            twitter.update_status(status=status)
            time.sleep(10)
            #es
            random.shuffle(hashtags)
            status = '%s ediciones - ¡Míralo en directo! https://tools.wmflabs.org/wmcounter/ %s' % (number.replace(',', '.'), ' '.join(hashtags[:htl]))
            twitter.update_status(status=status)
            time.sleep(10)
            #fr
            random.shuffle(hashtags)
            status = '%s éditions - https://tools.wmflabs.org/wmcounter/ %s' % (number.replace(',', ' '), ' '.join(hashtags[:htl]))
            twitter.update_status(status=status)
            time.sleep(10)
            #pt
            random.shuffle(hashtags)
            status = '%s edições - https://tools.wmflabs.org/wmcounter/ %s' % (number.replace(',', '.'), ' '.join(hashtags[:htl]))
            twitter.update_status(status=status)
            time.sleep(10)
            #ru
            random.shuffle(hashtags)
            status = '%s правок - https://tools.wmflabs.org/wmcounter/ %s' % (number.replace(',', ' '), ' '.join(hashtags[:htl]))
            twitter.update_status(status=status)
            time.sleep(10)
            
            g = open('%s/wmcounter.log' % (os.path.dirname(os.path.realpath(__file__))), 'w')
            g.write(str(current_count_round))
            g.close()
        else:
            print('Update not needed yet',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    main()
