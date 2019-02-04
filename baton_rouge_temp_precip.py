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
