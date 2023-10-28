"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio,SENSOR,TipusCasella



class EstatProfunditat():

    def __init__(self,tauler):
        self.tauler = tauler

    #Hem de revisar si a cualque lloc del tauler existeix un cuatre en ratlla, ho farem de manera bruta encara que existeixen
    #maneres mes eficients de trobar-ho
    def es_meta(self):
        for fila in range(len(self.tauler)):
            for columna in (range(len(self.tauler[0]))):
                # Suposam que el lloc sempre serà cuatre en ratlla i no un altre número en ratlla.
                if(self.tauler[fila][columna] == TipusCasella.CARA):
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
        if fila < 0 or columna < 0 or fila > len(self.tauler) or columna > len(self.tauler):
            return False
        else :
            return self.tauler[fila][columna] == TipusCasella.CARA
    

class Agent(joc.Agent):
    def __init__(self, nom):
        #pa abajo
        """self.__ACCIONSPERFER = [
            (Accio.POSAR,(2,2)),
            (Accio.POSAR,(2,3)),
            (Accio.POSAR,(2,4)),
            (Accio.POSAR,(2,5))
        ]"""

        # - - - - 
        """
        self.__ACCIONSPERFER = [
            (Accio.POSAR,(2,2)),
            (Accio.POSAR,(3,2)),
            (Accio.POSAR,(4,2)),
            (Accio.POSAR,(5,2))
        ]"""
        # diagonal
        """
        self.__ACCIONSPERFER = [
            (Accio.POSAR,(1,2)),
            (Accio.POSAR,(2,3)),
            (Accio.POSAR,(3,4)),
            (Accio.POSAR,(4,5))
        ]
        """
        
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
        estat = EstatProfunditat(percepcio[SENSOR.TAULELL])
        print(estat.es_meta())
        if(self.numACCIONSFETES > len(self.__ACCIONSPERFER) - 1):
            return Accio.ESPERAR
        else:
            accio = self.__ACCIONSPERFER[self.numACCIONSFETES]
            self.numACCIONSFETES = self.numACCIONSFETES + 1
        return accio

    def cercaamplada(self,estatInicial):
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
                #Nomes afegirem els estats que son segurs, legals
                #i que encara no hem visitat                
                for fill in fills:
                    if(fill.es_segur() and fill.legal() and fill not in self.__tancats):
                        self.__oberts.append(fill)
        return False
    