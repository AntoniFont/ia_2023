import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
sys.path.append("C:\\Users\\juanjo\\Documents\\GitHub\\ia_2023")
sys.path.append("C:\\Users\\marij\\Desktop\\IA")
from practica1 import agentAstar, agentMaxMiniAgarrameElPepini, agentProfunditat,joc,entorn


def main():    

    #quatre = joc.Taulell([agentAstar.Agent("Miquel")])
    quatre = joc.Taulell([agentProfunditat.Agent("Miquel")])
    
    quatre.comencar()


if __name__ == "__main__":
    main()
