"""
ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from typing import List, Optional, Tuple
from queue import PriorityQueue
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR, TipusCasella

# Definim un tipus per la colocació de una peça
TipusPosarPesa = Tuple[Accio, Tuple[int, int]]

class Estat:   

    def __init__(
        self,
        taulell: List[List[TipusCasella]],
        tipus: TipusCasella,
        n: int,
        pare: Optional["Estat"] = None,
        accions_previes: Optional[List[TipusPosarPesa]] = None,
    ) -> None:
        self._taulell = taulell
        self._n = n
        self._tipus = tipus
        self._pare = pare
        self._accions_previes = accions_previes or []
        self._acc_pos = [
            (Accio.POSAR, (row, col)) for row in range(n) for col in range(n)
        ]

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: "Estat") -> bool:
        return self._taulell == other._taulell

    def __str__(self) -> str:
        return "\n" + (
            "\n".join(
                [
                    " ".join(
                        [
                            "_"
                            if col == TipusCasella.LLIURE
                            else "O"
                            if col == TipusCasella.CARA
                            else "X"
                            for col in row
                        ]
                    )
                    for row in self._taulell
                ]
            )
            + "\n"
        )

    def __repr__(self) -> str:
        return str(self)

    # Devuelve una copia del estado actual actualizado con el movimiento pasado por argumento
    def __fer_accio(
        self, accio: Tuple[Accio.POSAR, Tuple[int, int]]
    ) -> List[List[TipusCasella]]:
        _, pos = accio
        taulell = [row[:] for row in self._taulell]  # Copies the grid
        taulell[pos[0]][pos[1]] = self._tipus
        return taulell

    # Comprueba que la casilla este libre
    def __legal(self, accio: Tuple[Accio.POSAR, Tuple[int, int]]) -> bool:
        _, pos = accio
        return self._taulell[pos[0]][pos[1]] == TipusCasella.LLIURE

    def _cambia_jugador(self) -> TipusCasella:
        return (
            TipusCasella.CARA if self._tipus == TipusCasella.CREU else TipusCasella.CREU
        )

    def accions_previes(self) -> List[TipusPosarPesa]:
        return self._accions_previes

    def es_meta(self) -> Tuple[bool, int]:
        if not self._accions_previes:
            return (False, 0) # Empty board
        
        n = self._n
        taulell = self._taulell
        row, col = self._accions_previes[-1][1]
        contrari = self._cambia_jugador()

        directions = [
            (0, -1),  # left
            (0, 1),  # right
            (-1, 0),  # top
            (1, 0),  # down
            (-1, 1),  # diagonal top right
            (1, 1),  # diagonal bottom right
            (1, -1),  # diagonal bottom left
            (-1, -1),  # diagonal bottom left
        ]

        for dx, dy in directions:
            count = 0
            for k in range(4):
                x, y = row + k * dx, col + k * dy

                if 0 <= x < n and 0 <= y < n:
                    if taulell[x][y] == contrari:
                        count += 1

            if count == 4:
                return (True, 1)  # El contrari va fer un moviment guanyador

        for i in range(n):
            for j in range(n):
                if taulell[i][j] == TipusCasella.LLIURE:
                    return (False, 0)  # Encara es pot jugar

        return (True, 0)  # Empat

    def genera_fills(self, cambia_jugador: bool = False) -> List["Estat"]:
        return [
            self.__class__(
                taulell=self.__fer_accio(accio),
                n=self._n,
                tipus=self._tipus if not cambia_jugador else self._cambia_jugador(),
                pare=self,
                accions_previes=self._accions_previes + [accio],
            )
            for accio in self._acc_pos
            if self.__legal(accio)
        ]


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass