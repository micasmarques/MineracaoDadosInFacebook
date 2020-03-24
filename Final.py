import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from pylab import bar, xticks, plt, show, arange

user = str(input("Qual seu email: "))
pwd = str(input("Qual a senha: "))
grupo = str(input("Qual o link do grupo(Acrescente um espaço antes de dar enter): "))

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\micas\PycharmProjects\projeto\venv\selenium\webdriver/chromedriver.exe")

def login(user, pwd):
    driver.get('https://pt-br.facebook.com/')
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(user)
    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(pwd)
    loguin_btn = driver.find_element_by_id('loginbutton')
    loguin_btn.submit()

def date_conversor(date):
    date = date.split()
    month = date[2]
    if (int(date[0]) == 1) or (int(date[0]) == 2) or (int(date[0]) == 3) or (int(date[0]) == 4) or (int(date[0]) == 5) or (int(date[0]) == 6) or (int(date[0]) == 7) or (int(date[0]) == 8) or (int(date[0]) == 9):
        day = '0' + date[0]
    else:
        day = date[0]

    try:
        year = date[4]
    except IndexError:
        return
    month = month.lower()
    months = {'janeiro': '01', 'fevereiro': '02', 'março': '03',
              'abril': '04', 'maio': '05',  'junho': '06',
              'julho': '07',  'agosto': '08', 'setembro': '09',
              'outubro': '10', 'novembro': '11', 'dezembro': '12'}
    final_date = "{}".format(day + '-' + '%s' % months[month] + '-' + year).replace(',','')
    return final_date

def pega_link():
    login(user, pwd)
    driver.get(grupo)
    codigofonte = BeautifulSoup(driver.page_source, 'html.parser')
    qtdmembrossujo = (codigofonte.select("span#count_text")[0].contents)
    qtdmembrossujo = qtdmembrossujo[0]
    limpadorqtdmembros = qtdmembrossujo.find("membros")
    if "." in qtdmembrossujo:
        qtdmembroslimpo = int(qtdmembrossujo[:limpadorqtdmembros - 1].replace(".", ""))
    else:
        qtdmembroslimpo = int(qtdmembrossujo[:limpadorqtdmembros - 1])
    id = grupo[32:]
    barra = id.find("/")
    id = id[:barra]
    paginamembros = 'https://www.facebook.com/groups/' + id + '/members/'
    driver.get(paginamembros)
    numeropagedown = int(qtdmembroslimpo)
    contadorend = 0
    while True:
        driver.find_element_by_tag_name('html').send_keys(Keys.END)
        contadorend += 1
        time.sleep(0.1)
        if contadorend == numeropagedown:
            break

    arq = open("Links de cada pessoa.txt", "w")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.find_all('a', '_60rg'):
        arq.write(link.get('href'))
        arq.write('\n')
    driver.close()
    arq.close()

def pega_data():
    userf = ["mariabarroshehe@hotmail.com", "joaobarroskmb@gmail.com",
             "isabellarochagomes@hotmail.com"]
    pwdf = ["mariabarros123", "joaobarros123", "isabella123"]
    userf.append(user)
    pwdf.append(pwd)
    links_grupo = open("Links de cada pessoa.txt", "r")
    links = links_grupo.readlines()
    arq = open("Data de nascimento.txt", "w")
    links_grupo.close()
    for i in range(len(user)):
        if len(links) == 0:
            break
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=r"C:\Users\micas\PycharmProjects\projeto\venv\selenium\webdriver/chromedriver.exe")
        driver.get('https://pt-br.facebook.com/')

        username_box = driver.find_element_by_id('email')
        username_box.send_keys(userf[i])

        password_box = driver.find_element_by_id('pass')
        password_box.send_keys(pwdf[i])

        loguin_btn = driver.find_element_by_id('loginbutton')
        loguin_btn.submit()
        for x in range(30):
            if len(links) == 0:
                break
            driver.get(links[0])
            del links[0]
            count = 0
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for i in soup.find_all('a', '_6-6'):
                count += 1
                if count == 2:
                    sobre = i.get('href')

            infobasicasdecontato = sobre + "&section=contact-info"
            driver.get(infobasicasdecontato)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            query = soup.find_all('li', class_='_3pw9')

            for li in query:
                item = li.select('._50f4')
                item = str(item)
                if 'Data de nascimento' in item:
                    date = li.select('._2iem')[0].contents[0]
                    if date_conversor(date) == None:
                        pass
                    else:
                        arq.write(date_conversor(date))
                        arq.write('\n')

        driver.quit()
    arq.close()

def pega_idade():
    now = datetime.now()

    arquivo = open("Data de nascimento.txt", "r")
    datanascimento = arquivo.readlines()
    qtddatanascimento = (len(datanascimento))

    anoatual = now.year
    mesatual = now.month
    diaatual = now.day

    arq = open("Idade.txt", "w")

    for i in range(0, qtddatanascimento):
        ano = int(datanascimento[i][6:10])
        mes = int(datanascimento[i][3:5])
        dia = int(datanascimento[i][:2])
        idade = anoatual - ano
        if mesatual > mes:
            idade += 1
        if mesatual == mes:
            if diaatual >= dia:
                idade += 1
        arq.write(str(idade))
        arq.write('\n')
    arq.close()

def cada_idade_apareceu():
    arq_idade = open("Idade.txt", "r")
    idade = arq_idade.readlines()
    idade_convertida = []
    arq_idade.close()
    for i in idade:
        j = int(i)
        idade_convertida.append(j)

    age = {13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0,
           23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0,
           33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0, 41: 0, 42: 0,
           43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 0, 52: 0,
           53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0,
           63: 0, 64: 0, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0, 70: 0, 71: 0, 72: 0,
           73: 0, 74: 0, 75: 0, 76: 0, 77: 0, 78: 0, 79: 0, 80: 0, 81: 0, 82: 0,
           83: 0, 84: 0, 85: 0, 86: 0, 87: 0, 88: 0, 89: 0, 90: 0, 91: 0, 92: 0,
           93: 0, 94: 0, 95: 0, 96: 0, 97: 0, 98: 0, 99: 0, 100: 0}

    for i in idade_convertida:
        if i in age:
            age[i] += 1

    for i in range(13, 101):
        if age[i] == 0:
            del age[i]

    arq = open("Quantas vezes cada idade aparece.txt", "w")
    for i in age.items():
        grafico = str(i).lstrip("(").rstrip(")").strip()
        grafico = grafico.replace(", ", ";")
        arq.write(grafico)
        arq.write('\n')
    arq.close()

def grafico():
    names = []
    values = []

    arq = open("Quantas vezes cada idade aparece.txt")

    for line in arq:
        name, value = line.strip().split(";")
        names.append(name)
        values.append(int(value))

    pos = arange(len(names)) + .5

    bar(pos, values, align='center', color='#b8ff5c')
    xticks(pos, names)
    plt.title("Grafico de Idades")
    plt.xlabel("Idade das pessoas no grupo")
    plt.ylabel("Quantas pessoas tem a idade igual")

    show()
    arq.close()

pega_link()

pega_data()

pega_idade()

cada_idade_apareceu()

grafico()
