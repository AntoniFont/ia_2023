import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
sys.path.append("C:\\Users\\juanjo\\Documents\\GitHub\\ia_2023")
sys.path.append("C:\\Users\\marij\\Desktop\\IA")
from practica1 import agentAstar, agentMiniMax,agentProfunditat, joc
from entorn import TipusCasella


def main():    

    #MINIMAX
    #quatre = joc.Taulell([agentMiniMax.Agent("Miquel",TipusCasella.CARA),agentMiniMax.Agent("Tomeu",TipusCasella.CREU)])
    #PROFUNDITAT
    #quatre = joc.Taulell([agentProfunditat.Agent("Miquel")])
    #A STAR
    quatre = joc.Taulell([agentAstar.Agent("Miquel")])
    


    quatre.comencar()


if __name__ == "__main__":
    main()
