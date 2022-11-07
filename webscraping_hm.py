import os
import pandas as pd
import numpy as np
import requests
import re
import math
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine


def data_collection(url01, headers):

    # Request to URL
    page = requests.get(url01, headers=headers)

    # Beautiful Soup object
    soup = BeautifulSoup(page.text, 'html.parser')

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

    return data

def data_collection_product(data, headers):

    #empty dataframe
    df_final = pd.DataFrame()

    # Auxiliar list in order to monitor new columns
    aux = []

    # All columns found on website
    df_pattern = pd.DataFrame(columns= ['Art. No.', 'Composition', 'Fit', 'More sustainable materials', 'Size'])

    for i in range(len(data)):

        #API request
        # conteudo de headers eh padrao
        url02 = "https://www2.hm.com/en_us/productpage." + data.loc[i, 'product_id'] + ".html"
        logger.debug('Product: %s', url02)

        page = requests.get(url02, headers=headers)

        #Beautiful Soup object
        soup = BeautifulSoup(page.text, 'html.parser')

        # ============================= Color =========================

        #product list
        product_list = soup.find_all('a', class_='filter-option miniature active') + soup.find_all('a', class_='filter-option miniature')

        #color
        product_color = [p.get('data-color') for p in product_list] 

        #id
        product_id = [p.get('data-articlecode') for p in product_list]

        #dataframe
        df_color = pd.DataFrame([product_id, product_color]).T
        df_color.columns = ['product_id', 'color']

        for j in range(len(df_color)):
            
            # ============== API request ========================= 
            
            # conteudo de headers eh padrao
            url03 = "https://www2.hm.com/en_us/productpage." + df_color.loc[j, 'product_id'] + ".html"
            logger.debug('Color: %s', url03)

            page = requests.get(url03, headers=headers)

            #Beautiful Soup object
            soup = BeautifulSoup(page.text, 'html.parser')
            
            # ============== Product name ==========================
            
            product_name = soup.find('section', class_ = 'product-name-price').find_all('h1')
            product_name = product_name[0].get_text()
            
            # ============== Product price =========================
            
            product_price = soup.find_all('div', class_ = 'primary-row product-item-price')
            product_price = re.findall(r'\d+\.?\d+', product_price[0].get_text())[0]
            

            # ============================ Composition =====================

            # Product list -- we used find and find_all because we could not return composition list only by using find_all in the beginning
            product_composition_list = soup.find('div', class_='content pdp-text pdp-content').find_all('div')

            # Composition
            product_composition = [list( filter( None, p.get_text().split('\n') ) ) for p in product_composition_list]

            # dataframe
            df_composition = pd.DataFrame(product_composition).T

            # Columns name
            df_composition.columns = df_composition.iloc[0]

            # Filling None/NA values
            df_composition = df_composition.iloc[1:].fillna(method='ffill')

            # Removing pocket lining, shell and lining
            df_composition['Composition'] = df_composition['Composition'].str.replace('Pocket lining: ', '', regex=True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Shell: ', '', regex=True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Lining: ', '', regex=True)

            # The same number of columns (pattern)
            df_composition = pd.concat( [df_pattern, df_composition] )
            
            # Rename columns
            if j == 0:
                df_composition.columns = ['product_id', 'composition', 'fit', 'product_safety', 'size']
                df_color['product_id'] = df_color['product_id'].astype(str)
                df_composition['product_id'] = df_composition['product_id'].astype(str)
                
            else:
                break

            # Keep new columns if it shows up
            aux = aux + df_composition.columns.tolist()

            data_merge = pd.merge(df_composition[['product_id', 'composition', 'fit', 'product_safety', 'size']], df_color, 
                                how='left', on='product_id')
            data_merge.loc[j, 'product_name'] = product_name
            data_merge.loc[j, 'product_price'] = product_price
            
            # ======================= Concatenate ==========================================
            df_final = pd.concat( [df_final, data_merge], axis=0 )
            
            
    # Creating style_id + color_id
    df_final['style_id'] = df_final['product_id'].apply(lambda x: x[:-3])
    df_final['color_id'] = df_final['product_id'].apply(lambda x: x[-3:])

    df_final['scrape_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data_raw = df_final.copy().reset_index().drop(columns='index')

    #data_raw.to_csv("data_raw.csv")

    return data_raw

def data_cleaning(data_raw):

    data = data_raw.dropna(subset=['product_id'])

    data = data.reset_index(drop=True)

    data['product_price'] = data['product_price'].astype(float)

    data['scrape_datetime'] = pd.to_datetime(data['scrape_datetime'], format='%Y-%m-%d %H:%M:%S')

    data['color'] = data['color'].apply(lambda x: x.replace(' ', '_').replace('/', '_').replace('-', '_').lower() )

    data['fit'] = data['fit'].apply(lambda x: x.replace(' ', '_').lower() ) 

    data['product_name'] = data['product_name'].astype(str)
    data['product_name'] = data['product_name'].apply(lambda x: x.replace(' ', '_').replace(':', '').replace('®', '').replace('-', '_').lower() )

    data = data[~data['composition'].str.contains('Pocket lining:')]
    data = data[~data['composition'].str.contains('Lining:')]
    data = data[~data['composition'].str.contains('Shell:')]
    data = data[~data['composition'].str.contains('Pocket:')]

    df1 = data['composition'].str.split(',', expand=True).reset_index(drop=True)

    df_ref = pd.DataFrame(index=np.arange(len(data)), columns=['Cotton', 'Polyester', 'Spandex', 'Lyocell', 
                                                            'Rayon', 'Elastomultiester'])

    # ================================ Cotton =============================
    df_cotton_0 = df1.loc[df1[0].str.contains('Cotton', na=True), 0]
    df_cotton_0.name = 'cotton'
    df_cotton_1 = df1.loc[df1[1].str.contains('Cotton', na=True), 1]
    df_cotton_1.name = 'cotton'

    df_cotton = df_cotton_0.combine_first(df_cotton_1)

    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated()]
    df_ref = df_ref.drop(columns=['Cotton'], axis=1) 
    df_ref['cotton'] = df_ref['cotton'].fillna('Cotton 0%')

    # ============================== Polyester =============================
    df_polyester_0 = df1.loc[df1[0].str.contains('Polyester', na=True), 0]
    df_polyester_0.name = 'polyester'
    df_polyester_1 = df1.loc[df1[1].str.contains('Polyester', na=True), 1]
    df_polyester_1.name = 'polyester'

    df_polyester = df_polyester_0.combine_first(df_polyester_1)

    df_ref = pd.concat([df_ref, df_polyester], axis=1)
    df_ref = df_ref.drop(columns=['Polyester'], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated()] 
    df_ref['polyester'] = df_ref['polyester'].fillna('Polyester 0%')

    # =============================== Spandex ===============================
    df_spandex_1 = df1.loc[df1[1].str.contains('Spandex', na=True), 1]
    df_spandex_1.name = 'spandex'
    df_spandex_2 = df1.loc[df1[2].str.contains('Spandex', na=True), 2]
    df_spandex_2.name = 'spandex'

    df_spandex = df_spandex_1.combine_first(df_spandex_2)

    df_ref = pd.concat([df_ref, df_spandex], axis=1)
    df_ref = df_ref.drop(columns=['Spandex'], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated()]
    df_ref['spandex'] = df_ref['spandex'].fillna('Spandex 0%')

    # ============================== Lyocell ================================
    df_lyocell_0 = df1.loc[df1[0].str.contains('Lyocell', na=True), 0]
    df_lyocell_0.name = 'lyocell'
    df_lyocell_1 = df1.loc[df1[1].str.contains('Lyocell', na=True), 1]
    df_lyocell_1.name = 'lyocell' 

    df_lyocell = df_lyocell_0.combine_first(df_lyocell_1)

    df_ref = pd.concat([df_ref, df_lyocell], axis=1)
    df_ref = df_ref.drop(columns=['Lyocell'], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated()]
    df_ref['lyocell'] = df_ref['lyocell'].fillna('Lyocell 0%')

    # ============================== Rayon ================================
    df_rayon_0 = df1.loc[df1[0].str.contains('Rayon', na=True), 0]
    df_rayon_0.name = 'rayon'
    df_rayon_2 = df1.loc[df1[2].str.contains('Rayon', na=True), 2]
    df_rayon_2.name = 'rayon' 

    df_rayon = df_rayon_0.combine_first(df_rayon_2)

    df_ref = pd.concat([df_ref, df_rayon], axis=1)
    df_ref = df_ref.drop(columns=['Rayon'], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated()]
    df_ref['rayon'] = df_ref['rayon'].fillna('Rayon 0%')

    # ============================== Elastomultiester ================================
    df_elastomultiester = df1.loc[df1[1].str.contains('Elastomultiester', na=True), 1]
    df_elastomultiester.name = 'elastomultiester'

    df_ref = pd.concat([df_ref, df_elastomultiester], axis=1)
    df_ref = df_ref.drop(columns=['Elastomultiester'], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated()]
    df_ref['elastomultiester'] = df_ref['elastomultiester'].fillna('Elastomultiester 0%')

    # ========================= Including new columns on data dataframe =======================
    data = pd.concat([data.reset_index(), df_ref.reset_index()], axis=1)
    data = data.drop(columns=['index'], axis=1)
    data = data.iloc[:, ~data.columns.duplicated()]

    data = data.drop_duplicates()

    # ============== join of combine with product_id ==============

    df_aux = pd.concat( [data['product_id'].reset_index(drop=True), df_ref], axis=1 )


    # =============== Excluding strings in order to keep only numbers for composition columns ==============

    df_aux['cotton'] = df_aux['cotton'].apply(lambda x: int( re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['polyester'] = df_aux['polyester'].apply(lambda x: int( re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['spandex'] = df_aux['spandex'].apply(lambda x: int( re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['lyocell'] = df_aux['lyocell'].apply(lambda x: int( re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['rayon'] = df_aux['rayon'].apply(lambda x: int( re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['elastomultiester'] = df_aux['elastomultiester'].apply(lambda x: int( re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)

    df_aux = df_aux.groupby('product_id').max().reset_index().fillna(0)
    data = data.drop(columns=['cotton', 'polyester', 'spandex', 'lyocell', 'rayon', 'elastomultiester'])
    data = pd.merge( data, df_aux, on='product_id', how='left' )

    # ====== inserting model_size and jeans_size instead of size =========

    data['model_size'] = data['size'].apply(lambda x: re.search('\d{3}', x).group(0) if pd.notnull(x) else x).astype(float)
    data['jeans_size'] = data['size'].str.extract('(\d+/\\d+)')
        
    data = data.drop(columns=['size', 'product_safety', 'composition'], axis=1).reset_index(drop=True)

    #data.to_csv("data_clean.csv")

    return data

def data_insertion(data):
    data_insert = data[[
        'product_id',
        'style_id',
        'color_id',
        'product_name',
        'color',
        'fit',
        'product_price',
        'jeans_size',
        'model_size',
        'cotton',
        'polyester',
        'spandex',
        'lyocell',
        'rayon', 
        'elastomultiester',
        'scrape_datetime'
    ]]

    # create database connection
    create_engine( 'sqlite:///database_hm.sqlite', echo=False )

    # data insertion
    data_insert.to_sql( 'vitrine', con=conn, if_exists='append', index=False)

    return None


if __name__ == '__main__':

    # logging
    path = '/Users/lucasquemelli/Documents/repos/ds_ao_dev'

    if not os.path.exists(path + 'Logs'):
        os.makedirs(path + 'Logs')

    loggin.basicConfig(
        filename = path + 'Logs/webscraping_hm.txt',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger( 'webscraping_hm' )

    # Parameters and constants
    url01 = "https://www2.hm.com/en_us/men/products/jeans.html?sort=stock&image-size=small&image=model&offset=0&page-size=72"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    # Data Collection
    data = data_collection(url01, headers)
    logger.info('Data collection is done!')

    # Data Collection (inside each product)
    data_raw = data_collection_product(data, headers)
    logger.info('Data collection for each product is done!')

    # Data Cleaning
    data = data_cleaning(data_raw)
    logger.info('Data cleaning is done!')

    # Data Insertion
    data_insertion(data)
    logger.info('Data insertion is done!')
