import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()


def shorten_link(token, url):
    headers = {'Authorization': token}
    payload = {'long_url': url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json().get('id')
    return bitlink


def count_clicks(token, link):
    headers = {'Authorization': token}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary', headers=headers)
    response.raise_for_status()
    total_clicks = response.json().get('total_clicks')
    return total_clicks


def main():
    BITLY_TOKEN = os.getenv("BITLY_TOKEN")
    headers = {'Authorization': BITLY_TOKEN}
    parser = argparse.ArgumentParser(
        description='Input link')
    parser.add_argument('link', help='bitly link')
    args = parser.parse_args()
    user_url = args.link
    link_without_https = f'{urlparse(user_url).netloc}{urlparse(user_url).path}'
    if requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link_without_https}/clicks/summary', headers=headers).ok:
        try:
            clicks_count = count_clicks(BITLY_TOKEN, link_without_https)
            print(f'Всего переходов по ссылке - {clicks_count}')
        except requests.exceptions.HTTPError:
            print('Произошла ошибка. Вы ввели неверную ссылку.')
    else:
        try:
            bitlink = shorten_link(BITLY_TOKEN, user_url)
            print(f'Битлинк - {bitlink}')
        except requests.exceptions.HTTPError:
            print('Произошла ошибка. Вы ввели неверную ссылку.')


if __name__ == '__main__':
    main()