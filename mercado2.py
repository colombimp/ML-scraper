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
    marca , modelo =  elem.split()
    
    autos.append(''.join([marca,'/',modelo,'/']))

for modelo in autos:
    prices_page = ''.join(["https://autos.mercadolibre.com.ar/",modelo])
    
    myFile = open(''.join(['./precios/prices_',prices_page[34:].replace('/','_'),str(datetime.today()).split()[0],'.csv']), 'w')
    
    contador = 49
    
    prices_pagenuevo = prices_page
    
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(['Modelo',"Precio","Antiguedad" , "Kilometraje"])
        while True: 
            try:
                print(prices_pagenuevo)    
                uClient = uReq(prices_pagenuevo)
                page_html = uClient.read()
                uClient.close()                
           
                #Read the data
                page_soup = soup(page_html, "html.parser")
          
                atributos = page_soup.findAll("div", {"class":"ui-search-result__content-wrapper"})
                #precio = page_soup.findAll("div", {"class":"ui-search-price ui-search-price--size-medium ui-search-item__group__element"})
                if atributos == []:
                    break
                link = page_soup.findAll("a", {"class":"ui-search-result__content ui-search-link"})[0]
                for att in atributos:
    
                        vincle = link['href']
    
                        #vincle.replace(',','')
                        zone = att.findAll("span",{"class":"ui-search-item__group__element ui-search-item__location"})
                        zona = zone[0].text.strip() 
                        zona = zona.encode('utf-8')
                        # zona = zona.replace(',','')
                        price = att.findAll("span",{"class":"price-tag-fraction"})
                        precio = price[0].text.strip()
                        precio = precio.replace('.','')
                        name = att.findAll("div",{"class":"ui-search-item__group ui-search-item__group--title"})
                        nombre = name[0].text.strip() 
                        nombre = nombre.encode('utf-8')
                        #nombre = nombre.replace(',','')
                        anio = att.findAll("li",{"class":"ui-search-card-attributes__attribute"})[0]
                        antiguedad = anio.text.strip()
                        #antiguedad = antiguedad.replace(',','')
                        kms = att.findAll("li",{"class":"ui-search-card-attributes__attribute"})[1]
                        kilometraje = kms.text.strip()
                        kilometraje = kilometraje.replace('Km','')
                        kilometraje = kilometraje.replace('.','')
                        data = [nombre,float(precio),float(antiguedad),kilometraje]
    
                        'guardo los datos'            
                        writer.writerows([data])
                        

                                            
                        
                prices_pagenuevo = prices_page + ''.join(['_Desde_',str(contador)]) 
                contador += 48
                
            except urllib.error.HTTPError as exception:
    
                print(exception)
                break
                