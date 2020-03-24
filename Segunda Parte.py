from selenium import webdriver
from bs4 import BeautifulSoup

def date_conversor(date):
    date = date.split()
    month = date[0]
    day = date[1]
    try:
        year = date[2]
    except IndexError:
        year = "0000"
    final_date = ""
    month = month.lower()
    months = {'janeiro': 1, 'fevereiro': 2, 'março': 3,
              'abril': 4, 'maio': 5,  'junho': 6,
              'julho': 7,  'agosto': 8, 'setembro': 9,
              'outubro': 10, 'novembro': 11, 'dezembro': 12}
    final_date = "{}".format(year + '-' + '%s' % months[month] + '-' + day).replace(',','')
    return final_date

user = ["mariabarroshehe@hotmail.com", "joanabarros123kkkk@hotmail.com", "oiisinho@hotmail.com",
        "isabellarochagomes@hotmail.com", "caiocunhacavalcanti@hotmail.com"]
pwd = ["mariabarros123", "joanabarros123", "livia123", "isabella123", "caiocunha123"]

lista = open("Primeira Parte Projeto.txt", "r")
listaatualizada = lista.readlines()
arq = open("Segunda Parte Projeto.txt", "w")
for i in range(len(user)):
    if len(listaatualizada) == 0:
        break
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"C:\Users\micas\PycharmProjects\projeto\venv\selenium\webdriver/chromedriver.exe")
    driver.get('https://pt-br.facebook.com/')

    username_box = driver.find_element_by_id('email')
    username_box.send_keys(user[i])

    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(pwd[i])

    loguin_btn = driver.find_element_by_id('loginbutton')
    loguin_btn.submit()

    arquivo = open("Primeira Parte Projeto.txt", "r")
    listalinks = arquivo.readlines()
    qtdlinks = (len(listalinks))
    for x in range(30):
        if len(listaatualizada) == 0:
            break
        driver.get(listaatualizada[0])
        del listaatualizada[0]
        count = 0
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for i in soup.find_all('a' , '_6-6'):
            count += 1
            if count == 2:
                sobre = i.get('href')

        infobasicasdecontato = sobre+"&section=contact-info"
        driver.get(infobasicasdecontato)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        query = soup.find_all('li' , class_= '_3pw9')

        for li in query:
            item = li.select('._50f4')
            item = str(item)
            if 'Data de nascimento' in item:
                date = li.select('._2iem')[0].contents[0]
                if date_conversor(date)  == None:
                    pass
                else:
                    arq.write(date_conversor(date))
                    arq.write('\n')

    driver.quit()
