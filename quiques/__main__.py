import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
from quiques import agent_amplada, agent_profunditat, joc


def main():
    barca = agent_amplada.BarcaAmplada()
    illes = joc.Illes([barca])
    illes.comencar()


if __name__ == "__main__":
    main()
