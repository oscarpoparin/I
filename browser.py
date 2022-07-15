#codigo para buscar algo automaticamente en chrome

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def search(something):
    browser = webdriver.Chrome(executable_path='C:\\Chromedriver91\\chromedriver.exe') #
    browser.maximize_window()                       # maximiza la ventana 
    browser.get('https://www.google.com/')          # abre el buscador de google
    findElem = browser.find_element_by_name('q')    # busca el elemento por nombre
    findElem.send_keys(something)                   # ubica la palabra a buscar y coloca en el buscador
    findElem.send_keys(Keys.RETURN)                 # nos retorna lo buscado

#descargar chromedriver dependiendo la version y guardar en una carpeta en el disco local c