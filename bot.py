#! /usr/bin/python2
# -*- coding: utf-8 -*-

import urllib2
import urllib
import json

channelID = "@username_bot"
botToken = ""
sentFile = "" #Create a file in this path. So the bot can store last sent posts
RedditLimit = 20
RedditUrl = "https://reddit.com/r/YourSubreddit/new/.json?limit=" + str(RedditLimit)
useragent = "Reddit Telegram Bot"

def sendMessage(msg):
	msg = urllib.quote(msg)
	url = "https://api.telegram.org/bot" + botToken  + "/sendMessage?chat_id=" + channelID + "&parse_mode=html&text=" + msg 
	print " - Sending the post to telegram... "
	urllib2.urlopen(url)

def isSent(id):
	file = open(sentFile,"r")
	for line in file:
		if id+'\n' == line:
			file.close()
			return True
	file.close()
	return False

def newSent(arr):
	file = open(sentFile,"w")
	for x in range(RedditLimit-1, -1, -1):
		id = arr[x]["data"]["id"].encode("UTF-8").strip()
		file.write(id+'\n')
	file.close()

opener = urllib2.build_opener()
opener.addheaders = [("User-Agent", useragent)]
jsonDownload = opener.open(RedditUrl)
jsonData = json.loads(jsonDownload.read())["data"]["children"]

print " - Sending the request to Reddit API. post limit: " + str(RedditLimit)

for x in range(RedditLimit-1, -1, -1):
	msgTitle = jsonData[x]["data"]["title"].encode("UTF-8").strip()
	msgAuthor = jsonData[x]["data"]["author"].encode("UTF-8").strip()
	msgUrl = jsonData[x]["data"]["url"].encode("UTF-8").strip()
	msgID = jsonData[x]["data"]["id"].encode("UTF-8").strip()
	msgPermalink = "https://redd.it/" + msgID
	if isSent(msgID):
		print " - Post already has been sent. ID: " + msgID
	else:
		sendMessage("<b>{0}</b>\nby: {1}\n\n{2}\n\n💬<a href='{3}'>comments</a>".format(msgTitle,msgAuthor,msgUrl,msgPermalink))
		newSent(jsonData)
		print " - Post ID added to the log file: " + msgID
