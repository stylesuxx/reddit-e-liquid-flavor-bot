import praw
import re
import urllib
from lxml import html
import time

userAgent = 'E-Juice Flavor Lookup 0.0.0 (by /u/stylesuxx)'
username = 'flavor_bot'
subreddit = 'test'

searchUrlELR = 'http://e-liquid-recipes.com/flavors/?%s'

pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
limitSubmissions = 25
pauseSeconds = 60

reddit = praw.Reddit(user_agent=userAgent, site_name=username)

# 1.
# print reddit.get_authorize_url('uniqueKey', 'read submit', True)
# 2.
# accessInformation = reddit.get_access_information('token_from_above')
# print accessInformation

reddit.refresh_access_information()

# reddit.login(username=username, disable_warning=True)

processedSubmissions = []
processedComments = []


def topHitELR(term):
    params = urllib.urlencode({
        'q': term,
        'sort': 'num_recipes',
        'direction': 'desc'})
    url = searchUrlELR % (params)
    f = urllib.urlopen(url)
    tree = html.fromstring(f.read())
    text = tree.xpath(
        '//table[contains(@class, "flavorlist")]/tbody/tr[1]/td[1]//a/text()')
    link = tree.xpath(
        '//table[contains(@class, "flavorlist")]/tbody/tr[1]/td[1]//a/@href')

    if text and link:
        return {'text': text[0], 'link': link[0]}

    return None


def buildReply(links):
    reply = '| ELR Top Hit |  \n'
    reply += '| ----------- |  \n'
    for link in links:
        reply += '| %s |  \n' % (link)
    reply += '  \n'
    reply += '  \n'
    reply += 'To use, post a flavor name like so: [[ Flavor Name by Business'
    reply += ' Short Name ]] or [[ Flavor Name ]]  \n'
    reply += 'My source may be found on [github]'
    reply += '(https://github.com/stylesuxx/reddit-e-liquid-flavor-bot). '
    reply += 'Feel free to submit bug reports or feature requests.'

    return reply


def getLinkELR(match):
    match = match.split('by')
    if len(match) > 1:
        match = '%s (%s)' % (
            match[0].strip(), match[1].strip())
    else:
        match = match[0]

    link = topHitELR(match)
    if link:
        link = '[%s](%s)' % (link['text'], link['link'])
        return link

    return None


def processMatches(matches):
    matches = map(lambda match: match.strip(), matches)
    links = map(lambda match: getLinkELR(match), matches)

    return set(links)


def processSubmission(submission):
    matches = pattern.findall(submission.selftext)
    if matches:
        links = processMatches(matches)
        if len(links) > 0:
            reply = buildReply(links)
            submission.add_comment(reply)
            print 'Processed submission: %s' % submission.id


def processComment(comment):
    if comment.author.name != username:
        matches = pattern.findall(comment.body)
        if matches:
            links = processMatches(matches)
            if len(links) > 0:
                reply = buildReply(links)
                comment.reply(reply)
                print 'Processed comment: %s' % comment.id


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
                processSubmission(submission)
                processedSubmissions.append(submission.id)

        for comment in sub.get_comments():
            if comment.id not in processedComments:
                processComment(comment)
                processedComments.append(comment.id)

    except praw.errors.RateLimitExceeded:
        print 'Hit rate limit - sleeping for %i seconds...' % (pauseSeconds)
        time.sleep(pauseSeconds)
