# this script is running every morning at 945am through a cronjob
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

# scraping from profish
url = 'https://profish.com/order?source=category&category=Fish+Fresh'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# dd/mm/YY take today's date

today = date.today()
d1 = today.strftime("%d/%m/%Y")

fish = soup.find_all('div', class_='label_container')
prices = soup.find_all('h4')

# structure into a pandas dataframe
names = [i.h3.text for i in fish]
price_items = [float(i.text.split()[0].strip('$')) for i in prices]

profish_data_today = pd.DataFrame.from_dict(zip(names, price_items))

profish_data_today.columns = ['name', 'price']

profish_data_today['date'] = d1

# do not uncomment, except when being run the first time to create a file
# profish_data_today.to_csv("prices_daily.csv")


# adds to existing dataset
profish_adding = pd.read_csv('prices_daily.csv', index_col=0)
profish_adding = profish_adding.append(profish_data_today, ignore_index=True)
profish_adding.to_csv("prices_daily.csv")
