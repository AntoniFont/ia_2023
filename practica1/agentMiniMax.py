"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from collections import deque
from typing import List, Tuple, Union

from ia_2022 import entorn
from practica1 import joc, agent
from practica1.entorn import Accio, TipusCasella, SENSOR


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)
        self.prueba = True

    def pinta(self, display):
        pass

    def cerca(self, estat, pas: int = 0, profunditat: int = 3):

        if pas >= profunditat - 1:  # no hauria d'arribar aquí
            return None

        is_max = pas % 2 == 0
        if is_max:
            jugador = self.jugador
        else:
            jugador = TipusCasella.CARA if self.jugador is TipusCasella.CREU else TipusCasella.CREU

        successors = estat.genera_fill(jugador)
        estat.heretar_a_b()
        estat.valor = -float('inf') if is_max else float('inf')
        estat_fill = successors[0]

        #print(f"{COL_DEBUG}El estado en paso {pas} es{COL_DEF}\n{str(estat)}")

        if pas >= profunditat - 2:
            pass#print(f"{COL_DEBUG}Como ha llegado al penúltimo nivel, genera los {len(successors)} estados:{COL_DEF}")

        for succ in successors:
            if pas >= profunditat - 2:
                succ.set_valor()
                #print(f"{COL_DEBUG}Con valor {succ.cost_total} el estado es{COL_DEF}\n{str(succ)}")
            else:
                #print(f"Entra")
                self.cerca(succ, pas + 1, profunditat)

            if not is_max:
                if succ.valor < estat.valor:
                    estat_fill = succ
                estat.valor = min(estat.valor, succ.valor)
                estat.beta = min(succ.beta, succ.valor)
            else:
                if succ.valor > estat.valor:
                    estat_fill = succ
                estat.valor = max(estat.valor, succ.valor)
                estat.alpha = max(succ.alpha, succ.valor)

            if estat.alpha >= estat.beta:
                #print(f"{COL_DEBUG}PODA{COL_DEF}")
                break

        if pas == 0:
            pass#print(f"{COL_DEBUG}El estado al que va a ir tiene coste {estat_fill.cost_total}, és\n{COL_DEF}{str(estat_fill)}")

        return estat_fill.accions_previes

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | Tuple[entorn.Accio, object]:
        
        taulell = percepcio[SENSOR.TAULELL]
        self.__accions = self.cerca(agent.Estat(taulell), 0, 3)        
        if len(self.__accions) > 0:                
            return Accio.POSAR, self.__accions[0]
        else:
            return Accio.ESPERAR, None
   
