"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio,SENSOR,TipusCasella


class Agent(joc.Agent):
    def __init__(self, nom):
        self.prueba = True
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass
 
    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        print(percepcio[SENSOR.MIDA])
        print("estat tauler "  + str(percepcio[SENSOR.TAULELL]))
        if(self.prueba == True):
            self.prueba = False
            return (Accio.POSAR,(2,2))
        else: 
            return Accio.ESPERAR