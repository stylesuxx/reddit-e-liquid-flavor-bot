from nose.tools import assert_equal
from flavor_bot.Source import ATF, ELR


class TestSource:
    def test_atf_vendor_list(self):
        atf = ATF()
        vendors = atf.getVendorList()

        assert len(vendors) > 0
        assert_equal(vendors['CAP'], 'Capella')
        assert_equal(vendors['INW'], 'Inawera')

    def test_atf_top_hit_with_delimited_vendor(self):
        atf = ATF()

        hit = atf.getTopHit('Strawberry Ripe TPA')
        assert_equal(hit['text'], '(TPA) Strawberry (ripe)')
        assert_equal(hit['link'], ('https://alltheflavors.com/flavors/'
                                   'the-flavor-apprentice-strawberry-ripe'))

    def test_atf_top_hit_without_vendor(self):
        atf = ATF()

        hit = atf.getTopHit('Strawberry Ripe')
        assert_equal(hit['text'], '(TPA) Strawberry (ripe)')
        assert_equal(hit['link'], ('https://alltheflavors.com/flavors/'
                                   'the-flavor-apprentice-strawberry-ripe'))

    def test_atf_top_hit_without_match(self):
        atf = ATF()

        hit = atf.getTopHit('Wiener Schnitzel')
        assert_equal(hit, None)

    def test_elr_top_hit_with_delimited_vendor(self):
        elr = ELR()

        hit = elr.getTopHit('Strawberry Ripe TPA')
        assert_equal(hit['text'], 'Strawberry (Ripe) (TPA)')
        assert_equal(hit['link'], 'http://e-liquid-recipes.com/flavor/5361')

    def test_elr_top_hit_without_vendor(self):
        elr = ELR()

        hit = elr.getTopHit('Strawberry Ripe')
        assert_equal(hit['text'], 'Strawberry ripe')
        assert_equal(hit['link'], 'http://e-liquid-recipes.com/flavor/115914')

    def test_elr_top_hit_without_match(self):
        elr = ELR()

        hit = elr.getTopHit('Wiener Schnitzel')
        assert_equal(hit, None)
