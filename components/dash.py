import pandas as pd
import numpy as np
from datetime import datetime

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, TextInput, DataTable, DateFormatter, TableColumn, DateRangeSlider, RangeSlider
from bokeh.models import ColumnDataSource, CDSView
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.layouts import column, row, WidgetBox

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from traitlets import HasTraits, observe, Dict

import logging
logger = logging.getLogger()


class DashboardComponent(HasTraits):

    """ Base class for UI dashboard components.
    This class must have two attributes, ``root`` and ``source``, and one
    method ``update``:

    *  source: a Bokeh ColumnDataSource
    *  root: a Bokeh Model
    *  update: a method that consumes the messages dictionary found in
               distributed.bokeh.messages
    """

    def __init__(self, df, **kwargs):

        #make all keywords attributes of the class
        for i in kwargs:
            setattr(self, i, kwargs[i])

        self.source = self.make_dataset(df, **kwargs)
        self.root = self.make_component(self.source, **kwargs)

    def make_dataset(self, df, **kwargs):
        """Create a pandas dataframe which holds the data needed for this component"""
        return df

    def make_component(self, data, **kwargs):
        p = figure(plot_width = 300, plot_height = 300,
                  title = 'PlaceHolder for Dashboard Component',
                  x_axis_label = 'x-Axis', y_axis_label = 'Y-Axis')
                 
        p = self.style_component(p)
        return p

    def style_component(self, p, **kwargs):
        return p

    def update_component(self, attr, old, new):
        """Updates self.source """
        print("Base components: {} {} {}".format(attr, old, new))
 

class DropdownComponent(DashboardComponent):

    def make_dataset(self, df, **kwargs):
        df = df.copy()
        colname = kwargs["colname"]
        df[colname] = df[colname].astype(str)
        valuelist = ['All'] + sorted(df[colname].unique())
        logger.debug(valuelist)
        return valuelist

    def make_component(self, data, **kwargs):
        colname = kwargs["colname"]
        mydrop = Select(title=colname, options=data)
        return mydrop
    

class DropdownGroupComponent(DashboardComponent):

    def make_dataset(self, df, **kwargs):
        levels = kwargs["levels"]
        df = df[levels].drop_duplicates()
        return df

    def make_component(self, data, **kwargs):
        self.dropdowns = [DropdownComponent(data, colname=col).root for col in data.columns]
        for dropdown in self.dropdowns:
            dropdown.on_change('value', self.update_component)
        return column(self.dropdowns)
    
    
class TextboxComponent(DashboardComponent):

    def make_component(self, data, **kwargs):
        label = kwargs["column"]
        tbox = TextInput(placeholder="default", title=label)
        return tbox
        
class DateRangeSliderComponent(DashboardComponent):
    
    def make_dataset(self, df, **kwargs):
        label = kwargs["column"]
        df = df[label].drop_duplicates()
        df = pd.to_datetime(df)
        return df

    def make_component(self, data, **kwargs):
        label = kwargs["column"]
        start = data.min().date()
        end = data.max().date()
        print(start, end)
        
        drslide = DateRangeSlider(start=start, end=end, value=(start, end), step=1, title=label)
        return drslide
        
class RangeSliderComponent(DashboardComponent):

    def make_dataset(self, df, **kwargs):
        label = kwargs["column"]
        df = df[[label]].drop_duplicates()
        df = df.astype(float)
        return df

    def make_component(self, data, **kwargs):
        label = kwargs["column"]
        start = float(data.min())
        end = float(data.max())
        rslide = RangeSlider(start=start, end=end, value=(start, end), title=label)
        return rslide
    
class TableComponent(DashboardComponent):

	def make_component(self, data, **kwargs):
		cols = [TableColumn(field=col, title=col) for col in data.columns]
		myindex = data.index
		if isinstance(data, pd.DataFrame):
			data = ColumnDataSource(data)
		try:
			data.remove('index')
		except:
			pass
			#data.add(myindex, 'index')
		data_table = DataTable(source=data, columns=cols,   width=600, height=400)
		return data_table
	 
	def update_component(self, **kwargs):
		
		if "df" in kwargs:	
			df = kwargs["df"]
			data = self.make_dataset(df)
		source = ColumnDataSource(data)
		filters=[]
		if "filters" in kwargs:
			filters = kwargs["filters"]
		view = CDSView(source=source, filters=filters)
		self.root.source.data.update(df) #only this is used
		#self.root.source.data.update(self.root.source)
	 
