from decimal import Decimal as D


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