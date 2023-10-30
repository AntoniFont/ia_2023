"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""

import queue
from typing import Tuple

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, TipusCasella, SENSOR

class Estat:
    def __init__(self, taulell, mida) -> None:
        self.taulell = taulell
        self.mida = mida
        self.depth = 0
        self.maxScore = 1000
        self.minScore = -1000
        self.queue = queue.PriorityQueue()
        self.torn_max = True

    def es_meta(self):
        for fila in range(len(self.taulell)):
            for columna in (range(len(self.taulell[0]))):
                # Suposam que el lloc sempre serà cuatre en ratlla i no un altre número en ratlla.
                if(self.taulell[fila][columna] == TipusCasella.CARA):
                    # (x) x x x
                    #
                    #
                    #
                    if(self.estaOcupat(fila +1,columna) and self.estaOcupat(fila +2, columna) and self.estaOcupat(fila + 3,columna)):
                        return True
                    # (x)
                    #  x
                    #  x
                    #  x
                    if(self.estaOcupat(fila,columna +1) and self.estaOcupat(fila, columna +2) and self.estaOcupat(fila,columna +3)):
                        return True
                    # (x)
                    #   x
                    #    x
                    #     x
                    if(self.estaOcupat(fila +1,columna +1) and self.estaOcupat(fila+2, columna +2) and self.estaOcupat(fila+3,columna +3)):
                        return True
                    #        x
                    #      x
                    #    x
                    # (x)    
                    if(self.estaOcupat(fila +1,columna -1) and self.estaOcupat(fila+2, columna -2) and self.estaOcupat(fila+3,columna -3)):
                        return True
        return False         
    def estaOcupat(self,fila,columna):
        #Suposam que el tauler es sempre un quadrat
        if fila < 0 or columna < 0 or fila > len(self.taulell) or columna > len(self.taulell):
            return False
        else :
            return self.taulell[fila-1][columna-1] == TipusCasella.CARA    

    def calc_score_position(self, row, col, inc_row, inc_col, taulell):
        ai_points = 0
        player_points = 0

        for i in range(4):  # connect "4"
            if taulell[col][row] == TipusCasella.CREU:
                ai_points += 1
            elif taulell[col][row] == TipusCasella.CARA:
                player_points += 1

            row += inc_row
            col += inc_col

        if player_points == 4:
            return self.minScore
        elif ai_points == 4:
            return self.maxScore
        else:
            return ai_points
            
    def is_full(self, taulell):
        for i in range(len(taulell)):
            for j in range(len(taulell[i])):
                if taulell[i][j] == TipusCasella.LLIURE:
                    return False
        return True    
         
    def is_done(self, taulell, score : int):
        return self.depth >= 8 or self.is_full(taulell) or score >= self.maxScore or score <= self.minScore
    
    def clone(self, taulell):
        cloned_board = [[cell for cell in row] for row in taulell]
        return cloned_board
    
    def place(self, taulell, col, is_max) -> bool:
        if taulell[col][0] == TipusCasella.LLIURE and 0 <= col < self.mida[1]:
            for j in range(self.mida[0] - 1, -1, -1):
                if taulell[col][j] == TipusCasella.LLIURE:
                    taulell[col][j] = TipusCasella.CARA if is_max else TipusCasella.CREU
                    return True
        return False
        
    #Jugada De Jugador Max    
    def max_play(self, taulell, alpha, beta) -> Tuple:
        score = self.calc_score(taulell)

        if self.is_done(taulell, score):
            return (-1, score)

        max = (-1, 0)
        tmp = None

        for column in range(self.mida[1]):
            tmp_taulell = self.clone(taulell)
            if self.place(tmp_taulell, column, True):
                self.depth += 1
                next_value = self.min_play(tmp_taulell, alpha, beta)

                print(next_value)
                if max[0] == -1 or next_value[1] > max[1]:
                    tmp = (column, next_value[1])
                    alpha = next_value[1]
                if beta <= alpha:
                    break

        return max if tmp is None else tmp

    def min_play(self, taulell, alpha, beta) -> Tuple:
        score = self.calc_score(taulell)

        if self.is_done(taulell, score):
            return (-1, score)

        min = (-1, 0)
        tmp = None

        for column in range(self.mida[1]):
            tmp_taulell = self.clone(taulell)
            if self.place(tmp_taulell, column, False):
                self.depth += 1
                next_value = self.max_play(tmp_taulell, alpha, beta)
                print(next_value)   

                if min[0] == -1 or next_value[1] < min[1]:
                    tmp = (column, next_value[1])
                    beta = next_value[1]

                if beta <= alpha:
                    break

        return min if tmp is None else tmp


    def calc_score(self, taulell):
        # Calcula el puntaje basado en las fichas en el tablero
        score = 0
        # Evaluar filas
        for row in range(self.mida[0]):
            for col in range(self.mida[1] - 3):
                score += self.calc_score_position(row, col, 0, 1, taulell)
        # Evaluar columnas
        for col in range(self.mida[1]):
            for row in range(self.mida[0] - 3):
                score += self.calc_score_position(row, col, 1, 0, taulell)
        # Evaluar diagonales ascendentes
        for row in range(self.mida[0] - 3):
            for col in range(self.mida[1] - 3):
                score += self.calc_score_position(row, col, 1, 1, taulell)
        # Evaluar diagonales descendentes
        for row in range(3, self.mida[0]):
            for col in range(self.mida[1] - 3):
                score += self.calc_score_position(row, col, -1, 1, taulell)
        return score    

    def minimax(self, alpha=float('-inf'), beta=float('inf')):
        best_move = self.max_play(self.taulell, alpha, beta)
        return best_move 
   
class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | Tuple[entorn.Accio, object]:
        estat_actual = Estat( 
            taulell=percepcio[SENSOR.TAULELL],   
            mida=percepcio[SENSOR.MIDA]        
        )
        if estat_actual.es_meta():
            return Accio.ESPERAR
        else:
            millor_accio = estat_actual.minimax()
            #print(millor_accio)
            return Accio.POSAR,millor_accio