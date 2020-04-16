def make_dataset(dataframe, age_groups):
	df = dataframe

	for group in age_groups:
		df.drop(group, axis=1, inplace=True)

	return df

def make_plot(dataframe):
	from bokeh.layouts import gridplot
	from bokeh.plotting import figure, output_file, show
	from bokeh.models import HoverTool
	from bokeh.plotting import ColumnDataSource
	
	colors = ['red', 'green', 'blue', 'grey', 'purple']
	# output to static HTML file
	#
	output_file("html_plots/grid_plot_age.html")
	
	
	# create a new plot with a title and axis labels
	p5 = figure(title="Total cumulative deaths from Covid-19 in UK grouped by age", x_axis_label='Date',
	            y_axis_label='Total deaths', x_axis_type="datetime")
	p6 = figure(title="Deaths per day from Covid-19 in UK grouped by age", x_axis_label='Date',
	            y_axis_label='Total deaths', x_axis_type="datetime")
	
	for i, group in enumerate(dataframe.columns.get_level_values(0).unique()):
		src = ColumnDataSource({'x':dataframe.index,
		                        'cum':dataframe[group]['cumulative total'],
		                        'deaths':dataframe[group]['deaths today']})
	
		p5.line(x='x', y='cum', source=src, line_width=1, line_color=colors[i], legend_label=group)
		p5.circle(x='x', y='cum', source=src, fill_color=colors[i], line_color=colors[i], size=6, legend_label=group)
	
		p6.line(x='x', y='deaths', source=src, line_width=1, line_color=colors[i], legend_label=group)
		p6.circle(x='x', y='deaths', source=src, fill_color=colors[i], line_color=colors[i], size=6, legend_label=group)
	
		hover5 = HoverTool(tooltips =[
			('age group',group),('(Date, Total deaths)','(@x{%F}, @cum)')],
			formatters={'@x': 'datetime'})
		hover6 = HoverTool(tooltips =[
			('age group',group),('(Date, deaths today)','(@x{%F}, @deaths)')],
			formatters={'@x': 'datetime'})
	
		p5.add_tools(hover5)
		p6.add_tools(hover6)
	
	p5.legend.location = "top_left"
	p6.legend.location = "top_left"
	p5.legend.click_policy="hide"
	p6.legend.click_policy="hide"
	

	# make a grid
	grid = gridplot([[p5, p6]], plot_width=500, plot_height=400)


	return grid
