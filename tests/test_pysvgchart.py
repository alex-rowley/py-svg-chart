import pysvgchart as psc
import random
import os
import datetime as dt
import math

random.seed(42)


def write_out(content, name, output_dir="showcase"):
    output_file = os.path.join(output_dir, name)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w+') as out_file:
        out_file.write(content)
    return output_file


def test_write_out_styles():
    write_out(psc.render_all_styles(), 'pysvgchart.css', 'styles')


def test_line_chart():
    x_values = list(range(100))
    y_values = [4000]
    for i in range(99):
        y_values.append(y_values[-1] + 100 * random.randint(0, 1))

    line_chart = psc.LineChart(
        x_values=x_values,
        y_values=[y_values, [1000 + y for y in y_values]],
        y_names=['predicted', 'actual'],
        x_max_ticks=20,
        y_zero=True,
        width=900,
        right_margin=200,
        y_margin=150
    )
    line_chart.add_grids(minor_y_ticks=4, minor_x_ticks=4)
    line_chart.add_legend()

    output_file = write_out(line_chart.render(), name="line.svg")

    assert os.path.exists(output_file), "SVG file was not created."
    assert 'svg' in line_chart.render().lower(), "SVG content is not in the render output."
    assert len(line_chart.y_axis.tick_texts) > 0, "Y-axis ticks are missing."
    assert line_chart.y_axis.tick_texts[-1].styles, "Y-axis tick styles are missing."
    assert isinstance(line_chart.series['predicted'].path_length, float), "Path length error"


STYLISED_LINE_CHART_DATA: dict | None = None


def init_stylised_line_chart_data():
    """
    make sure that the stylised line charts use the same data
    """
    global STYLISED_LINE_CHART_DATA
    if STYLISED_LINE_CHART_DATA is None:
        start_date = dt.date(2025, 2, 14)
        dates = [start_date - dt.timedelta(days=i) for i in range(500) if (start_date + dt.timedelta(days=i)).weekday() == 0][::-1]
        actual = [(1 + math.sin(d.timetuple().tm_yday / 183 * math.pi)) * 50000 + 1000 * i + random.randint(0, 20000) for i, d in enumerate(dates)]
        expected = [a + random.randint(-10000, 10000) for a in actual]
        STYLISED_LINE_CHART_DATA = {
            "dates": dates,
            "actual": actual,
            "expected": expected,
        }


