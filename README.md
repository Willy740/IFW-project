# IFW-project

Een Python-tool om het **Erdős kant-kleurspel** (edge-colouring game) op grafen te analyseren. Het programma roept een externe solver aan, visualiseert de grafen, en houdt een geschiedenis bij van de resultaten.

---

## Vereisten

- Python 3.11+ (voor `tomllib`)
- De volgende Python-pakketten:
  - `networkx`
  - `matplotlib`
- `bash` (voor het uitvoeren van de solver)
- De map `edge-colouring-games/` met daarin `Erdos-Game-Generic.sh`

Installeer de Python-afhankelijkheden via:

```bash
pip install networkx matplotlib
```

---

## Installatie

```bash
git clone https://github.com/Willy740/IFW-project.git
cd IFW-project
```

Maak eventueel een virtuele omgeving aan en activeer die:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Configuratie

Pas `config.toml` aan voor je experiment. De relevante velden staan onder `[game]`:

```toml
[project]
name = "IFW-project"

[game]
n              = 5           # aantal knopen in de graaf
base_graph     = "CF"        # startgraaf in graph6-formaat
red_graph      = "A_"        # startgraaf voor rood in graph6-formaat
blue_graph     = "?"         # startgraaf voor blauw in graph6-formaat
bias           = 1           # bias van het spel
threads        = 4           # aantal threads voor de solver
starting_player = 1          # beginspeler (1 = rood, 2 = blauw)
```

> Grafen worden opgegeven in **graph6-formaat** (bijv. `"CF"`, `"A_"`).  
> Zie de README van `Erdos-Game-Generic.sh` voor de exacte betekenis van elke parameter.

---

## Gebruik

Start het programma vanuit de hoofdmap van het project:

```bash
python main.py
```

### Wat het programma doet

1. **Config laden** — leest `config.toml` in en toont de instellingen.
2. **Visualisatie (optioneel)** — vraagt of je de drie startgrafen wil tekenen. Als je `ja` antwoordt, worden drie PNG-bestanden aangemaakt:
   - `graaf_start.png`
   - `graaf_rood.png`
   - `graaf_blauw.png`
3. **Solver aanroepen** — roept `edge-colouring-games/Erdos-Game-Generic.sh` aan met de parameters uit de config.
4. **Resultaat parsen** — leest de uitvoer van de solver en bepaalt wie gewonnen heeft (rood of blauw) en de bijbehorende score.
5. **Geschiedenis opslaan** — voegt een regel toe aan `geschiedenis.txt` met tijdstip, grafen, bias, winnaar en score.

---

## Projectstructuur

```
IFW-project/
├── edge-colouring-games/
│   └── Erdos-Game-Generic.sh   # externe solver
├── main.py                     # hoofdscript
├── config.toml                 # configuratiebestand
├── geschiedenis.txt            # automatisch bijgehouden resultaten
└── README.md
```

---

## Geschiedenis bekijken

Elk uitgevoerd spel wordt weggeschreven in `geschiedenis.txt` als een tab-gescheiden regel:

```
<tijdstip>    <startgraaf>    <rood>    <blauw>    <bias>    <winnaar>    <score>
```

Je kan dit bestand openen met een teksteditor of inladen in een spreadsheet voor verdere analyse.

---

## Bekende beperkingen / werk in uitvoering

- De `config.toml` bevat nog velden (`threads`, `starting_player`, `n`) die momenteel niet in alle versies zichtbaar zijn — controleer of je versie van het bestand volledig is.
- De solver vereist een Unix-omgeving met `bash`. Op Windows gebruik je best WSL.
- Foutafhandeling bij ongeldige graph6-strings is nog minimaal.
