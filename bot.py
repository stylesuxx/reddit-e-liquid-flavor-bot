import argparse
import praw
import time
import re

from Processor import Processor

userAgent = 'E-Juice Flavor Lookup 0.0.3 (by /u/stylesuxx)'
sources = ['ELR', 'ATF']

pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
limitSubmissions = 25
pauseSeconds = 60

parser = argparse.ArgumentParser(description=userAgent)
parser.add_argument('siteName', metavar='SITENAME',
                    help='Site name to use from the config')
parser.add_argument('-s', '--sub', dest='subreddit', metavar='SUB',
                    default='test', help='Subreddit to monitor')

args = parser.parse_args()
siteName = args.siteName
subreddit = args.subreddit

processedSubmissions = []
processedComments = []
processor = Processor(pattern)

reddit = praw.Reddit(user_agent=userAgent, site_name=siteName)
reddit.refresh_access_information()

username = reddit.get_me()

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
            if(submission.id not in processedSubmissions and
               submission.author != username):
                processor.submission(submission)
                processedSubmissions.append(submission.id)

        for comment in sub.get_comments():
            if(comment.id not in processedComments and
               comment.author != username):
                processor.comment(comment)
                processedComments.append(comment.id)

    except praw.errors.RateLimitExceeded as err:
        print 'Hit rate limit - sleeping for %i seconds... (%s)' % (
            pauseSeconds, err)

        time.sleep(pauseSeconds)
