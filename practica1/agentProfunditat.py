"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio,SENSOR,TipusCasella



class Estat():

    def __init__(self,tauler):
        self.tauler = tauler

    def es_meta():



class Agent(joc.Agent):
    def __init__(self, nom):
        self.__oberts = None
        self.__tancats = None
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass
 
    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:        
        print("estat tauler "  + str(percepcio[SENSOR.TAULELL]))
        return Accio.ESPERAR

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
    