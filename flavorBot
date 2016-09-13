#!/usr/bin/python

import argparse
import praw
import time
import re

from flavor_bot.Processor import Processor

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
username = reddit.user.me()

# Mark items and comments as processed, so we only care for new ones
sub = reddit.subreddit(subreddit)
for submission in sub.new(limit=limitSubmissions):
    processedSubmissions.append(submission.id)

for comment in sub.comments(limit=limitSubmissions):
    processedComments.append(comment.id)

while True:
    try:
        for submission in sub.new(limit=limitSubmissions):
            if(submission.id not in processedSubmissions and
               submission.author != username):
                reply = processor.process(submission.selftext)
                if reply:
                    submission.reply(reply)
                    # print reply
                    print 'Processed submission: %s' % submission.id

                processedSubmissions.append(submission.id)

        for comment in sub.comments(limit=limitSubmissions):
            if(comment.id not in processedComments and
               comment.author != username):
                reply = processor.process(comment.body)
                if reply:
                    comment.reply(reply)
                    # print reply
                    print 'Processed comment: %s' % comment.id

                processedComments.append(comment.id)

    except praw.exceptions.APIException as err:
        print 'Hit rate limit - sleeping for %i seconds... (%s)' % (
            pauseSeconds, err)

        time.sleep(pauseSeconds)
