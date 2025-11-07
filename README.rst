Python SVG Chart Generator (pysvgchart)
=======================================

A Python package for creating and rendering SVG charts, including line
charts, axes, legends, and text labels. This package supports both
simple and complex chart structures and is highly customisable for
various types of visualisations.

Why did I make this project
---------------------------
This project is designed to produce charts that are easily embedded into python web applications (or other web applications) with minimum fuss.

Many charting libraries for the web rely on JavaScript-driven client-side rendering, often requiring an intermediate
canvas before producing a polished visual. On the other hand, popular python based charting libraries focus on
image-based rendering. Such images are rigid and intractable once embedded into web applications and detailed
customisation is impossible. Although some libraries do generate resolution independent output
it is very difficult to customise.


This package takes a different approach: it generates clean, standalone SVG charts
entirely within Python that can be immediately embedded into a web application. By leveraging SVG’s inherent scalability
and styling flexibility, it eliminates the need for JavaScript dependencies, client-side rendering, or post-processing
steps. The result is a lightweight, backend-friendly solution for producing high-quality, resolution-independent
charts without sacrificing control or maintainability.

Every chart element is designed to be easily modified, giving developers precise control over appearance and structure.
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

A simple donut chart:

.. code:: python

    import pysvgchart as psc

    values = [11.3, 20, 30, 40]
    donut_chart = psc.DonutChart(values)
    svg_string = donut_chart.render()

.. image:: https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/donut.svg
   :alt: Simple donut chart example
   :width: 200px


Donut chart hovers
^^^^^^^^^^^^^^^^^^
The donut is nice but a little boring. To make it a bit more interesting, lets add interactive hover
effects. These effects can be added to any base elements but I thought you'd mostly use it for data labels.

.. code:: python

    def hover_modifier(position, name, value, chart_total):
        text_styles = {'alignment-baseline': 'middle', 'text-anchor': 'middle'}
        return [
            psc.Text(x=position.x, y=position.y-10, content=name, styles=text_styles),
            psc.Text(x=position.x, y=position.y+10, content="{:.2%}".format(value/chart_total), styles=text_styles)
        ]

    values = [11.3, 20, 30, 40]
    names = ['Apples', 'Bananas', 'Cherries', 'Durians']
    donut_chart = psc.DonutChart(values, names)
    donut_chart.add_hover_modifier(hover_modifier)
    donut_chart.render_with_all_styles()

`Here <https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/donut_hover.svg>`_ is the output of this code.
In order to get the hover modifiers to display successfully you will need to either render the svg with styles
or include the relevant css separately

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

.. image:: https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/line.svg
   :alt: Simple line chart example

More stylised example
^^^^^^^^^^^^^^^^^^^^^

