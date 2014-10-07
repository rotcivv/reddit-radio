import requests
import subprocess
import os
import sys

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

# Reddit Parameters.
params = {
	'after': 0,
	'before': 0,
	'count': 0,
	'limit': '100'
}

# delete temporary file if it exists
#if os.path.isfile('temp.radio'):
#	os.remove('temp.radio')

session = requests.Session()
session.headers.update({"User-Agent": "Reddit Radio/0.1",})

while 1:
	response = session.post(base_subreddit, data=params)

	params['after'] = response.json()['data']['after']
	params['before'] = response.json()['data']['before']
	params['count'] += len(response.json()['data']['children'])

	for i in response.json()['data']['children']:
		if i['data']['domain'] in domain_white_list:
			os.system("youtube-dl -q -f bestaudio -o temp.radio " + i['data']['url'])
			print '[PLAYING] ' + i['data']['title']
			process = subprocess.Popen("mplayer -really-quiet temp.radio", stdin=subprocess.PIPE, shell=True)
			while True:
				key = raw_input()
				if key == 'q':
					process.kill()
					os.remove('temp.radio')
					break

	if count >= data_limit:
		break
