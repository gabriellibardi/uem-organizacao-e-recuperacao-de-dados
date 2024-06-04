def main():
    nome_arq = input('Insira o nome do arquivo a ser lido: ')
    try:
        entrada = open(nome_arq, 'r')
    except:
        print('Erro na abertura.')
        exit()
    campo = leia_campo(entrada)
    i = 1
    while campo != '':
        print('    Campo #' + str(i) + ': ', end='')
        print(campo)
        i += 1
        campo = leia_campo(entrada)

    entrada.close()
    exit()

def leia_campo(entrada) -> str:
    campo = ''
    c = entrada.read(1)
    while c != '' and c != '|':
        campo = campo + c
        c = entrada.read(1)
    return campo

main()
