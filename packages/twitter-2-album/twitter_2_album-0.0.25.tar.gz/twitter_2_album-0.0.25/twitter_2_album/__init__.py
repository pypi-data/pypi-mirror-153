#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'twitter_2_album'

import yaml
from telegram_util import AlbumResult as Result
from telegram_util import compactText, matchKey
import tweepy
import json
import html
import pkg_resources

allowlist = pkg_resources.resource_string(__name__, 'allowlist')
allowlist = set([str(item, 'utf-8') for item in allowlist.split() if item])

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
auth = tweepy.OAuthHandler(CREDENTIALS['twitter_consumer_key'], CREDENTIALS['twitter_consumer_secret'])
auth.set_access_token(CREDENTIALS['twitter_access_token'], CREDENTIALS['twitter_access_secret'])
twitterApi = tweepy.API(auth)

def getTid(path):
	index = path.find('?')
	if index > -1:
		path = path[:index]
	return path.split('/')[-1]

def getCap(status):
	text = list(status.full_text)
	for x in status.entities.get('media', []):
		for pos in range(x['indices'][0], x['indices'][1]):
			text[pos] = ''
	text = html.unescape(''.join(text))
	for x in status.entities.get('urls', []):
		if len(x['expanded_url']) < 30:
			text = text.replace(x['url'], ' ' + x['expanded_url'])
			text = text.replace('  ' + x['expanded_url'], ' ' + x['expanded_url'])
		else:
			text = text.replace(x['url'], '[%s](%s)' % ('link', x['expanded_url']))
	text = compactText(html.unescape(text))
	return text

def getEntities(status):
	try:
		return status.extended_entities
	except:
		return status.entities

def getImgs(status):
	if not status:
		return []
	# seems video is not returned in side the json, there is nothing we can do...
	return [x['media_url'] for x in getEntities(status).get('media', [])
		if x['type'] == 'photo']

def getVideo(status):
	if not status:
		return ''
	videos = [x for x in getEntities(status).get('media', []) if x['type'] == 'video']
	if not videos:
		return ''
	variants = [x for x in videos[0]['video_info']['variants'] if x['content_type'] == 'video/mp4']
	variants = [(x.get('bitrate'), x) for x in variants]
	variants.sort()
	return variants[-1][1]['url']

def getQuote(status, func):
	result = func(status)
	try:
		result = result or func(status.quoted_status)
	except:
		...

	try:
		result = result or func(status.retweeted_status)
	except:
		...

	try:
		result = result or func(status.retweeted_status.quoted_status)
	except:
		...

	return result

def getInReplyToLink(status):
	if status.in_reply_to_screen_name and status.in_reply_to_status_id:
		return ' [origin](https://twitter.com/%s/status/%d)' % (status.in_reply_to_screen_name, status.in_reply_to_status_id)
	return ''

# origin param is deprecated
def get(path, origin = []):
	tid = getTid(path)
	status = twitterApi.get_status(tid, tweet_mode="extended")
	r = Result()
	r.video = getQuote(status, getVideo) or ''
	r.imgs = getQuote(status, getImgs) or []
	r.cap = getCap(status) + getInReplyToLink(status)
	if r.cap.startswith('RT '):
		try:
			r.cap = getCap(status.retweeted_status)
		except:
			...
	if matchKey(path, ['twitter', 'http']):
		r.url = path
	else:
		r.url = 'http://twitter.com/%s/status/%s' % (
			status.user.screen_name or status.user.id, tid)
	return r
