import unittest
from unittest.mock import MagicMock, call


from pysvgchart.helpers import collapse_element_list


class TestCollapseElementList(unittest.TestCase):

    def test_no_args(self):
        # given
        args = []
        # when
        actual = collapse_element_list()
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_none(self):
        # given
        args = [
            None,
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_non_iterable(self):
        # given
        args = [
            42,
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_empty_iterable(self):
        # given
        args = [
            [],
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_iterable_one_without(self):
        # given
        args = [
            [
                42,
            ],
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_iterable_one_with_but_empty(self):
        # given
        mock_built_in = MagicMock()
        mock_built_in.get_element_list.return_value = []
        args = [
            [
                mock_built_in,
            ],
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = [
            call.get_element_list(),
        ]
        self.assertListEqual(expect, mock_built_in.mock_calls)
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_iterable_one_with_that_has_one(self):
        # given
        mock_built_in = MagicMock()
        mock_built_in.get_element_list.return_value = [
            42,
        ]
        args = [
            [
                mock_built_in,
            ],
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = [
            call.get_element_list(),
        ]
        self.assertListEqual(expect, mock_built_in.mock_calls)
        expect = [
            42,
        ]
        self.assertListEqual(expect, actual)

    def test_one_iterable_one_with_that_has_some(self):
        # given
        mock_built_in = MagicMock()
        mock_built_in.get_element_list.return_value = [
            42,
        ]
        args = [
            [
                mock_built_in,
                mock_built_in,
                mock_built_in,
            ],
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = [
            call.get_element_list(),
            call.get_element_list(),
            call.get_element_list(),
        ]
        self.assertListEqual(expect, mock_built_in.mock_calls)
        expect = [
            42,
            42,
            42,
        ]
        self.assertListEqual(expect, actual)

    def test_some_iterable_one_with_that_has_onee(self):
        # given
        mock_built_in = MagicMock()
        mock_built_in.get_element_list.return_value = [
            42,
        ]
        args = [
            [
                mock_built_in,
            ],
            [
                mock_built_in,
            ],
            [
                mock_built_in,
            ],
        ]
        # when
        actual = collapse_element_list(*args)
        # then
        expect = [
            call.get_element_list(),
            call.get_element_list(),
            call.get_element_list(),
        ]
        self.assertListEqual(expect, mock_built_in.mock_calls)
        expect = [
            42,
            42,
            42,
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
