def main():
    nome_arq = input('Insira o nome do arquivo a ser lido: ')

    try:
        entrada = open(nome_arq, 'br')
    except:
        print('Erro na abertura.')
        exit()

    chave = input('Insira o SOBRENOME para buscar o registro: ')
    achou = False
    reg = leia_reg(entrada)

    while reg != '' and not achou:
        sobrenome = reg.split(sep='|')[0]
        if sobrenome == chave:
            achou = True
        else:
            reg = leia_reg(entrada)

    if achou:
        print()
        print('Registro encontrado:')
        print()
        campos = reg.split(sep='|')
        num_campo = 1
        for campo in campos:
            if campo != '':
                print('Campo ' + str(num_campo) +': ', end='')
                print(campo)
                num_campo += 1
    else:
        print()
        print('Registro não encontrado.')

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
