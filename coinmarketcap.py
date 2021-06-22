from requests import Session
import json


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

headers = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY':'your-coinmarkcap-key'
}

session = Session()
session.headers.update(headers)

def set_coin_dict(coin: str):
    coin_dict = {
        'symbol':coin,
        'convert':'USD'
    }
    return coin_dict

def get_data(coin: str):
    coin_dict = set_coin_dict(coin)
    response = session.get(url, params=coin_dict)
    return json.loads(response.text)['data'][coin]['quote']['USD']


def write_data(coin: str):
    with open('data.txt', 'w') as f:
        json.dump(get_data(coin), f)

def get_some_info(coin: str):
    L = ['price','percent_change_24h','percent_change_7d','percent_change_30d','percent_change_90d']
    new_dict = {}
    for key, val in get_data(coin).items():
        if key in L:
            d = {key: val}
            new_dict.update(d)
    return new_dict

def new_dict(coin: str):
    prev_d , d = get_some_info(coin) , {}
    price = prev_d.pop('price')
    d['price'] = format(price, '4f')
    d['change_24h'] = format(price + prev_d['percent_change_24h'] * price / 100, '4f')
    d['change_7d'] = format(price + prev_d['percent_change_7d'] * price / 100, '4f')
    d['change_30d'] = format(price + prev_d['percent_change_30d'] * price / 100, '4f')
    d['change_90d'] = format(price + prev_d['percent_change_90d'] * price / 100, '4f')
    return d

def write_info(coin: str):
    with open('crypto.txt', 'w') as file:
        json.dump(new_dict(coin), file, indent=4)
