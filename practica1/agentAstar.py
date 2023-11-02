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
    
    def pes(self):
        return self.heuristica + len(self.accions_previes)
    

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
            self.cerca(Estat(
                percepcio[SENSOR.TAULELL]
                ))
            return Accio.ESPERAR
        else:
            if(len(self.__accions)!=0):
                accio = self.__accions.pop(0)
                return accio
            else:
                return Accio.ESPERAR
        
    def cerca(self,estatInicial):
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
                bestFill = fills[0]
                for fill in fills:
                    if(fill.pes() < bestFill.pes()):
                        bestFill = fill
                self.__oberts.insert(0,bestFill)
        return False
