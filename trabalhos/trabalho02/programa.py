import sys 
import io
import os
import arvoreb

NOME_ARQ_DADOS : str = 'games.dat' # Nome do arquivo de registros
NOME_ARQ_SAIDA : str = 'btree.dat' # Nome do arquivo de armazenamento do índice

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

if __name__ == '__main__':
    main()
