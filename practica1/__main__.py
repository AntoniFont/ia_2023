import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
sys.path.append("C:\\Users\\juanjo\\Documents\\GitHub\\ia_2023")
from practica1 import agentProfunditat, agentMaxMiniAgarrameElPepini, joc,entorn


def main():    

    quatre = joc.Taulell([agentMaxMiniAgarrameElPepini.Agent("Miquel",entorn.TipusCasella.CARA),
                          agentMaxMiniAgarrameElPepini.Agent("Toni",entorn.TipusCasella.CREU)])
    quatre.comencar()


if __name__ == "__main__":
    main()
