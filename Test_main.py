import pytest
from unittest.mock import patch

# prevent main() from running on import
with patch("builtins.input", return_value="nee"):       # opgezocht
    import main as m


# teste parseer


class TestParseerResultaat:

    def test_red_wins(self):
        uitvoer = "Red wins\nScore: 3\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar == "rood"
        assert score == 3

    def test_red_wins_upper_case(self):
        uitvoer = "RED WINS\nScore: 7\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar == "rood"

    def test_blue_wins(self):
        uitvoer = "Blue wins\nScore: 3\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar == "blauw"
        assert score == 3

    def test_blue_wins_uper_case(self):
        uitvoer = "BLUE WINS\nScore: 7\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar == "blauw"

    def test_score_zero(self):
        uitvoer = "Red wins\nScore: 0\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert score == 0

    def test_score_large_number(self):
        uitvoer = "Blue wins\nScore: 999\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert score == 999
    def test_empty_output(self):
        winnaar, score = m.parseer_resultaat("")
        assert winnaar is None
        assert score == 0

    def test_no_winner_line(self):
        uitvoer = "Score: 4\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar is None
        assert score == 4

    def test_no_score_line(self):
        uitvoer = "Red wins\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar == "rood"
        assert score == 0

    def test_invalid_score_value(self):
        uitvoer = "Blue wins\nScore: !çfhi\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar == "blauw"
        assert score == 0

    def test_random_output(self):
        uitvoer = "random\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert winnaar is None
        assert score == 0

    def test_multiple_score_lines_last_wins(self):
        uitvoer = "Red wins\nScore: 1\nScore: 42\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        assert score == 42

    # we verwachten een error omdat splitlines() geen None kan verwerken
    def test_none_input(self):
        with pytest.raises(AttributeError):
            m.parseer_resultaat(None)

# testen geschiedenis

class TestSlaGeschiedenisOp:

    def test_line_is_appended(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
        assert len(bestand.read().splitlines()) == 1

    def test_columns_in_line(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
        cols = bestand.read().strip().split("\t")
        assert len(cols) == 7  # timestamp + 6 argumenten

    def test_data_present_in_line(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("XY", "AB", "CD", 2, "blauw", 7)
        content = bestand.read()
        assert "XY" in content
        assert "AB" in content
        assert "CD" in content
        assert "blauw" in content
        assert "7" in content

    def test_multiple_lines(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
        assert len(bestand.read().splitlines()) == 2

    def test_none_winner(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, None, 3)
        assert "None" in bestand.read() # checkt of None in geschiedenis staat
    def test_no_graphs(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("", "", "", 1, "rood", 3)
        assert len(bestand.read()) > 0

    def test_negative_score(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", -1)
        assert "-1" in bestand.read()

    def test_wrong_order(self, tmpdir):
        bestand = tmpdir.join("geschiedenis.txt")
        with patch.object(m, "geschiedenis", str(bestand)):
            m.sla_geschiedenis_op(3, "rood", 1, "?", "A_", "CF")  # omgekeerde volgorde
        cols = bestand.read().strip().split("\t")
        assert cols[1] != "CF"
        assert cols[5] != "rood"
