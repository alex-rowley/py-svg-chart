import pytest
import pysvgchart as psc
import random
import os


def test_simple_line_chart_creation():
    x_values = list(range(100))
    y_values = [4000]
    for i in range(99):
        y_values.append(y_values[-1] + 100 * random.randint(0, 1))

    line_chart = psc.SimpleLineChart(
        x_values=x_values,
        y_values=[y_values, [1000 + y for y in y_values]],
        y_names=['predicted', 'actual']
    )
    line_chart.add_grids(minor_y_ticks=4,minor_x_ticks=4)
    line_chart.add_legend()

    output_dir = "outputs"
    output_file = os.path.join(output_dir, "temp.svg")

    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w+') as out_file:
        out_file.write(line_chart.render())

    assert os.path.exists(output_file), "SVG file was not created."
    assert 'svg' in line_chart.render().lower(), "SVG content is not in the render output."
    assert len(line_chart.y_axis.tick_text) > 0, "Y-axis ticks are missing."
    assert line_chart.y_axis.tick_text[-1].styles, "Y-axis tick styles are missing."
