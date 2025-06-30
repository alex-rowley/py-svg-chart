"""Top-level package for py-svg-chart"""

__author__ = "Alex Rowley"
__email__ = ""
__version__ = "0.5.1"

from .charts import (
    BarChart,
    DonutChart,
    LineChart,
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
