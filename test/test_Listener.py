from flavor_bot.Listener import Comment, Submission
from nose.tools import assert_equal
import prawcore

import flavor_bot.settings


class TestListener:
    def setup(self):
        flavor_bot.settings.init(True)
        self.counter = 0
        self.comments = [type('obj', (object,), {
            'id': 'foo#1',
            'author': 'name',
            'body': 'for comments',
            'selftext': 'for submissions'})]

    def feeder(self):
        if len(self.comments) > 0:
            comment = self.comments.pop()
            print comment
            return [comment]

        return []

    def handler(self, item):
        self.counter += 1

    def throw(self, item):
        raise prawcore.exceptions.RequestException(Exception, None, None)

    def test_comment_listener(self):
        listener = Comment(self.feeder, self.handler)
        listener.start()
        listener.join()

        assert_equal(self.counter, 1)

    def test_submission_listener(self):
        listener = Submission(self.feeder, self.handler)
        listener.start()
        listener.join()

        assert_equal(self.counter, 1)

    def test_failing_comment_listener(self):
        listener = Comment(self.feeder, self.throw)
        listener.start()
        listener.join()

        assert_equal(self.counter, 0)

    def test_failing_submission_listener(self):
        listener = Submission(self.feeder, self.throw)
        listener.start()
        listener.join()

        assert_equal(self.counter, 0)
