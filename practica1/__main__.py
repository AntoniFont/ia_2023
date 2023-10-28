    import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
from practica1 import agentProfunditat, agentMiniMax, joc


def main():
    quatre = joc.Taulell([agentProfunditat.Agent("Miquel")])

    un = joc.Taulell([agentMiniMax.Agent("Miquel")])
    dos = joc.Taulell([agentMiniMax.Agent("Tomas")])

    un.comencar()
    dos.comencar()
    #quatre.comencar()


if __name__ == "__main__":
    main()
