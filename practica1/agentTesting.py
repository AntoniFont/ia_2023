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


class Agent(joc.Agent):
    def __init__(self, nom):
        self.primeraExecucio = True
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
        if(self.numACCIONSFETES > len(self.__ACCIONSPERFER) - 1):
            return Accio.ESPERAR
        else:
            accio = self.__ACCIONSPERFER[self.numACCIONSFETES]
            self.numACCIONSFETES = self.numACCIONSFETES + 1
        return accio
        
    