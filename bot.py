import praw
import time
import re

from Processor import Processor

userAgent = 'E-Juice Flavor Lookup 0.0.0 (by /u/stylesuxx)'
username = 'flavor_bot'
subreddit = 'test'
sources = ['ELR', 'ATF']

pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
limitSubmissions = 25
pauseSeconds = 60

processedSubmissions = []
processedComments = []
processor = Processor(pattern, username)

reddit = praw.Reddit(user_agent=userAgent, site_name=username)

# 1.
# print reddit.get_authorize_url('uniqueKey', 'read submit', True)
# 2.
# accessInformation = reddit.get_access_information('token_from_above')
# print accessInformation

reddit.refresh_access_information()

# Mark items and comments as processed, so we only care for new ones
sub = reddit.get_subreddit(subreddit)
for submission in sub.get_new(limit=limitSubmissions):
    processedSubmissions.append(submission.id)

for comment in sub.get_comments():
    processedComments.append(comment.id)

while True:
    try:
        sub = reddit.get_subreddit(subreddit)
        for submission in sub.get_new(limit=limitSubmissions):
            if submission.id not in processedSubmissions:
                processor.submission(submission)
                processedSubmissions.append(submission.id)

        for comment in sub.get_comments():
            if comment.id not in processedComments:
                processor.comment(comment)
                processedComments.append(comment.id)

    except praw.errors.RateLimitExceeded as err:
        print 'Hit rate limit - sleeping for %i seconds... (%s)' % (
            pauseSeconds, err)

        time.sleep(pauseSeconds)
