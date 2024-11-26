Python SVG Chart Generator (pysvgchart)
=======================================

A Python package for creating and rendering SVG charts, including line
charts, axes, legends, and text labels. This package supports both
simple and complex chart structures and is highly customizable for
various types of visualizations.

Features
--------

-  **Modular Structure**: Create SVG charts with reusable components
   like ``Line``, ``Text``, ``Axis``, and ``Shape``.
-  **Axis Scaling**: Automatically generates axis tick values based on
   the data range with customizable limits.
-  **Customizable Styles**: Supports custom styles for lines, text, and
   axes.
-  **Legends**: Add legends to your charts to represent different data
   series.
-  **Dynamic Rendering**: Render a chart in SVG format with full control
   over size, style, and elements.
-  **Support for Simple and Advanced Charts**: Create simple line charts
   or extend the functionality for more complex visualizations.

Installation
------------

.. code:: bash

   pip install svg-chart-generator

Alternatively, you can clone this repository and install it locally:

.. code:: bash

   git clone https://github.com/arowley-ai/py-svg-chart.git
   cd py-svg-chart
   pip install .

Usage
-----

Create a simple line chart with the following code:

.. code:: python

   from svg_chart_generator import SimpleLineChart

   # Sample data
   x_values = [0, 1, 2, 3, 4, 5]
   y_values = [[0, 2, 4, 6, 8, 10], [0, 1, 2, 3, 4, 5]]

   # Create the chart
   chart = SimpleLineChart(x_values, y_values, y_names=["Series 1", "Series 2"])

   # Add a legend
   chart.add_legend(x_position=500, y_position=60, element_x=100, element_y=0, line_length=20, line_text_gap=5)

   # Render the chart as an SVG string
   svg_output = chart.render

   # Save the SVG output to a file
   with open("chart.svg", "w") as f:
       f.write(svg_output)


   chart.series[0].styles['stroke'] = 'red'
   chart.series[1].styles['stroke'] = 'blue'
   chart.x_axis.axis_line.styles['stroke'] = 'black'

Extensible Configuration
------------------------

The entire codebase is designed to be extensible to enable unlimited
customisation. All of the lower level elements are accessible via
properties of the charts.

Contributing
------------

We welcome contributions! If you’d like to contribute to the project,
please follow these steps:

Fork this repository.
---------------------

Create a new branch (git checkout -b feature-branch). Commit your
changes (git commit -am ‘Add feature’). Push to the branch (git push
origin feature-branch). Open a Pull Request.

License
-------

This project is licensed under the MIT License - see the LICENSE file
for details.
