import io
from os import SEEK_END

ORDEM : int = 3 # Ordem da árvore-b
TAM_CABECALHO : int = 4 # Quantidade de bytes que a árvore-b usa para armazenar o cabeçalho
TAM_ELEMENTOS_PAGINA: int = 4 # Quantidade de bytes para representar os elementos das páginas na árvore-b
TAM_PAGINA = TAM_ELEMENTOS_PAGINA + 2 * (TAM_ELEMENTOS_PAGINA * (ORDEM - 1)) + TAM_ELEMENTOS_PAGINA # quantidade de bytes da página = qntChaves + chaves + bytesoffsets + filhos

class Pagina:
    def __init__(self) -> None:
        self.num_chaves : int = 0
        self.chaves : list[int] = [-1] * (ORDEM - 1)
        self.byteoffsets : list[int] = [-1] * (ORDEM - 1)
        self.filhos : list[int] = [-1] * ORDEM


def le_pagina(arq_arvore: io.BufferedRandom, rrn: int) -> Pagina:
    '''
    Lê e cria do arquivo da árvore a página com o rrn especificado de acordo
    com os dados armazenados
    '''
    byteoffset = TAM_CABECALHO + (rrn * TAM_PAGINA)
    arq_arvore.seek(byteoffset)

    pagina = Pagina()
    pagina.num_chaves = int.from_bytes((arq_arvore.read(TAM_ELEMENTOS_PAGINA)))
    for i in range(0, ORDEM - 1):
        pagina.chaves[i] = int.from_bytes((arq_arvore.read(TAM_ELEMENTOS_PAGINA)))
    for i in range(0, ORDEM - 1):
        pagina.byteoffsets[i] = int.from_bytes((arq_arvore.read(TAM_ELEMENTOS_PAGINA)))
    for i in range(0, ORDEM):
        pagina.filhos[i] = int.from_bytes((arq_arvore.read(TAM_ELEMENTOS_PAGINA)))
    return pagina

def escreve_pagina(arq_arvore: io.BufferedRandom, rrn: int, pagina: Pagina):
    byteoffset = TAM_CABECALHO + (rrn * TAM_PAGINA)
    arq_arvore.seek(byteoffset)

    arq_arvore.write(pagina.num_chaves.to_bytes(4))
    for i in range(0, ORDEM - 1):
        arq_arvore.write((pagina.chaves[i]).to_bytes(4))
    for i in range(0, ORDEM - 1):
        arq_arvore.write((pagina.byteoffsets[i]).to_bytes(4))
    for i in range(0, ORDEM):
        arq_arvore.write((pagina.filhos[i]).to_bytes(4))

def busca_na_pagina(chave: int, pagina: Pagina) -> tuple[bool, int]:
    posicao = 0
    while posicao < pagina.num_chaves and chave > pagina.chaves[posicao]:
        posicao += 1
    if posicao < pagina.num_chaves and chave == pagina.chaves[posicao]:
        return True, posicao
    else:
        return False, posicao

def insere_na_pagina(chave: int, byteoffset: int, filho_dir: int, pagina: Pagina):
    if pagina.num_chaves >= ORDEM - 1: # Árvore cheia
        pagina.chaves.append(-1)
        pagina.byteoffsets.append(-1)
        pagina.filhos.append(-1)
    i = pagina.num_chaves
    while i > 0 and chave < pagina.chaves[i - 1]:
        pagina.chaves[i] = pagina.chaves[i - 1]
        pagina.byteoffsets[i] = pagina.byteoffsets[i - 1]
        pagina.filhos[i + 1] = pagina.filhos[i]
        i -= 1
    pagina.chaves[i] = chave
    pagina.byteoffsets[i] = byteoffset
    pagina.filhos[i + 1] = filho_dir
    pagina.num_chaves += 1

