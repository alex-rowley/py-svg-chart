"""
pysvgchart - Python SVG Chart Generator

Generate clean, standalone SVG charts in Python for embedding in web applications.

Chart Types:
    LineChart, SimpleLineChart - Line plots for time series and trends
    BarChart - Vertical bar charts for category comparisons
    HorizontalBarChart - Horizontal bars (useful for long category names)
    NormalisedBarChart - 100% stacked bars for part-of-whole comparisons
    ScatterChart - Scatter plots for correlation/distribution
    DonutChart - Pie/donut charts for proportions

Shape Primitives (for custom elements):
    Circle, Line, Text

Styling:
    hover_style_name - CSS class name for hover elements
    render_all_styles() - Generate CSS for hover effects

Quick Start:
    >>> import pysvgchart as psc
    >>> chart = psc.DonutChart([25, 30, 20, 25], labels=['Q1', 'Q2', 'Q3', 'Q4'])
    >>> svg = chart.render()

    >>> chart = psc.SimpleLineChart(x_values=[1,2,3], y_values=[[10,20,15]], y_names=['Sales'])
    >>> chart.add_legend()
    >>> svg = chart.render()

Documentation:
    README.rst - Full documentation with examples and API reference
    CLAUDE.md - Architecture overview for AI assistants and quick reference
"""

__author__ = "Alex Rowley"
__email__ = ""
__version__ = "0.7.0"

from .charts import (
    BarChart,
    CartesianChart,
    DonutChart,
    HorizontalBarChart,
    HorizontalChart,
    LineChart,
    NormalisedBarChart,
    ScatterChart,
    SimpleLineChart,
    VerticalChart,
)
from .shapes import (
    Circle,
    Line,
    Text,
)
from .styles import (
    hover_style_name,
    render_all_styles,
)
