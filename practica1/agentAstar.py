"""
ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from queue import PriorityQueue
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio,SENSOR,TipusCasella
from copy import deepcopy
import time

class Estat():

    def __init__(self, tauler, accionsPrevies = []):
        self.tauler = tauler
        self.accions_previes = accionsPrevies
        self.heuristica = self.calcul_heuristica() if accionsPrevies else 1000
        
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
        
    def calcul_heuristica(self) -> int:

        n = len(self.tauler[0])
        taulell = self.tauler
        l = len(self.accions_previes)
        darreraAccio = self.accions_previes[l-1][1]
        row = darreraAccio[0]
        col = darreraAccio[1]
        casella = taulell[row][col]
        count = 0

        direccions = [
            (1, 1),  # diagonal amunt dreta
            (-1, -1),# diagonal avall esquerra
            (-1, 1), # diagonal avall dreta
            (1, -1), # diagonal amunt esquerra
            (-1, 0), # amunt
            (1, 0),  # avall
            (0, 1),  # dreta
            (0, -1)  # esquerra
        ]

        #Comprovam per a cada moviment posible
        for i, j in direccions:
            #Cercam el 4 en linea
            for k in range(4):
                x = row + k * i
                y = col + k * j

                #si el moviment es legal
                if 0 <= x < n and 0 <= y < n:
                    #comprova que la casella a la que estam no sigui igual a la de la darrera acció
                    #per tal de millorar la heurística, incrementant el valor de les caselles de la darrera acció
                    if casella == taulell[x][y]:
                        count += 1
        #totes les combinacions on es pot fer 4 en linea menys el count
        return 3 * len(direccions) - count  
        
    def genera_fill(self):
        fills = []
        for fila in range(len(self.tauler)):
            for columna in (range(len(self.tauler[0]))):
                if(self.tauler[fila][columna] == TipusCasella.LLIURE):
                    nouTauler = deepcopy(self.tauler)
                    nouAccionsPrevies = deepcopy(self.accions_previes)
                    nouTauler[fila][columna] = TipusCasella.CARA
                    nouAccionsPrevies.append((Accio.POSAR,(fila,columna)))
                    fills.append(Estat(nouTauler, nouAccionsPrevies)) 
        return fills
    
    def __lt__(self, altre):
        return self.f()<altre.f()
    
    def pes(self):
        return len(self.accions_previes)
    
    def f(self):
        return self.heuristica + self.pes()
    
class CoaPrioridad(PriorityQueue):
    def __init__(self):
        super(CoaPrioridad,self).__init__()
    
    def contains(self,elem):
        for i in range(super().qsize()):
            elemeLlista = self.getSenseTreure(i)
            if (elem == elemeLlista):
                return elemeLlista
                        
    def getSenseTreure(self,index):
        eleme = super().get(index)
        super().put(eleme)
        return eleme
    
    def put(self,elem):
        super().put(elem)
    
    def get(self,elem):
        return super().get(elem)
    
class Agent(joc.Agent):
    
    def __init__(self, nom):
        self.__oberts = PriorityQueue()
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
            self.cerca(Estat(
                percepcio[SENSOR.TAULELL]
                ))
            endTime = time.time()
            print("Duracio a* (segons): ", endTime-startTime)
            return Accio.ESPERAR
        else:
            if(len(self.__accions)!=0):
                accio = self.__accions.pop(0)
                return accio
            else:
                return Accio.ESPERAR
        
    def cerca(self,estatInicial):
        self.__oberts = CoaPrioridad()
        self.__oberts.put(estatInicial)
        self.__tancats = []
        while not self.__oberts.empty():
            estatActual = self.__oberts.get(0)
            self.__tancats.append(estatActual)
            if(estatActual.es_meta()):
                self.__accions = estatActual.accions_previes
                return True
            else:
                fills = estatActual.genera_fill()
                #Nomes els fills que encara no hem visitat           
                for fill in fills:
                    if(fill in self.__tancats):
                        break
                    if(self.__oberts.contains(fill)):
                        primer = self.__oberts.getSenseTreure()
                        if(fill.pes() > primer): 
                            break
                    
                    self.__oberts.put(fill)
        return False
