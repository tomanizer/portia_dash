import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, TextInput
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.layouts import column, row, WidgetBox

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

import logging

logger = logging.getLogger()


class DashboardComponent(object):

    """ Base class for UI dashboard components.
    This class must have two attributes, ``root`` and ``source``, and one
    method ``update``:

    *  source: a Bokeh ColumnDataSource
    *  root: a Bokeh Model
    *  update: a method that consumes the messages dictionary found in
               distributed.bokeh.messages
    """

    def __init__(self, df, **kwargs):

        #make all keywaords attributes of the class
        for i in kwargs:
            setattr(self, i, kwargs[i])

        self.source = self.make_dataset(df, **kwargs)
        self.root = self.make_component(self.source, **kwargs)

    def make_dataset(self, df, **kwargs):
        """Create a pandas dataframe which holds the data needed for this component"""
        return ColumnDataSource(df)

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
        new_source = self.make_dataset(new)
        self.source.data.update(new_source.data)
 

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
    
    def update_component(self, attr, old, new):
        """Updates self.source """
        print("I changed")
        print(attr, old, new)

class DropdownGroupComponent(DashboardComponent):

    def make_dataset(self, df, **kwargs):
        levels = kwargs["levels"]
        #print(levels)
        df = df[levels].drop_duplicates()
        #print(df)
        return df

    def make_component(self, data, **kwargs):
        dropdowns = [DropdownComponent(data, colname=col).root for col in data.columns]
        #print(dropdowns)
        #return WidgetBox(dropdowns)
        for dropdown in dropdowns:
            dropdown.on_change('value', self.update_component)
        return column(dropdowns)
    
    def update_component(self, attr, old, new):
        """Updates self.source """
        print("I changed")
        print(attr, old, new)

class TextboxComponent(DashboardComponent):

    def make_component(self, data, **kwargs):
        label = kwargs["label"]
        tbox = TextInput(value="default", title=label)
        return WidgetBox(tbox)
    
    def update_component(self, attr, old, new):
        """Updates self.source """
        print("Previous label: " + old)
        print("Updated label: " + new)
