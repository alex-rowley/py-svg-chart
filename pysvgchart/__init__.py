"""Top-level package for py-svg-chart"""

__author__ = "Alex Rowley"
__email__ = ""
__version__ = "0.6.0"

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
