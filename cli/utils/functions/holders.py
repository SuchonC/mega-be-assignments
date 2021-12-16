import requests
import click
from utils.common import ETHER_SCAN_URL
from utils.functions.detail import get_contract_detail
from bs4 import BeautifulSoup as bs


def get_holders(n, contract_address):
    # scraping from etherscan's holder chart
    if not 1 <= n <= 100:
        click.echo('N must be between 1 and 100 (inclusive)')
        exit()

    details = get_contract_detail(contract_address)
    data = requests.get(f'{ETHER_SCAN_URL}/token/tokenholderchart/{contract_address}',
                        headers={
                            'User-Agent': 'Firefox'  # to bypass Captcha
                        },
                        params={
                            'range': n
                        }).text

    def save_to_file(data, filename='top_n_holders.txt'):
        with open(filename, 'a') as file:
            for d in data:
                file.write(f'\
{d["rank"]}. Holder address : {d["holder_address"]}\n\
{" "*(len(d["rank"])+2)}Balance        : {d["balance"]} {d["symbol"]}\n\n')  # formatted this way for better readability in the output file

    soup = bs(data, 'html.parser')
    rows = soup.find_all('tr')
    data = []
    for row in rows[1:]:  # 0th row is the header
        tds = row.find_all('td')
        holder_address_start_idx = tds[1].a['href'].find('?a=') + 3
        data.append({
            'rank': tds[0].string,
            'holder_address': tds[1].a['href'][holder_address_start_idx:],
            'balance': tds[2].string,
            'symbol': details['symbol']
        })
    save_to_file(data, filename=f'top_{n}_holders_of_{details["name"]}.txt')
