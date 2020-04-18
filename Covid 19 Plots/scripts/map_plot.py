from bokeh.layouts import row
from bokeh.models import Panel

colormap = {'East Of England':'black', 'London': 'blue', 'Midlands':'red',
            'North East And Yorkshire':'green', 'North East and Yorkshire':'orange',
            'North West':'grey', 'South East':'purple', 'South West':'white'}

def map_tab(dataframe, google_api_key):

	def add_plot_styles(col):
		from sklearn.preprocessing import MinMaxScaler
		df = dataframe
		df['color'] = df['NHS England Region'].map(lambda x: colormap[x])

		if col == 'Total':
			scaler = MinMaxScaler(feature_range=(0.1,1))
			df['Size'] = 100*scaler.fit_transform(df[[col]])
		else:
			scaler = MinMaxScaler(feature_range=(0,0.8))
			scaler.fit(df[[dataframe.columns[-6]]])
			df['Size'] = 40*scaler.transform(df[[col]])

		return df

	def make_dataset(date):
		from bokeh.models import ColumnDataSource
		df = add_plot_styles(date)
		data = {'Region': df['NHS England Region'],
		        'Name': df['Name'],
		        'Deaths': df[date],
		        'Longitude': df['longitude'],
		        'Latitude': df['latitude'],
		        'Color': df['color'],
		        'Size': df['Size']}

		new_src = ColumnDataSource(data)

		return new_src

	def make_plot(src, api_key):
		from bokeh.plotting import gmap
		from bokeh.models import GMapOptions, HoverTool
		from datetime import date

		map_options = GMapOptions(lat=53.200817,lng=-1.488043, map_type="hybrid", zoom=7,
		                          scale_control=True)


		p = gmap(api_key, map_options, title="Covid-19 deaths by Trust - (Updated " + str(
			date.today()) + ")", plot_width=1200, plot_height=900)

		hover = HoverTool(tooltips =[
			('Name','@Name'),('Deaths','@Deaths')])

		p.add_tools(hover)
		p.circle(x="Longitude", y="Latitude", size='Size', fill_alpha=0.8, source=src,
		         legend_group="Region", fill_color = 'Color', line_color='black', line_width=0.5)

		p.legend.click_policy="hide"
		p = style(p)
		return p

	# Styling
	def style(p):

		# Title
		p.title.align = 'center'
		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

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
		available_dates = list(dataframe.columns[3:-4].values)

		menu = Select(options=available_dates, value='Total', title='Data', width=150)

		return menu

	def get_selection(checkbox):
		date_selected = []
		for i, act in enumerate(checkbox.active):
			if act == 1:
				date_selected.append(checkbox.labels[i])
				break
		return date_selected

	def callback(attr, old, new):
		new_src = make_dataset(date_selection.value)

		src.data.update(new_src.data)




	# Make a ColumnDataSource for bokeh to use
	# Start off with the graph showing the 'Total' column from the dataframe
	src = make_dataset('Total')
	# Make a checkbox group
	date_selection = make_dropdown()
	# Specify the update function for the checkbox to use when it is clicked
	date_selection.on_change('value', callback)
	# Make the plot
	p = make_plot(src, google_api_key)

	layout = row(date_selection, p)
	tab = Panel(child=layout, title='Map')

	return tab

