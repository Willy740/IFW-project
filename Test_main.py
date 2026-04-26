import os
import tempfile
import unittest
from unittest.mock import patch, mock_open, MagicMock
import importlib, sys

# prevent main from running on import
with patch("builtins.input", return_value="nee"): # opgezocht
    import main as m



class TestParseerResultaat(unittest.TestCase):          # (unittest.TestCase opgezocht)

    # testing if parseer_resultaat reads the output correctly

    # red wins (lower case)
    def test_red_wins(self):
        uitvoer = "Red wins\nScore: 3\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(winnaar, "rood")
        self.assertEqual(score, 3)

    # red wins (upper case)
    def test_red_wins_case_insensitive(self):
        uitvoer = "RED WINS\nScore: 7\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(winnaar, "rood")

    # blue wins (lower case)
    def test_blue_wins(self):
        uitvoer = "Blue wins\nScore: 3\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(winnaar, "blauw")
        self.assertEqual(score, 5)

    def test_blue_wins_case_insensitive(self):
        uitvoer = "BLUE WINS\nScore: 7\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(winnaar, "blauw")

    # edge cases

    def test_score_zero(self):
        uitvoer = "Red wins\nScore: 0\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(score, 0)

    def test_score_large_number(self):
        uitvoer = "Blue wins\nScore: 999\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(score, 999)

    # testing empty output
    def test_empty_output(self):
        winnaar, score = m.parseer_resultaat("")
        self.assertIsNone(winnaar)      # basic (see main)
        self.assertEqual(score, 0)      # basic value (see main

    # testing with only score given
    def test_no_winner_line(self):
        uitvoer = "Score: 4\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertIsNone(winnaar)
        self.assertEqual(score, 4)

    # testing with only winner given
    def test_no_score_line(self):
        uitvoer = "Red wins\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(winnaar, "rood")
        self.assertEqual(score, 0)

    # testing if the score isn't a integer
    def test_invalid_score_value(self):
        uitvoer = "Blue wins\nScore: !çfhi\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(winnaar, "blauw")
        self.assertEqual(score, 0)

    # testing if output is something random
    def test_garbage_output(self):
        uitvoer = "random\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertIsNone(winnaar)
        self.assertEqual(score, 0)

    # testing if there are multiple scores given
    def test_multiple_score_lines_last_wins(self):
        uitvoer = "Red wins\nScore: 1\nScore: 42\n"
        winnaar, score = m.parseer_resultaat(uitvoer)
        self.assertEqual(score, 42)     # in the main can you see that the firstscore is ov>

    # testing with no input                             opgezocht
    def test_none_input(self):
        with self.assertRaises(AttributeError):
            m.parseer_resultaat(None)



# TESTING GESCHIEDENIS

class TestSlaGeschiedenisOp(unittest.TestCase):

# setup en teardown opgezocht (blijkbaar herkent python die namen en doet het voor en na ie>

    def setUp(self):
        # Maak één tijdelijk bestand aan voor elke test
        self.tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
        # delete needs to be False else python will delete the file after closing
        self.tmp.close()

    def tearDown(self):
        # Verwijder het tijdelijke bestand na elke test
        os.unlink(self.tmp.name)

    def test_line_is_appended(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
        # opgezocht hoe je een tijdelijke kopie maakt van "geschiedenis" zodat de testen he>
        # daarvoor is de setup handig
	m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
        with open(self.tmp.name) as f:
            lines = f.read().splitlines()
        self.assertEqual(len(lines), 1)

    def test_columns_in_line(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
        with open(self.tmp.name) as f:
            cols = f.read().strip().split("\t")
        self.assertEqual(len(cols), 7)          # 6 arguments that need to be saved + a tim>

    def test_data_present_in_line(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op("XY", "AB", "CD", 2, "blauw", 7)
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertIn("XY", content)
        self.assertIn("AB", content)
        self.assertIn("CD", content)
        self.assertIn("blauw", content)
        self.assertIn("7", content)
    def test_multiple_calls_append(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", 3)
        with open(self.tmp.name) as f:
            lines = f.read().splitlines()
        self.assertEqual(len(lines), 2)

    def test_none_winner(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, None, 3)
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertIn("None", content)

    # testing if the program doesn't crash if there are nog graphs
    def test_empty_strings(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op("", "", "", 1, "rood", 3)
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertTrue(len(content) > 0)

    def test_negative_score(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op("CF", "A_", "?", 1, "rood", -1)
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertIn("-1", content)

    def test_wrong_order_raises_or_corrupts(self):
        with patch.object(m, "geschiedenis", self.tmp.name):
            m.sla_geschiedenis_op(3, "rood", 1, "?", "A_", "CF")  # reversed order
        with open(self.tmp.name) as f:
            content = f.read()
        cols = content.strip().split("\t")
        # opgezocht hoe testen welke positie
        self.assertNotEqual(cols[1], "CF")   # start staat niet meer op positie 1
        self.assertNotEqual(cols[5], "rood") # winnaar staat niet meer op positie 5


if __name__ == "__main__":
    unittest.main()
