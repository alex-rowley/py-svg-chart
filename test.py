import pysvgchart as psc
import datetime
import random

# start_date = datetime.date(datetime.datetime.now().year, 1, 1)
# x_values = [start_date + datetime.timedelta(weeks=i) for i in range(30)]

x_values = list(range(100))

y_values = [4000]
for i in range(99):
    y_values.append(y_values[-1]+100*random.randint(0, 1))

line_chart = psc.SimpleLineChart(x_values, [y_values, [1000+y for y in y_values]],['predicted', 'actual'])
line_chart.add_legend()

with open('outputs/temp.svg', 'w+') as out_file:
    out_file.write(line_chart.render)

print(line_chart.y_axis.tick_text[-1].styles)