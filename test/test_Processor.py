from nose.tools import assert_equal
from nose.tools import assert_not_equal
import re

from flavor_bot.Formatter import Markdown
from flavor_bot.Source import ATF, ELR
from flavor_bot.Processor import Processor


class TestProcessor:
    def test_without_match(self):
        atf = ATF()
        formatter = Markdown()
        sources = [atf]
        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources)
        result = processor.process('xxxxxxxx')

        assert_equal(result, None)

    def test_with_match(self):
        atf = ATF()
        formatter = Markdown()
        sources = [atf]
        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources)
        result = processor.process('[[Strawberry ripe]]')

        assert_not_equal(result, None)
