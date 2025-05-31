import unittest


from pysvgchart.charts import VerticalChart


class TestSetPalette(unittest.TestCase):
    """
    test the VerticalChart.set_palette() method
    """

    def setUp(self) -> None:
        self.maxDiff = None
        self.instance = VerticalChart(
            x_values=[0,1,2,3,4,5],
            y_values=[
                [0,1,2,3,4,5],
                [1,2,3,4,5,6],
                [3,4,5,6,7,8],
            ],
            y_names=["A", "B", "C"],
        )

    def test_no_colours(self):
        # given
        colours = []
        # when
        self.instance.set_palette(colours)
        colour_property = self.instance.colour_property
        expect = self.instance.__colour_defaults__[0]
        self.assertEqual(expect, self.instance.series["A"].styles[colour_property])
        expect = self.instance.__colour_defaults__[1]
        self.assertEqual(expect, self.instance.series["B"].styles[colour_property])
        expect = self.instance.__colour_defaults__[2]
        self.assertEqual(expect, self.instance.series["C"].styles[colour_property])

    def test_one_colour(self):
        # given
        colours = [
            "snake-green",
        ]
        # when
        self.instance.set_palette(colours)
        # then
        colour_property = self.instance.colour_property
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["A"].styles[colour_property])
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["B"].styles[colour_property])
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["C"].styles[colour_property])

    def test_two_colours(self):
        # given
        colours = [
            "snake-green",
            "foo-bar",
        ]
        # when
        self.instance.set_palette(colours)
        # then
        colour_property = self.instance.colour_property
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["A"].styles[colour_property])
        expect = "foo-bar"
        self.assertEqual(expect, self.instance.series["B"].styles[colour_property])
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["C"].styles[colour_property])

    def test_three_colours(self):
        # given
        colours = [
            "snake-green",
            "foo-bar",
            "melon-red",
        ]
        # when
        self.instance.set_palette(colours)
        # then
        colour_property = self.instance.colour_property
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["A"].styles[colour_property])
        expect = "foo-bar"
        self.assertEqual(expect, self.instance.series["B"].styles[colour_property])
        expect = "melon-red"
        self.assertEqual(expect, self.instance.series["C"].styles[colour_property])

    def test_more_colours(self):
        # given
        colours = [
            "snake-green",
            "foo-bar",
            "melon-red",
            "bondy-blue",
            "tequila-sunrise",
        ]
        # when
        self.instance.set_palette(colours)
        # then
        colour_property = self.instance.colour_property
        expect = "snake-green"
        self.assertEqual(expect, self.instance.series["A"].styles[colour_property])
        expect = "foo-bar"
        self.assertEqual(expect, self.instance.series["B"].styles[colour_property])
        expect = "melon-red"
        self.assertEqual(expect, self.instance.series["C"].styles[colour_property])


if __name__ == "__main__":
    unittest.main()
