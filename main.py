import tomllib					# opgezocht welke import
with open("config_willy.toml","rb") as f:	# heb rb opgezocht
	config=tomllib.load(f)
# gegevens uit config_willy.toml halen

naam=config["project_name"]
frequentie=config["project"]["polling_frequency"]
drempel=config["project"]["alert_threshold"]

print(f"je kan beginnen met {naam}")
