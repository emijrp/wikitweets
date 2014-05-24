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
import json
import os
import random
import re
import time
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

def getUserEditCount(username=''):
    urleditcount = 'http://en.wikipedia.org/w/api.php?action=query&list=users&ususers=%s&usprop=groups|editcount|gender&format=json' % (username.encode('utf-8'))
    jsoneditcount = json.loads(unicode(urllib.urlopen(urleditcount).read(), 'utf-8'))
    return jsoneditcount['query']['users'][0]['editcount']

def getUserGroups(username=''):
    urleditcount = 'http://en.wikipedia.org/w/api.php?action=query&list=users&ususers=%s&usprop=groups|editcount|gender&format=json' % (username.encode('utf-8'))
    jsoneditcount = json.loads(unicode(urllib.urlopen(urleditcount).read(), 'utf-8'))
    return jsoneditcount['query']['users'][0]['groups']

def imageIsOnCommons(image=''):
    image_ = re.sub(ur' ', ur'_', image)
    urlimage = 'http://en.wikipedia.org/w/api.php?action=query&titles=File:%s&prop=imageinfo&format=json' % (image_.encode('utf-8'))
    jsonimage = json.loads(unicode(urllib.urlopen(urlimage).read(), 'utf-8'))
    return jsonimage['query']['pages'][jsonimage['query']['pages'].keys()[0]]['imagerepository'] == 'shared' and True or False

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    if os.path.exists('%s/thumb.jpg' % (os.path.dirname(os.path.realpath(__file__)))):
        os.remove('%s/thumb.jpg' % (os.path.dirname(os.path.realpath(__file__))))
    elif os.path.exists('%s/thumb.png' % (os.path.dirname(os.path.realpath(__file__)))):
        os.remove('%s/thumb.png' % (os.path.dirname(os.path.realpath(__file__))))
    
    #load tweeted pages
    f = open('%s/enwikinewpages.tweeted' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    tweetedbefore = unicode(f.read(), 'utf-8').splitlines()
    #print tweetedbefore
    f.close()
    
    #get new pages
    rcend = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%Y%m%d%H%M%S')
    print rcend
    urlnewpages = 'http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rctype=new&rcnamespace=0&rcshow=!redirect|!anon&rcprop=title|user|timestamp|sizes&rcend=%s&rclimit=500&format=json' % (rcend)
    jsonnewpages = json.loads(unicode(urllib.urlopen(urlnewpages).read(), 'utf-8'))
    print len(jsonnewpages['query']['recentchanges'])
    newpages_candidates = []
    minlength = 2000
    minuserexperience = 500 # in number of edits
    for page in jsonnewpages['query']['recentchanges']:
        #exclude newbies, tiny pages, etc
        if page['newlen'] < minlength or getUserEditCount(page['user']) < minuserexperience:
            continue
        
        page_title_ = re.sub(ur' ', ur'_', page['title'])
        page_url = 'https://en.wikipedia.org/w/index.php?title=%s&action=raw' % (page_title_.encode('utf-8'))
        page_text = unicode(urllib.urlopen(page_url).read(), 'utf-8')
        if not page_text or len(page_text) < minlength:
            continue
        
        #exclude pages with issues
        if re.search(ur"(?im)\{\{\s*(Unreviewed|NPOV|db|prod|proposed)", page_text):
            continue
        
        #we prefer articles with references
        if not re.search(ur"(?im)(<ref>|<ref name=)", page_text):
            continue
        
        #print page_title_
        #we prefer articles with images, and on Commons (they are free)
        images = re.findall(ur"(?im)(?:\|\s*image\s*\=|\[\[\s*(?:File|Image)\s*\:)\s*([^\n\[\]\|\=]+?\.(?:jpe?g|png|svg))", page_text)
        if not images:
            continue
        image_candidate = ''
        for image in images:
            #print image
            image = re.sub(ur'_', ur' ', image)
            if imageIsOnCommons(image):
                image_candidate = image
                break
        if not image_candidate:
            continue
        
        newpages_candidates.append([page['title'], image_candidate])
    
    print newpages_candidates
    c = 0
    maxtweets = 3
    for page_title, image_title in newpages_candidates:
        if c >= maxtweets:
            break
        if page_title in tweetedbefore:
            print u'[[%s]] was tweeted before' % (page_title)
            continue
        page_title_ = re.sub(ur' ', ur'_', page_title)
        image_title_ = re.sub(ur' ', ur'_', image_title)
        if len(page_title) > 60:
            page_title = '%s...' % (page_title[:60])
        md5 = hashlib.md5(image_title_.encode('utf-8')).hexdigest()
        thumburl = 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/800px-%s' % (md5[0], md5[:2], urllib.quote(image_title_.encode('utf-8')), urllib.quote(image_title_.encode('utf-8')))
        thumbfilename = '%s/thumb' % (os.path.dirname(os.path.realpath(__file__)))
        if image_title.endswith('.svg'):
            thumburl += '.png'
            thumbfilename += '.png'
        elif image_title.endswith('.png'):
            thumbfilename += '.png'
        else:
            thumbfilename += '.jpg'
        urllib.urlretrieve(thumburl, thumbfilename)
        
        print u'Tweeting [[%s]]' % (page_title)
        thumb = open(thumbfilename, 'rb')
        url = 'https://en.wikipedia.org/wiki/%s' % (page_title_)
        twitter.update_status_with_media(status='%s %s #wikipedia #newpages' % (page_title, url), media=thumb)
        g = open('%s/enwikinewpages.tweeted' % (os.path.dirname(os.path.realpath(__file__))), 'a')
        output = '%s\n' % (page_title)
        g.write(output.encode('utf-8'))
        g.close()
        time.sleep(20)
        c += 1

if __name__ == '__main__':
    main()