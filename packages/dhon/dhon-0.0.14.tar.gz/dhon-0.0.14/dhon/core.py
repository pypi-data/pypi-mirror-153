import xml.dom.minidom
import requests
import os
from datetime import datetime

UPDATE_THRESHOLD = 4

XMLURL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
FILEURL = "eurofxref-daily.xml"

CURRENCY_LIST = ['EUR']

def update_rates():
    try:
        r = requests.get(XMLURL)
    except:
        print("could not update, failed to connect to server")
    else:
        try:
            with open(FILEURL, 'wb') as f:
                f.write(r.content)
            print("rates updated")
        except:
            print("failed to save updates!")

def parse_xml(url):
    rate_dict = {}
    DOMTree = xml.dom.minidom.parse(url)
    collection = DOMTree.documentElement
    currencies = collection.getElementsByTagName("Cube")

    for currency in currencies:
        if currency.hasAttribute("currency") and currency.hasAttribute("rate"):
            currency_name = currency.getAttribute("currency")
            currency_rate_eur = currency.getAttribute("rate")

            rate_dict[currency_name] = float(currency_rate_eur)
            CURRENCY_LIST.append(currency_name)

    return rate_dict

def conv_eur_to_other(curr, rate_dict):
    return rate_dict[curr]

def conv_other_to_eur(curr, rate_dict):
    return 1/rate_dict[curr]

def conv_other_to_other(curr1, curr2, rate_dict):
    return conv_other_to_eur(curr1, rate_dict) * \
        conv_eur_to_other(curr2, rate_dict)

def get_days_since_modified():
    last_mod_epochtime = os.path.getmtime(FILEURL)
    modtime = datetime.fromtimestamp(last_mod_epochtime)
    diff_days = datetime.today() - modtime
    return diff_days

def convert(val, curr_from, curr_to, rate_dict):
    if curr_from == curr_to:
        conv_rate = 1
    elif curr_from == 'EUR':
        conv_rate = conv_eur_to_other(curr_to, rate_dict)
    elif curr_to == 'EUR':
        conv_rate = conv_other_to_eur(curr_from, rate_dict)
    else:
        conv_rate = conv_other_to_other(curr_from, curr_to, rate_dict)

    return val * conv_rate

def pretty_print(in_val, curr_from, out_val, curr_to, decimal_num = 2):
    print(f"{in_val} {curr_from} = {round(out_val, decimal_num)} {curr_to}")

if __name__ == '__main__':
    days_since_mod = get_days_since_modified()
    if (days_since_mod.days > UPDATE_THRESHOLD):
        update_rates()

    rate_dict = parse_xml(FILEURL)
    print(conv_eur_to_other('INR', rate_dict))
    print(conv_other_to_eur('USD', rate_dict))
    print(conv_other_to_other('USD', 'INR', rate_dict))
