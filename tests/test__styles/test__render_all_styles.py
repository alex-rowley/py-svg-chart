import unittest

from pygments.lexer import include

from pysvgchart.styles import render_all_styles


class TestRenderAllStyles(unittest.TestCase):
    """
    test the render_all_styles() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_nothing(self):
        # given
        styles = {}
        include_default = False
        # when
        actual = render_all_styles(styles, include_default)
        # then
        expect = ""
        self.assertEqual(expect, actual)

    def test_no_default(self):
        # given
        styles = {
            "foo": {"bar": "snake"},
            "bar": {"baz": "python"},
            "baz": {"foo": "serpent"},
        }
        include_default = False
        # when
        actual = render_all_styles(styles, include_default)
        # then
        expect = """
foo {
    bar: snake;
}

bar {
    baz: python;
}

baz {
    foo: serpent;
}
        """.strip()
        self.assertEqual(expect, actual)

    def test_only_default(self):
        # given
        styles = {}
        include_default = True
        # when
        actual = render_all_styles(styles, include_default)
        # then
        expect = """
.psc-hover-group .psc-hover-data {
    display: none;
}

.psc-hover-group:hover .psc-hover-data {
    display: inline;
}
        """.strip()
        self.assertEqual(expect, actual)

    def test_both(self):
        # given
        styles = {
            "foo": {"bar": "snake"},
            "bar": {"baz": "python"},
            "baz": {"foo": "serpent"},
        }
        include_default = True
        # when
        actual = render_all_styles(styles, include_default)
        # then
        expect = """
foo {
    bar: snake;
}

bar {
    baz: python;
}

baz {
    foo: serpent;
}

.psc-hover-group .psc-hover-data {
    display: none;
}

.psc-hover-group:hover .psc-hover-data {
    display: inline;
}
        """.strip()
        self.assertEqual(expect, actual)

    def test_overwrite(self):
        # given
        styles = {
            ".psc-hover-group .psc-hover-data": {
                "TEST": "OVERWRITE;",
            },
        }
        include_default = True
        # when
        actual = render_all_styles(styles, include_default)
        # then
        expect = """
.psc-hover-group .psc-hover-data {
    display: none;
}

.psc-hover-group:hover .psc-hover-data {
    display: inline;
}
        """.strip()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
