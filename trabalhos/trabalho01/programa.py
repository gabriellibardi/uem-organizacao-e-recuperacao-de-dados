import sys 
import io
import os

# Arquivo de dados formado por um cabeçalho de 4 bytes, onde
# cada registro é precedido por 2 bytes, que informam seu tamanho.

NOME_ARQ_DADOS = 'dados.dat'
TAM_CABECALHO = 4
TAM_TAMANHO_REG = 2
TAM_PONTEIRO_LED = 4
PONTEIRO_VAZIO = b'\xff\xff\xff\xff'
CARACTERE_REMOCAO = '*'

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
    bvalor = valor.encode()
    chave = valor.split('|')[0]

    if operacao == 'b': # busca
        try:
            arq_dados = open(nome_arq_dados, 'br')
        except:
            print('Arquivo de dados não encontrado.')
            exit()
        registro = busca(arq_dados, chave)[0]
        print('Busca pelo registro de chave "' + chave + '"')
        print(registro + '\n')

    elif operacao == 'i': # inserção
        try:
            arq_dados = open(nome_arq_dados, 'r+b')
        except:
            print('Arquivo de dados não encontrado.')
            exit()
        local, tamanho = insercao(arq_dados, bvalor)
        print('Inserção do registro de chave "' + chave + '" (' + str(tamanho) + ' bytes)')    
        print('Local: ' + local + '\n')

    elif operacao == 'r': # remoção
        try:
            arq_dados = open(nome_arq_dados, 'r+b')
        except:
            print('Arquivo de dados não encontrado.')
            exit()
        resultado, qnt_removida, byteoffset = remocao(arq_dados, chave)
        print('Remoção do registro de chave "' + chave + '"')
        if resultado == False:
            print('Erro: registro não encontrado!\n')
        else:
            print('Registro removido! (' + str(qnt_removida) + ' bytes)')
            print('Local: offset = ' + str(byteoffset) + ' bytes (' + str(hex(byteoffset) + ')'))
    else:
        raise Exception('Operação não encontrada.')
    
    arq_dados.close()

def busca(arq_dados: io.BufferedReader, chave_buscada: str) -> tuple[str, int, int]:
    '''
    Busca um registro no *arq_dados* com a chave primária *chave_buscada*
    e retorna uma tupla, contento o registro, seu byte-offset e tamanho.
    '''
    cabecalho = arq_dados.read(TAM_CABECALHO)
    registro, tamanho = le_registro(arq_dados)
    achou = False
    byteoffset = TAM_CABECALHO

    while registro and not achou:
        chave_atual = registro.split('|')[0]
        if chave_atual == chave_buscada:
            achou = True
        else:
            byteoffset += TAM_TAMANHO_REG + tamanho
            registro, tamanho = le_registro(arq_dados)

    if achou:
        return registro, byteoffset, tamanho
    else:
        return 'Registro não encontrado.', -1, 0

def insercao(arq_dados: io.BufferedRandom, bdado: bytes) -> tuple[str, int]:
    '''
    Insere o *bdado* no *arq_dados* e retorna o local que foi inserido e seu tamanho.
    O *arq_dados* e o *bdado* e estão em binário.
    '''
    bcabecalho = arq_dados.read(TAM_CABECALHO)
    cabecalho = int.from_bytes(bcabecalho)
    tam_dado = len(bdado)

    if (bcabecalho == PONTEIRO_VAZIO) or (cabecalho < tam_dado):
        # LED tá vazia ou o dado não cabe no arquivo
        local = 'fim do arquivo'
        insercao_fim(arq_dados, bdado)
    else:
        local = 'na LED'
        insercao_meio()
    return local, tam_dado

def remocao(arq_dados: io.BufferedRandom, chave: str) -> tuple[bool, int, int]:
    '''
    Remove o registro com a chave *chave* no *arq_dados* e insere ele na LED
    Retorna uma tupla com um bool, indicando se a remoção foi feita,
    o número de bytes removidos e o byteoffset do registro removido
    '''
    registro, byteoffset, tamanho = busca(arq_dados, chave)
    if tamanho == 0:
        return False, 0, -1
    else:
        arq_dados.seek(byteoffset + TAM_TAMANHO_REG, os.SEEK_SET)
        arq_dados.write(CARACTERE_REMOCAO.encode()) # inserindo o indicador de remoção
        arq_dados.seek(os.SEEK_SET)
        insercao_led(arq_dados, byteoffset, tamanho)
        return True, tamanho, byteoffset

def le_registro(arq: io.BufferedReader) -> tuple[str, int]:
    '''
    Lê o primeiro registro de *arquivo* e retorna em formato string.
    Retorna também seu tamanho
    '''
    btam_registro = arq.read(TAM_TAMANHO_REG)
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
    arq_dados.write(tam_dado.to_bytes(TAM_TAMANHO_REG))
    arq_dados.write(bdado)

def insercao_meio():
    return NotImplementedError

def insercao_led(arq_dados: io.BufferedRandom, byteoffset: int, tamanho: int):
    '''
    Insere o *byteoffset* do registro na LED mantida no *arq_dados*.
    A LED leva em conta a organização worst-fit, sendo ordenada
    de forma decrescente levando em conta o *tamanho* dos registros.
    '''
    cabecalho = int.from_bytes(arq_dados.read(TAM_CABECALHO))

    if cabecalho == PONTEIRO_VAZIO: # LED está vazia
        arq_dados.seek(os.SEEK_SET)
        arq_dados.write(byteoffset.to_bytes(4))
        arq_dados.seek(byteoffset + TAM_TAMANHO_REG + 1, os.SEEK_SET)
        arq_dados.write(PONTEIRO_VAZIO)
    else: # LED já possui registros
        arq_dados.seek(cabecalho)
        tam_proximo = int.from_bytes(arq_dados.read(2))
        proximo = int.from_bytes(arq_dados.read(5)[1:])
        while (proximo != PONTEIRO_VAZIO) and (tam_proximo > tamanho):
            atual = proximo
            arq_dados.seek(proximo, os.SEEK_SET)
            tam_proximo = int.from_bytes(arq_dados.read(2))
            proximo = int.from_bytes(arq_dados.read(5)[1:])
        arq_dados.seek(byteoffset + TAM_TAMANHO_REG + 1, os.SEEK_SET)
        arq_dados.write(proximo.to_bytes())
        arq_dados.seek(atual + TAM_TAMANHO_REG + 1, os.SEEK_SET)
        arq_dados.write(byteoffset.to_bytes())

if __name__ == '__main__':
    main()
