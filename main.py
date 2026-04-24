import tomllib
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

geschiedenis= "geschiedenis.txt"
solver		= "edge-colouring-games/Erdos-Game-Generic.sh"

##################### config laden #################################

def laad_config(pad):
    with open(pad, "rb") as f:          # opgezocht, r werkte niet
        return tomllib.load(f)


##################### solver aanroepen ##############################

def roep_solver_aan(n, start, red, blue, threads, starting_player): # gecorigeerd door AI door start toe te voegen
    commando = [				# uit de README van de solver gehaald
        "bash", solver,				#
        str(n), start, red, blue,		#
        str(threads), str(starting_player),	#
    ]

    print(f"\nSolver starten")
    print(f"  commando: {' '.join(commando)}")

    resultaat = subprocess.run(
        commando,
        capture_output=True,    # stdout en stderr opvangen (opgezocht)
        text=True,              # als tekst teruggeven
    )

    if resultaat.returncode == 0:	# in README van solver staat dat returncode = 0 succes is en bij de rest is er iets fout gegaan
        print("  Solver klaar.")
        print(resultaat.stdout)		# opgezocht stdout
    else:
	print(f"  FOUT (returncode {resultaat.returncode}):")
        print(resultaat.stderr)		# opgezocht stderr

    return resultaat.stdout


def parseer_resultaat(uitvoer):			# AI gegenereerd zal dit nog eens moeten opzoeken in de README van de solver
    winnaar = None
    score   = 0

    for regel in uitvoer.splitlines():
        regel = regel.strip().lower()
        if regel.startswith("red wins"):
            winnaar = "rood"
        elif regel.startswith("blue wins"):
            winnaar = "blauw"
        elif regel.startswith("score:"):
            try:
                score = int(regel.split(":")[1].strip())
            except ValueError:
                pass

    return winnaar, score


##################### visualisatie #################################

def teken_graaf(graph6, titel, bestandsnaam):
    G = nx.from_graph6_bytes(graph6.encode())   # opgezocht

    print(f"\n  {titel} ({graph6})")
    print(f"    knopen : {G.number_of_nodes()}")
    print(f"    bogen  : {G.number_of_edges()}")
    print(f"    knopen : {list(G.nodes)}")
    print(f"    bogen  : {list(G.edges)}")

    nx.draw(G, with_labels=True, font_weight="bold")    # uit tutorial
    plt.title(titel)
    plt.savefig(f"{bestandsnaam}.png")                  # opgezocht
    plt.clf()                                           # leegmaken anders grafen over elkaar
    print(f"    opgeslagen als {bestandsnaam}.png")


def visualiseer_spelgrafen(start, red, blue):
    print("\n=== Visualisatie van de spelgrafen ===")
    teken_graaf(start, "Startgraaf",         "graaf_start")
    teken_graaf(red,   "Startgraaf Rood",    "graaf_rood")
    teken_graaf(blue,  "Startgraaf Blauw",   "graaf_blauw")


#################### geschiedenis #######################################
def sla_geschiedenis_op(start, red, blue, bias, winnaar, score):
    timestamp = datetime.now()
    regel = f"{timestamp}\t{start}\t{red}\t{blue}\t{bias}\t{winnaar}\t{score}\n"

    with open(geschiedenis, "a") as g:
        g.write(regel)

    print(f"\n  Geschiedenis opgeslagen in '{geschiedenis}'.")


############################# Main ###############################################

def main():
    # config laden
    config          = laad_config("config.toml")
    spel            = config["game"]
    n               = spel["n"]
    start_graph     = spel["base_graph"]
    red_graph       = spel["red_graph"]
    blue_graph      = spel["blue_graph"]
    bias            = spel["bias"]
    threads         = spel["threads"]
    starting_player = spel["starting_player"]

    print(f"Project : {config['project']['name']}")
    print(f"n={n}, start={start_graph}, rood={red_graph}, blauw={blue_graph}")
    print(f"bias={bias}  threads={threads}  beginspeler={starting_player}")

    # visualisatie
    keuze = input("\nWil je de startgrafen visualiseren? (ja/nee): ").strip().lower()
    if keuze == "ja":
        visualiseer_spelgrafen(start_graph, red_graph, blue_graph)

    # solver aanroepen
    uitvoer = roep_solver_aan(n, start_graph, red_graph, blue_graph,
                               threads, starting_player)

    # resultaat parsen
    winnaar, score = parseer_resultaat(uitvoer)

    # geschiedenis opslaan
    sla_geschiedenis_op(start_graph, red_graph, blue_graph, bias, winnaar, score)


if __name__ == "__main__":
    main()

