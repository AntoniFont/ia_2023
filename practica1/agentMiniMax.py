"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from typing import Tuple

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, TipusCasella, SENSOR

class Estat:
    def __init__(self, taulell, mida) -> None:
        self.taulell = taulell
        self.mida = mida
        self.maxScore = 1000
        self.minScore = -1000
        self.torn_max = True
    
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
        return self.is_full(taulell) or score >= self.maxScore or score <= self.minScore
    
    def clone(self, taulell):
        cloned_board = [[cell for cell in row] for row in taulell]
        return cloned_board
    
    def place(self, taulell, col, is_max) -> bool:
        if taulell[col][0] == TipusCasella.LLIURE and 0 <= col < self.mida[1]:
            for j in range(self.mida[0] -1, -1, -1):
                if taulell[col][j] is TipusCasella.LLIURE:
                    taulell[col][j] = TipusCasella.CARA if is_max else TipusCasella.CREU
                    return True                  
        return False
    
    def minimax(self, is_max, depth, alpha, beta) -> Tuple:
        score = self.calc_score(self.taulell)
        
        if self.is_done(self.taulell, score) or depth == 0:
            return (-1, score)
        tmp = None
        
        if is_max:
            max_val = (-1, float('-inf'))
            for col in range(self.mida[1]):
                tmp_taulell = self.clone(self.taulell)
                if self.place(tmp_taulell, col, True):
                    value = self.minimax(False, depth - 1, alpha, beta)
                    if value[1] > max_val[1]:
                        tmp = (col, value[1])
                    alpha = max(alpha, value[1])
                    if beta <= alpha:
                        break
            return tmp
        else:
            min_val = (-1, float('inf'))            
            for col in range(self.mida[1]):
                tmp_taulell = self.clone(self.taulell)
                if self.place(tmp_taulell, col, False):
                    value = self.minimax(True, depth - 1, alpha, beta)
                    if value[1] < min_val[1]:
                        tmp = (col, value[1])
                    beta = min(beta, value[1])
                    if beta <= alpha:
                        break
            return tmp

    def minimax_decision(self, depth=8):
        best_move = self.minimax(True, depth, float('-inf'), float('inf'))
        return best_move

    def calc_score(self, taulell):
        vScore = 0
        hScore = 0
        ddScore = 0
        adScore = 0
        total_score = 0

        for row in range(self.mida[0] - 3):
            for col in range(self.mida[1]):
                tmp = self.calc_score_position(row, col, 1, 0, taulell)
                vScore += tmp
                if tmp >= self.maxScore or tmp <= self.minScore:
                    return tmp

        for row in range(self.mida[0]):
            for col in range(self.mida[1] - 3):
                tmp = self.calc_score_position(row, col, 0, 1, taulell)
                hScore += tmp
                if tmp >= self.maxScore or tmp <= self.minScore:
                    return tmp

        for row in range(self.mida[0] - 3):
            for col in range(self.mida[1] - 3):
                tmp = self.calc_score_position(row, col, 1, 1, taulell)
                ddScore += tmp
                if tmp >= self.maxScore or tmp <= self.minScore:
                    return tmp
        
        for row in range(3, self.mida[0]):
            for col in range(self.mida[1] - 4):
                tmp = self.calc_score_position(row, col, -1, 1, taulell)
                adScore += tmp
                if tmp >= self.maxScore or tmp <= self.minScore:
                    return tmp
        
        total_score = vScore + hScore + ddScore + adScore
        return total_score     
   
class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)
        self.a = True

    def pinta(self, display):
        pass

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | Tuple[entorn.Accio, object]:
        estat_actual = Estat( 
            taulell=percepcio[SENSOR.TAULELL],   
            mida=percepcio[SENSOR.MIDA]        
        )
        
        value = estat_actual.calc_score(percepcio[SENSOR.TAULELL])
        if value == estat_actual.maxScore or value == estat_actual.minScore:
            return Accio.ESPERAR
        else:
            millor_accio = estat_actual.minimax_decision()
            print(millor_accio)
            return Accio.POSAR, millor_accio  