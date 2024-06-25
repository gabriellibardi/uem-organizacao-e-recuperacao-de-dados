def main():
    nome_arq = input('Insira o nome do arquivo a ser lido: ')
    try:
        entrada = open(nome_arq, 'br')
    except:
        print('Erro na abertura.')
        exit()
    buffer = leia_reg(entrada)
    num_registro = 0

    while buffer != '':
        num_registro += 1
        print('Registro #' + str(num_registro) + ' (Tam - ' + str(len(buffer)) + '):')
        lista_campos = str.split(buffer, sep='|')
        num_campo = 1
        for campo in lista_campos:
            if campo != '':
                print('    Campo #' + str(num_campo) + ': ', end='')
                num_campo += 1
                print(campo)
        buffer = leia_reg(entrada)
        print()
    entrada.close()
    exit()
    
def leia_reg(entrada):
    tam = entrada.read(2)
    tam = int.from_bytes(tam)
    if tam > 0:
        buffer = entrada.read(tam)
        buffer = bytes.decode(buffer)
        return buffer
    else:
        return ''

main()
