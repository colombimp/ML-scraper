"""
Created on Sat May  8 20:45:07 2021

@author: mariapapla
"""

from urllib.request import urlopen as uReq  
import urllib.error
from bs4 import BeautifulSoup as soup 
import csv
from datetime import datetime

entrada = input('Ingrese el/los modelos que desea buscar el precio, separados por coma')

lista = entrada.split(',')

autos = []
for elem in lista:
    marca , model =  elem.split()
    
    autos.append(''.join([marca,'/',model,'/']))

import matplotlib.pyplot as plt
import numpy as np

k = 0
for modelo in autos:
    priceplot = []
    yearplot = []
    prices_page = ''.join(["https://autos.mercadolibre.com.ar/",modelo])
    
    myFile = open(''.join(['./precios/prices_',prices_page[34:].replace('/','_'),str(datetime.today()).split()[0],'.csv']), 'w')
    contador = 49
    
    prices_pagenuevo = prices_page
    
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(['Modelo',"Precio","Antiguedad" , "Kilometraje","Zona"])
        while True: 
            try:
                #print(prices_pagenuevo)    
                uClient = uReq(prices_pagenuevo)
                page_html = uClient.read()
                uClient.close()                
           
                #Read the data
                page_soup = soup(page_html, "html.parser")
          
                atributos = page_soup.findAll("div", {"class":"ui-search-result__content-wrapper"})
                
                if atributos == []:
                    break
                link = page_soup.findAll("a", {"class":"ui-search-result__content ui-search-link"})[0]
                for att in atributos:
    
                        vincle = link['href']

                        zone = att.findAll("span",{"class":"ui-search-item__group__element ui-search-item__location"})
                        zona = zone[0].text.strip() 

                        price = att.findAll("span",{"class":"price-tag-fraction"})
                        precio = price[0].text.strip()
                        precio = precio.replace('.','')
                        
                        priceplot.append(float(precio))
                        name = att.findAll("div",{"class":"ui-search-item__group ui-search-item__group--title"})
                        nombre = name[0].text.strip() 

    
                        anio = att.findAll("li",{"class":"ui-search-card-attributes__attribute"})[0]
                        antiguedad = anio.text.strip()
                            
                        yearplot.append(float(antiguedad))
                        kms = att.findAll("li",{"class":"ui-search-card-attributes__attribute"})[1]
                        kilometraje = kms.text.strip()
                        kilometraje = kilometraje.replace('Km','')
                        kilometraje = kilometraje.replace('.','')
                        data = [nombre,float(precio),float(antiguedad),kilometraje, zona]
    
                        'guardo los datos'            
                        writer.writerows([data])
                                         
                        
                prices_pagenuevo = prices_page + ''.join(['_Desde_',str(contador)]) 
                contador += 48
                
            except urllib.error.HTTPError as exception:
    
                print(exception)
                break
   
    plt.plot(np.array(yearplot), np.array(priceplot)/1000.,'m.')
    plt.xlabel('Year')
    plt.ylabel('Price (thousands of ARS)')
    plt.title(''.join(['Price vs year plot for ',lista[k]]))
    plt.savefig(''.join(['price_year_',lista[k],'.png']))
    plt.show()        
    k += 1

