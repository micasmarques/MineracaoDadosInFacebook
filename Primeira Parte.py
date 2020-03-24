import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

user = str(input("Qual seu email: "))
pwd = str(input("Qual a senha: "))
site = str(input("Qual o link do grupo:(Acrescente um espaço antes de dar enter) "))

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\micas\PycharmProjects\projeto\venv\selenium\webdriver/chromedriver.exe")
driver.get('https://pt-br.facebook.com/')

username_box = driver.find_element_by_id('email')
username_box.send_keys(user)
password_box = driver.find_element_by_id('pass')
password_box.send_keys(pwd)
loguin_btn = driver.find_element_by_id('loginbutton')
loguin_btn.submit()
driver.get(site)

codigofonte = BeautifulSoup(driver.page_source, 'html.parser')
qtdmembrossujo = (codigofonte.select("span#count_text")[0].contents)
qtdmembrossujo = qtdmembrossujo[0]
limpadorqtdmembros = qtdmembrossujo.find("membros")
if "." in qtdmembrossujo:
    qtdmembroslimpo = int(qtdmembrossujo[:limpadorqtdmembros-1].replace(".",""))
else:
    qtdmembroslimpo = int(qtdmembrossujo[:limpadorqtdmembros-1])
id = site[32:]
barra = id.find("/")
id = id[:barra]
paginamembros = 'https://www.facebook.com/groups/'+id+'/members/'
driver.get(paginamembros)
numeropagedown = int(qtdmembroslimpo)
contadorend = 0
while True:
    driver.find_element_by_tag_name('html').send_keys(Keys.END)
    contadorend += 1
    time.sleep(0.1)
    if contadorend == numeropagedown:
        break

arq = open("Primeira Parte Projeto.txt", "w")
soup = BeautifulSoup(driver.page_source, 'html.parser')
for link in soup.find_all('a' , '_60rg'):
    arq.write(link.get('href'))
    arq.write('\n')
driver.close()
