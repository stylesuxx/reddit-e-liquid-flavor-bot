from Listener import Listener


class Comment(Listener):
    name = 'Comment'

    def __init__(self, stream, action):
        super(Comment, self).__init__(stream, action)

    def getItem(self, comment):
        text = comment.body
        return {'op': comment, 'text': text}
