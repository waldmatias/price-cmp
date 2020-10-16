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


def fetch_products():
    info = []
    # gama
    pid = '10000746'
    url = f'https://compraenlinea.excelsiorgama.com/p/{pid}'
    #'https://compraenlinea.excelsiorgama.com/BEBIDAS/Aguas-y-Gaseosas/Aguas/AGUA-MINERAL-NEVADA-5-LT/p/10000746'
    s = open_url(url)
    info.append([
        'gama', 
        s.find('div', {'class':'name'}).text, 
        convert_price('Bs', s.find('div', {'class':'from-price-value'}).text)
    ])

    # plaza
    pid = '10003139'
    suc = '1013' #centro plaza
    url = f'https://www.elplazas.com/Product.php?code={pid}&suc={suc}'
    s = open_url(url)
    info.append([
        'plaza', 
        s.find('div', {'class':'ProductName'}).text.strip(), 
        D((s.select('span#productprice.Moneda')[-1].text).replace(',' , ''))  #digit formatting different ,.
    ])

    # cm
    url = 'https://tucentralonline.com/distrito-capital-06/producto/agua-nevada-5lt/'
    s = open_url(url)
    info.append([
        'cm', 
        s.select('h2.product_title')[-1].text.strip(), 
        convert_price('Bs', s.select('p.price bdi')[-1].text)
    ])

    # farmatodo
    pid = '111240637'
    url = f'https://farmatodo.com.ve/producto/{pid}'
    s = open_url(url)
    info.append([
        'farmatodo', 
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