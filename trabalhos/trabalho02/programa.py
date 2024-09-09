import sys
import io
import arvoreb

NOME_ARQ_DADOS : str = 'games20.dat' # Nome do arquivo de registros
NOME_ARQ_SAIDA : str = 'btree2.dat' # Nome do arquivo de armazenamento do índice
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
    #elif sys.argv[1] == '-e':
        #le_operacoes()
    #elif sys.argv[1] == '-p':
        #imprime_indice()
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
        print(prox_chave, byteoffset)
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


if __name__ == '__main__':
    main()
