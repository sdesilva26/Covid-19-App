def clean_data(filepath):
	import pandas as pd
	raw_data_trusts = pd.read_excel(filepath, sheet_name=0, header=15)
	raw_data_region = pd.read_excel(filepath, sheet_name=1, header=15)
	raw_data_age = pd.read_excel(filepath, sheet_name=2, header=15)

	# Remove NaN values from datasets
	for dataset in [raw_data_region, raw_data_age, raw_data_trusts]:
		for col in dataset.columns:
			if (type(col) == str) and ("Unnamed" in col):
				dataset.drop(col, axis=1, inplace=True, errors='ignore')
		dataset.dropna(inplace=True)
		dataset.drop(index=0, inplace=True, errors='ignore')
		dataset.drop('Awaiting verification', inplace=True, axis=1, errors='ignore')

	# Drop columns that are not datetime format
	raw_data_trusts.drop(['Up to 01-Mar-20'], axis=1, inplace=True, errors='ignore')
	raw_data_region.drop(['Up to 01-Mar-20', 'Total'], axis=1, inplace=True, errors='ignore')
	raw_data_age.drop(['Up to 01-Mar-20', 'Total'], axis=1, inplace=True, errors='ignore')

	# Switch the index to use the dates for the age dataset
	df = raw_data_age.transpose()[1:]
	df.columns = raw_data_age['Age group'].unique()
	raw_data_age = df

	# Switch the index to use the dates for the region dataset
	df = raw_data_region.transpose()[1:]
	df.columns = raw_data_region['NHS England Region'].unique()
	raw_data_region = df

	return raw_data_trusts, raw_data_age, raw_data_region


def append_location_data(data_trusts, filepath, google_api_key):
	# filepath is path to the etr.csv file downloaded from
	# https://data.england.nhs.uk/dataset/ods-nhs-trusts-and-sites

	import pandas as pd
	from geopy.geocoders import GoogleV3
	from geopy.extra.rate_limiter import RateLimiter

	data_trusts_additional = pd.read_csv(filepath, header=None)

	columns = 'Organisation Code, Name, National_Grouping, High_Level_Health_Geography, Address_Line_1, Address_Line_2, \
Address_Line_3, Address_Line_4, Address_Line_5, Postcode, Open_Date, Close_Date, Null, Null, Null, Null, Null, Telephone, \
Null, null, Null, Amended_Record_Indicator, Null, GOR_Code, Null, Null, Null'.split(", ")

	data_trusts_additional.columns = columns
	data_trusts_additional.dropna(axis=1, inplace=True)

	# I added in here NHS because that seems to help the Google Maps API find the correct address later
	def address_constructor(datapoint):
		address = ""
		address_array = datapoint[['Address_Line_1',
		                           'Address_Line_4',
		                           'Address_Line_5',
		                           'Postcode']]

		for index, i in enumerate(address_array):
			if (index == len(address_array) - 1) and (type(i) == str):
				address += i + ", NHS"
			elif type(i) == str:
				address += i + ", "

		return address

	data_trusts_additional['address'] = data_trusts_additional.apply(lambda x:
	                                                                 address_constructor(x), axis=1)

	def google_address_from_address(datapoint):


		geolocator = GoogleV3(api_key=google_api_key,
		                      domain="maps.google.co.uk")
		geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)
		location = geocode(datapoint['address'])

		if location.latitude != None:
			datapoint['latitude'] = location.latitude
		if location.longitude != None:
			datapoint['longitude'] = location.longitude
		if location.address != None:
			datapoint['address'] = location.address

		return datapoint

	print("Getting longitude and latitude for trusts...")
	data_trusts_additional = data_trusts_additional.apply(google_address_from_address, axis=1)
	print("Finished getting longitude and latitude data for trusts")

	data_trusts_additional.rename(columns={'Organisation Code': 'Code'}, inplace=True)

	def append_lat_long(datapoint):
		matched_data = data_trusts_additional[data_trusts_additional['Code'] == datapoint['Code']]
		if (matched_data['latitude'].empty == False):
			datapoint['latitude'] = matched_data['latitude'].values[0]
		else:
			datapoint['latitude'] = None
		if (matched_data['longitude'].empty == False):
			datapoint['longitude'] = matched_data['longitude'].values[0]
		else:
			datapoint['longitude'] = None
		return datapoint

	data_trusts_complete = data_trusts.apply(append_lat_long, axis=1)
	data_trusts_complete.dropna(axis=0, inplace=True)

	return data_trusts_complete

def add_cumul_change_relchange(dataframe):
	import pandas as pd

	array = [dataframe.columns.values,
	         ['deaths today', 'cumulative total', 'change', 'relative change']]

	index = pd.MultiIndex.from_product(array, names=['Age group', 'Death data'])

	df_restructure = pd.DataFrame(index = dataframe.index, columns=index)

	for col in dataframe.columns:
		df_restructure.loc[:, (col, 'deaths today')] = dataframe[col]
		df_restructure.loc[:, (col, 'change')] = dataframe[col].diff()
		df_restructure.loc[:, (col, 'relative change')] = dataframe[col].pct_change()*100
		df_restructure.loc[:, (col, 'cumulative total')] = dataframe[col].values.cumsum()

	return df_restructure




