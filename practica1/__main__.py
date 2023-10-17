import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
from practica1 import agentProfunditat, joc


def main():
    quatre = joc.Taulell([agentProfunditat.Agent("Miquel")])
    quatre.comencar()


if __name__ == "__main__":
    main()
