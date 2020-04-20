from bokeh.models.widgets import Div

information = "<h3> Information</h3>" \
              "<p>All data is taken from the NHS England website and can be found <a " \
              "href=https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily" \
              "-deaths/ target=_blank> here</a></br>" \
              "</br>From the website:</br>" \
              "<blockquote cite:https://www.england.nhs.uk/statistics/statistical-work-areas" \
              "/covid-19-daily-deaths/> <i>\"All " \
              "deaths are recorded against the date of death rather than the date the deaths were  " \
              "announced. Interpretation of the figures should take into account the fact that  " \
              "totals by date of death, particularly for most recent days, are likely to be " \
              "updated in future releases.</br>" \
              "These figures will be updated at 2pm each day and include confirmed cases reported at 5pm " \
				"the previous day. Confirmation of COVID-19 diagnosis, death notification and " \
              "reporting in central figures can take up to several days and the hospitals " \
              "providing the data are under significant operational pressure. This means that the " \
			"totals reported at 5pm on each day may not include all deaths that occurred on that " \
              "day or on recent prior days.</br>" \
              "These figures do not include deaths outside hospital, such as those in care" \
              "homes. This approach makes it possible to compile deaths data on a daily basis " \
              "using up to date figures.\"</blockquote></i></p> "


def make_info_paragraph():
	information_para = Div(text=information, name='Information', width=150,
	                       style={'font-size': '100%', 'color': 'white'}, sizing_mode=
	                       "scale_width")

	return information_para
