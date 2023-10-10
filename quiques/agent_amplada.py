from ia_2022 import entorn
from quiques.agent import Barca, Estat
from quiques.entorn import AccionsBarca, SENSOR


class BarcaAmplada(Barca):
    def __init__(self):
        super(BarcaAmplada, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
        self.primeraExecucio = True
                        
    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        if(self.primeraExecucio):
            self.primeraExecucio = False
            estatActual = Estat(percepcio[SENSOR.LLOC],percepcio[SENSOR.LLOP_ESQ],percepcio[SENSOR.QUICA_ESQ])
            self.cercaamplada(estatActual)
        if(len(self.__accions)!=0):
            accio = self.__accions.pop(0)
            return (AccionsBarca.MOURE, accio)
        else:
            return AccionsBarca.ATURAR
    
    
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
    