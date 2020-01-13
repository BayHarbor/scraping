import requests
from bs4 import BeautifulSoup
import tweepy as tw
import config
from datetime import datetime
import random
import string
import os


def send_tweet(content, image_url):
    # Authenticate
    auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Get the image
    request = requests.get(image_url, stream=True)
    filename = ''.join(random.choice(string.ascii_lowercase) for i in range(8)) + ".jpg"  # Generate a random file name
    if request.status_code == 200:  # If we successfully get the image
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=content)  # Post the tweet and image
        os.remove(filename)  # Delete the image after tweeting.
    else:  # If we don't get the image
        api.update_status(content)  # Tweet without the image


def data_collection(category, url):
    result = ""
    the_image_url = ""

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

        cheapest_product.find_all('a')
        for link in cheapest_product.find_all('a'):
            if link.get('href'):
                # print(link)
                image_div = link.find('div', {'class': 'mod-product-img'})
                if (image_div and image_div.find('img')):
                    asdf = image_div.find('img')
                    the_image_url = asdf.get('src').split('&width')

                product_uri = link.get('href')

        result = "Cheapest " + category + ": " + title + "\r\n" + qty_one + "\r\n" + qty_two + "\r\nhttps://www.apmex.com" + product_uri + "\r\nAutomated at: " + datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    return result, the_image_url[0]


urls = {"Apmex Silver Bar": "https://www.apmex.com/category/25457/1-oz-apmex-silver-bars?sortby=priceasc",
        "Apmex Silver Round": "https://www.apmex.com/category/25057/1-oz-apmex-silver-rounds?sortby=priceasc&f_bulliontype=round&page=1",
        "Apmex Gold": "https://www.apmex.com/category/19110/apmex-gold-bars-rounds?sortby=priceasc&f_bulliontype=bar%2cround&page=1&f_productoz=1+oz",
        "Best Seller": "https://www.apmex.com/category/10002/gold-silver-platinum-palladium-top-picks?sortby=priceasc&f_metalname=silver%2cgold&page=1&f_bulliontype=bar%2cround"}

for category, url in urls.items():
    tweet, image_url = data_collection(category, url)
    send_tweet(tweet, image_url)
