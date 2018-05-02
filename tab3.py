import logging
logger = logging.getLogger(__name__)

import pandas as pd

from bokeh.io import curdoc

from components.dash import DropdownComponent, DropdownGroupComponent, TextboxComponent, DashboardComponent, DateRangeSliderComponent, RangeSliderComponent
from bokeh.models import ColumnDataSource, Panel, WidgetBox
from bokeh.layouts import row, column


class OverviewComponent(DashboardComponent):

	def make_dataset(self, df, **kwargs):
		"""Create a pandas dataframe which holds the data needed for this component"""
		return df

	def make_component(self, data, **kwargs):
		dc = TextboxComponent(data, column='glucose')
		drs = DateRangeSliderComponent(data, column='datetime')
		rs = RangeSliderComponent(data, column="glucose")
		graph1 = DashboardComponent(data)
		k = WidgetBox(dc.root, drs.root, rs.root)
		l = row(k, graph1.root)
		return l


def tab(df):
	oc = OverviewComponent(df)	
	return Panel(child = oc.root, title = "Riskfactor")
