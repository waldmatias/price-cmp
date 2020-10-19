from urllib.request import urlopen
from bs4 import BeautifulSoup
from decimal import Decimal as D
from db import get_db


def log(e):
    """
        logging
    """
    pass

def open_url(url):
    """
        open url strategy, also handles redirects automatically
    """
    return BeautifulSoup(urlopen(url),'html.parser')

def fetch_product_wwwpage(source, product_key, store_key):
    try:
        product = source['products'][product_key]
        pid = product['supplier_id']
        base_url = source['base_url']
        return open_url(base_url.format(pid, store_key))
    except KeyError as e:
        log(e)


def fetch_product_pricing(product_key):
    info = []

    db = get_db()

    sites = [
        ('gama', None),
        ('plazas','1013'),
        ('cm','distrito-capital-06'),
        ('farmatodo', None)
    ]

    for site, store in sites:
        src = db[site]
        wwwpage = fetch_product_wwwpage(src, product_key, store)

        if(wwwpage):    
            info.append([
                src['name'], src['desc-parser'](wwwpage), src['price-parser'](wwwpage)
            ])

    return info


def print_view(price_list):
    for source, product, price in price_list:
        print(f'{source.upper():>20} : {product.lower():<50} : Bs. {price:<10,.2f}')


def print_cheapest_view(price_list):
    # item[2] is price
    source, _, price = min(price_list, key=lambda item: item[2])
    # build comparison line, sort, min to max
    # min < n1 < n2 < ... < max
    print('-' * 20)
    print(f'cheapest price at: {source.upper()}, Bs. {price:,.2f}')


if __name__ == '__main__':
    product_list = [
        'nevada-5l',
        'arroz-mary-tradicional-kg',
        'crustissimo-650gr',
    ]

    for product_key in product_list:
        print(f'Fetching prices for {product_key} ...')
        price_list = fetch_product_pricing(product_key)
        print_view(price_list)
        print_cheapest_view(price_list)