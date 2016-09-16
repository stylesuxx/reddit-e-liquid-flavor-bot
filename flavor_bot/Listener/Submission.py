from Listener import Listener


class Submission(Listener):
    name = 'Submission'

    def __init__(self, stream, action):
        super(Submission, self).__init__(stream, action)

    def getItem(self, submission):
        text = submission.selftext
        return {'op': submission, 'text': text}
