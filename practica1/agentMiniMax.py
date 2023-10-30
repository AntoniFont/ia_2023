"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""

from errno import ERANGE
from typing import List, Tuple

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, TipusCasella, SENSOR

class Estat:
    def __init__(self, taulell, mida):
        self.taulell = taulell
        self.mida = mida
        self.depth = 0
        self.maxScore = 1000
        self.minScore = -1000
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
            return self.tauler[fila][columna] == TipusCasella.CARA    

    def calc_score_position(self, row, col, inc_row, inc_col, taulell):
        ai_points = 0
        player_points = 0

        for i in range(4):  # connect "4"
            if taulell[col][row] == 2:
                ai_points += 1
            elif taulell[col][row] == 1:
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
        return self.depth >= 4 or self.is_full(taulell) or score >= self.maxScore or score <= self.minScore
    
    def clone(self, taulell):
        cloned_board = [[cell for cell in row] for row in taulell]
        return cloned_board
    
    def place(self, taulell, col, is_max):
        if taulell[col][0] == TipusCasella.LLIURE and 0 <= col < self.mida[1]:
            for j in range(self.mida[0] - 1, -1, -1):
                if taulell[col][j] == TipusCasella.LLIURE:
                    taulell[col][j] = TipusCasella.CARA if is_max else TipusCasella.CREU
                    return True
        return False

    def max_play(self, taulell, alpha, beta):
        score = self.calc_score(taulell)

        if self.is_done(self, score):
            return [-1, score]

        max_value = [-1, 0]

        for column in range(self.mida[1]):
            tmp_taulell = self.clone(taulell)
            if self.place(tmp_taulell, column, True):
                self.depth += 1
                next_value = self.min_play(self, tmp_taulell, alpha, beta)

                if max_value[0] == -1 or next_value[1] > max_value[1]:
                    max_value[0] = column
                    max_value[1] = next_value[1]
                    alpha = next_value[1]

                if beta <= alpha:
                    return max_value

        return max_value

    def min_play(self, taulell, alpha, beta):
        score = self.calc_score(taulell)

        if self.is_done(self, taulell, score):
            return [-1, score]

        min_value = [-1, 0]

        for column in range(self.mida[1]):
            tmp_taulell = self.clone(taulell)
            if self.place(tmp_taulell, column, False):
                self.depth += 1
                next_value = self.max_play(self, tmp_taulell, alpha, beta)

                if min_value[0] == -1 or next_value[1] < min_value[1]:
                    min_value[0] = column
                    min_value[1] = next_value[1]
                    beta = next_value[1]

                if beta <= alpha:
                    return min_value

        return min_value
       

    def calc_score(self, taulell):

        rows = self.mida[0]
        cols = self.mida[1]
        vertical_points = 0
        horizontal_points = 0
        desc_diagonal_points = 0
        asc_diagonal_points = 0
        total_points = 0

        for row in range(rows - 3):
            for column in range(rows):
                tmp_punt = self.calc_score_position(row, column, 1, 0, taulell)
                vertical_points += tmp_punt
                if tmp_punt >= self.maxScore or tmp_punt <= self.minScore:
                    return tmp_punt

        for row in range(rows):
            for column in range(cols - 3):
                tmp_punt = self.calc_score_position(row, column, 0, 1, taulell)
                horizontal_points += tmp_punt
                if tmp_punt >= self.maxScore or tmp_punt <= self.minScore:
                    return tmp_punt

        for row in range(rows - 3):
            for column in range(cols - 3):
                tmp_punt = self.calc_score_position(row, column, 1, 1, taulell)
                desc_diagonal_points += tmp_punt
                if tmp_punt >= self.maxScore or tmp_punt <= self.minScore:
                    return tmp_punt

        for row in range(3, rows):
            for column in range(cols - 4):
                tmp_punt = self.calc_score_position(row, column, -1, 1, taulell)
                asc_diagonal_points += tmp_punt
                if tmp_punt >= self.maxScore or tmp_punt <= self.minScore:
                    return tmp_punt

        total_points = vertical_points + horizontal_points + desc_diagonal_points + asc_diagonal_points
        return total_points     

    def minimax(self, alpha=float('-inf'), beta=float('inf')):       
          self.max_play(self.taulell, alpha, beta)    

    
    
   
   
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

            return millor_accio