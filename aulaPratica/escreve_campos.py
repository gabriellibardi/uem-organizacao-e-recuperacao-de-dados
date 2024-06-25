nome_arq = input('Insira um nome para seu arquivo: ')
saida = open(nome_arq, 'w')
sobrenome = input('Digite o sobrenome: ')

while sobrenome != '':
    nome = input('Digite o nome: ')
    endereco = input('Digite o endereço: ')
    cidade = input('Digite a cidade: ')
    estado = input('Digite o estado: ')
    cep = input('Digite o cep: ')
    
    saida.write(sobrenome + '|')
    saida.write(nome + '|')
    saida.write(endereco + '|')
    saida.write(cidade + '|')
    saida.write(estado + '|')
    saida.write(cep + '|')

    sobrenome = input('Insira outro sobrenome: ')

saida.close()
exit()
