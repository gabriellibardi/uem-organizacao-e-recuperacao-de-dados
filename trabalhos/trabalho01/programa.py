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
CARACTERE_REMOCAO = b'*'

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3: # Verifica se o programa recebe o número correto de argumentos
        raise TypeError('Número inválido de argumentos.')      

    if sys.argv[1] == '-e':
        le_operacoes()
        exit()
    elif sys.argv[1] == '-p':
        imprime_led()
        exit()
    else:
        raise TypeError('Argumento inválido.')

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
        executa_operacao(operacao, valor)
        linha = arq_operacoes.readline()
        if linha != '':
            operacao = linha[0]
            valor = linha[2:].strip()
    arq_operacoes.close()

def executa_operacao(operacao: str, valor: str):
    '''
    Executa a *operacao* no arquivo de dados utilizando *valor* como argumento.
    As operações são 'b' = busca;
                     'i' = inserção;
                     'r' = remoção;
    '''
    bvalor = valor.encode()
    chave = valor.split('|')[0]

    if operacao == 'b': # busca
        executa_busca(chave)

    elif operacao == 'i': # inserção
        executa_insercao(bvalor, chave)

    elif operacao == 'r': # remoção
        executa_remocao(chave)
    else:
        raise Exception('Operação não encontrada.')
    
def executa_busca(chave: str):
    '''
    Executa a operação de busca do registro com *chave* no arquivo de dados
    '''
    try:
        arq_dados = open(NOME_ARQ_DADOS, 'br')
    except:
        print('Arquivo de dados não encontrado.')
        exit()
    registro = busca(arq_dados, chave)[0]
    print('Busca pelo registro de chave "' + chave + '"')
    print(registro + ' (' + str(len(registro)) + ' bytes)\n')
    arq_dados.close()

def executa_insercao(valor: bytes, chave: str):
    '''
    Executa a operação de inserção do *valor* com *chave* no arquivo de dados
    '''
    try:
        arq_dados = open(NOME_ARQ_DADOS, 'r+b')
    except:
        print('Arquivo de dados não encontrado.')
        exit()
    local, tamanho = insercao(arq_dados, valor)
    print('Inserção do registro de chave "' + chave + '" (' + str(tamanho) + ' bytes)')    
    print('Local: ' + local + '\n')
    arq_dados.close()

def executa_remocao(chave: str):
    '''
    Executa a operação de remoção do registro com *chave* no arquivo de dados
    '''
    try:
        arq_dados = open(NOME_ARQ_DADOS, 'r+b')
    except:
        print('Arquivo de dados não encontrado.')
        exit()
    resultado, qnt_removida, byteoffset = remocao(arq_dados, chave)
    print('Remoção do registro de chave "' + chave + '"')
    if resultado == False:
        print('Erro: registro não encontrado!\n')
    else:
        print('Registro removido! (' + str(qnt_removida) + ' bytes)')
        print('Local: offset = ' + str(byteoffset) + ' bytes (' + str(hex(byteoffset) + ')\n'))
    arq_dados.close()

def busca(arq_dados: io.BufferedReader, chave_buscada: str) -> tuple[str, int, int]:
    '''
    Busca um registro no *arq_dados* com a chave primária *chave_buscada*
    e retorna uma tupla, contento o registro, seu offset e tamanho.
    '''
    cabecalho = arq_dados.read(TAM_CABECALHO)
    registro, tamanho = le_registro(arq_dados)
    achou = False
    offset = TAM_CABECALHO

    while registro and not achou:
        chave_atual = registro.split('|')[0]
        if chave_atual == chave_buscada:
            achou = True
        else:
            offset += TAM_TAMANHO_REG + tamanho
            registro, tamanho = le_registro(arq_dados)

    if achou:
        return registro, offset, tamanho
    else:
        return 'Registro não encontrado.', -1, 0

