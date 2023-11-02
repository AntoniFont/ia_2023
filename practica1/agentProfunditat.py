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
import time


class EstatProfunditat():

    def __init__(self,tauler,accionsPrevies = []):
        self.tauler = tauler
        self.accions_previes = accionsPrevies
        
    #Retorna true si existeix un cuatre en ratlla del nostre jugador.
    def es_meta(self):
        for fila in range(len(self.tauler)):
            for columna in (range(len(self.tauler[0]))):
                # Suposam que el lloc sempre serà cuatre en ratlla i no un altre número en ratlla.
                if(self.tauler[fila][columna] == TipusCasella.CARA):
                    # (x) x x x
                    #
                    #
                    #
                    if(self._estaOcupatPerCara(fila +1,columna) and self._estaOcupatPerCara(fila +2, columna) and self._estaOcupatPerCara(fila + 3,columna)):
                        return True
                    # (x)
                    #  x
                    #  x
                    #  x
                    if(self._estaOcupatPerCara(fila,columna +1) and self._estaOcupatPerCara(fila, columna +2) and self._estaOcupatPerCara(fila,columna +3)):
                        return True
                    # (x)
                    #   x
                    #    x
                    #     x
                    if(self._estaOcupatPerCara(fila +1,columna +1) and self._estaOcupatPerCara(fila+2, columna +2) and self._estaOcupatPerCara(fila+3,columna +3)):
                        return True
                    #        x
                    #      x
                    #    x
                    # (x)    
                    if(self._estaOcupatPerCara(fila +1,columna -1) and self._estaOcupatPerCara(fila+2, columna -2) and self._estaOcupatPerCara(fila+3,columna -3)):
                        return True
        return False         

    #Retorna True si una posicio esta ocupada, false si no esta ocupada i false també si la posicio esta
    #fora del tauler
    def _estaOcupatPerCara(self,fila,columna):
        #Suposam que el tauler es sempre un quadrat
        if fila < 0 or columna < 0 or fila > len(self.tauler)-1 or columna > len(self.tauler)-1:
            return False
        else :
            return self.tauler[fila][columna] == TipusCasella.CARA
        
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
        self.__oberts = []
        self.__tancats = []
        self.__accions = []
        self.primeraExecucio = True
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass
 
    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:        
        if(self.primeraExecucio == True):
            self.primeraExecucio = False
            startTime = time.time()
            self.cercaprofunditat(EstatProfunditat(percepcio[SENSOR.TAULELL]))
            endTime = time.time()
            print("Duracio profunditat (segons): ", endTime-startTime)
            return Accio.ESPERAR
        else:
            if(len(self.__accions)!=0):
                accio = self.__accions.pop(0)
                return accio
            else:
                return Accio.ESPERAR
        
    def cercaprofunditat(self,estatInicial):
        self.__oberts = [estatInicial]
        self.__tancats = []
        while len(self.__oberts) != 0:
            estatActual = self.__oberts.pop(0)
            if(estatActual.es_meta()):
                self.__accions = estatActual.accions_previes
                self.__tancats.append(estatActual)
                return True
            else:
                fills = estatActual.genera_fill()
                self.__tancats.append(estatActual)
                #Nomes els fills que encara no hem visitat            
                for fill in fills:
                    if(fill not in self.__tancats):
                        self.__oberts.insert(0,fill)
        return False
    