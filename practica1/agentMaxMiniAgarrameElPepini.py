"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio,SENSOR,TipusCasella
from copy import deepcopy

class EstatMaxMini():

    def __init__(self,tauler,accionsPrevies = []):
        self.tauler = tauler
        self.accions_previes = accionsPrevies
    
    #Cerca per tot el tauler i retorna la ratlla amb posibilitats de ser completada
    #mes gran que hi hagi del jugador seleccionat 
    #Una ratlla de 3, ex:(x x x o) que mai pugi ser completada contará com a 0.
    def calc_score(self,jugador):
        #
        #(x) x x x
        #
        #
        HORITZONTAL = ((0,0),(1,0),(2,0),(3,0))
        # (x)
        #  x
        #  x
        #  x
        VERTICAL = ((0,0),(0,1),(0,2),(0,3))
        # (x)
        #   x
        #    x
        #     x
        DIAGONAL_INF = ((0,0),(1,1),(2,2),(3,3))
        #        x
        #      x
        #    x
        # (x)
        DIAGONAL_SUP = ((0,0),(1,-1),(2,-2),(3,-3))
        ratlles_valides = (HORITZONTAL,VERTICAL,DIAGONAL_INF,DIAGONAL_SUP)    
        puntuacions = [0, # Ratlla horitzontal mes llarga, en percentatge respecte a 4 en ratlla
                       0, # Ratlla vertical mes llarga, en percentatge respecte a 4 en ratlla
                       0, # Ratlla diagonal_inf mes llarga, en percentatge respecte a 4 en ratlla
                       0] # Ratlla diagonal_sup mes llarga, en percentatge respecte a 4 en ratlla
        for fila in range(len(self.tauler)):
            for columna in (range(len(self.tauler[0]))):
                if(self.tauler[fila][columna] == jugador):
                    for i in range(len(ratlles_valides)):
                        ratlla = ratlles_valides[i]
                        percentatgeRatllaCompletat = self.percentatgePatroCompletat(fila,columna,ratlla,jugador)
                        if(percentatgeRatllaCompletat > puntuacions[i]):
                            puntuacions[i] = percentatgeRatllaCompletat
        return max(puntuacions)

    #Retorna el percentatge del patró que has completat. Si mai podràs completar el patró(perque un altre jugador
    # bloquetja la posibilitat), retorna 0.
    def percentatgePatroCompletat(self,x_inicial,y_inicial,patro,jugador):
        pasosDelPatroCompletats = 0
        for x,y in patro:
            if(self._estaOcupatPerJugador(x_inicial + x,y_inicial + y,jugador)):
                pasosDelPatroCompletats = pasosDelPatroCompletats + 1
            elif(self._estaOcupatPerJugador(x_inicial + x,y_inicial + y,TipusCasella.LLIURE)):
                pass
                #No fer res, encara hi ha potencial per completar mes patró
            else: # Esta ocupat per jugador rival 
                if(pasosDelPatroCompletats != len(patro)): #Mai podràs completar tot el patró, puntuació 0.
                    pasosDelPatroCompletats = 0
        return pasosDelPatroCompletats / len(patro)

    #Retorna true si existeix un cuatre en ratlla del nostre jugador.
    def es_meta(self):
        self.calc_score(TipusCasella.CARA) == 4

    #Retorna True si una posicio esta ocupada, false si no esta ocupada i false també si la posicio esta
    #fora del tauler
    def _estaOcupatPerJugador(self,fila,columna,jugador):
        #Suposam que el tauler es sempre un quadrat
        if fila < 0 or columna < 0 or fila > len(self.tauler)-1 or columna > len(self.tauler)-1:
            return False
        else :
            return self.tauler[fila][columna] == jugador
        
    def genera_fill(self):
        fills = []
        for fila in range(len(self.tauler)):
            for columna in (range(len(self.tauler[0]))):
                if(self.tauler[fila][columna] == TipusCasella.LLIURE):
                    nouTauler = deepcopy(self.tauler)
                    nouAccionsPrevies = deepcopy(self.accions_previes)
                    nouTauler[fila][columna] = TipusCasella.CARA
                    nouAccionsPrevies.append((Accio.POSAR,(fila,columna)))
                    fills.append(EstatProfunditat(nouTauler,nouAccionsPrevies)) 
        return fills



class Agent(joc.Agent):
    def __init__(self, nom):
        self.primeraExecucio = True       
        self.__ACCIONSPERFER = [
            (Accio.POSAR,(3,5)),
            (Accio.POSAR,(4,4)),
            (Accio.POSAR,(5,3)),
            (Accio.POSAR,(6,2))
        ]
        
        self.numACCIONSFETES = 0
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass
 
    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:        
        print(EstatMaxMini(percepcio[SENSOR.TAULELL]).calc_score(TipusCasella.CARA))
        if(self.numACCIONSFETES > len(self.__ACCIONSPERFER) - 1):
            return Accio.ESPERAR
        else:
            accio = self.__ACCIONSPERFER[self.numACCIONSFETES]
            self.numACCIONSFETES = self.numACCIONSFETES + 1
        return accio
        
    