def busca_na_arvore(arq_arvore: io.BufferedRandom, chave: int, rrn: int) -> tuple[bool, int, int]:
    if rrn == -1: # Fim da árvore
        return False, -1, -1
    else:
        pagina = le_pagina(arq_arvore, rrn)
        achou, posicao = busca_na_pagina(chave, pagina)
        if achou:
            return True, rrn, posicao
        else: # Busca na página filha
            return busca_na_arvore(arq_arvore, chave, pagina.filhos[posicao])
        
def insere_na_arvore(arq_arvore: io.BufferedRandom, chave: int, byteoffset: int, rrn_atual: int) \
    -> tuple[bool, int, int, int]:
    if rrn_atual == -1:
        chave_promovida = chave
        byteoffset_promovida = byteoffset
        filho_dir_promovida = -1
        return True, chave_promovida, byteoffset_promovida, filho_dir_promovida
    else:
        pagina = le_pagina(arq_arvore, rrn_atual)
        achou, posicao = busca_na_pagina(chave, pagina)

    if achou:
        print('Chave duplicada.')
        quit()
    
    promocao, chave_promovida, byteoffset_promovida, filho_dir_promovida = \
        insere_na_arvore(arq_arvore, chave, byteoffset, pagina.filhos[posicao])
    if not promocao:
        return False,-1, -1, -1
    else:
        if pagina.num_chaves < ORDEM - 1: # Tem espaço para inserir a chave promovida
            insere_na_pagina(chave_promovida, byteoffset_promovida, filho_dir_promovida, pagina)
            escreve_pagina(arq_arvore, rrn_atual, pagina)
            return False,-1, -1, -1
        else:
            chave_promovida, byteoffset_promovida, filho_dir_promovida, pagina, nova_pagina = \
                divide(arq_arvore, chave_promovida, byteoffset_promovida, filho_dir_promovida, pagina)
            escreve_pagina(arq_arvore, rrn_atual, pagina)
            escreve_pagina(arq_arvore, filho_dir_promovida, nova_pagina)
            return True, chave_promovida, byteoffset_promovida, filho_dir_promovida 

def divide(arq_arvore: io.BufferedRandom, chave: int, byteoffset: int, filho_dir: int, pagina: Pagina) \
    -> tuple[int, int, int, Pagina, Pagina]:
    insere_na_pagina(chave, byteoffset, filho_dir, pagina)
    meio = ORDEM // 2
    chave_promovida = pagina.chaves[meio]
    byteoffset_promovida = pagina.byteoffsets[meio]
    filho_dir_promovida = novo_rrn(arq_arvore)

    pagina_atual = Pagina()
    pagina_atual.num_chaves = meio
    pagina_atual.chaves = pagina.chaves[:meio]
    pagina_atual.byteoffsets = pagina.byteoffsets[:meio]
    pagina_atual.filhos = pagina.filhos[:meio + 1]
    while len(pagina_atual.chaves) < ORDEM - 1:
        pagina_atual.chaves.append(-1)
        pagina_atual.byteoffsets.append(-1)
    while len(pagina_atual.byteoffsets) < ORDEM:
        pagina_atual.filhos.append(-1)

    pagina_nova = Pagina()
    pagina_nova.num_chaves = ORDEM - meio - 1
    pagina_nova.chaves = pagina.chaves[meio + 1:]
    pagina_nova.byteoffsets = pagina.byteoffsets[meio + 1:]
    pagina_nova.filhos = pagina.filhos[meio + 1:]
    while len(pagina_nova.chaves) < ORDEM - 1:
        pagina_nova.chaves.append(-1)
        pagina_nova.byteoffsets.append(-1)
    while len(pagina_nova.byteoffsets) < ORDEM:
        pagina_nova.filhos.append(-1)
    
    return chave_promovida, byteoffset_promovida, filho_dir_promovida, pagina_atual, pagina_nova

def novo_rrn(arq_arvore: io.BufferedRandom):
    arq_arvore.seek(0, SEEK_END)
    byteoffset = arq_arvore.tell()
    return (byteoffset - TAM_CABECALHO) // TAM_PAGINA
