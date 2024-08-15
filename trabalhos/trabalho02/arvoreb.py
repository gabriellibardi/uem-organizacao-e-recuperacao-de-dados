from __future__ import annotations

class Pagina:

    ordem: int
    numChaves: int
    chaves: list[int | None] 
    byteoffsets: list[int | None]
    filhos: Pagina | None
    
    def __init__(self, ordem: int) -> None:
        self.ordem = ordem
        self.numChaves = 0
        self.chaves = [None] * (ordem - 1)
        self.byteoffsets = [None] * (ordem - 1)
        self.filho = [None] * ordem
