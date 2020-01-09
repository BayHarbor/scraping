import requests
from bs4 import BeautifulSoup
import tweepy as tw
import config
from datetime import datetime


def sendTweet(content):
    # Authenticate
    auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Post the tweet
    api.update_status(content)


def dataCollection(url):
    # Results
    result = ""

    # Get the data
    data = requests.get(url)

    # Load data into bs4
    soup = BeautifulSoup(data.text, 'html.parser')

    # Find the items returned from the search and iterate over them
    cheapest_product = soup.find_all('div', {'class': 'mod-product-card'})[0]

    # Find the div with the title
    product = cheapest_product.find('div', {'class': 'mod-product-title'})
    title = product.find('span')

    # Find the div with the pricing
    pricing_div = cheapest_product.find('div', {'class': 'product_item_details_container'})

    # Not all products returned have prices listed.
    if pricing_div:
        title = title.text.strip()
        prices = pricing_div.find('tbody')

        trs = prices.find_all('tr')

        tds = trs[0].find_all('td')
        qty_one = " (" + tds[0].text.replace(" ", "") + ") " + tds[1].text.replace(" ", "")

        tds = trs[1].find_all('td')
        qty_two = " (" + tds[0].text.replace(" ", "") + ") " + tds[1].text.replace(" ", "")

        result = title + "\r\n" + qty_one + "\r\n" + qty_two + "\r\nAutomated at: " + datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    return result


urls = ["https://www.apmex.com/category/25457/1-oz-apmex-silver-bars?sortby=priceasc",
        "https://www.apmex.com/category/25057/1-oz-apmex-silver-rounds?sortby=priceasc&f_bulliontype=round&page=1",
        "https://www.apmex.com/category/19110/apmex-gold-bars-rounds?sortby=priceasc&f_bulliontype=bar%2cround&page=1&f_productoz=1+oz"]

for url in urls:
    tweet = dataCollection(url)
    sendTweet(tweet)