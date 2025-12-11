# CLAUDE.md

This file provides guidance for Claude Code (and human developers) working with the py-svg-chart codebase.

## Project Overview

**py-svg-chart** is a Python library for generating SVG charts entirely in Python. It produces clean, standalone SVG output that can be embedded directly in web applications without JavaScript dependencies or post-processing.

**Key differentiator:** Unlike image-based charting libraries or JS-dependent solutions, this generates resolution-independent, customizable SVG markup server-side.

## Quick Start

```bash
pip install pysvgchart
```

```python
import pysvgchart as psc

# Simple donut chart
chart = psc.DonutChart([25, 30, 20, 25])
svg = chart.render()

# Line chart
chart = psc.SimpleLineChart(
    x_values=[1, 2, 3, 4, 5],
    y_values=[[10, 20, 15, 25, 30]],
    y_names=['Sales']
)
chart.add_legend()
svg = chart.render()
```

## Architecture Overview

```
pysvgchart/
├── charts.py      # Chart classes (entry points for users)
├── axes.py        # Axis management (XAxis, YAxis, CategoryYAxis)
├── series.py      # Data series (LineSeries, BarSeries, ScatterSeries, DonutSegment)
├── scales.py      # Scale calculations (Linear, Logarithmic, Categorical)
├── legends.py     # Legend rendering
├── shapes.py      # SVG primitives (Point, Line, Circle, Rect, Text, Group)
├── helpers.py     # Utility functions (tick generation, formatting)
├── styles.py      # CSS style rendering for hover effects
└── shared.py      # Type definitions
```

### Class Hierarchy

```
Chart (ABC)
├── CartesianChart
│   ├── VerticalChart        # Y-axis vertical, X-axis horizontal
│   │   ├── LineChart        # Line/area charts
│   │   │   ├── SimpleLineChart
│   │   │   ├── BarChart
│   │   │   ├── NormalisedBarChart
│   │   │   └── ScatterChart
│   │   └── (inherits axis setup)
│   └── HorizontalChart      # X-axis has values, Y-axis has categories
│       └── HorizontalBarChart
└── DonutChart               # Pie/donut (non-Cartesian)
```

### Data Flow

1. **User creates chart** with x_values, y_values, configuration
2. **Axes created** via `x_axis_type`/`y_axis_type` using `scale_maker` functions
3. **Series constructed** via `series_constructor` (converts data to positioned shapes)
4. **Optional additions:** legends, grids, hover modifiers, custom elements
5. **Render:** `chart.render()` or `chart.render_with_all_styles()` produces SVG string

### Key Design Patterns

- **Factory Pattern:** `series_constructor` functions create appropriate Series types
- **Template Method:** Base `Chart` defines `render()`, subclasses implement `get_element_list()`
- **Strategy Pattern:** Pluggable `scale_maker` functions, `label_format` callbacks
- **Composition:** Charts compose axes, series, legends, shapes

## Chart Types

| Chart | Class | Use Case |
|-------|-------|----------|
| Line | `LineChart`, `SimpleLineChart` | Time series, trends |
| Bar (vertical) | `BarChart` | Category comparisons |
| Bar (horizontal) | `HorizontalBarChart` | Long category names |
| Stacked (100%) | `NormalisedBarChart` | Part-of-whole comparisons |
| Scatter | `ScatterChart` | Correlation, distribution |
| Donut/Pie | `DonutChart` | Proportions |

## Common Patterns

### Adding Interactivity (Hover Effects)

```python
def hover_fn(position, x_value, y_value, series_name, styles):
    return [psc.Text(x=position.x, y=position.y-10, content=str(y_value),
                     classes=['psc-hover-data'])]

chart.add_hover_modifier(hover_fn, radius=5)
svg = chart.render_with_all_styles()  # Must use this for hovers
```

### Custom Styling

```python
# Direct series style modification
chart.series['Series Name'].styles = {'stroke': 'red', 'stroke-width': '3'}

# Access axis elements
chart.x_axis.tick_lines = []  # Remove tick marks
chart.y_axis.axis_line.styles['stroke'] = '#ccc'
```

### Adding Custom Elements

```python
chart.add_custom_element(psc.Circle(x=100, y=100, radius=5, styles={'fill': 'red'}))
chart.add_custom_element(psc.Text(x=200, y=50, content='Annotation'))
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pysvgchart.py

# Tests generate SVG files in showcase/ directory
```

The `showcase/` directory contains generated SVG examples from the test suite.

## File Purposes

| File | Purpose |
|------|---------|
| `charts.py` | Main entry points. All public chart classes. Series constructors. |
| `axes.py` | Axis rendering, tick generation, scale positioning |
| `series.py` | Data series types that render as SVG paths/shapes |
| `scales.py` | Numeric scale calculations (min/max, tick intervals) |
| `shapes.py` | Low-level SVG elements (Point, Line, Circle, Text, Group) |
| `legends.py` | Legend components for each chart type |
| `helpers.py` | Utility functions (formatting, element list flattening) |
| `styles.py` | CSS generation for hover effects |
| `shared.py` | Type aliases used across modules |

## Type System

Key type aliases from `shared.py`:
- `number = float | int`
- `numbers_sequence = list[number] | tuple[number, ...]`
- `style_def = dict[str, str]` (SVG style attributes)

## Common Tasks

### Adding a new chart type

1. Choose base class (`VerticalChart`, `HorizontalChart`, or `Chart`)
2. Set class attributes: `x_axis_type`, `y_axis_type`, `series_constructor`, `scale_maker`s
3. Override `add_legend()` if needed
4. Add to `__init__.py` exports

### Modifying axis behavior

Axes are in `axes.py`. Key methods:
- `get_positions()` - Convert data values to pixel positions
- Scale creation via `scale_maker` parameter

### Adding new shapes

Add to `shapes.py`. Inherit from `Element` or `Shape`, implement `get_element_list()` to return SVG strings.

## Dependencies

- Python 3.10+
- No runtime dependencies (standard library only)
- Dev: pytest for testing
