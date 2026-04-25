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
