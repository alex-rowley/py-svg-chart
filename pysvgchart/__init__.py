"""Top-level package for py-svg-chart"""

__author__ = 'Alex Rowley'
__email__ = ''
__version__ = '0.1.1'

from .charts import LineChart, SimpleLineChart, DonutChart, Line
from .shapes import Text, Line, Circle
from .styles import render_all_styles, hover_style_name
