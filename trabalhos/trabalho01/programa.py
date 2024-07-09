from sys import argv
import io

NOME_ARQ_DADOS = 'dados.dat'

def main():
    if len(argv) != 3: # Verifica se o programa recebe o número correto de argumentos
        raise Exception('Número inválido de argumentos.')      
    if argv[1] == '-e':
        try:
            arq_operacoes = open(argv[2], 'r')
        except:
            print('Arquivo de operações não encontrado.')

        linha = arq_operacoes.readline()
        if linha != '': # Linha do arquivo de operações possui elementos
            elementos = linha.split()
            operacao = elementos[0]
            valor = elementos[1]

        while linha: # Arquivo de operações ainda não terminou
            if operacao == 'b':
                busca(NOME_ARQ_DADOS, valor)
            elif operacao == 'i':
                insercao(NOME_ARQ_DADOS, valor)
            elif operacao == 'r':
                remocao(NOME_ARQ_DADOS, valor)
            else:
                raise Exception('Operação não encontrada.')
            linha = arq_operacoes.readline()
            if linha != '':
                elementos = linha.split()
                operacao = elementos[0]
                valor = elementos[1]

        arq_operacoes.close()

def busca(nome_arq_dados: str, chave_buscada: str):
    '''
    Busca um jogo específico no arquivo de dados com o *nome_arq_dados* por meio de sua *chave*.
    '''
    arq_dados = open(nome_arq_dados, 'br')

    print('Busca pelo registro de chave "' + chave_buscada + '"')

    cabecalho = arq_dados.read(4)
    registro = le_registro(arq_dados)
    achou = False
    while registro and not achou:
        chave_atual = registro.split('|')[0]
        if chave_atual == chave_buscada:
            achou = True
        else:
            registro = le_registro(arq_dados)

    if achou:
        print(registro + '\n')
    else:
        print('Registro não encontrado.\n')
    
    arq_dados.close()

def insercao():
    return NotImplementedError

def remocao():
    return NotImplementedError

def le_registro(arq: io.BufferedReader) -> str:
    '''
    Lê o primeiro registro de *arquivo* e retorna em formato string.
    '''
    btam_registro = arq.read(2)
    tam_registro = int.from_bytes(btam_registro)
    if tam_registro > 0:
        bbuffer = arq.read(tam_registro)
        buffer = bbuffer.decode()
        return buffer
    else:
        return ''
    
if __name__ == '__main__':
    main()
