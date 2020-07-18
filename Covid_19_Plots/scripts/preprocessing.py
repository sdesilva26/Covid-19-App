

def clean_data(filepath):
	import pandas as pd
	import datetime
	import numpy as np
	raw_data_trusts = pd.read_excel(filepath, sheet_name="Tab4 Deaths by trust", header=15)
	raw_data_region = pd.read_excel(filepath, sheet_name="Tab1 Deaths by region", header=15)
	raw_data_age = pd.read_excel(filepath, sheet_name="Tab3 Deaths by age", header=15)

	# Remove empty columns values from datasets
	for dataset in [raw_data_region, raw_data_age, raw_data_trusts]:
		for col in dataset.columns:
			if (type(col) == str) and ("Unnamed" in col):
				dataset.drop(col, axis=1, inplace=True, errors='ignore')
		dataset.dropna(inplace=True)
		dataset.drop(index=0, inplace=True, errors='ignore')
		dataset.drop('Awaiting verification', inplace=True, axis=1, errors='ignore')

	# Drop columns that are not needed
	raw_data_trusts.drop(['Up to 01-Mar-20'], axis=1, inplace=True, errors='ignore')
	raw_data_region.drop(['Up to 01-Mar-20', 'Total'], axis=1, inplace=True, errors='ignore')
	raw_data_age.drop(['Up to 01-Mar-20', 'Total'], axis=1, inplace=True, errors='ignore')

	# Switch the index to use the dates for the age dataset
	df = raw_data_age.transpose()[1:]
	df.columns = raw_data_age['Age group (years)'].unique()
	raw_data_age = df

	# Switch the index to use the dates for the region dataset
	df = raw_data_region.transpose()[1:]
	df.columns = raw_data_region['NHS England Region'].unique()
	raw_data_region = df

	# For both regional and age datasets add an "All" group
	for df in [raw_data_age, raw_data_region]:
		new_df = pd.DataFrame(df.apply(lambda x: np.sum(x), axis=1), columns=['All'])
		df.insert(loc=0, value=new_df, column='All')

	#raw_data_region['All'] = raw_data_region.apply(lambda x: np.sum(x), axis=1)
	#raw_data_age['All'] = raw_data_age.apply(lambda x: np.sum(x), axis=1)

	# drop the time from datetime columns in trusts dataset
	df = raw_data_trusts
	new_index = []
	for index in df.columns.values:
		if type(index) == datetime.datetime:
			new_index.append(index.date().strftime("%d %B %y"))
		else:
			new_index.append(index)
	df.columns = new_index
	raw_data_trusts = df

	return raw_data_trusts, raw_data_age, raw_data_region


def append_location_data(data_trusts, filepath):
	# filepath is path to the locations.csv file
	import pandas as pd

	data_trusts_additional = pd.read_csv(filepath)

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

def add_statistics(dataframe):
	import pandas as pd
	import numpy as np

	array = [dataframe.columns.values,
	         ['Deaths', 'Cumulative Total', 'Change', 'Relative Change']]

	index = pd.MultiIndex.from_product(array, names=['Age group', 'Death data'])

	df_restructure = pd.DataFrame(index = dataframe.index, columns=index)

	for col in dataframe.columns:
		df_restructure.loc[:, (col, 'Deaths')] = dataframe[col]
		df_restructure.loc[:, (col, 'Change')] = dataframe[col].diff()
		df_restructure.loc[:, (col, 'Relative Change')] = dataframe[col].pct_change()*100
		df_restructure.loc[:, (col, 'Cumulative Total')] = dataframe[col].values.cumsum()

	df_restructure.replace(to_replace=np.Inf, value=np.NaN, inplace=True)

	return df_restructure





