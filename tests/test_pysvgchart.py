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


def test_stylised_line_chart():
    def y_labels(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        rtn = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
        return rtn.replace('.00', '').replace('.0', '')

    def x_labels(date):
        return date.strftime('%b')

    start_date = dt.date(2025, 2, 14)
    dates = [start_date - dt.timedelta(days=i) for i in range(500) if (start_date + dt.timedelta(days=i)).weekday() == 0][::-1]
    actual = [(1 + math.sin(d.timetuple().tm_yday / 183 * math.pi)) * 50000 + 1000 * i + random.randint(0, 20000) for i, d in enumerate(dates)]
    expected = [a + random.randint(-10000, 10000) for a in actual]
    line_chart = psc.LineChart(x_values=dates, y_values=[actual, expected], y_names=['Actual sales', 'Predicted sales'], x_max_ticks=30, x_label_format=x_labels, y_label_format=y_labels, width=1200, left_margin=100, right_margin=100)
    line_chart.series['Actual sales'].styles = {'stroke': "#DB7D33", 'stroke-width': '3'}
    line_chart.series['Predicted sales'].styles = {'stroke': '#2D2D2D', 'stroke-width': '3', 'stroke-dasharray': '4,4'}
    line_chart.add_legend(x_position=700, element_x=200, element_y=0, y_position=60, line_length=35, line_text_gap=20)
    line_chart.add_y_grid(minor_ticks=0, major_grid_style={'stroke': '#E9E9DE'})
    line_chart.x_axis.tick_lines, line_chart.y_axis.tick_lines = [], []
    line_chart.x_axis.axis_line = None
    line_chart.y_axis.axis_line.styles['stroke'] = '#E9E9DE'
    line_end = line_chart.legend.lines[0].end
    act_styles = {'fill': '#FFFFFF', 'stroke': '#DB7D33', 'stroke-width': '3'}
    line_chart.add_custom_element(psc.Circle(x_position=line_end.x, y_position=line_end.y, radius=4, styles=act_styles))
    line_end = line_chart.legend.lines[1].end
    pred_styles = {'fill': '#2D2D2D', 'stroke': '#2D2D2D', 'stroke-width': '3'}
    line_chart.add_custom_element(psc.Circle(x_position=line_end.x, y_position=line_end.y, radius=4, styles=pred_styles))
    for limit, tick in zip(line_chart.x_axis.limits, line_chart.x_axis.tick_texts):
        if tick.content == 'Jan':
            line_chart.add_custom_element(psc.Text(x_position=tick.position.x, y_position=tick.position.y + 15, content=str(limit.year), styles=tick.styles))

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
            psc.Circle(x_position=position.x, y_position=position.y, radius=3, classes=classes, styles=marker_styles),
            psc.Text(x_position=position.x, y_position=position.y - 10, content=x_content, classes=classes, styles=text_styles),
            psc.Text(x_position=position.x, y_position=position.y - 30, content=y_content, classes=classes, styles=text_styles),
            psc.Text(x_position=position.x, y_position=position.y - 50, content=series_name, classes=classes, styles=text_styles)
        ]

    line_chart.add_hover_modifier(hover_modifier, radius=3)
    write_out(line_chart.render_with_all_styles(), name="detailed.svg")


def test_donut():
    values = [11.3, 20, 30, 40]
    donut_chart = psc.DonutChart(values)
    write_out(donut_chart.render(), name="donut.svg")


def test_donut_hover():
    def hover_modifier(position, name, value, chart_total):
        text_styles = {'alignment-baseline': 'middle', 'text-anchor': 'middle'}
        params = {'styles': text_styles, 'classes': [psc.hover_style_name]}
        return [
            psc.Text(x_position=position.x, y_position=position.y - 10, content=name, **params),
            psc.Text(x_position=position.x, y_position=position.y + 10, content="{:.2%}".format(value / chart_total), **params)
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
