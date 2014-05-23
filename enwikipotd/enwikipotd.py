#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 emijrp
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
import urllib
from twython import Twython

def read_keys():
    f = open('.twitter_keys', 'r')
    w = f.read()
    APP_KEY = re.findall(ur'(?im)^APP_KEY\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    APP_SECRET = re.findall(ur'(?im)^APP_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return APP_KEY, APP_SECRET

def read_tokens():
    f = open('.twitter_tokens', 'r')
    w = f.read()
    OAUTH_TOKEN = re.findall(ur'(?im)^OAUTH_TOKEN\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    OAUTH_TOKEN_SECRET = re.findall(ur'(?im)^OAUTH_TOKEN_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    if os.path.exists('thumb.jpg'):
        os.remove('thumb.jpg')
    elif os.path.exists('thumb.png'):
        os.remove('thumb.png')

    urltemplate = 'https://en.wikipedia.org/wiki/Template:POTD/%s?action=raw' % (datetime.datetime.now().strftime('%Y-%m-%d'))
    raw = unicode(urllib.urlopen(urltemplate).read(), 'utf-8')
    imagename = re.findall(ur'(?im)\|\s*image\s*=\s*([^\n\|]+?)[\n\|]', raw)[0].strip()
    imagename_ = re.sub(ur' ', ur'_', imagename)
    texttitle = re.findall(ur'(?im)\|\s*texttitle\s*=\s*([^\n\|]+?)[\n\|]', raw)[0].strip()
    md5 = hashlib.md5(imagename_.encode('utf-8')).hexdigest()
    thumburl='https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/800px-%s' % (md5[0], md5[:2], imagename_, imagename_)
    thumbfilename = 'thumb'
    if imagename.endswith('.svg'):
        thumburl += '.png'
        thumbfilename += '.png'
    else:
        thumbfilename += '.jpg'
    urllib.urlretrieve(thumburl, thumbfilename)

    thumb = open(thumbfilename, 'rb')
    url = 'https://en.wikipedia.org/wiki/File:%s' % (imagename_)
    twitter.update_status_with_media(status='%s %s #wikipedia #potd' % (texttitle, url), media=thumb)

if __name__ == '__main__':
    main()
