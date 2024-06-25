def main():
    print('----- PROGRAMA PARA INSERÇÃO E ALTERAÇÃO DE REGISTROS -----\n')
    nome_arq = input('Insira o nome do arquivo a ser lido: ')
    try:
        arq = open(nome_arq, 'r+b')
        cab = arq.read(4)
        total_reg = int.from_bytes(cab)
    except:
        arq = open(nome_arq, 'w+b')
        total_reg = 0
        arq.write(total_reg.to_bytes(4))

    print('\nSuas opções são:\n')
    print('1. Inserir um novo registro')
    print('2. Buscar um registro por RRN para alterações')
    print('3. Terminar o programa')
    opcao = int(input('\nDigite o número da sua escolha: '))        
    print()

    while opcao < 3:
        if opcao == 1:
            sobrenome = input('Sobrenome: ')
            nome = input('Primeiro nome: ')
            endereco = input('Endereço: ')
            cidade = input('Cidade: ')
            estado = input('Estado: ')
            cep = input('CEP: ')
            reg = sobrenome + '|' + nome + '|' + endereco + '|' + cidade + '|' + estado + '|' + cep + '|'
            reg = reg.encode()
            reg.ljust(64, b'\0')            
            offset = total_reg * 64 + 4
            arq.seek(offset)
            arq.write(reg)
            total_reg += 1
        elif opcao == 2:
            rrn = int(input('Digite o RRN do registro: '))
            if rrn >= total_reg:
                print('Esse registro não existe.\n')
            else:
                offset = rrn * 64 + 4
                arq.seek(offset)
                reg = arq.read(64)
                reg = bytes.decode(reg)
                campos = reg.split('|')
                print('Conteúdo do registro:\n')
                for campo in campos:
                    print(campo)
                print('\nVocê quer modificar este registro?')
                alterar = input('   Responda S ou N, seguido de <ENTER> ==> ').upper()
                if alterar == 'S':
                    sobrenome = input('Sobrenome: ')
                    nome = input('Primeiro nome: ')
                    endereco = input('Endereço: ')
                    cidade = input('Cidade: ')
                    estado = input('Estado: ')
                    cep = input('CEP: ')
                    reg = sobrenome + '|' + nome + '|' + endereco + '|' + cidade + '|' + estado + '|' + cep + '|'
                    reg = reg.encode()
                    reg.ljust(64, b'\0')
                    arq.seek(offset)
                    arq.write(reg)
        opcao = int(input('\nDigite o número da sua escolha: '))
    arq.seek(0)
    arq.write(total_reg.to_bytes(4))
    arq.close()
    exit()
main()