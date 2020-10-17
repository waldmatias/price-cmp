from decimal import Decimal as D
from parseutils import convert_price

def get_db_products():
    return {
        'gama': {
            'products': {
                'nevada-5l': {
                    'supplier_id': '10000746'
                },
                'arroz-mary-tradicional-kg': {
                    'supplier_id': '10029311'
                },
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
            },
        },
    }


def get_db():
    return {
        'gama' : {
            'name' : 'Excelsior Gama',
            'base_url' : 'https://compraenlinea.excelsiorgama.com/p/{0}',
            'desc-parser': lambda page: page.find('div', {'class':'name'}).text.strip(),
            'price-parser': lambda page: convert_price('Bs', page.find('div', {'class':'from-price-value'}).text),
            'products' : get_db_products()['gama']['products'],
        },
        'plazas' : {
            'name' : 'El Plazas',
            'base_url' : 'https://www.elplazas.com/Product.php?code={0}&suc={1}',
            'desc-parser': lambda page: page.find('div', {'class':'ProductName'}).text.strip(),
            'price-parser': lambda page: D((page.select('span#productprice.Moneda')[-1].text).replace(',' , '')),  # digit formatting different ,.,
            'products' : get_db_products()['plazas']['products'],
        },
        'cm' : {
            'name' : 'Central Madeirense',
            'base_url' : 'https://tucentralonline.com/{1}/producto/{0}/', # non-numeric, alpha-key
            'desc-parser': lambda page: page.select('h2.product_title')[-1].text.strip(),
            'price-parser': lambda page: convert_price('Bs', page.select('p.price bdi')[-1].text),
            'products' : get_db_products()['cm']['products'],
        },
        'farmatodo' : {
            'name' : 'Farmatodo',
            'base_url' : 'https://farmatodo.com.ve/producto/{0}',
            'desc-parser': lambda page: page.find('p', {'class':'description'}).text.strip(), 
            'price-parser': lambda page: convert_price('Bs.', page.find('p', {'class':'p-blue'}).text.strip()),
            'products' : get_db_products()['farmatodo']['products'],
        },
    }