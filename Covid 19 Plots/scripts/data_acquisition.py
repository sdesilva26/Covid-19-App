
def get_todays_data(url, filename, today=True):
	import urllib.request
	import requests
	from bs4 import BeautifulSoup
	from datetime import date, timedelta

	response = requests.get(url)

	soup = BeautifulSoup(response.text, "html.parser")

	if(today):
		dateTimeObj = date.today()
	else:
		dateTimeObj = date.today() - timedelta(days=1)

	timestampStr = dateTimeObj.strftime("%d %B %y")

	all_hplinks = soup.find_all('a')
	index = []
	for i, hplink in enumerate(all_hplinks):
		if timestampStr in str(hplink):

			index.append(i)

	print("Downloading data from link: " + str(all_hplinks[index[0]]['href']))
	total_deaths_link = all_hplinks[index[0]]['href']
	urllib.request.urlretrieve(total_deaths_link, filename)
	print('Successfully downloaded data')