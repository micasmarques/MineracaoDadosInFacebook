from datetime import datetime
now = datetime.now()

arquivo = open("Segunda Parte Projeto.txt", "r")
datanascimento = arquivo.readlines()
qtddatanascimento = (len(datanascimento))

arq = open("Terceira Parte Projeto.txt", "w")
for i in range(0 ,qtddatanascimento):
    anoatual = now.year
    mesatual = now.month
    diaatual = now.day

    ano = int(datanascimento[i][6:])
    mes = int(datanascimento[i][3:5])
    dia = int(datanascimento[i][:2])

    idade = anoatual - ano
    if mesatual > mes:
        idade += 1
    if mesatual == mes:
        if diaatual >= dia:
            idade +=1
    arq.write(str(idade))
    arq.write('\n')
