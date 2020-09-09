import requests
from bs4 import BeautifulSoup

# Get the data
data = requests.get("https://www.apmex.com/category/25457/1-oz-apmex-silver-bars?sortby=priceasc")

# Load data into bs4
soup = BeautifulSoup(data.text, 'html.parser')

# Find the items returned from the search and iterate over them
for thing in soup.find_all('div', {'class': 'mod-product-card'}):
    # Find the div with the title
    product = thing.find('div', {'class': 'mod-product-title'})
    title = product.find('span')

    # Find the div with the pricing
    pricingDiv = thing.find('div', {'class': 'product_item_details_container'})

    # Not all products returned have prices listed.
    if pricingDiv:
        print(title.text.strip())
        prices = pricingDiv.find('tbody')

        for tr in prices.find_all('tr'):
            tds = tr.find_all('td')
            print(tds[0].text.replace(" ", "") + ": " + tds[1].text.replace(" ", ""))

        print(" ")

