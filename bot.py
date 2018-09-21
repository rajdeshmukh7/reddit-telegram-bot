#! /usr/bin/python2
# -*- coding: utf-8 -*-
import urllib2, urllib, json

# Config
channelID = "@ChannelID" # Telegram channel ID. You can use a chat_id instead if you want to send them to a chat/group
botToken = ""
sentFile = "" # Store last sent posts in this file
redditLimit = 20
redditUrl = "https://reddit.com/r/YourSubreddit/new/.json?limit=" + str(redditLimit)
userAgent = "A Telegram Bot"

# Send the message to the Telegram channel
def sendMessage(msg):
	msg = urllib.quote(msg) # URL encode the message
	url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=html&text={2}".format(botToken, channelID, msg)
	print " - Sending the post to Telegram..."
	urllib2.urlopen(url) # Open the URL

# Check to see if post's ID is stored in the log file
def isSent(postID):
	file = open(sentFile, "r")
	for line in file:
		if line == postID + "\n":
			return True
	return False

# Store post IDs from Reddit's JSON response
def saveSent(jsonList):
	file = open(sentFile, "w")
	for x in range(redditLimit-1, -1, -1):
		postID = jsonList[x]["data"]["id"]
                file.write(postID + "\n")

opener = urllib2.build_opener()
opener.addheaders = [("User-Agent", userAgent)] # Add the useragent to the header
print " - Sending the request to Reddit API. post limit: " + str(redditLimit)
jsonResponse = opener.open(redditUrl)
jsonList = json.loads(jsonResponse.read())
jsonList = jsonList["data"]["children"]

for x in range(redditLimit-1, -1, -1):
	postTitle = jsonList[x]["data"]["title"]
	postAuthor = jsonList[x]["data"]["author"]
	postUrl = jsonList[x]["data"]["url"]
	postID = jsonList[x]["data"]["id"]
	postPermalink = "https://redd.it/" + postID

	if isSent(postID):
		print " - The post has been sent. ID: " + postID
	else:
		sendMessage("<b>{0}</b>\nby: {1}\n\n{2}\n\n💬<a href='{3}'>comments</a>".format(postTitle, postAuthor, postUrl, postPermalink))
                saveSent(jsonList)
		print " - Post ID added to the log file. ID: " + postID
