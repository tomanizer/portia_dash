# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs, Panel, Div
from bokeh.layouts import row, column


# Each tab is drawn by one script
from components.dash import DropdownComponent, DropdownGroupComponent, TextboxComponent, DashboardComponent



df = pd.read_csv("/home/thomas/.bokeh/data/CGM.csv")

div = Div(text='<div "style="background-color:lightblue"> <h1 >This is my cool header</h1></div>', width=1600)

div = Div(text='<div style="background-color:lightblue"> <h3>This is a heading in a div element</h3>  <p>This is some text in a div element.</p> </div>', width=1400)

# Create each of the tabs
dc = DropdownGroupComponent(df, levels=['isig', 'glucose'])
graph1 = DashboardComponent(df)
graph2 = DashboardComponent(df)
graph3 = DashboardComponent(df)
l = row(dc.root, graph1.root, graph2.root, graph3.root)
tab1 = Panel(child = l, title = 'Glucose')

dd = DropdownGroupComponent(df, levels=['isig', 'glucose'])
tab2 = Panel(child = dd.root, title = 'ISIG')

de = TextboxComponent(df, label="Enterme")
tab3 = Panel(child = de.root, title = 'External')



# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3], width=1400)



# Put the tabs in the current document for display
curdoc().add_root(column(div, tabs))
