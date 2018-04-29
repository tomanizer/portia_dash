
import logging
logger = logging.getLogger(__name__)

# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs, Div
from bokeh.layouts import row, column


# Each tab is drawn by one script
import tab1
import tab2
import tab3

df = pd.read_csv("/home/thomas/.bokeh/data/CGM.csv")
df["glucose"] = df["glucose"].astype(float)
#df["datetime"] = pd.to_datetime(df["datetime"])
#print(df["datetime"].head())

# Create each of the tabs
tab1 = tab1.TabComponent(df)
tab2 = tab2.tab(df)
tab3 = tab3.tab(df)


# Put all the tabs into one application
#tabs = Tabs(tabs = [tab1, tab2, tab3], width=1400)
tabs = Tabs(tabs = [tab1.root, tab2, tab3], width=1400)

div = Div(text='<h4>This is a heading in a div element</h4>', width=1400, height=10)

# Put the tabs in the current document for display
curdoc().add_root(column(div, tabs))
