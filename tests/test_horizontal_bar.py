"""
Simple test script to demonstrate the new HorizontalBarChart
"""
import pysvgchart as psc

# Create a simple horizontal bar chart
categories = ['Apples', 'Bananas', 'Cherries', 'Dates', 'Elderberries']
values = [[25, 40, 15, 30, 35]]

horizontal_bar_chart = psc.HorizontalBarChart(
    x_values=values,
    y_values=categories,
    x_names=['Sales'],
    x_zero=True,
    y_axis_title='Products',
    x_axis_title='Units Sold',
    width=800,
    height=600,
    left_margin=200,
    y_axis_title_offset=90,
)

# Save the chart
horizontal_bar_chart.save('showcase/horizontal_bar_test.svg')


# Also test that existing VerticalChart still works
vertical_bar_chart = psc.BarChart(
    x_values=categories,
    y_values=values,
    y_names=['Sales'],
    y_zero=True,
    x_axis_title='Products',
    y_axis_title='Units Sold',
    width=800,
    height=400,
)

vertical_bar_chart.save('showcase/vertical_bar_test.svg')

