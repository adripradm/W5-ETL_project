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


def wallapop(url2):
    
    url2='https://es.wallapop.com/app/search?category_ids=100&filters_source=seo_landing&longitude=-3.69196&latitude=40.41956'  
    driver=webdriver.Chrome(PATH, options=opciones)
    driver.get(url2)
    sleep(randint(1,2))
    cookies=driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]')
    cookies.click()
    sleep(randint(2,10))
    roll=driver.find_element_by_xpath('//*[@id="btn-load-more"]/button')
    roll.click()
    def run_script():
    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    count = 0
    while count < 200:
        run_script()
        count+=1
        time.sleep(2)

    soup = bs(driver.page_source, 'html.parser')

    modelo =[e.text.strip().split('\n') for e in soup.find_all(class_='ItemCardWide__title d-inline-block text-truncate w-100')]
    precio=[" ".join(i.text.strip().split('\n')) for i in soup.find_all(class_='ItemCardWide__price ItemCardWide__price--bold')]
    combustible=[" ".join(c.text.split('\n')) for c in soup.find_all(class_='ItemExtraInfo d-flex')]
    
    df=pd.DataFrame(modelo)
    df['precio']=precio
    df['caracteristicas']=combustible
    df.rename(columns={0: "modelo"}, inplace=True)
    df.to_csv('wallapop.csv')
    
    return df
    
    

