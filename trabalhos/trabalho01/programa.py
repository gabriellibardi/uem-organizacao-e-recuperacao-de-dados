import sys 
import io
import os

NOME_ARQ_DADOS = 'dados.dat'
MAX_4BYTES_INT = 4294967295

def main():
    if len(sys.argv) != 3: # Verifica se o programa recebe o número correto de argumentos
        raise TypeError('Número inválido de argumentos.')      
    if sys.argv[1] == '-e':
        try:
            arq_operacoes = open(sys.argv[2], 'r')
        except:
            print('Arquivo de operações não encontrado.')
            exit()

        linha = arq_operacoes.readline()
        if linha != '': # Linha do arquivo de operações possui elementos
            operacao = linha[0]
            valor = linha[2:].strip()

        while linha: # Arquivo de operações ainda não terminou
            executa_operacao(operacao, NOME_ARQ_DADOS, valor)
            linha = arq_operacoes.readline()
            if linha != '':
                operacao = linha[0]
                valor = linha[2:].strip()

        arq_operacoes.close()

def executa_operacao(operacao: str, nome_arq_dados: str, valor: str):
    '''
    Executa a *operacao* no arquivo de dados com *nome_arq_dados*,
    utilizando *valor* como argumento.
    As operações são 'b' = busca;
                     'i' = inserção;
                     'r' = remoção;
    '''
    tam_valor = len(valor)
    bvalor = valor.encode()
    chave = valor.split('|')[0]
    if operacao == 'b':
        try:
            arq_dados = open(nome_arq_dados, 'br')
        except:
            print('Arquivo de dados não encontrado.')
            exit()
        print('Busca pelo registro de chave "' + chave + '"')
        resultado = busca(arq_dados, chave)
        print(resultado + '\n')
    elif operacao == 'i':
        try:
            arq_dados = open(nome_arq_dados, 'r+b')
        except:
            print('Arquivo de dados não encontrado.')
            exit()
        print('Inserção do registro de chave "' + chave + '" (' + str(tam_valor) + ' bytes)')    
        print('Local: ' + insercao(arq_dados, bvalor) + '\n')
    elif operacao == 'r':
        try:
            arq_dados = open(nome_arq_dados, 'r+b')
        except:
            print('Arquivo de dados não encontrado.')
            exit()
        remocao(arq_dados, bvalor)
    else:
        raise Exception('Operação não encontrada.')
    arq_dados.close()

def busca(arq_dados: io.BufferedReader, chave_buscada: str) -> str:
    '''
    Busca um jogo específico no *arq_dados* por meio da *chave_buscada*.
    '''
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
        return registro + ' ('+ str(len(registro)) + ' bytes)'
    else:
        return 'Registro não encontrado.'

def insercao(arq_dados: io.BufferedRandom, bdado: bytes) -> str:
    '''
    Insere o *bdado* no *arq_dados* e retorna o local que foi inserido.
    O *arq_dados* e o *bdado* e estão em binário.
    '''
    bcabecalho = arq_dados.read(4)
    cabecalho = int.from_bytes(bcabecalho)
    tam_dado = len(bdado)

    if (cabecalho == MAX_4BYTES_INT) or (cabecalho < tam_dado):
        local = 'fim do arquivo'
        insercao_fim(arq_dados, bdado)  # LED tá vazia ou o dado não cabe no arquivo
    else:
        insercao_meio() 
    return local

def remocao(arq_dados: io.BufferedRandom, bdado: bytes):
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
    
def insercao_fim(arq_dados: io.BufferedRandom, bdado: bytes):
    '''
    Insere o *bdado* no fim do *arq_dados*.
    O *arq_dados* e o *bdado* estão em binário.
    '''
    tam_dado = len(bdado)
    arq_dados.seek(0, os.SEEK_END)
    arq_dados.write(tam_dado.to_bytes(2))
    arq_dados.write(bdado)

def insercao_meio():
    return NotImplementedError

if __name__ == '__main__':
    main()
