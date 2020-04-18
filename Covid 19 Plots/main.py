from scripts.data_acquisition import get_todays_data
from scripts.preprocessing import clean_data, append_location_data, add_statistics
from scripts.map_plot import map_tab
from scripts.line_plot import line_tab
# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

template = """
{% block postamble %}
<style>
.bk-root .bk-tab {
    background-color: cyan;
    width: 200px;
    color: red;
    font-style: italic;
}

.bk-root .bk-tabs-header .bk-tab.bk-active{
background-color: yellow;
color: blue;
font-style: normal;
font-weight: bold;
}

.bk-root .bk-tabs-header .bk-tab:hover{
background-color: yellow
}

</style>
{% endblock %}
"""

# Fetch the data and preprocess it
print("Getting today's data...")
# get_todays_data("https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily-deaths/",
#                 "./data/COVID-19-total-announced-deaths.xlsx", today=True)
print("Cleaning the data...")
raw_data_trusts, raw_data_age, raw_data_region = clean_data(
    "./data/COVID-19-total-announced-deaths.xlsx")

print("Adding statistics to region and age data...")
raw_data_region = add_statistics(raw_data_region)
raw_data_age = add_statistics(raw_data_age)

print("Matching NHS Trusts' locations...")
data_trusts_complete = append_location_data(raw_data_trusts, "./data/locations.csv",)

tab1 = map_tab(data_trusts_complete, "AIzaSyB45-xIjLn0P8TrvAWX7Tn1riFhNQOPX_k")
tab2 = line_tab(raw_data_age, "Age")
tab3 = line_tab(raw_data_region, "Region")

tabs = Tabs(tabs=[tab1, tab2, tab3])

curdoc().add_root(tabs)
