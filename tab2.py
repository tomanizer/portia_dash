import logging
logger = logging.getLogger(__name__)

import pandas as pd

from bokeh.io import curdoc

from components.dash import DropdownComponent, DropdownGroupComponent, TextboxComponent, DashboardComponent
from bokeh.models import ColumnDataSource, Panel
from bokeh.layouts import row, column


class OverviewComponent(DashboardComponent):

	def make_dataset(self, df, **kwargs):
		"""Create a pandas dataframe which holds the data needed for this component"""
		return df

	def make_component(self, data, **kwargs):
		dc = DropdownGroupComponent(data, levels=['isig', 'glucose'])
		graph1 = DashboardComponent(data)
		graph2 = DashboardComponent(data)
		l = row(dc.root, graph1.root, graph2.root)	
		return l


	def update_component(self, attr, old, new):
		"""update components"""
		for dropdown in dc.dropdowns:
			print(dropdown)

def tab(df):		
	oc = OverviewComponent(df)	
	return Panel(child = oc.root, title = "Tickets")

