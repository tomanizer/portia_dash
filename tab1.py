
import logging
logger = logging.getLogger(__name__)

from functools import partial

import pandas as pd

from bokeh.io import curdoc

from components.dash import DropdownComponent, DropdownGroupComponent, TextboxComponent, DashboardComponent, TableComponent, RangeSliderComponent, DateRangeSliderComponent
from bokeh.models import ColumnDataSource, Panel, InputWidget, GroupFilter, IndexFilter, CDSView
from bokeh.layouts import row, column
from bokeh.models import WidgetBox, GroupFilter
from traitlets import observe, Dict, Integer


class InputComponent(DashboardComponent):
	"""
	Create the user interface based on the data it received.
	"""
	
	filterdict = Dict() # Traitlet which automatically triggers updates when changed. See Note!

	def make_component(self, data, **kwargs):
		dc = DropdownGroupComponent(data, levels=['isig', 'glucose'], tags = "input")
		for dropdown in dc.dropdowns:
			dropdown.on_change("value", partial(self.update_component, widget=dropdown))
		drs = DateRangeSliderComponent(data, column='datetime')
		drs.root.on_change("value", partial(self.update_component, widget=drs.root))
		rs = RangeSliderComponent(data, column="glucose")
		rs.root.on_change("value", partial(self.update_component, widget=rs.root))
		l = column(dc.root, drs.root, rs.root)
		return l
		
	@observe("filterdict")
	def changed(self, change):
		print("Dictionary updated")
		print(change)

	def update_component(self, attr, old, new, widget):
		"""Update the filter dict property and trigger the update event
		
		Note: The dictionary cannot be changed in place.
		Hence we create a new dictionary, update it and then assign its value to the trait ditionary.
		This will trigger an update.
		"""
		
		print("dropdown changed")
		#print("This is the Input component {}. Widget Title: {}. Widget Value {}.".format(attr, widget.title, widget.value))
		newfilter = self.filterdict.copy()
		if not widget.value == "All":
			#self.filterdict[widget.title] = widget.value
			newfilter[widget.title] = widget.value
		else:
			if widget.title in self.filterdict.keys():
				del newfilter[widget.title]
				#del self.filterdict[widget.title]
				print("remove key from filterdict".format(widget.title))
		self.filterdict = newfilter.copy()
		print("Has filter changed?: {}. Old filter {}  new filter {}".format(newfilter != self.filterdict, newfilter, self.filterdict))


class GraphComponent(DashboardComponent):
	"""
	Combination of graphs and tables which give the dashboard view
	"""

	def make_component(self, data, **kwargs):
		self.graph1 = DashboardComponent(data)
		self.graph2 = DashboardComponent(data)
		self.table = TableComponent(data)
		return row(self.table.root, self.graph1.root, self.graph2.root)
		
	def update_component(self, change):
		"""update components"""
		print("Updating the graphs component {}".format(change))


class TabComponent(DashboardComponent):
	"""
	Root contains a panel with input an graph components
	"""

	def make_dataset(self, df, **kwargs):
		"""Create a pandas dataframe which holds the data needed for this component"""
		self.df = df
		return df

	def make_component(self, data, **kwargs):
		
		#input box
		self.ic = InputComponent(data)
		self.ic.observe(self.update_component, names=["filterdict"])
		
		#graph and table box
		self.gc = GraphComponent(data)
		
		l = row(self.ic.root, self.gc.root)
		p = Panel(child=l, title="Glucose")
		return p

	def update_component(self, change):
		"""update components"""
		print("Updating the tab component {}".format(change))
		filteredsource = self.source.copy()
		for key,value in self.ic.filterdict.items():
			if isinstance(value, tuple):
				mymin, mymax = value
				print(mymin)
				print(mymax)
				filteredsource = filteredsource[(filteredsource[key] >= mymin) &  (filteredsource[key] <= mymax)]
				print(filteredsource.head())
			else:
				filteredsource = filteredsource[filteredsource[key] == value]
		filteredsource = filteredsource.reindex()
		#groupfilters = [(GroupFilter(column_name=key, group=value)) for key,value in self.ic.filterdict.items()]
		#self.gc.table.source = CDSView(source=self.gc.table.source, filters=groupfilters)
		#self.gc.table.update_component(df=filteredsource, filter=groupfilters)
		self.gc.table.update_component(df=filteredsource)




