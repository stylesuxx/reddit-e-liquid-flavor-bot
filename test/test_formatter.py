from flavor_bot.Formatter import Markdown
from nose.tools import assert_equal


class TestFormatter:
    def test_link_not_found(self):
        formatter = Markdown()
        link = formatter.link(None)

        assert_equal(link, 'Not found')

    def test_link_formatting(self):
        formatter = Markdown()
        link = formatter.link({'link': 'foo', 'text': 'bar'})

        assert_equal(link, '[bar](foo)')
