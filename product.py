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
                'nevada-5l': {'supplier_id': '10000746'},
            },
        },
        'plazas' : {
            'name' : 'El Plazas',
            'base_url' : 'https://www.elplazas.com/Product.php?code={0}&suc={1}',
            'products' : {
                'nevada-5l': {
                    'supplier_id': '10003139', 
                    'store_id' : '1013'
                }
            }
        },
        'cm' : {
            'name' : 'Central Madeirense',
            'base_url' : 'https://tucentralonline.com/{1}/producto/{0}/', #non-numeric, alpha-key
            'products' : {
                'nevada-5l': {
                    'supplier_id': 'agua-nevada-5lt', 
                    'store_id' : 'distrito-capital-06'
                }
            }
        },
        'farmatodo' : {
            'name' : 'Farmatodo',
            'base_url' : 'https://farmatodo.com.ve/producto/{0}',
            'products' : { 
                'nevada-5l': {
                    'supplier_id': '111240637'
                }, 
            }
        },
    }


def get_db_product(source_name, key):
    source = get_db().get(source_name)
    product = source.get('products').get(key)
    return product


def fetch_product_by_key(db, source_name, key):
    product = get_db_product(source_name, key)
    pid = product.get('supplier_id')
    base_url = db.get(source_name).get('base_url')
    return open_url(base_url.format(pid))
    

def fetch_product_by_store(db, source_name, store_id, key):
    product = get_db_product(source_name, key)
    pid = product.get('supplier_id')
    base_url = db.get(source_name).get('base_url')
    return open_url(base_url.format(pid, store_id))


def fetch_products():
    info = []

    db = get_db()
    product_key = 'nevada-5l'

    # gama
    src = 'gama'
    # source, description, price = fetch_product(db, src, 'nevada-5l')
    # info.append([source, desription, price])
    s = fetch_product_by_key(db, src, product_key)
    info.append([
        src, 
        s.find('div', {'class':'name'}).text.strip(), 
        convert_price('Bs', s.find('div', {'class':'from-price-value'}).text)
    ])

    # plaza
    src = 'plazas'
    suc = '1013' #centro plaza
    s = fetch_product_by_store(db, src, suc, product_key)
    # s = open_url(db['plazas']['base_url'].format(pid, suc))
    info.append([
        src,
        s.find('div', {'class':'ProductName'}).text.strip(), 
        D((s.select('span#productprice.Moneda')[-1].text).replace(',' , ''))  #digit formatting different ,.
    ])

    # cm
    src = 'cm'
    suc = 'distrito-capital-06'
    s = fetch_product_by_store(db, src, suc, product_key)
    info.append([
        src, 
        s.select('h2.product_title')[-1].text.strip(), 
        convert_price('Bs', s.select('p.price bdi')[-1].text)
    ])

    # farmatodo
    src = 'farmatodo'
    s = fetch_product_by_key(db, src, product_key)
    info.append([
        src, 
        s.find('p', {'class':'description'}).text.strip(), 
        convert_price('Bs.', s.find('p', {'class':'p-blue'}).text.strip())
    ])

    return info

if __name__ == '__main__':
    print(f'Fetching prices ...')
    product_list = fetch_products()
    for source, product, price in product_list:
        print(f'{source.upper():>10} : {product:<40} : Bs. {price:<10,.2f}')
    
    # item[2] is price
    source, _, price = min(product_list, key=lambda item: item[2])
    print('-' * 10)
    print(f'cheapest price is at: {source.upper()} and its price is: Bs. {price:,.2f}')