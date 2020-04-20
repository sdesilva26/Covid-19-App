from bokeh.layouts import row, column
from bokeh.models import Panel, Label
from bokeh.models.widgets import Div
from scripts.information_paragraph import make_info_paragraph
from scripts.utilities import get_last_updated
y_label_title = {'Deaths Today': 'Deaths',
                 'Cumulative Total': 'Total deaths',
                 'Change': 'Change in deaths',
                 'Relative Change': 'Change in deaths (%)'}
stats_explanations = {'Deaths Today': '</br> <b>Deaths Today:</b> the deaths recorded today that '
                                      'list '
                                      'Covid-19 as cause of death',
                 'Cumulative Total': '</br><b>Cumulative Total:</b> the total deaths recorded up '
                                     'until today '
                                     'that list Covid-19 as a cause of death',
                 'Change': '</br><b>Change:</b> the change in deaths due to Covid-19 compared to '
                           'the deaths '
                           'on the previous days',
                 'Relative Change': '</br><b>Relative Change:</b> the change in deaths due to '
                                    'Covid-19 '
                                    'compared to the deaths '
                                    'on the previous days shown as a percentage'}



def line_tab(dataframe, tab_title, filepath):

	def make_dataset(type_of_plot):
		import pandas as pd
		from bokeh.plotting import ColumnDataSource
		df = dataframe

		type_of_data = dataframe.columns.get_level_values(0).name
		groups = dataframe.columns.get_level_values(0).unique().values
		new_df = pd.DataFrame(dataframe.T.loc[(groups, type_of_plot),:].T.values, columns=groups,
		                      index=dataframe.index)
		# new_df = new_df.T.unstack().reset_index(level=1, name='Deaths').rename(columns={
		# 	'level_1':type_of_data})[[
		# 	'Deaths',type_of_data]]

		new_src = ColumnDataSource(new_df)

		return new_src

	def make_plot(src):
		from bokeh.plotting import figure
		from bokeh.models import HoverTool
		from bokeh.palettes import Dark2_8 as palette
		import itertools

		groups = dataframe.columns.get_level_values(0).unique().values
		type_of_data = dataframe.columns.get_level_values(0).name

		y_title = y_label_title[statistic_selection.value]

		p = figure(title="Statistics about deaths in the UK grouped by " + tab_title, x_axis_label='Date',
		            y_axis_label=y_title, x_axis_type="datetime", plot_width=900, plot_height=600)

		colors = itertools.cycle(palette)

		for group, color in zip(groups, colors):
		# p.line(x='index', y='Deaths', source=src, line_width=1, legend_label=type_of_data)
		# p.circle(x='index', y='Deaths', source=src, size=6, legend_label=type_of_data)
			p.multi_line(xs='index', ys=group,
		             line_width=5, line_alpha=0.6, hover_line_alpha=1.0,
		             source=src)

		hover = HoverTool(tooltips =[(type_of_data, '@columns}'),
		 	('Date','@index{%F}'),(y_title,'@Deaths{0}')],
		 	formatters={'@index': 'datetime'})

		p.add_tools(hover)

		p.legend.location = "top_left"
		p.legend.click_policy="hide"
		p = style(p)

		return p

	# Styling
	def style(p):

		# Title
		p.title.align = 'center'
		p.title.text_font_size = '18pt'
		#p.title.text_font = 'serif'

		# Axis titles
		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		# Tick labels
		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		return p

	def make_dropdown():
		from bokeh.models.widgets import Select
		available_statistics = list(dataframe.columns.get_level_values(1).unique().values)

		menu = Select(options=available_statistics, value=available_statistics[0],
		              title='Statistic to plot',
		              width=150, sizing_mode = "scale_width")

		return menu


	# # Update the plot based on selections
	def callback(attr, old, new):
		new_src = make_dataset(statistic_selection.value)
		two_col_row.children[1] = make_plot(new_src)
		stats_explanation.text = stats_explanations[statistic_selection.value]
		#src.data.update(new_src.data)


	# Make a ColumnDataSource for bokeh to use
	# Start off with the graph showing the first statistic in the dataframe
	src = make_dataset(dataframe.columns.get_level_values(1).unique().values[0])
	# Make a dropdown menu
	statistic_selection = make_dropdown()
	# Specify the update function for the checkbox to use when it is clicked
	statistic_selection.on_change('value', callback)
	# Make the plot

	stats_explanation = Div(text=stats_explanations[dataframe.columns.get_level_values(
		1).unique().values[0]], name='Statistics explanation', width=150,
	                        style={'font-size': '120%', 'color': 'white'})

	last_updated = Div(text='<b>Last updated:</b> ' + get_last_updated(filepath), name='Last '
	                                                                                  'updated '
	                'text', style={'font-size': '120%', 'color': 'white'}, width=150)

	col = column(statistic_selection, stats_explanation, last_updated)
	two_col_row = row(col, make_plot(src), make_info_paragraph())
	#layout = column(two_col_row, make_info_paragraph())
	layout = two_col_row
	tab = Panel(child=layout, title=tab_title)

	return tab