Here's a heavily customised line chart example

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

    dates = [dt.date.today() - dt.timedelta(days=i) for i in range(500) if (dt.date.today() + dt.timedelta(days=i)).weekday() == 0][::-1]
    actual = [(1 + math.sin(d.timetuple().tm_yday / 183 * math.pi)) * 50000 + 1000 * i + random.randint(-10000, 10000) for i, d in enumerate(dates)]
    expected = [a + random.randint(-10000, 10000) for a in actual]
    line_chart = psc.SimpleLineChart(x_values=dates, y_values=[actual, expected], y_names=['Actual sales', 'Predicted sales'], x_max_ticks=30, x_label_format=x_labels, y_label_format=y_labels, width=1200)
    line_chart.series['Actual sales'].styles = {'stroke': "#DB7D33", 'stroke-width': '3'}
    line_chart.series['Predicted sales'].styles = {'stroke': '#2D2D2D', 'stroke-width': '3', 'stroke-dasharray': '4,4'}
    line_chart.add_legend(x=700, element_x=200, line_length=35, line_text_gap=20)
    line_chart.add_y_grid(minor_ticks=0, major_grid_style={'stroke': '#E9E9DE'})
    line_chart.x_axis.tick_lines, line_chart.y_axis.tick_lines = [], []
    line_chart.x_axis.axis_line = None
    line_chart.y_axis.axis_line.styles['stroke'] = '#E9E9DE'
    line_end = line_chart.legend.lines[0].end
    act_styles = {'fill': '#FFFFFF', 'stroke': '#DB7D33', 'stroke-width': '3'}
    line_chart.add_custom_element(psc.Circle(x=line_end.x, y=line_end.y, radius=4, styles=act_styles))
    line_end = line_chart.legend.lines[1].end
    pred_styles = {'fill': '#2D2D2D', 'stroke': '#2D2D2D', 'stroke-width': '3'}
    line_chart.add_custom_element(psc.Circle(x=line_end.x, y=line_end.y, radius=4, styles=pred_styles))
    for limit, tick in zip(line_chart.x_axis.scale.ticks, line_chart.x_axis.tick_texts):
        if tick.content == 'Jan':
            line_chart.add_custom_element(psc.Text(x=tick.position.x, y=tick.position.y + 15, content=str(limit.year), styles=tick.styles))

    def hover_modifier(position, x_value, y_value, series_name, styles):
        text_styles = {'alignment-baseline': 'middle', 'text-anchor': 'middle'}
        params = {'styles': text_styles, 'classes': ['psc-hover-data']}
        return [
            psc.Circle(x=position.x, y=position.y, radius=3, classes=['psc-hover-data'], styles=styles),
            psc.Text(x=position.x, y=position.y - 10, content=str(x_value), **params),
            psc.Text(x=position.x, y=position.y - 30, content="{:,.0f}".format(y_value), **params),
            psc.Text(x=position.x, y=position.y - 50, content=series_name, **params)
        ]

    line_chart.add_hover_modifier(hover_modifier, radius=5)
    line_chart.render_with_all_styles()

.. image:: https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/detailed.svg
   :alt: Complex line chart example

`View <https://raw.githubusercontent.com/arowley-ai/py-svg-chart/refs/heads/main/showcase/detailed.svg>`_ with hover effects


Chart Types Reference
----------------------

All chart types with their parameters and usage patterns.

LineChart
^^^^^^^^^

Standard line chart with vertical values and horizontal categories.

.. code:: python

    psc.LineChart(
        x_values=['Jan', 'Feb', 'Mar'],      # Categories on X-axis (horizontal)
        y_values=[[10, 20, 15], [12, 18, 14]], # Values on Y-axis (vertical)
        y_names=['Sales', 'Costs'],          # Series names
        x_zero=False, y_zero=True,           # Include zero on axes
        x_max_ticks=12, y_max_ticks=10,      # Maximum ticks
        x_label_format=str, y_label_format=str, # Label formatters
        x_axis_title='Month', y_axis_title='Amount',
        width=800, height=600,
    )

SimpleLineChart
^^^^^^^^^^^^^^^

Simplified line chart with minimal configuration.

.. code:: python

    psc.SimpleLineChart(
        x_values=[1, 2, 3, 4, 5],
        y_values=[[10, 20, 30, 25, 35]],
        y_names=['Data'],
    )

BarChart
^^^^^^^^

Vertical bar chart (bars grow upward).

.. code:: python

    psc.BarChart(
        x_values=['A', 'B', 'C'],            # Categories on X-axis
        y_values=[[10, 20, 30], [15, 25, 35]], # Values on Y-axis
        y_names=['Q1', 'Q2'],
        y_zero=True,                         # Start Y-axis at zero
        bar_width=40, bar_gap=2,             # Bar sizing
        width=800, height=600,
    )

HorizontalBarChart
^^^^^^^^^^^^^^^^^^

Horizontal bar chart (bars grow rightward). Note: parameters are swapped compared to vertical charts.