def insercao(arq_dados: io.BufferedRandom, bdado: bytes) -> tuple[str, int]:
    '''
    Insere o *bdado* no *arq_dados* e retorna o local que foi inserido e seu tamanho.
    O *arq_dados* e o *bdado* e estão em binário.
    '''
    bcabecalho = arq_dados.read(TAM_CABECALHO)
    cabecalho = int.from_bytes(bcabecalho)
    arq_dados.seek(cabecalho, os.SEEK_SET)
    tam_atual = int.from_bytes(arq_dados.read(TAM_TAMANHO_REG))
    tam_dado = len(bdado)

    if (bcabecalho == PONTEIRO_VAZIO) or (tam_atual < tam_dado):
        # LED tá vazia ou o dado não cabe no arquivo
        local = 'fim do arquivo'
        insercao_fim(arq_dados, bdado)
    else: # O registro vai entrar no primeiro espaço da LED
        local = str(cabecalho)
        arq_dados.seek(cabecalho, os.SEEK_SET)
        arq_dados.write(tam_dado.to_bytes(TAM_TAMANHO_REG))
        arq_dados.seek(len(CARACTERE_REMOCAO), os.SEEK_CUR)
        proximo = arq_dados.read(TAM_PONTEIRO_LED)
        arq_dados.seek(cabecalho + TAM_TAMANHO_REG, os.SEEK_SET)
        arq_dados.write(bdado)
        arq_dados.seek(0, os.SEEK_SET)
        arq_dados.write(proximo) # Atualiza a cabeça da LED
        tam_restante = tam_atual - tam_dado
        if tam_restante > 10: # Espaço restante volta pra LED
            offset = cabecalho + TAM_TAMANHO_REG + tam_dado
            arq_dados.seek(offset, os.SEEK_SET)
            arq_dados.write(tam_restante.to_bytes(TAM_TAMANHO_REG))
            arq_dados.write(CARACTERE_REMOCAO)
            insercao_led(arq_dados, offset, tam_restante)
    return local, tam_dado

def remocao(arq_dados: io.BufferedRandom, chave: str) -> tuple[bool, int, int]:
    '''
    Remove o registro com a chave *chave* no *arq_dados* e insere ele na LED
    Retorna uma tupla com um bool, indicando se a remoção foi feita,
    o número de bytes removidos e o byteoffset do registro removido
    '''
    registro, offset, tamanho = busca(arq_dados, chave)
    if tamanho == 0:
        return False, 0, -1
    else:
        arq_dados.seek(offset + TAM_TAMANHO_REG, os.SEEK_SET)
        arq_dados.write(CARACTERE_REMOCAO) # inserindo o indicador de remoção
        insercao_led(arq_dados, offset, tamanho)
        return True, tamanho, offset

def le_registro(arq: io.BufferedReader) -> tuple[str, int]:
    '''
    Lê o primeiro registro de *arquivo* e retorna em formato string.
    Retorna também seu tamanho
    '''
    btam_registro = arq.read(TAM_TAMANHO_REG)
    tam_registro = int.from_bytes(btam_registro)
    if tam_registro > 0:
        bbuffer = arq.read(tam_registro)
        if bbuffer[:len(CARACTERE_REMOCAO)] == CARACTERE_REMOCAO: # Caractere removido
            return ('', 0)
        else:
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

def insercao_led(arq_dados: io.BufferedRandom, offset: int, tamanho: int):
    '''
    Insere o *byteoffset* do registro na LED mantida no *arq_dados*.
    A LED leva em conta a organização worst-fit, sendo ordenada
    de forma decrescente levando em conta o *tamanho* dos registros.
    '''
    arq_dados.seek(os.SEEK_SET)
    cabecalho = arq_dados.read(TAM_CABECALHO)

    if cabecalho == PONTEIRO_VAZIO: # LED vazia
        insercao_cabeca_led(arq_dados, offset, cabecalho)
    else:
        bproximo = cabecalho
        arq_dados.seek(int.from_bytes(bproximo), os.SEEK_SET)
        tam_proximo = int.from_bytes(arq_dados.read(TAM_TAMANHO_REG))

        if tam_proximo <= tamanho: # Registro vai entrar na cabeça da LED
            insercao_cabeca_led(arq_dados, offset, bproximo)
        else: # Registro vai entrar no meio da LED
            insercao_meio_led(arq_dados, offset, bproximo, tamanho, tam_proximo)

