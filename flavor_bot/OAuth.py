# 1. Enable developer mode:
#    https://www.reddit.com/prefs/apps/
#    name can be anything, description too, no about URL, select script
#    redirect uri: http://127.0.0.1:12345/redirect
# 2. Add app id, secret and redirect url to praw.ini
# 3. Run this script

import praw

userAgent = 'E-Juice Flavor Lookup 0.0.3 (by /u/stylesuxx)'
username = 'flavor_whore'
permissions = 'read submit identity'

reddit = praw.Reddit(user_agent=userAgent, site_name=username)
print 'Open the following URL in your browser:'
print reddit.get_authorize_url('uniqueKey', permissions, True)
token = raw_input('Paste token from URL bar: ')
accessInformation = reddit.get_access_information(token)
print '\n'
print 'Add to praw.ini:'
print 'oauth_refresh_token: ' + accessInformation['refresh_token']
