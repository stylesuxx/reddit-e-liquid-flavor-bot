from flavor_bot.Formatter import Markdown
from nose.tools import assert_equal


class TestFormatter:
    def setup(self):
        self.formatter = Markdown()

    def teardown(self):
        pass

    def test_link_not_found(self):
        link = self.formatter.link(None)
        assert_equal(link, 'Not found')

    def test_link_formatting(self):
        link = self.formatter.link({'link': 'foo', 'text': 'bar'})
        assert_equal(link, '[bar](foo)')
