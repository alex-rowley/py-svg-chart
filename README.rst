Python SVG Chart Generator (pysvgchart)
=======================================

A Python package for creating and rendering SVG charts, including line
charts, axes, legends, and text labels. This package supports both
simple and complex chart structures and is highly customisable for
various types of visualizations.

Why did I make this project
---------------------------
This project is designed for charts that are easily embedded into python web applications (or other web applications) with minimum fuss.

Many charting libraries rely on JavaScript-driven client-side rendering, often requiring an intermediate canvas before
producing a polished visual. This package takes a different approach: it generates clean, standalone SVG charts
entirely within Python. By leveraging SVG’s inherent scalability and styling flexibility, it eliminates the need for
JavaScript dependencies, client-side rendering, or post-processing steps. The result is a lightweight, backend-friendly
solution for producing high-quality, resolution-independent charts without sacrificing control or maintainability.

While many popular Python charting libraries focus on image-based rendering, and those that support SVG output often
produce cumbersome, hard-to-customise files, this library is built with customisation at its core. Every chart
element is designed to be easily modified, giving developers precise control over appearance and structure.
As such, all of the lower level elements are accessible via properties of the charts.

Installation
------------

.. code:: bash

   pip install pysvgchart

Alternatively, you can clone this repository and install it locally:

.. code:: bash

   git clone https://github.com/arowley-ai/py-svg-chart.git
   cd py-svg-chart
   pip install .

Usage
-----

Usage depends on which chart you had in mind but each one follows similar principles.

Simple donut chart
^^^^^^^^^^^^^^^^^^

Create a simple donut chart:

.. code:: python

    import pysvgchart as psc

    values = [10, 20, 30, 40]
    donut_chart = psc.DonutChart(values)
    svg_string = donut_chart.render()

The following is the output of this code

.. image:: https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/donut.svg
   :alt: Simple donut chart example
   :width: 200px

Simple line chart
^^^^^^^^^^^^^^^^^

Create a simple line chart:

.. code:: python

   import pysvgchart as psc

    x_values = list(range(100))
    y_values = [4000]
    for i in range(99):
        y_values.append(y_values[-1] + 100 * random.randint(0, 1))

    line_chart = psc.SimpleLineChart(
        x_values=x_values,
        y_values=[y_values, [1000 + y for y in y_values]],
        y_names=['predicted', 'actual'],
        x_max_ticks=20,
        y_zero=True,
    )
    line_chart.add_grids(minor_y_ticks=4, minor_x_ticks=4)
    line_chart.add_legend()

    svg_string = line_chart.render()

The following is the output of this code

.. image:: https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/simple.svg
   :alt: Simple line chart example

More stylised example
^^^^^^^^^^^^^^^^^^^^^

The following code demonstrates a heavily customised line chart example

.. code:: python

    import pysvgchart as psc

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

    dates = [dt.date.today() - dt.timedelta(days=i) for i in range(500) if (dt.date.today() + dt.timedelta(days=i)).weekday() == 0]
    actual = [(1 + math.sin(d.timetuple().tm_yday / 183 * math.pi)) * 50000 + 1000 * i + random.randint(-10000, 10000) for i, d in enumerate(dates)]
    expected = [a + random.randint(-10000, 10000) for a in actual]
    line_chart = psc.SimpleLineChart(x_values=dates, y_values=[actual, expected], y_names=['Actual sales', 'Predicted sales'], x_max_ticks=30, x_label_format=x_labels, y_label_format=y_labels, width=1200)
    line_chart.series['Actual sales'].styles = {'stroke': "#DB7D33", 'stroke-width': '3'}
    line_chart.series['Predicted sales'].styles = {'stroke': '#2D2D2D', 'stroke-width': '3', 'stroke-dasharray': '4,4'}
    line_chart.add_legend(x_position=700, element_x=200, line_length=35, line_text_gap=20)
    line_chart.add_y_grid(minor_ticks=0, major_grid_style={'stroke': '#E9E9DE'})
    line_chart.x_axis.tick_lines, line_chart.y_axis.tick_lines = [], []
    line_chart.x_axis.axis_line = None
    line_chart.y_axis.axis_line.styles['stroke'] = '#E9E9DE'
    line_end = line_chart.legend.lines[0].end
    styles = {'fill': '#FFFFFF', 'stroke': '#DB7D33', 'stroke-width': '3'}
    line_chart.add_custom_element(psc.Circle(x_position=line_end.x, y_position=line_end.y, radius=4, styles=styles))
    line_end = line_chart.legend.lines[1].end
    styles = {'fill': '#2D2D2D', 'stroke': '#2D2D2D', 'stroke-width': '3'}
    line_chart.add_custom_element(psc.Circle(x_position=line_end.x, y_position=line_end.y, radius=4, styles=styles))
    for limit, tick in zip(line_chart.x_axis.limits, line_chart.x_axis.tick_text):
        if tick.content == 'Jan':
            line_chart.add_custom_element(psc.Text(x_position=tick.position.x, y_position=tick.position.y + 15, content=str(limit.year), styles=tick.styles))

The following is the output of this code

.. image:: https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/detailed.svg
   :alt: Complex line chart example

Contributing
------------

We welcome contributions! If you’d like to contribute to the project,
please follow these steps:

- Fork this repository.
- Optionally, create a new branch (eg. git checkout -b feature-branch).
- Commit your changes (git commit -am ‘Add feature’).
- Push to the branch (eg. git push origin feature-branch).
- Open a pull request.

Created a neat chart?
---------------------

All of the charts in the showcase folder are generated by pytest. If you create something neat that you'd
like to share then see if it can be added to the test suite and it will be generated alongside other
showcase examples.


License
-------

This project is licensed under the MIT License - see the LICENSE file
for details.
