from pylab import *

names = []
values = []

arq = open("Quarta Parte Projeto.txt")

for line in arq:
    name , value = line.strip().split(";")
    names.append(name)
    values.append(int(value))

pos = arange(len(names)) + .5

bar(pos , values , align = 'center',color = '#b8ff5c')
xticks(pos,names)
show()