import requests
import subprocess
import os
import sys

#test

#set the subreddit name from the passed argument or set the default
if 1 < len(sys.argv):
  sub = str(sys.argv[1])
else:
  sub = 'trance'

base_subreddit = 'http://reddit.com/r/' + sub + '/.json'

#list of playable domains
domain_white_list = ['youtube.com', 'soundcloud.com', 'mixcloud.com']

#limit of entries retrieved from reddit
data_limit = 50

#base data for reddit api
after = 'null'
before = 'null'
count = 0

# delete temporary file if it exists
#if os.path.isfile('temp.radio'):
#	os.remove('temp.radio')

session = requests.Session()
session.headers.update({"User-Agent": "Reddit Radio/0.1",})

while 1:
	payload = {'after': after, 'before': before, 'count': count, 'limit': '100'}
	r = session.post(base_subreddit, data=payload)

	after = r.json()['data']['after']
	before = r.json()['data']['before']
	count += len(r.json()['data']['children']);

	for i in r.json()['data']['children']:
		if i['data']['domain'] in domain_white_list:
			os.system('python youtube-dl -q -f bestaudio -o temp.radio ' + i['data']['url'])
			print 'Playing song... ' + i['data']['title']
			os.system('mpv -really-quiet temp.radio')
			os.remove('temp.radio')

	if count >= data_limit:
		break
