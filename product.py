from urllib.request import urlopen
from bs4 import BeautifulSoup
from decimal import Decimal as D

def open_url(url):
    """
        open url strategy, also handles redirects automatically
    """
    return BeautifulSoup(urlopen(url),'html.parser')


def parse_rate(text):
    if type(text) is float:
        return D(text).quantize(D('1.00'))

    try:
        # leave only the last 2 digits after the last .
        text = text.replace('.' , '').replace(',','.') #
        return D(text)
    except Exception as e:
        print(f'{e}')


def string_rateparser(start_prefix, string):
    start_pos = string.index(start_prefix) + len(start_prefix)
    return string[start_pos:].strip()


def convert_price(prefix, text):
    return parse_rate(string_rateparser(prefix, text))


def get_db():
    return {
        'gama' : {
            'name' : 'Excelsior Gama',
            'base_url' : 'https://compraenlinea.excelsiorgama.com/p/{0}',
            'products' : {
                'nevada-5l': {
                    'supplier_id': '10000746'
                },
            },
            'desc-parser': lambda page: page.find('div', {'class':'name'}).text.strip(),
            'price-parser': lambda page: convert_price('Bs', page.find('div', {'class':'from-price-value'}).text),
        },
        'plazas' : {
            'name' : 'El Plazas',
            'base_url' : 'https://www.elplazas.com/Product.php?code={0}&suc={1}',
            'products' : {
                'nevada-5l': {
                    'supplier_id': '10003139', 
                    'store_id' : '1013'
                }
            },
            'desc-parser': lambda page: page.find('div', {'class':'ProductName'}).text.strip(),
            'price-parser': lambda page: D((page.select('span#productprice.Moneda')[-1].text).replace(',' , '')),  #digit formatting different ,.,
        },
        'cm' : {
            'name' : 'Central Madeirense',
            'base_url' : 'https://tucentralonline.com/{1}/producto/{0}/', #non-numeric, alpha-key
            'products' : {
                'nevada-5l': {
                    'supplier_id': 'agua-nevada-5lt', 
                    'store_id' : 'distrito-capital-06'
                }
            },
            'desc-parser': lambda page: page.select('h2.product_title')[-1].text.strip(),
            'price-parser': lambda page: convert_price('Bs', page.select('p.price bdi')[-1].text)
        },
        'farmatodo' : {
            'name' : 'Farmatodo',
            'base_url' : 'https://farmatodo.com.ve/producto/{0}',
            'products' : { 
                'nevada-5l': {
                    'supplier_id': '111240637'
                }, 
            },
            'desc-parser': lambda page: page.find('p', {'class':'description'}).text.strip(), 
            'price-parser': lambda page: convert_price('Bs.', page.find('p', {'class':'p-blue'}).text.strip())
        },
    }


def fetch_product(source, product_key, store_key):
    product = source['products'][product_key]
    pid = product['supplier_id']
    base_url = source['base_url']
    return open_url(base_url.format(pid, store_key))


def fetch_products(product_key):
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
        wwwpage = fetch_product(src, product_key, store)
        info.append([
            src['name'], src['desc-parser'](wwwpage), src['price-parser'](wwwpage)
        ])

    return info


def print_view(product_list):
    for source, product, price in product_list:
        print(f'{source.upper():>20} : {product:<40} : Bs. {price:<10,.2f}')
    
    # item[2] is price
    source, _, price = min(product_list, key=lambda item: item[2])
    print('-' * 20)
    print(f'cheapest price at: {source.upper()} and is: Bs. {price:,.2f}')


if __name__ == '__main__':
    product_key = 'nevada-5l'

    print(f'Fetching prices for {product_key} ...')
    products = fetch_products(product_key)
    print_view(products)