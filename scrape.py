import requests
from bs4 import BeautifulSoup

#Get the data
data = requests.get("https://www.apmex.com/product/27086/1-oz-silver-bar-apmex")

# load data into bs4
soup = BeautifulSoup(data.text, 'html.parser')

# Find the pricing table
volumeTable = soup.find('table', {'class': 'product-volume-pricing'})

# Find the TR for buying 20 to 99 units
twentyTo99Pricing = volumeTable.find('tr', {'data-range': '99'})

# Find the TDs under the TR
tableData = twentyTo99Pricing.find_all('td')

# Print it out
print("Volume: ", tableData[0].text)
print("Check/Wire: ", tableData[1].text)
print("BTC/BCH: ", tableData[2].text)
print("CC/PayPal: ", tableData[3].text)
