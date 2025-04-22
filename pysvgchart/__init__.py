"""Top-level package for py-svg-chart"""

__author__ = 'Alex Rowley'
__email__ = ''
__version__ = '0.2.4'

from .charts import LineChart, SimpleLineChart, DonutChart, BarChart
from .shapes import Text, Line, Circle
from .styles import render_all_styles, hover_style_name
