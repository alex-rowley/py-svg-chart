"""Top-level package for py-svg-chart"""

__author__ = "Alex Rowley"
__email__ = ""
__version__ = "0.4.0"

from .charts import (
    BarChart,
    DonutChart,
    LineChart,
    LogarithmicChart,
    NormalisedBarChart,
    ScatterChart,
    SimpleLineChart,
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
