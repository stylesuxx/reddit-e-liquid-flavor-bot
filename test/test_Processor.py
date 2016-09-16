from nose.tools import assert_equal
from nose.tools import assert_not_equal
import re

from flavor_bot.Formatter import Markdown
from flavor_bot.Source import ATF, ELR
from flavor_bot.Processor import Processor


class TestProcessor:
    def test_without_match(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        sources = [atf, elr]
        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources)
        result = processor.process('xxxxxxxx')

        assert_equal(result, None)

    def test_with_match(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        sources = [atf, elr]

        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources, {
                'vendors': atf.getVendorList()})
        result = processor.process('[[Strawberry ripe]]')

        print result
        assert ('https://alltheflavors.com/flavors'
                '/the-flavor-apprentice-strawberry-ripe') in result
        assert 'http://e-liquid-recipes.com/flavor/115914' in result

    def test_vendor_prefixed(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        sources = [atf, elr]

        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources, {
                'vendors': atf.getVendorList()})
        result = processor.process('[[TPA Strawberry ripe]]')

        print result
        assert ('https://alltheflavors.com/flavors'
                '/the-flavor-apprentice-strawberry-ripe') in result
        assert 'http://e-liquid-recipes.com/flavor/5361' in result
        assert '| Strawberry ripe TPA |' in result

    def test_vendor_delimited(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        sources = [atf, elr]

        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources, {
                'vendors': atf.getVendorList()})
        result = processor.process('[[Strawberry ripe by TPA]]')

        print result
        assert ('https://alltheflavors.com/flavors'
                '/the-flavor-apprentice-strawberry-ripe') in result
        assert 'http://e-liquid-recipes.com/flavor/5361' in result
        assert '| Strawberry ripe TPA |' in result

    def test_vendor_prefixed_1(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        sources = [atf, elr]

        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources, {
                'vendors': atf.getVendorList()})
        result = processor.process('[[ CAP Sugar Cookie ]]')

        print result
        assert ('https://alltheflavors.com/flavors/'
                'capella-sugar-cookie') in result
        assert 'http://e-liquid-recipes.com/flavor/4871' in result
        assert '| Sugar Cookie CAP |' in result

    def test_vendor_alias_elr(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        alias = {'INW': 'Inawera'}

        elr.setVendorAlias(alias)
        sources = [elr]

        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources, {
                'vendors': atf.getVendorList()})
        result = processor.process('[[ INW Biscuit ]]')

        print result
        assert ('http://e-liquid-recipes.com/flavor/13528') in result
        assert '| Biscuit INW |' in result

    def test_not_found(self):
        atf = ATF()
        elr = ELR()
        formatter = Markdown()
        sources = [atf, elr]

        pattern = re.compile('\[\[([^\]]*)\]\]', re.MULTILINE)
        processor = Processor(pattern, formatter, sources, {
                'vendors': atf.getVendorList()})
        result = processor.process('[[ Wiener Schnitzel ]]')

        print result
        assert '| Not found | Not found |' in result
