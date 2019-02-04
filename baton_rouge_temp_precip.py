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
