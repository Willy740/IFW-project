import tomllib					# opgezocht welke import
import networkx as nx				# zoals in tutorial
import matplotlib.pyplot as plt
with open("config.toml","rb") as f:		# heb rb opgezocht (r werkte niet)
	config=tomllib.load(f)
# gegevens uit config.toml halen

naam		= config["project_name"]
frequentie	= config["project"]["polling_frequency"]
drempel		= config["project"]["alert_threshold"]
graphs		= config["project"]["graphs"]

print(f"je kan beginnen met {naam}")

keuze=input("wil je de graaf visualiseren: ").strip().lower()	# zorgt dat het geen rekening houd met spaties en hoofdletters
if keuze=="ja":
	for i,string in enumerate(graphs):
		G=nx.from_graph6_bytes(string.encode())		# opgezocht

		print("")
		print(f"Graaf{i+1}:{string}")			# i+1 omdat het zou starten bij 1 ipv 0
		print(f"	aantal knopen: {G.number_of_nodes()}")
		print(f"	aantal bogen: {G.number_of_edges()}")
		print(f"	knopen: {list(G.nodes)}")
		print(f"	bogen: {list(G.edges)}")
		nx.draw(G, with_labels=True, font_weight='bold') # uit tutorial
		plt.show()
