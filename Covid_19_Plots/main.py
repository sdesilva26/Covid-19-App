from scripts.data_acquisition import get_todays_data
from scripts.preprocessing import clean_data, append_location_data, add_statistics
from scripts.map_plot import map_tab
from scripts.line_plot import line_tab
import os
# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

print("Cleaning the data...")
raw_data_trusts, raw_data_age, raw_data_region = clean_data(
    "./Covid_19_Plots/data/COVID-19-total-announced-deaths.xlsx")

print("Adding statistics to region and age data...")
raw_data_region = add_statistics(raw_data_region)
raw_data_age = add_statistics(raw_data_age)

print("Matching NHS Trusts' locations...")
data_trusts_complete = append_location_data(raw_data_trusts, "./Covid_19_Plots/data/locations.csv",)

tab1 = map_tab(data_trusts_complete, os.getenv('GOOGLE_API_KEY'), "./Covid_19_Plots/data/COVID-19-total-announced-deaths.xlsx")
tab2 = line_tab(raw_data_age, "Age", "./Covid_19_Plots/data/COVID-19-total-announced-deaths.xlsx")
tab3 = line_tab(raw_data_region, "Region", "./Covid_19_Plots/data/COVID-19-total-announced-deaths.xlsx")

tabs = Tabs(tabs=[tab1, tab2, tab3])

curdoc().add_root(tabs)
