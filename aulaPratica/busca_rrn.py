def main():
    nome_arq = input('Insira o nome do arquivo a ser lido: ')
    try:
        entrada = open(nome_arq, 'br')
    except:
        print('Erro na abertura.')
        exit()

    cab = entrada.read(4)
    total_reg = int.from_bytes(cab)
    print()
    rrn = int(input('Insira o RRN do registro para buscá-lo: '))
    if rrn >= total_reg:
        print()
        print('Registro não encontrado.')
        exit()
    offset = rrn * 64 + 4
    entrada.seek(offset)
    reg = entrada.read(64)
    reg = bytes.decode(reg)

    campos = reg.split('|')
    for campo in campos:
        print(campo)
    print()
    entrada.close()
    exit()
main()
