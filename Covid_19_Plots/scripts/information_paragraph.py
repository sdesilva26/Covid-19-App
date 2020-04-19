from bokeh.models.widgets import Div

information = "<h3> Information</h3>" \
              "<p>All data is taken from the NHS England website and can be found <a " \
              "href=https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily" \
              "-deaths/ target=_blank> here</a></br>" \
              "</br>From the website:</br>" \
              "<blockquote cite:https://www.england.nhs.uk/statistics/statistical-work-areas" \
              "/covid-19-daily-deaths/> <i>All " \
              "deaths are recorded against the date of death rather than the date the deaths were  " \
              "announced. Interpretation of the figures should take into account the fact that  " \
              "totals by date of death, particularly for most recent days, are likely to be " \
              "updated in future releases. For example as deaths are confirmed as testing " \
              "positive for COVID-19, as more post-mortem tests are processed and data from them " \
              "are validated.</blockquote></i></p> "
def make_info_paragraph():

	information_para = Div(text=information, name='Information', width=150,
	                        style={'font-size': '120%', 'color': 'white'}, sizing_mode =
	                        "scale_width")

	return information_para