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

