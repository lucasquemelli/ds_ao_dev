#### Libraries
import pandas as pd
import numpy as np
import requests
import re
import math
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine

#### Data Collection (products)

# URL
url01 = "https://www2.hm.com/en_us/men/products/jeans.html?sort=stock&image-size=small&image=model&offset=0&page-size=72"

# Parameters
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Request to URL
page = requests.get(url01, headers=headers)

# Beautiful Soup object
soup = BeautifulSoup(page.text, 'html.parser')

# ========================= Product Data ====================== #

# List which contains all products
products = soup.find('ul', 'products-listing small')
  
# product_id_categort list
product_id_category = products.find_all('article', 'hm-product-item')

# product_name list
product_name = products.find_all('a', 'link')

# product_price list
product_price = products.find_all('span', 'price regular')

product_id = [p.get('data-articlecode') for p in product_id_category]
product_category = [p.get('data-category') for p in product_id_category]
product_name = [p.get_text() for p in product_name]
product_price = [p.get_text() for p in product_price]

data = pd.DataFrame([product_id, product_name, product_category, product_price]).T
data.columns = ['product_id', 'product_name', 'product_type', 'price']

data['scrape_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')