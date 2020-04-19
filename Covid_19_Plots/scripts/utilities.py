def get_NHS_addresses(etr_file, google_api_key, filepath):
	import pandas as pd

	data_trusts_additional = pd.read_csv(etr_file, header=None)

	columns = 'Organisation Code, Name, National_Grouping, High_Level_Health_Geography, Address_Line_1, Address_Line_2, \
Address_Line_3, Address_Line_4, Address_Line_5, Postcode, Open_Date, Close_Date, Null, Null, Null, Null, Null, Telephone, \
Null, null, Null, Amended_Record_Indicator, Null, GOR_Code, Null, Null, Null'.split(", ")

	data_trusts_additional.columns = columns
	data_trusts_additional.dropna(axis=1, inplace=True)

	data_trusts_additional['address'] = data_trusts_additional.apply(lambda x: address_constructor(x),
	                                                                 axis=1)
	print("Querying Google for all address in " + etr_file)
	data_trusts_additional = data_trusts_additional.apply(lambda x: google_address_from_address(
		x, google_api_key), axis=1)


	print("Saving to results to " + filepath)
	data_trusts_additional.to_csv(filepath)



def address_constructor(datapoint):
	address = ""
	address_array = datapoint[['Address_Line_1',
	                           'Address_Line_4',
	                           'Address_Line_5',
	                           'Postcode']]

	for index, i in enumerate(address_array):
		if (index == len(address_array)-1) and (type(i) == str):
			address += i + ", NHS"
		elif type(i) == str:
			address += i + ", "

	return address

def google_address_from_address(datapoint, google_api_key):
	from geopy.geocoders import GoogleV3
	from geopy.extra.rate_limiter import RateLimiter

	geolocator = GoogleV3(api_key=google_api_key, domain="maps.google.co.uk")
	geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)
	location = geocode(datapoint['address'])

	if (location.latitude != None):
		datapoint['latitude'] = location.latitude
	if (location.longitude != None):
		datapoint['longitude'] = location.longitude
	if (location.address != None):
		datapoint['address'] = location.address

	return datapoint

def get_last_updated(filepath):
	import time
	import os
	modTimeSinceEpoch = os.path.getmtime(filepath)
	modTime = time.strftime("%d %B %y at %H:%M:%S", time.localtime(modTimeSinceEpoch))

	return modTime