def insercao_cabeca_led(arq_dados:io.BufferedRandom, byteoffset: int, cabeca_atual: bytes):
    '''
    Insere o *byteoffset* do registro na cabeça da LED mantida no *arq_dados*.
    Além disso, atribui o próximo valor da LED como sendo a *cabeça_atual*
    '''
    arq_dados.seek(os.SEEK_SET)
    arq_dados.write(byteoffset.to_bytes(TAM_CABECALHO))
    arq_dados.seek(byteoffset, os.SEEK_SET)
    arq_dados.seek(TAM_TAMANHO_REG + len(CARACTERE_REMOCAO), os.SEEK_CUR)
    arq_dados.write(cabeca_atual)

def insercao_meio_led(arq_dados:io.BufferedRandom, byteoffset: int, bproximo: bytes,
                       tam: int, tam_proximo: int):
    '''
    Insere o *byteoffset* do registro no meio ou fim da LED, mantida no *arq_dados*,
    seguindo a organização de worst-fit.
    '''
    while (bproximo != PONTEIRO_VAZIO) and (tam_proximo > tam):
        batual = bproximo
        arq_dados.seek(int.from_bytes(bproximo), os.SEEK_SET)
        arq_dados.seek(TAM_TAMANHO_REG + len(CARACTERE_REMOCAO), os.SEEK_CUR)
        bproximo = arq_dados.read(TAM_PONTEIRO_LED)
        arq_dados.seek(int.from_bytes(bproximo), os.SEEK_SET)
        tam_proximo = int.from_bytes(arq_dados.read(TAM_TAMANHO_REG))
    arq_dados.seek(byteoffset, os.SEEK_SET)
    arq_dados.seek(TAM_TAMANHO_REG + len(CARACTERE_REMOCAO), os.SEEK_CUR)
    arq_dados.write(bproximo)
    arq_dados.seek(int.from_bytes(batual), os.SEEK_SET)
    arq_dados.seek(TAM_TAMANHO_REG + len(CARACTERE_REMOCAO), os.SEEK_CUR)
    arq_dados.write(byteoffset.to_bytes(TAM_PONTEIRO_LED))

def imprime_led():
    try:
        arq_dados = open(NOME_ARQ_DADOS, 'br')
    except:
        print('Arquivo de dados não encontrado.')
        exit()

    cabecalho = arq_dados.read(TAM_CABECALHO)
    espacos_disponiveis = 0

    if cabecalho == PONTEIRO_VAZIO:
        print('LED -> [offset: -1]')
    else:
        offset = int.from_bytes(cabecalho)
        print('LED -> ', end='')
        while offset != int.from_bytes(PONTEIRO_VAZIO):
            arq_dados.seek(offset, os.SEEK_SET)
            tam_registro = int.from_bytes(arq_dados.read(TAM_TAMANHO_REG))
            espacos_disponiveis += 1
            print('[offset: ' + str(offset) + ', tam: ' + str(tam_registro) + '] -> ', end='')
            arq_dados.seek(offset, os.SEEK_SET)
            arq_dados.seek(TAM_TAMANHO_REG + len(CARACTERE_REMOCAO), os.SEEK_CUR)
            offset = int.from_bytes(arq_dados.read(TAM_PONTEIRO_LED))
        print('[offset: -1]')
    
    print('Total: ' + str(espacos_disponiveis) + ' espaços disponíveis')
    arq_dados.close()
    exit()

if __name__ == '__main__':
    main()
