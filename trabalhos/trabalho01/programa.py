import sys 
import io
import os

NOME_ARQ_DADOS = 'dados.dat'
MAX_4BYTES_INT = 4294967295

def main():
    if len(sys.argv) != 3: # Verifica se o programa recebe o número correto de argumentos
        raise TypeError('Número inválido de argumentos.')      
    
    if sys.argv[1] == '-e':
        le_operacoes()
        exit()

def le_operacoes():
    '''
    Lê o arquivo de operações e executa cada linha
    '''
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
        registro = busca(arq_dados, chave)
        print(registro[0] + '\n')

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

def busca(arq_dados: io.BufferedReader, chave_buscada: str) -> tuple[str, int]:
    '''
    Busca um registro no *arq_dados* com a chave primária *chave_buscada*
    e retorna uma tupla, contento o registro e seu byte-offset.
    '''
    cabecalho = arq_dados.read(4)
    registro = le_registro(arq_dados)
    achou = False
    byteoffset = 4

    while registro[0] and not achou:
        chave_atual = registro[0].split('|')[0]
        if chave_atual == chave_buscada:
            achou = True
        else:
            byteoffset += 2 + registro[1]
            registro = le_registro(arq_dados)
    if achou:
        return (registro[0], byteoffset)
    else:
        return ('Registro não encontrado.', -1)

def insercao(arq_dados: io.BufferedRandom, bdado: bytes) -> str:
    '''
    Insere o *bdado* no *arq_dados* e retorna o local que foi inserido.
    O *arq_dados* e o *bdado* e estão em binário.
    '''
    bcabecalho = arq_dados.read(4)
    cabecalho = int.from_bytes(bcabecalho)
    tam_dado = len(bdado)

    if (cabecalho == MAX_4BYTES_INT) or (cabecalho < tam_dado):
        # LED tá vazia ou o dado não cabe no arquivo
        local = 'fim do arquivo'
        insercao_fim(arq_dados, bdado)
    else:
        insercao_meio() 
    return local

def remocao(arq_dados: io.BufferedRandom, bdado: bytes):
    '''
    Remove o *bdado* no *arq_dados* e insere ele na LED
    '''
    return NotImplementedError

def le_registro(arq: io.BufferedReader) -> tuple[str, int]:
    '''
    Lê o primeiro registro de *arquivo* e retorna em formato string.
    Retorna também seu tamanho
    '''
    btam_registro = arq.read(2)
    tam_registro = int.from_bytes(btam_registro)
    if tam_registro > 0:
        bbuffer = arq.read(tam_registro)
        buffer = bbuffer.decode()
        return (buffer, tam_registro)
    else:
        return ('', 0)
    
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
