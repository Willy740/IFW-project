import shutil
from pathlib import Path
from datetime import datetime

script_dir = Path(__file__).parent.resolve()			#
geschiedenis_bestand = script_dir / "geschiedenis.txt"		# opgezocht hoe zo efficient mogelijk
backup_dir = Path.home() / ".played-games"			#

def maak_backup():
    backup_dir.mkdir(parents=True, exist_ok=True)

    if not geschiedenis_bestand.exists():
        print(f"Fout: '{geschiedenis_bestand}' niet gevonden.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_bestand = backup_dir / f"geschiedenis_{timestamp}.txt"
    shutil.copy2(geschiedenis_bestand, backup_bestand)
    print(f"Backup aangemaakt: {backup_bestand}")
    return True

if __name__ == "__main__":
    maak_backup()
