"""Top-level package for py-svg-chart"""

__author__ = 'Alex Rowley'
__email__ = ''
__version__ = '0.3.1'

from .charts import LineChart, SimpleLineChart, DonutChart, BarChart, NormalisedBarChart
from .shapes import Text, Line, Circle
from .styles import render_all_styles, hover_style_name
