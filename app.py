# from videocapture import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

import pandas as pd
df= pd.read_csv('Timestamps.csv', parse_dates=['Start', 'End'])

df['Start_string'] = df['Start'].dt.strftime('%H:%M:%S')
df['End_string'] = df['End'].dt.strftime('%H:%M:%S')

cds = ColumnDataSource(df)

p = figure(x_axis_type= 'datetime', height=100, width= 500, sizing_mode= 'scale_width', title= 'Motion Graph')
p.ygrid.grid_line_color = None

hover = HoverTool(tooltips= [('Start', '@Start_string'), ('End', '@End_string')])

p.add_tools(hover)


p.quad(left='Start', right='End', bottom = 0, top =1, color = 'green', source=cds)

output_file('Graph.html')
show(p)
