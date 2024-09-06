import io

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

def busca_na_pagina(chave: int, pagina: Pagina) -> tuple[bool, int]:
    posicao = 0
    while posicao < pagina.num_chaves and chave > pagina.chaves[posicao]:
        posicao += 1
    if posicao < pagina.num_chaves and chave == pagina.chaves[posicao]:
        return True, posicao
    else:
        return False, posicao

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

