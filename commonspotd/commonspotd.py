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
    f = open('%s/.twitter_keys' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    APP_KEY = re.findall(ur'(?im)^APP_KEY\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    APP_SECRET = re.findall(ur'(?im)^APP_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return APP_KEY, APP_SECRET

def read_tokens():
    f = open('%s/.twitter_tokens' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    OAUTH_TOKEN = re.findall(ur'(?im)^OAUTH_TOKEN\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    OAUTH_TOKEN_SECRET = re.findall(ur'(?im)^OAUTH_TOKEN_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    if os.path.exists('%s/thumb.jpg' % (os.path.dirname(os.path.realpath(__file__)))):
        os.remove('%s/thumb.jpg' % (os.path.dirname(os.path.realpath(__file__))))
    elif os.path.exists('%s/thumb.png' % (os.path.dirname(os.path.realpath(__file__)))):
        os.remove('%s/thumb.png' % (os.path.dirname(os.path.realpath(__file__))))

    urltemplate = 'https://commons.wikimedia.org/wiki/Template:Potd/%s?action=raw' % (datetime.datetime.now().strftime('%Y-%m-%d'))
    raw = unicode(urllib.urlopen(urltemplate).read(), 'utf-8')
    imagename = re.findall(ur'(?im)\{\{\s*Potd[ _]filename\s*\|\s*([^\n\|]+?)[\n\|]', raw)[0].strip()
    imagename_ = re.sub(ur' ', ur'_', imagename)
    
    urltemplate2 = 'https://commons.wikimedia.org/wiki/Template:Potd/%s_(en)?action=raw' % (datetime.datetime.now().strftime('%Y-%m-%d'))
    raw2 = unicode(urllib.urlopen(urltemplate2).read(), 'utf-8')
    description = re.findall(ur'(?im)\{\{\s*Potd[ _]description\s*\|\s*1\s*=\s*([^\n]+?)\|\s*2\s*=\s*en', raw2)[0].strip()
    description = re.sub(ur'(?im)\[\[[^\|\]]*\|([^\]]*?)\]\]', ur'\1', description)
    description = re.sub(ur'(?im)\[\[([^\]]*?)\]\]', ur'\1', description)
    if len(description) > 80:
        description = '%s...' % (description[:80])
    
    md5 = hashlib.md5(imagename_.encode('utf-8')).hexdigest()
    thumburl='https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/800px-%s' % (md5[0], md5[:2], urllib.quote(imagename_.encode('utf-8')), urllib.quote(imagename_.encode('utf-8')))
    thumbfilename = '%s/thumb' % (os.path.dirname(os.path.realpath(__file__)))
    if imagename.endswith('.svg'):
        thumburl += '.png'
        thumbfilename += '.png'
    else:
        thumbfilename += '.jpg'
    urllib.urlretrieve(thumburl, thumbfilename)

    thumb = open(thumbfilename, 'rb')
    url = 'https://commons.wikimedia.org/wiki/File:%s' % (imagename_)
    twitter.update_status_with_media(status='%s %s #commons #potd' % (description, url), media=thumb)

if __name__ == '__main__':
    main()