.. code:: python

    psc.HorizontalBarChart(
        x_values=[[10, 20, 30], [15, 25, 35]], # Values on X-axis (horizontal)
        y_values=['A', 'B', 'C'],            # Categories on Y-axis (vertical)
        x_names=['Q1', 'Q2'],
        x_zero=True,                         # Start X-axis at zero
        bar_width=40, bar_gap=2,             # Bar thickness and gap
        y_axis_title='Products',
        x_axis_title='Sales',
        width=800, height=600,
        left_margin=200,                     # Extra margin for long labels
    )

NormalisedBarChart
^^^^^^^^^^^^^^^^^^

Stacked bar chart normalised to 100%.

.. code:: python

    psc.NormalisedBarChart(
        x_values=['A', 'B', 'C'],
        y_values=[[10, 20, 30], [5, 10, 15]],
        y_names=['Part 1', 'Part 2'],
        bar_width=40,
        width=800, height=600,
    )

ScatterChart
^^^^^^^^^^^^

Scatter plot with individual data points.

.. code:: python

    psc.ScatterChart(
        x_values=[1, 2, 3, 4, 5],
        y_values=[[10, 20, 15, 25, 30]],
        y_names=['Data Points'],
        x_zero=True, y_zero=True,
        width=800, height=600,
    )

DonutChart
^^^^^^^^^^

Donut/pie chart for proportional data.

.. code:: python

    psc.DonutChart(
        values=[25, 30, 20, 25],            # Segment sizes
        names=['Q1', 'Q2', 'Q3', 'Q4'],     # Segment labels
        width=400, height=400,
        inner_radius=80,                     # Hole size
        outer_radius=150,                    # Outer edge
        colours=['red', 'blue', 'green', 'yellow'],
    )

Common Parameters
^^^^^^^^^^^^^^^^^

Most charts share these parameters:

**Axis Configuration:**

- ``x_min``, ``x_max``, ``y_min``, ``y_max``: Set axis ranges
- ``x_zero``, ``y_zero``: Force zero to appear on axis
- ``x_max_ticks``, ``y_max_ticks``: Maximum number of tick marks
- ``x_label_format``, ``y_label_format``: Functions to format axis labels
- ``x_axis_title``, ``y_axis_title``: Axis titles
- ``x_shift``, ``y_shift``: Shift data relative to axis

**Canvas Settings:**

- ``width``, ``height``: Chart dimensions in pixels
- ``left_margin``, ``right_margin``: Horizontal margins
- ``y_margin``, ``x_margin``: Vertical margins (varies by chart orientation)

**Styling:**

- ``colours``: List of colours for series
- ``bar_width``, ``bar_gap``: Bar chart specific (bar thickness and spacing)

Common Methods
^^^^^^^^^^^^^^

All charts support these methods:

.. code:: python

    # Rendering
    svg_string = chart.render()                    # Basic SVG output
    svg_string = chart.render_with_all_styles()    # With inline CSS (for hovers)
    chart.save('output.svg')                       # Save to file

    # Legends
    chart.add_legend(x_position=700, y_position=200)

    # Grids
    chart.add_grids(minor_x_ticks=4, minor_y_ticks=4)
    chart.add_y_grid(minor_ticks=5)
    chart.add_x_grid(minor_ticks=5)

    # Hover effects (requires render_with_all_styles)
    def hover_fn(position, x_value, y_value, series_name, styles):
        return [psc.Text(x=position.x, y=position.y, content=str(y_value))]

    chart.add_hover_modifier(hover_fn, radius=5)

    # Custom elements
    chart.add_custom_element(psc.Circle(x=100, y=100, radius=5))
    chart.add_custom_element(psc.Line(x=50, y=50, width=100, height=0))
    chart.add_custom_element(psc.Text(x=200, y=200, content='Label'))

    # Direct series styling
    chart.series['Series Name'].styles = {'stroke': 'red', 'stroke-width': '3'}

    # Modify all series
    chart.modify_series(lambda s: s)


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
