"""Top-level package for py-svg-chart"""

__author__ = "Alex Rowley"
__email__ = ""
__version__ = "0.4.0"

from .charts import (
    LineChart,
    SimpleLineChart,
    DonutChart,
    BarChart,
    NormalisedBarChart,
    ScatterChart,
)
from .shapes import (
    Text,
    Line,
    Circle,
)
from .styles import (
    render_all_styles,
    hover_style_name,
)