def stylised_line_chart(x_shift=False, y_shift=False, x_log=False, y_log=False):
    def y_labels(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        rtn = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
        return rtn

    def x_labels(date):
        return date.strftime('%b')

    init_stylised_line_chart_data()
    dates = STYLISED_LINE_CHART_DATA["dates"]
    actual = [v if v > 0.0 or not y_log else 0.001 for v in STYLISED_LINE_CHART_DATA["actual"]]
    expected = [v if v > 0.0 or not y_log else 0.001 for v in STYLISED_LINE_CHART_DATA["expected"]]
    chart = psc.LineChart(
        x_values=dates,
        y_values=[actual, expected],
        y_names=['Actual sales', 'Predicted sales'],
        x_max_ticks=30,
        x_label_format=x_labels,
        y_label_format=y_labels,
        width=1200,
        left_margin=100,
        right_margin=100,
        x_shift=x_shift,
        y_shift=y_shift,
        x_log=x_log,
        y_log=y_log,
    )
    chart.series['Actual sales'].styles = {'stroke': "#DB7D33", 'stroke-width': '3'}
    chart.series['Predicted sales'].styles = {'stroke': '#2D2D2D', 'stroke-width': '3', 'stroke-dasharray': '4,4'}
    chart.add_legend(x_position=700, element_x=200, element_y=0, y_position=60, line_length=35, line_text_gap=20)
    chart.add_y_grid(minor_ticks=0, major_grid_style={'stroke': '#E9E9DE'})
    chart.x_axis.tick_lines, chart.y_axis.tick_lines = [], []
    chart.x_axis.axis_line = None
    chart.y_axis.axis_line.styles['stroke'] = '#E9E9DE'
    line_end = chart.legend.lines[0].end
    act_styles = {'fill': '#FFFFFF', 'stroke': '#DB7D33', 'stroke-width': '3'}
    chart.add_custom_element(psc.Circle(x=line_end.x, y=line_end.y, radius=4, styles=act_styles))
    line_end = chart.legend.lines[1].end
    pred_styles = {'fill': '#2D2D2D', 'stroke': '#2D2D2D', 'stroke-width': '3'}
    chart.add_custom_element(psc.Circle(x=line_end.x, y=line_end.y, radius=4, styles=pred_styles))
    for limit, tick in zip(chart.x_axis.scale.ticks, chart.x_axis.tick_texts):
        if tick.content == 'Jan':
            chart.add_custom_element(psc.Text(x=tick.position.x, y=tick.position.y + 15, content=str(limit.year), styles=tick.styles))

    def hover_modifier(position, x_value, y_value, series_name, styles=None):
        default_stroke = "#808080"
        classes = [
            psc.hover_style_name,
        ]
        marker_styles = {
            "fill": "#FFFFFF",
            "stroke": default_stroke if styles is None else styles.get("stroke", default_stroke),
            "stroke-width": "3",
        }
        text_styles = {
            "alignment-baseline": "middle",
            "text-anchor": "middle",
        }
        x_content = str(x_value)
        y_content = "{:,.0f}".format(y_value)
        return [
            psc.Circle(x=position.x, y=position.y, radius=3, classes=classes, styles=marker_styles),
            psc.Text(x=position.x, y=position.y - 10, content=x_content, classes=classes, styles=text_styles),
            psc.Text(x=position.x, y=position.y - 30, content=y_content, classes=classes, styles=text_styles),
            psc.Text(x=position.x, y=position.y - 50, content=series_name, classes=classes, styles=text_styles)
        ]

    chart.add_hover_modifier(hover_modifier, radius=3)
    return chart


def test_stylised_line_chart_without_shift():
    chart = stylised_line_chart(x_shift=False, y_shift=False)
    write_out(chart.render_with_all_styles(), name="detailed.svg")


def test_stylised_line_chart_with_x_shift():
    chart = stylised_line_chart(x_shift=True, y_shift=False)
    write_out(chart.render_with_all_styles(), name="detailed-x-shift.svg")


def test_stylised_line_chart_with_y_shift():
    chart = stylised_line_chart(x_shift=False, y_shift=True)
    write_out(chart.render_with_all_styles(), name="detailed-y-shift.svg")


def test_stylised_line_chart_with_xy_shift():
    chart = stylised_line_chart(x_shift=True, y_shift=True)
    write_out(chart.render_with_all_styles(), name="detailed-xy-shift.svg")


def test_stylised_log_chart_with_y_log():
    chart = stylised_line_chart(x_log=False, y_log=True)
    write_out(chart.render_with_all_styles(), name="detailed-y-log.svg")


def test_donut():
    values = [11.3, 20, 30, 40]
    donut_chart = psc.DonutChart(values)
    write_out(donut_chart.render(), name="donut.svg")


def test_donut_legend():
    values = [11.3, 20, 30, 40]
    donut_chart = psc.DonutChart(values)
    donut_chart.add_legend()
    write_out(donut_chart.render(), name="donut_legend.svg")


def test_donut_hover():
    def hover_modifier(position, name, value, chart_total):
        text_styles = {'alignment-baseline': 'middle', 'text-anchor': 'middle'}
        params = {'styles': text_styles, 'classes': [psc.hover_style_name]}
        return [
            psc.Text(x=position.x, y=position.y - 10, content=name, **params),
            psc.Text(x=position.x, y=position.y + 10, content="{:.2%}".format(value / chart_total), **params)
        ]

    values = [11.3, 20, 30, 40]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    donut_chart = psc.DonutChart(values, names)
    donut_chart.add_hover_modifier(hover_modifier)
    write_out(donut_chart.render_with_all_styles(), name="donut_hover.svg")


def test_simple_line_chart():
    values = [11.3, 20, 30, 40]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    simple_line_chart = psc.SimpleLineChart(x_values=names, y_values=[values], y_names=['number'], y_zero=True)
    write_out(simple_line_chart.render(), name="simple.svg")


def test_simple_line_chart_with_axis_titles():
    values = [11.3, 20, 30, 40]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    simple_line_chart = psc.SimpleLineChart(x_values=names, y_values=[values], y_names=['number'], y_zero=True, x_axis_title='Fruit', y_axis_title='Sold')
    write_out(simple_line_chart.render(), name="simple_titled.svg")

def test_simple_line_chart_with_secondary_axis_titles():
    values = [11.3, 20, 30, 40]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    simple_line_chart = psc.SimpleLineChart(x_values=names, y_values=[values], sec_y_values=[values], sec_y_names=['number'], sec_y_zero=True, x_axis_title='Fruit', sec_y_axis_title='Sold')
    write_out(simple_line_chart.render(), name="simple_titled_secondary.svg")


def test_bar_chart():
    values = [[10, 20, 30, 40], [30, 10, 10, 20]]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    bar_chart = psc.BarChart(x_values=names, y_values=values, y_names=['Monday', 'Tuesday'], y_zero=True, width=900, right_margin=200)
    bar_chart.add_legend()
    write_out(bar_chart.render(), name="bar.svg")


def test_normalised_bar_chart():
    values = [[10, 20, 30, 40], [30, 10, 10, 20]]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    bar_chart = psc.NormalisedBarChart(x_values=names, y_values=values, y_names=['Monday', 'Tuesday'], y_zero=True, width=900, right_margin=200, y_label_format=lambda value: "{:.0%}".format(value))
    bar_chart.add_legend()
    write_out(bar_chart.render(), name="normalised_bar.svg")


SCATTER_CHART_DATA: dict | None = None


def init_scatter_chart_data():
    """
    make sure that the scatter charts use the same data
    """
    global SCATTER_CHART_DATA
    if SCATTER_CHART_DATA is None:
        x_values = [random.random() for _ in range(50)]
        y_values = [
            [x * 0.3 + random.random() * 0.7 for x in x_values],
            [x * 0.5 + random.random() * 0.5 for x in x_values],
        ]
        SCATTER_CHART_DATA = {
            "x_values": x_values,
            "y_values": y_values,
        }


def scatter_chart(x_shift=False, y_shift=False, x_log=False, y_log=False):
    init_scatter_chart_data()
    x_values = SCATTER_CHART_DATA["x_values"]
    y_values = SCATTER_CHART_DATA["y_values"]
    chart = psc.ScatterChart(x_values=x_values, y_values=y_values, y_names=["A", "B"], x_shift=x_shift, y_shift=y_shift, x_log=x_log, y_log=y_log)
    chart.add_legend()
    return chart


def test_scatter_chart_without_shift():
    chart = scatter_chart(x_shift=False, y_shift=False)
    write_out(chart.render(), name="scatter.svg")


def test_scatter_chart_xy_shift():
    chart = scatter_chart(x_shift=True, y_shift=True)
    write_out(chart.render(), name="scatter-xy-shift.svg")


def test_scatter_chart_x_log():
    chart = scatter_chart(x_log=True, y_log=False)
    write_out(chart.render(), name="scatter-x-log.svg")


def test_scatter_chart_y_log():
    chart = scatter_chart(x_log=False, y_log=True)
    write_out(chart.render(), name="scatter-y-log.svg")


def test_scatter_chart_xy_log():
    chart = scatter_chart(x_log=True, y_log=True)
    write_out(chart.render(), name="scatter-xy-log.svg")


def test_horizontal_bar_chart():
    categories = ['Apples', 'Bananas', 'Cherries', 'Dates', 'Elderberries']
    values = [[25, 40, 15, 30, 35]]
    chart = psc.HorizontalBarChart(
        x_values=values,
        y_values=categories,
        x_names=['Sales'],
        x_zero=True,
    )
    svg = chart.render()
    write_out(svg, name="horizontal_bar.svg")
    assert '<svg' in svg
    assert '<rect' in svg


def test_horizontal_bar_chart_negative_values():
    categories = ['A', 'B', 'C', 'D']
    values = [[-20, 30, -10, 40]]
    chart = psc.HorizontalBarChart(
        x_values=values,
        y_values=categories,
        x_names=['Score'],
        x_zero=True,
    )
    svg = chart.render()
    write_out(svg, name="horizontal_bar_negative.svg")
    assert '<svg' in svg
    assert '<rect' in svg
    # All rect widths should be positive
    import re
    widths = re.findall(r'<rect[^>]*width="([^"]+)"', svg)
    for w in widths:
        assert float(w) >= 0, f"Negative rect width found: {w}"
    # Y-axis line should be at the zero position, not at the left margin
    zero_fraction = chart.x_axis.scale.value_to_fraction(0)
    expected_zero_x = chart.x_axis.position.x + zero_fraction * chart.x_axis.length
    assert chart.y_axis.axis_line.position.x == expected_zero_x
    assert chart.y_axis.axis_line.end.x == expected_zero_x


def test_horizontal_bar_chart_all_negative():
    categories = ['X', 'Y', 'Z']
    values = [[-30, -10, -20]]
    chart = psc.HorizontalBarChart(
        x_values=values,
        y_values=categories,
        x_names=['Score'],
        x_zero=True,
    )
    svg = chart.render()
    write_out(svg, name="horizontal_bar_all_negative.svg")
    assert '<svg' in svg
    import re
    widths = re.findall(r'<rect[^>]*width="([^"]+)"', svg)
    for w in widths:
        assert float(w) >= 0, f"Negative rect width found: {w}"


def test_horizontal_bar_chart_multi_series_negative():
    categories = ['A', 'B', 'C']
    values = [[-10, 20, -5], [15, -25, 10]]
    chart = psc.HorizontalBarChart(
        x_values=values,
        y_values=categories,
        x_names=['Series 1', 'Series 2'],
        x_zero=True,
    )
    svg = chart.render()
    write_out(svg, name="horizontal_bar_multi_negative.svg")
    assert '<svg' in svg
    import re
    widths = re.findall(r'<rect[^>]*width="([^"]+)"', svg)
    for w in widths:
        assert float(w) >= 0, f"Negative rect width found: {w}"


def test_text_escaping_ampersand():
    text = psc.Text(x=0, y=0, content='AT&T')
    elements = text.get_element_list()
    assert len(elements) == 1
    assert '&amp;' in elements[0]
    assert 'AT&T' not in elements[0]  # raw & should not appear


def test_text_escaping_angle_brackets():
    text = psc.Text(x=0, y=0, content='a < b > c')
    elements = text.get_element_list()
    assert '&lt;' in elements[0]
    assert '&gt;' in elements[0]


def test_text_escaping_in_chart_labels():
    categories = ['R&D', 'Sales & Marketing', 'Q<3']
    values = [[10, 20, 15]]
    chart = psc.HorizontalBarChart(
        x_values=values,
        y_values=categories,
        x_names=['Budget'],
        x_zero=True,
    )
    svg = chart.render()
    write_out(svg, name="horizontal_bar_escaped_labels.svg")
    assert 'R&amp;D' in svg
    assert 'Sales &amp; Marketing' in svg
    assert 'Q&lt;3' in svg


def test_text_preserves_original_content():
    text = psc.Text(x=0, y=0, content='AT&T')
    assert text.content == 'AT&T'  # original preserved
    elements = text.get_element_list()
    assert '&amp;' in elements[0]  # rendered escaped
