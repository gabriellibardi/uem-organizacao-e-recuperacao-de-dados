import sys
import io
import arvoreb
from os import SEEK_END

NOME_ARQ_DADOS : str = 'games20.dat' # Nome do arquivo de registros
NOME_ARQ_SAIDA : str = 'btree.dat' # Nome do arquivo de armazenamento do índice
TAM_CABECALHO: int = 4 # Quantidade de bytes que o arquivo de registros usa para armazenar o cabeçalho
TAM_TAM_REGISTRO: int = 2 # Quantidade de bytes que o arquivo de registros usa para armazenar o tamanho dos registros

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3: # Verifica se o programa recebe o número correto de argumentos
        print('Número inválido de argumentos.')
        exit()
    executa_argumento()
    exit()

def executa_argumento():
    '''
    Executa a funcionalidade do programa de acordo com o argumento passado:

    -c -> Criação do índice (arvore-b) a partir do arquivo de registros
    -e -> Execução do um arquivo de operações passado
    -p -> Impressão das informações do índice (arvore-b)
    '''
    if sys.argv[1] == '-c':
        cria_indice()
    elif sys.argv[1] == '-e':
        le_operacoes()
    elif sys.argv[1] == '-p':
        imprime_indice()
    else:
        print('Argumento inválido.')

def cria_indice():
    '''
    Cria um índice com os registros do arquivo de registros como uma árvore-b
    '''
    arq_arvore = open(NOME_ARQ_SAIDA, 'w+b')
    arvoreb.inicializa_arvore(arq_arvore)

    try:
        arq_dados = open(NOME_ARQ_DADOS, 'rb')
    except:
        print('Arquivo de dados não encontrado.')
        quit()

    le_registros(arq_dados, arq_arvore)

    arq_dados.close()
    arq_arvore.close()

def le_registros(arq_dados: io.BufferedReader, arq_arvore: io.BufferedRandom):
    '''
    Lê os registros do arquivo de dados e insere na árvore-b
    '''
    arq_dados.seek(0)
    qnt_registros = int.from_bytes(arq_dados.read(TAM_CABECALHO), signed=True, byteorder='little')

    while qnt_registros > 0:
        prox_chave, byteoffset = le_chave(arq_dados)
        arvoreb.insere_chave(arq_arvore, prox_chave, byteoffset)
        qnt_registros -= 1

    print('Árvore-b criada com sucesso.')

def le_chave(arq_dados: io.BufferedReader) -> tuple[int, int]:
    '''
    Lê o próximo registro do arquivo de dados, retornando
    sua chave e seu byteoffset
    '''
    byteoffset = arq_dados.tell()
    tam_registro = int.from_bytes(arq_dados.read(TAM_TAM_REGISTRO), signed=True, byteorder='little')
    if tam_registro > 0:
        registro = (arq_dados.read(tam_registro)).decode()
        chave = int(registro[:registro.find('|')].strip())
        return chave, byteoffset
    else:
        return -1, byteoffset

def le_operacoes():
    '''
    Lê e executa as operações do arquivo de operações no arquivo de índices
    '''
    try:
        arq_operacoes = open(sys.argv[2], 'r')
    except:
        print('Arquivo de operações não encontrado.')
        quit()       

    try:
        arq_arvore = open(NOME_ARQ_SAIDA, 'r+b')
    except:
        print('Arquivo de índices não encontrado.')
        quit()

    try:
        arq_dados = open(NOME_ARQ_DADOS, 'r+b')
    except:
        print('Arquivo de dados não encontrado.')
        quit()
    
    linha = (arq_operacoes.readline()).strip()
    while linha:
        operacao = linha[:linha.find(' ')].strip()
        arg = linha[linha.find(' '):].strip()
        if operacao == 'b':
            executa_busca(arq_arvore, arq_dados, int(arg))
            print()
        elif operacao == 'i':
            executa_insercao(arq_arvore, arq_dados, arg)
            print()
        else:
            print('Operação inválida.')
        linha = (arq_operacoes.readline()).strip()

    arq_operacoes.close()
    arq_arvore.close()
    arq_dados.close()

def executa_busca(arq_arvore: io.BufferedRandom, arq_dados: io.BufferedRandom, chave: int):
    '''
    Executa a busca de um registro no índice por meio de sua chave
    '''
    print('Busca pelo registro de chave "' + str(chave) + '"')
    arq_arvore.seek(0)
    raiz = int.from_bytes(arq_arvore.read(arvoreb.TAM_CABECALHO), signed=True, byteorder='little')
    achou, rrn, posicao = arvoreb.busca_na_arvore(arq_arvore, chave, raiz)
    if achou:
        pagina = arvoreb.le_pagina(arq_arvore, rrn)
        arq_dados.seek(pagina.byteoffsets[posicao])
        tam_registro = int.from_bytes(arq_dados.read(TAM_TAM_REGISTRO), signed=True, byteorder='little')
        print((arq_dados.read(tam_registro)).decode() + \
               ' (' + str(tam_registro) + ' bytes - offset ' + str(pagina.byteoffsets[posicao]) + ')')
    else:
        print('ERRO: registro não encontrado!')

def executa_insercao(arq_arvore: io.BufferedRandom, arq_dados: io.BufferedRandom, registro: str):
    '''
    Executa a insercao do registro no arquivo de índices e de registros
    '''
    chave = registro[:registro.find('|')].strip()
    arq_arvore.seek(0)
    raiz = int.from_bytes(arq_arvore.read(arvoreb.TAM_CABECALHO), signed=True, byteorder='little')
    print('Inserção do registro de chave "' + chave + '"')
    achou = arvoreb.busca_na_arvore(arq_arvore, int(chave), raiz)[0]
    if achou:
        print('ERRO: chave "' + chave + '" já existe!')
    else:
        byteoffset, tam_registro = insere_registro(arq_dados, registro)
        arvoreb.insere_chave(arq_arvore, int(chave), byteoffset)
        print(registro + ' (' + str(tam_registro) + ' bytes - offset ' + str(byteoffset) + ')')

def insere_registro(arq_dados: io.BufferedRandom, registro: str) -> tuple[int, int]:
    '''
    Insere o registro no fim do arquivo de registros, retornando seu byteoffset e tamanho
    '''
    # Adiciona 1 na quantidade de registros
    arq_dados.seek(0)
    qnt_registros = int.from_bytes(arq_dados.read(TAM_CABECALHO), signed=True, byteorder='little')
    qnt_registros += 1
    arq_dados.seek(0)
    arq_dados.write(qnt_registros.to_bytes(TAM_CABECALHO, signed=True, byteorder='little'))

    # Escreve o registro no fim do arquivo
    arq_dados.seek(0, SEEK_END)
    byteoffset = arq_dados.tell()
    tam_registro = len(registro)
    arq_dados.write(tam_registro.to_bytes(TAM_TAM_REGISTRO, signed=True, byteorder='little'))
    arq_dados.write(registro.encode())

    return byteoffset, tam_registro

def imprime_indice():
    '''
    Imprime na tela os elementos do arquivo de índices
    '''
    try:
        arq_arvore = open(NOME_ARQ_SAIDA, 'rb')
    except:
        print('Arquivo de índices não encontrado.')
        quit()

    arvoreb.imprime_arvore(arq_arvore)
    arq_arvore.close()

if __name__ == '__main__':
    main()
