from decimal import Decimal as D
from parseutils import convert_price
import json

def db_products():
    # get these from a json file
    return {
        'gama': {
            'products': {
                'nevada-5l': { 
                    'supplier_id': '10000746'
                },
                'arroz-mary-tradicional-kg': {
                    'supplier_id': '10029311'
                },
                'crustissimo-650gr': {
                    'supplier_id': '10029867'
                }
            }
        },
        'plazas' : {
            'products' : {
                'nevada-5l': {
                    'supplier_id': '10003139', 
                    'store_id' : '1013'
                },
                'arroz-mary-tradicional-kg': {
                    'supplier_id': '16001524', 
                    'store_id' : '1013'
                },
                'crustissimo-650gr': {
                    'supplier_id': '10013034', 
                    'store_id' : '1013'
                }
            },  
        },
        'cm' : {
            'products' : {
                'nevada-5l': {
                    'supplier_id': 'agua-nevada-5lt', 
                    'store_id' : 'distrito-capital-06'
                },
                'arroz-mary-tradicional-kg': {
                    'supplier_id': 'arroz-mary-tipo1tradicional-1kg', 
                    'store_id' : 'distrito-capital-06'
                },
                'crustissimo-650gr': {
                    'supplier_id': 'pan-crustissimo-sandwich-blanco-650gr', 
                    'store_id' : 'distrito-capital-06'
                }
            },    
        },
        'farmatodo' : {
            'products' : { 
                'nevada-5l': {
                    'supplier_id': '111240637'
                },
                'arroz-mary-tradicional-kg': {
                    'supplier_id': '112084350', 
                },
                'crustissimo-650gr': {
                    'supplier_id': '111964031', 
                }
            },
        },
    }


def db_sources():
    return {
        'gama' : {
            'name' : 'Excelsior Gama',
            'base_url' : 'https://compraenlinea.excelsiorgama.com/p/{0}',
            'desc-parser': lambda page: page.find('div', {'class':'name'}).text.strip(),
            'price-parser': lambda page: convert_price('Bs', page.find('div', {'class':'from-price-value'}).text),
        },
        'plazas' : {
            'name' : 'El Plazas',
            'base_url' : 'https://www.elplazas.com/Product.php?code={0}&suc={1}',
            'desc-parser': lambda page: page.find('div', {'class':'ProductName'}).text.strip(),
            'price-parser': lambda page: D((page.select('span#productprice.Moneda')[-1].text).replace(',' , '')),  # digit formatting different ,.,
        },
        'cm' : {
            'name' : 'Central Madeirense',
            'base_url' : 'https://tucentralonline.com/{1}/producto/{0}/', # non-numeric, alpha-key
            'desc-parser': lambda page: page.select('h2.product_title')[-1].text.strip(),
            'price-parser': lambda page: convert_price('Bs', page.select('p.price bdi')[-1].text),
        },
        'farmatodo' : {
            'name' : 'Farmatodo',
            'base_url' : 'https://farmatodo.com.ve/producto/{0}',
            'desc-parser': lambda page: page.find('p', {'class':'description'}).text.strip(), 
            'price-parser': lambda page: convert_price('Bs.', page.find('p', {'class':'p-blue'}).text.strip()),
        },
    }

def get_db():
    # data sets
    sources = db_sources()
    products = db_products()

    for source in sources:
        sources[source].update(products[source])

    return sources