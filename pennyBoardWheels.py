import requests
from bs4 import BeautifulSoup


def scan_the_site():
    # A list to hold anything that's found to be in stock
    in_stock = []

    # Get the sites source code
    data = requests.get("https://www.pennyskateboards.com/collections/wheels")

    # Parse the data with BeautifulSoup
    soup = BeautifulSoup(data.text, 'html.parser')

    # Find the div with the products for sale
    product_div = soup.find_all('div', {'class': 'grid-product__content'})

    for div in product_div:
        sold_out = div.find('div', {'class': 'grid-product_tags-soldout'})
        the_img = div.find('img', {'class': 'grid-product__image'})

        if not sold_out:
            print(the_img['alt'] + ": IN STOCK.")
            in_stock.append(the_img['alt'])

    return in_stock
