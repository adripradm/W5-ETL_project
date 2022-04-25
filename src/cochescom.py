#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
PATH=ChromeDriverManager().install()
import numpy as np
from random import randint
import requests as req
import pandas as pd
import time
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
opciones=Options()



def cochescom(n):     
        pages = np.arange(1, n, 1)
        data=[]
        model=[]
        price=[]
        gas=[]
        horse=[]
        dis=[]
        place=[]
        year=[]
        li=[]

        for page in pages:

            page='https://www.coches.com/coches-segunda-mano/coches-ocasion.htm?page=' + str(page) 
            driver=webdriver.Chrome(PATH, options=opciones)
            driver.get(page)
            sleep(randint(1,2))
            cookies=driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
            cookies.click()
            sleep(randint(2,10))
            soup = bs(driver.page_source, 'html.parser')

            modelo =[" ".join(e.text.split('\n')) for e in soup.find_all(class_='make-model-version')]
            precio=[" ".join(i.text.split('\n')) for i in soup.find_all(class_='price')]
            combustible=[" ".join(c.text.split('\n')) for c in soup.find_all(class_='gas')]
            CV=[" ".join(cv.text.split('\n')) for cv in soup.find_all(class_='cv')]
            km=[" ".join(km.text.split('\n')) for km in soup.find_all(class_='km')]
            lugar=[" ".join(l.text.split('\n')) for l in soup.find_all(class_='location')]
            año=[" ".join(a.text.split('\n')) for a in soup.find_all(class_='year')]
            link=[li.find('a').attrs['href'] for li in soup.find_all(class_='pill-information')]
            
            model.append(modelo)
            price.append(precio)
            gas.append(combustible)
            horse.append(CV)
            dis.append(km)
            place.append(lugar)
            year.append(año)
            li.append(link)

            flat_list_modelo = [item for modelo in model for item in modelo]
            flat_list_precio = [item for precio in price for item in precio]
            flat_list_gas = [item for combustible in gas for item in combustible]
            flat_list_cv = [item for CV in horse for item in CV]
            flat_list_km = [item for km in dis for item in km]
            flat_list_lugar = [item for lugar in place for item in lugar]
            flat_list_año = [item for año in year for item in año]
            flat_list_link = [item for link in li for item in link]


            coches=pd.DataFrame(flat_list_modelo)
            
            coches['precio']=flat_list_precio
            coches['combustible']=flat_list_gas
            coches['CV']=flat_list_cv
            coches['km']=flat_list_km
            coches['lugar']=flat_list_lugar
            coches['año']=flat_list_año
            coches['link']=flat_list_link
            coches.rename(columns={'0': "modelo"}, inplace=True)
            x = coches[coches.lugar.str.contains('\d', regex=True)]
            x.drop(columns='combustible', inplace=True)
            x.rename(columns={'km': "lugar", 'CV':'combustible', 'lugar':'año', 'año':'km'}, inplace=True)
            x['CV']='Unknown'
            col=x.pop('CV')
            x.insert(3,'CV',col)
            col1=x.pop('km')
            x.insert(4,'km',col1)
            y = coches[coches.lugar.str.contains('[a-zA-Z]+', regex=True)]
            frames=[x,y]
            result=pd.concat(frames)
            result.reset_index(inplace=True)
            result.to_csv('result.csv')
            
        
        
        return result

