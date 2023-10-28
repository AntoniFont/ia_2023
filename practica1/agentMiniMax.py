"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from collections import deque
from typing import List, Tuple, Union

from ia_2022 import entorn
from practica1 import joc, Estat
from practica1.entorn import Accio, TipusCasella, SENSOR

TipusPosarPesa = Tuple[Accio, Tuple[int, int]]

class EstatMinMax(Estat):
    def __init__(
        self,
        taulell: List[List[TipusCasella]],
        tipus: TipusCasella,
        n: int = None,
        pare: Union[Estat,type(None)] = None,
        accions_previes: Union[List[TipusPosarPesa],type(None)] = None,
    ) -> None:
        super().__init__(taulell, tipus, n, pare, accions_previes)

    def _calcul_heuristica(self) -> int:
        pass

    def minimax(self, alpha, beta, maximizingPlayer, visitedNodes: set):
        final, score = self.es_meta()
        if final or not visitedNodes.add(self):
            if score == 0:
                return 0
            score = -score if maximizingPlayer else score
            return score

        MAX = float("inf")
        if maximizingPlayer:
            max_eval = -MAX
            for fill in self.genera_fills(True):
                eval = fill.minimax(alpha, beta, not maximizingPlayer, visitedNodes)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return max_eval
        else:
            min_eval = MAX
            for fill in self.genera_fills(True):
                eval = fill.minimax(alpha, beta, not maximizingPlayer, visitedNodes)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if alpha >= beta:
                    break
            return min_eval

    def millor_accio(self):
        MAX = float("inf")

        millor_valor = -MAX
        millor_accio = None

        visited = set()
        visited.add(self)

        for fill in self.genera_fills(True):
            eval = fill.minimax(-MAX, MAX, False, visited)
            if eval > millor_valor:
                millor_valor = eval
                millor_accio = fill._accions_previes[0]

        return millor_accio

class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | Tuple[entorn.Accio, object]:
        estat_actual = EstatMinMax(
            taulell=percepcio[SENSOR.TAULELL],
            n=percepcio[SENSOR.MIDA][0],
            tipus=self.jugador,
        )

        # millor_accio = estat_actual.millor_accio(self.jugador == TipusCasella.CARA)
        # return millor_accio if millor_accio else Accio.ESPERAR

        if estat_actual.es_meta()[0]:
            return Accio.ESPERAR
        else:
            millor_accio = estat_actual.millor_accio()
            return millor_accio
