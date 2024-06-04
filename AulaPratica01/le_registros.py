def main():
    nome_arq = input('Insira o nome do arquivo a ser lido: ')
    try:
        entrada = open(nome_arq, 'br')
    except:
        print('Erro na abertura.')
        exit()
    buffer_com_tam = leia_reg(entrada)
    buffer = buffer_com_tam[0]
    tam_registro = buffer_com_tam[1]
    num_registro = 0

    while buffer != '':
        num_registro += 1
        print('Registro #' + str(num_registro) + ' (Tam - ' + str(tam_registro) + '):')
        lista_campos = str.split(buffer, sep='|')
        i = 1
        for campo in lista_campos:
            if campo != '':
                print('    Campo #' + str(i) + ': ', end='')
                i += 1
            print(campo)
        buffer_com_tam = leia_reg(entrada)
        buffer = buffer_com_tam[0]
        tam_registro = buffer_com_tam[1]
    entrada.close()
    exit()
    
def leia_reg(entrada):
    tam = entrada.read(2)
    tam = int.from_bytes(tam)
    if tam > 0:
        buffer = entrada.read(tam)
        buffer = bytes.decode(buffer)
        return (buffer, tam)
    else:
        return ('', 0)

main()
