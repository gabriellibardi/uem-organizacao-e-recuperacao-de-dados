nome_arq = input('Insira um nome para seu arquivo: ')
saida = open(nome_arq, 'bw')
campo = input('Digite o/a sobrenome: ')
resto_campos = ['nome', 'endereço', 'cidade', 'estado', 'CEP']

while campo != '':
    buffer = ''
    buffer += campo + '|'
    for campo_restante in resto_campos:
        campo = input('Digite o/a ' + campo_restante + ': ')
        buffer += campo + '|'
    buffer_bin = buffer.encode()
    tam = len(buffer_bin)
    tam_bytes = tam.to_bytes(2)
    saida.write(tam_bytes)
    saida.write(buffer_bin)
    campo = input('Digite outro sobrenome: ')

saida.close()
exit()
