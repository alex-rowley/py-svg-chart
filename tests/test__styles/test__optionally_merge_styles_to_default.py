import unittest

from pysvgchart.styles import optionally_merge_styles_to_default


class TestOptionallyMergeStylesToDefault(unittest.TestCase):
    """
    test the optionally_merge_styles_to_default() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_nothing(self):
        # given
        styles = {}
        include_default = False
        # when
        actual = optionally_merge_styles_to_default(styles, include_default)
        # then
        expect = {}
        self.assertDictEqual(expect, actual)

    def test_no_default(self):
        # given
        styles = {
            "foo": "bar",
            "bar": "baz",
            "baz": "foo",
        }
        include_default = False
        # when
        actual = optionally_merge_styles_to_default(styles, include_default)
        # then
        expect = {
            "foo": "bar",
            "bar": "baz",
            "baz": "foo",
        }
        self.assertDictEqual(expect, actual)

    def test_only_default(self):
        # given
        styles = {}
        include_default = True
        # when
        actual = optionally_merge_styles_to_default(styles, include_default)
        # then
        expect = {
            ".psc-hover-group .psc-hover-data": {
                "display": "none",
            },
            ".psc-hover-group:hover .psc-hover-data": {
                "display": "inline",
            },
        }
        self.assertDictEqual(expect, actual)

    def test_both(self):
        # given
        styles = {
            "foo": "bar",
            "bar": "baz",
            "baz": "foo",
        }
        include_default = True
        # when
        actual = optionally_merge_styles_to_default(styles, include_default)
        # then
        expect = {
            "foo": "bar",
            "bar": "baz",
            "baz": "foo",
            ".psc-hover-group .psc-hover-data": {
                "display": "none",
            },
            ".psc-hover-group:hover .psc-hover-data": {
                "display": "inline",
            },
        }
        self.assertDictEqual(expect, actual)

    def test_overwrite(self):
        # given
        styles = {
            ".psc-hover-group .psc-hover-data": {
                "TEST": "OVERWRITE;",
            },
        }
        include_default = True
        # when
        actual = optionally_merge_styles_to_default(styles, include_default)
        # then
        expect = {
            ".psc-hover-group .psc-hover-data": {
                "display": "none",
            },
            ".psc-hover-group:hover .psc-hover-data": {
                "display": "inline",
            },
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
