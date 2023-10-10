import sys
sys.path.append("C:\\Users\\Toniuni\\Desktop\\Curso 23-24\\IA\\ia_2023")
sys.path.append("C:\\Users\\marij\\Desktop\\IA")
from quiques import agent_amplada, agent_profunditat, joc


def main():
    barca = agent_profunditat.BarcaProfunditat()
    illes = joc.Illes([barca])
    illes.comencar()


if __name__ == "__main__":
    main()
