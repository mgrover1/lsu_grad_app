#Import the neccessary libraries
import pandas as pd
import bokeh as bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_file, show, export_png
from bokeh.models import FactorRange, ColumnDataSource, CDSView, IndexFilter
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import column, layout, widgetbox
from bokeh.layouts import layout
import numpy as np
import datetime as datetime,time
from datetime import date
import csv
import urllib as urllib
import json
import matplotlib.pyplot as plt

#Part 1 - Read in the data and create basic plots and export a text file 
#Pull the json data provided by the Baton Rouge Airport 
json_string = urllib.request.urlopen('http://data.rcc-acis.org/StnData?sid=kbtr&sdate=20180101&edate=20181231&elems=maxt,mint,pcpn&output=json')

#Read in the json data and assign it to a variable to read 
f = json_string.read()

#Parse the json file to be read into a dataframe
parsed_json = json.loads(f)

#Extract the data from the parsed json file 
data = parsed_json['data']

#Create a dataframe to store the temp/precip data from the json file 
df = pd.DataFrame(data, columns=['date','high','low','precip'])

#Convert the date to datetime 
df['date'] = pd.to_datetime(df.date, format = '%Y/%m')

#Convert the string for high temperature to a numeric value
df['high'] = pd.to_numeric(df.high)

#Convert the string for low temperature to a numeric value
df['low'] = pd.to_numeric(df.low)

#Convert the "Trace" values to 0 then convert all values to numeric 
for i in range(len(df)):
    if df['precip'][i] == 'T':
        df['precip'][i] = 0.00
    else: 
        df['precip'][i] = df['precip'][i]
df['precip'] = pd.to_numeric(df.precip)

#Set the index to the datetime object 
df.set_index('date', inplace=True)

#Group together the monthly average high/low temperatures 
avg_high = df.groupby(pd.Grouper(freq='M')).mean()['high']
avg_low = df.groupby(pd.Grouper(freq='M')).mean()['low']

#Calculate the total monthly precipitation 
total_precip = df.groupby(pd.Grouper(freq='M')).sum()['precip']

#Create a summary dataframe containing all the average/total values 
summary_df = pd.DataFrame(avg_high)
summary_df['low'] = avg_low
summary_df['precip'] = total_precip 
summary_df.index = [datetime.date.strftime(x, '%Y-%m') for x in summary_df.index]

#Export the dataframe to a text file 
summary_df.to_csv('LSU_Grad_App.txt',header=False,float_format='%.2f')

#Create a bar graph for the monthly average high temperature 
fig1 = summary_df.high.plot.bar(title='Monthly Average High Temperature at Baton Rouge Airport', color ='r', figsize=(10,8))
fig1 = fig1.get_figure()
plt.xlabel('Month')
plt.ylabel('Temperature (F)')
fig1.savefig('avg_high_temp.png', dpi=300)

#Create a bar graph for the monthly average low temperature 
fig1 = summary_df.low.plot.bar(title='Monthly Average Low Temperature at Baton Rouge Airport', color ='b', figsize=(10,8))
fig1 = fig1.get_figure()
plt.xlabel('Month')
plt.ylabel('Temperature (F)')
fig1.savefig('avg_low_temp.png', dpi=300)

#Create a bar graph for the monthly total precipitation
fig1 = summary_df.precip.plot.bar(title='Monthly Total Precipitation at Baton Rouge Airport', color ='g', figsize=(10,8))
fig1 = fig1.get_figure()
plt.xlabel('Month')
plt.ylabel('Liquid Precipitation (Inches)')
fig1.savefig('total_precip.png', dpi=300)

#Part 2 
#Create interactive bar graphs and a table using bokeh, a java-based python library 

#Set an output file for the interative graphs 
output_file('Summary_Table.html')

#Create a list of months to be listed on the x-axis 
x = list(summary_df.index)

#Create a figure for the monthly high/low temperatures 
p = figure(x_range=x,title='Average Monthly Temperatures Baton Rouge, LA', plot_width=700, plot_height=500)
p.xaxis.axis_label = "Month"
p.yaxis.axis_label = "Temperature (F)"

#Plot the average monthly high temperature 
p.vbar(x=x, top=summary_df.high, color='red', width=0.9, legend='High Temperature') 

#Plot the average monthly low temperature
p.vbar(x=x, top=summary_df.low, color='blue', width=0.9, legend='Low Temperature') 

#Create a second figure that plots the total precipitation for each month
p1 = figure(x_range=x,title='Average Total Precipitation Baton Rouge, LA', plot_width=700, plot_height=500)
p1.xaxis.axis_label = "Month"
p1.yaxis.axis_label = "Total Liquid Precip (Inches)"

#Plot the bars for the total precip
p1.vbar(x=x, top=summary_df.precip, color='green', width=0.9) 

#Create a dictionary with the values from the summary dataframe
data = dict(
        dates = summary_df.index,
        high = summary_df.high,
        low = summary_df.low,
        precip = summary_df.low,
    )

#Convert the dictionary to column data source format to be read into the table 
data = ColumnDataSource(data)

#Set the column titles 
columns = [
        TableColumn(field="dates", title="Month"),
        TableColumn(field="high", title="Average High Temperature"),
        TableColumn(field="low", title="Average Low Temperature"),
        TableColumn(field="precip", title="Total Precipitation"),
    ]

#Create the data table 
data_table = DataTable(source=data, columns=columns,width=1400, height=500)

#Set the layout of the graphs and table 
l = layout([
  [p,p1],
  [widgetbox(data_table)],
],)

#Show the html file created from Bokeh 
show(l)
