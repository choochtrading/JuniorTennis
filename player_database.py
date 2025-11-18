"""
Player Database for ATP Tennis Prediction Model
Stores player information and statistics
"""

import json
import os
from typing import Dict, List, Optional

class PlayerDatabase:
    """Manages player data and statistics."""
    
    def __init__(self, db_file='players.json'):
        self.db_file = db_file
        self.players = self.load_players()
        
    def load_players(self) -> Dict:
        """Load players from JSON file or create default database."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return self._create_default_database()
        else:
            return self._create_default_database()
    
    def save_players(self):
        """Save players to JSON file."""
        with open(self.db_file, 'w') as f:
            json.dump(self.players, f, indent=2)
    
    def _create_default_database(self) -> Dict:
        """Create a default database with sample ATP players."""
        default_players = {
            "Novak Djokovic": {
                "rank": 1,
                "win_rate": 0.85,
                "hard_win_rate": 0.87,
                "clay_win_rate": 0.82,
                "grass_win_rate": 0.88,
                "recent_form": 0.83,
                "age": 37
            },
            "Carlos Alcaraz": {
                "rank": 2,
                "win_rate": 0.80,
                "hard_win_rate": 0.78,
                "clay_win_rate": 0.85,
                "grass_win_rate": 0.75,
                "recent_form": 0.82,
                "age": 21
            },
            "Daniil Medvedev": {
                "rank": 3,
                "win_rate": 0.78,
                "hard_win_rate": 0.82,
                "clay_win_rate": 0.65,
                "grass_win_rate": 0.70,
                "recent_form": 0.80,
                "age": 28
            },
            "Jannik Sinner": {
                "rank": 4,
                "win_rate": 0.77,
                "hard_win_rate": 0.80,
                "clay_win_rate": 0.72,
                "grass_win_rate": 0.75,
                "recent_form": 0.85,
                "age": 22
            },
            "Andrey Rublev": {
                "rank": 5,
                "win_rate": 0.72,
                "hard_win_rate": 0.70,
                "clay_win_rate": 0.75,
                "grass_win_rate": 0.68,
                "recent_form": 0.70,
                "age": 26
            },
            "Stefanos Tsitsipas": {
                "rank": 6,
                "win_rate": 0.71,
                "hard_win_rate": 0.68,
                "clay_win_rate": 0.78,
                "grass_win_rate": 0.65,
                "recent_form": 0.72,
                "age": 25
            },
            "Casper Ruud": {
                "rank": 7,
                "win_rate": 0.70,
                "hard_win_rate": 0.65,
                "clay_win_rate": 0.80,
                "grass_win_rate": 0.60,
                "recent_form": 0.68,
                "age": 25
            },
            "Alexander Zverev": {
                "rank": 8,
                "win_rate": 0.69,
                "hard_win_rate": 0.72,
                "clay_win_rate": 0.70,
                "grass_win_rate": 0.65,
                "recent_form": 0.75,
                "age": 27
            },
            "Holger Rune": {
                "rank": 9,
                "win_rate": 0.68,
                "hard_win_rate": 0.70,
                "clay_win_rate": 0.72,
                "grass_win_rate": 0.65,
                "recent_form": 0.65,
                "age": 21
            },
            "Taylor Fritz": {
                "rank": 10,
                "win_rate": 0.67,
                "hard_win_rate": 0.72,
                "clay_win_rate": 0.58,
                "grass_win_rate": 0.70,
                "recent_form": 0.70,
                "age": 26
            },
            "Grigor Dimitrov": {
                "rank": 11,
                "win_rate": 0.66,
                "hard_win_rate": 0.68,
                "clay_win_rate": 0.62,
                "grass_win_rate": 0.72,
                "recent_form": 0.75,
                "age": 33
            },
            "Tommy Paul": {
                "rank": 12,
                "win_rate": 0.65,
                "hard_win_rate": 0.70,
                "clay_win_rate": 0.58,
                "grass_win_rate": 0.68,
                "recent_form": 0.68,
                "age": 27
            },
            "Ben Shelton": {
                "rank": 13,
                "win_rate": 0.64,
                "hard_win_rate": 0.68,
                "clay_win_rate": 0.55,
                "grass_win_rate": 0.72,
                "recent_form": 0.70,
                "age": 21
            },
            "Ugo Humbert": {
                "rank": 14,
                "win_rate": 0.63,
                "hard_win_rate": 0.66,
                "clay_win_rate": 0.58,
                "grass_win_rate": 0.70,
                "recent_form": 0.72,
                "age": 25
            },
            "Karen Khachanov": {
                "rank": 15,
                "win_rate": 0.62,
                "hard_win_rate": 0.65,
                "clay_win_rate": 0.60,
                "grass_win_rate": 0.62,
                "recent_form": 0.65,
                "age": 28
            },
            "Sebastian Baez": {
                "rank": 16,
                "win_rate": 0.61,
                "hard_win_rate": 0.58,
                "clay_win_rate": 0.68,
                "grass_win_rate": 0.55,
                "recent_form": 0.63,
                "age": 23
            },
            "Lorenzo Musetti": {
                "rank": 17,
                "win_rate": 0.60,
                "hard_win_rate": 0.58,
                "clay_win_rate": 0.65,
                "grass_win_rate": 0.58,
                "recent_form": 0.62,
                "age": 22
            },
            "Alex de Minaur": {
                "rank": 18,
                "win_rate": 0.59,
                "hard_win_rate": 0.65,
                "clay_win_rate": 0.50,
                "grass_win_rate": 0.62,
                "recent_form": 0.60,
                "age": 25
            },
            "Nicolas Jarry": {
                "rank": 19,
                "win_rate": 0.58,
                "hard_win_rate": 0.60,
                "clay_win_rate": 0.62,
                "grass_win_rate": 0.52,
                "recent_form": 0.58,
                "age": 28
            },
            "Tallon Griekspoor": {
                "rank": 20,
                "win_rate": 0.57,
                "hard_win_rate": 0.62,
                "clay_win_rate": 0.52,
                "grass_win_rate": 0.58,
                "recent_form": 0.59,
                "age": 27
            },
            "Sebastian Korda": {
                "rank": 21,
                "win_rate": 0.56,
                "hard_win_rate": 0.60,
                "clay_win_rate": 0.52,
                "grass_win_rate": 0.58,
                "recent_form": 0.57,
                "age": 24
            },
            "Frances Tiafoe": {
                "rank": 22,
                "win_rate": 0.55,
                "hard_win_rate": 0.62,
                "clay_win_rate": 0.48,
                "grass_win_rate": 0.55,
                "recent_form": 0.56,
                "age": 26
            },
            "Matteo Berrettini": {
                "rank": 23,
                "win_rate": 0.54,
                "hard_win_rate": 0.58,
                "clay_win_rate": 0.52,
                "grass_win_rate": 0.65,
                "recent_form": 0.55,
                "age": 28
            },
            "Alejandro Tabilo": {
                "rank": 24,
                "win_rate": 0.53,
                "hard_win_rate": 0.55,
                "clay_win_rate": 0.58,
                "grass_win_rate": 0.48,
                "recent_form": 0.54,
                "age": 26
            },
            "Jan-Lennard Struff": {
                "rank": 25,
                "win_rate": 0.52,
                "hard_win_rate": 0.58,
                "clay_win_rate": 0.50,
                "grass_win_rate": 0.50,
                "recent_form": 0.53,
                "age": 34
            },
            "Lucas Pouille": {
                "rank": 26,
                "win_rate": 0.51,
                "hard_win_rate": 0.55,
                "clay_win_rate": 0.50,
                "grass_win_rate": 0.48,
                "recent_form": 0.52,
                "age": 30
            },
            "Mariano Navone": {
                "rank": 27,
                "win_rate": 0.50,
                "hard_win_rate": 0.48,
                "clay_win_rate": 0.58,
                "grass_win_rate": 0.45,
                "recent_form": 0.51,
                "age": 23
            },
            "Cameron Norrie": {
                "rank": 28,
                "win_rate": 0.49,
                "hard_win_rate": 0.52,
                "clay_win_rate": 0.48,
                "grass_win_rate": 0.50,
                "recent_form": 0.50,
                "age": 29
            },
            "Arthur Fils": {
                "rank": 29,
                "win_rate": 0.48,
                "hard_win_rate": 0.50,
                "clay_win_rate": 0.50,
                "grass_win_rate": 0.45,
                "recent_form": 0.49,
                "age": 20
            },
            "Tomas Martin Etcheverry": {
                "rank": 30,
                "win_rate": 0.47,
                "hard_win_rate": 0.45,
                "clay_win_rate": 0.55,
                "grass_win_rate": 0.42,
                "recent_form": 0.48,
                "age": 25
            },
            "Luciano Darderi": {
                "rank": 31,
                "win_rate": 0.46,
                "hard_win_rate": 0.48,
                "clay_win_rate": 0.52,
                "grass_win_rate": 0.40,
                "recent_form": 0.47,
                "age": 22
            },
            "Jordan Thompson": {
                "rank": 32,
                "win_rate": 0.45,
                "hard_win_rate": 0.50,
                "clay_win_rate": 0.42,
                "grass_win_rate": 0.48,
                "recent_form": 0.46,
                "age": 30
            },
            "Zhizhen Zhang": {
                "rank": 33,
                "win_rate": 0.44,
                "hard_win_rate": 0.48,
                "clay_win_rate": 0.42,
                "grass_win_rate": 0.42,
                "recent_form": 0.45,
                "age": 27
            },
            "Jiri Lehecka": {
                "rank": 34,
                "win_rate": 0.43,
                "hard_win_rate": 0.45,
                "clay_win_rate": 0.42,
                "grass_win_rate": 0.45,
                "recent_form": 0.44,
                "age": 23
            },
            "Christopher Eubanks": {
                "rank": 35,
                "win_rate": 0.42,
                "hard_win_rate": 0.48,
                "clay_win_rate": 0.35,
                "grass_win_rate": 0.50,
                "recent_form": 0.43,
                "age": 28
            },
            "Yannick Hanfmann": {
                "rank": 36,
                "win_rate": 0.41,
                "hard_win_rate": 0.42,
                "clay_win_rate": 0.45,
                "grass_win_rate": 0.38,
                "recent_form": 0.42,
                "age": 32
            },
            "Daniel Altmaier": {
                "rank": 37,
                "win_rate": 0.40,
                "hard_win_rate": 0.38,
                "clay_win_rate": 0.45,
                "grass_win_rate": 0.38,
                "recent_form": 0.41,
                "age": 25
            },
            "Fabian Marozsan": {
                "rank": 38,
                "win_rate": 0.39,
                "hard_win_rate": 0.40,
                "clay_win_rate": 0.42,
                "grass_win_rate": 0.35,
                "recent_form": 0.40,
                "age": 25
            },
            "Max Purcell": {
                "rank": 39,
                "win_rate": 0.38,
                "hard_win_rate": 0.42,
                "clay_win_rate": 0.35,
                "grass_win_rate": 0.40,
                "recent_form": 0.39,
                "age": 26
            },
            "Pedro Martinez": {
                "rank": 40,
                "win_rate": 0.37,
                "hard_win_rate": 0.35,
                "clay_win_rate": 0.42,
                "grass_win_rate": 0.35,
                "recent_form": 0.38,
                "age": 27
            },
            "Lorenzo Sonego": {
                "rank": 41,
                "win_rate": 0.36,
                "hard_win_rate": 0.38,
                "clay_win_rate": 0.38,
                "grass_win_rate": 0.35,
                "recent_form": 0.37,
                "age": 29
            },
            "Yoshihito Nishioka": {
                "rank": 42,
                "win_rate": 0.35,
                "hard_win_rate": 0.40,
                "clay_win_rate": 0.32,
                "grass_win_rate": 0.35,
                "recent_form": 0.36,
                "age": 28
            },
            "Miomir Kecmanovic": {
                "rank": 43,
                "win_rate": 0.34,
                "hard_win_rate": 0.38,
                "clay_win_rate": 0.35,
                "grass_win_rate": 0.32,
                "recent_form": 0.35,
                "age": 25
            },
            "Flavio Cobolli": {
                "rank": 44,
                "win_rate": 0.33,
                "hard_win_rate": 0.35,
                "clay_win_rate": 0.38,
                "grass_win_rate": 0.28,
                "recent_form": 0.34,
                "age": 22
            },
            "Dusan Lajovic": {
                "rank": 45,
                "win_rate": 0.32,
                "hard_win_rate": 0.30,
                "clay_win_rate": 0.38,
                "grass_win_rate": 0.30,
                "recent_form": 0.33,
                "age": 34
            },
            "Roberto Bautista Agut": {
                "rank": 46,
                "win_rate": 0.31,
                "hard_win_rate": 0.35,
                "clay_win_rate": 0.32,
                "grass_win_rate": 0.30,
                "recent_form": 0.32,
                "age": 36
            },
            "Dominic Stricker": {
                "rank": 47,
                "win_rate": 0.30,
                "hard_win_rate": 0.32,
                "clay_win_rate": 0.30,
                "grass_win_rate": 0.35,
                "recent_form": 0.31,
                "age": 22
            },
            "Facundo Diaz Acosta": {
                "rank": 48,
                "win_rate": 0.29,
                "hard_win_rate": 0.28,
                "clay_win_rate": 0.35,
                "grass_win_rate": 0.25,
                "recent_form": 0.30,
                "age": 24
            },
            "Thiago Seyboth Wild": {
                "rank": 49,
                "win_rate": 0.28,
                "hard_win_rate": 0.30,
                "clay_win_rate": 0.32,
                "grass_win_rate": 0.25,
                "recent_form": 0.29,
                "age": 24
            },
            "Jakub Mensik": {
                "rank": 50,
                "win_rate": 0.27,
                "hard_win_rate": 0.30,
                "clay_win_rate": 0.28,
                "grass_win_rate": 0.28,
                "recent_form": 0.28,
                "age": 19
            },
            "Emil Ruusuvuori": {
                "rank": 51,
                "win_rate": 0.26,
                "hard_win_rate": 0.32,
                "clay_win_rate": 0.22,
                "grass_win_rate": 0.25,
                "recent_form": 0.27,
                "age": 25
            },
            "Borna Coric": {
                "rank": 52,
                "win_rate": 0.25,
                "hard_win_rate": 0.28,
                "clay_win_rate": 0.25,
                "grass_win_rate": 0.22,
                "recent_form": 0.26,
                "age": 27
            },
            "Stan Wawrinka": {
                "rank": 53,
                "win_rate": 0.24,
                "hard_win_rate": 0.26,
                "clay_win_rate": 0.28,
                "grass_win_rate": 0.20,
                "recent_form": 0.25,
                "age": 39
            },
            "Richard Gasquet": {
                "rank": 54,
                "win_rate": 0.23,
                "hard_win_rate": 0.25,
                "clay_win_rate": 0.24,
                "grass_win_rate": 0.22,
                "recent_form": 0.24,
                "age": 38
            },
            "Marcos Giron": {
                "rank": 55,
                "win_rate": 0.22,
                "hard_win_rate": 0.28,
                "clay_win_rate": 0.18,
                "grass_win_rate": 0.20,
                "recent_form": 0.23,
                "age": 31
            },
            "Taro Daniel": {
                "rank": 56,
                "win_rate": 0.21,
                "hard_win_rate": 0.24,
                "clay_win_rate": 0.22,
                "grass_win_rate": 0.18,
                "recent_form": 0.22,
                "age": 31
            },
            "Rinky Hijikata": {
                "rank": 57,
                "win_rate": 0.20,
                "hard_win_rate": 0.25,
                "clay_win_rate": 0.18,
                "grass_win_rate": 0.22,
                "recent_form": 0.21,
                "age": 23
            },
            "Sumit Nagal": {
                "rank": 58,
                "win_rate": 0.19,
                "hard_win_rate": 0.22,
                "clay_win_rate": 0.20,
                "grass_win_rate": 0.16,
                "recent_form": 0.20,
                "age": 26
            },
            "Alexei Popyrin": {
                "rank": 59,
                "win_rate": 0.18,
                "hard_win_rate": 0.24,
                "clay_win_rate": 0.16,
                "grass_win_rate": 0.20,
                "recent_form": 0.19,
                "age": 25
            },
            "Mackenzie McDonald": {
                "rank": 60,
                "win_rate": 0.17,
                "hard_win_rate": 0.22,
                "clay_win_rate": 0.15,
                "grass_win_rate": 0.18,
                "recent_form": 0.18,
                "age": 29
            },
            "Nuno Borges": {
                "rank": 61,
                "win_rate": 0.16,
                "hard_win_rate": 0.20,
                "clay_win_rate": 0.18,
                "grass_win_rate": 0.14,
                "recent_form": 0.17,
                "age": 27
            },
            "Aleksandar Vukic": {
                "rank": 62,
                "win_rate": 0.15,
                "hard_win_rate": 0.21,
                "clay_win_rate": 0.14,
                "grass_win_rate": 0.16,
                "recent_form": 0.16,
                "age": 28
            },
            "Radu Albot": {
                "rank": 63,
                "win_rate": 0.14,
                "hard_win_rate": 0.18,
                "clay_win_rate": 0.16,
                "grass_win_rate": 0.12,
                "recent_form": 0.15,
                "age": 34
            },
            "James Duckworth": {
                "rank": 64,
                "win_rate": 0.13,
                "hard_win_rate": 0.20,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.15,
                "recent_form": 0.14,
                "age": 32
            },
            "Yasutaka Uchiyama": {
                "rank": 65,
                "win_rate": 0.12,
                "hard_win_rate": 0.19,
                "clay_win_rate": 0.11,
                "grass_win_rate": 0.14,
                "recent_form": 0.13,
                "age": 31
            },
            "Tomas Machac": {
                "rank": 66,
                "win_rate": 0.11,
                "hard_win_rate": 0.18,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.12,
                "recent_form": 0.12,
                "age": 24
            },
            "Constant Lestienne": {
                "rank": 67,
                "win_rate": 0.10,
                "hard_win_rate": 0.17,
                "clay_win_rate": 0.14,
                "grass_win_rate": 0.11,
                "recent_form": 0.11,
                "age": 32
            },
            "Bernabe Zapata Miralles": {
                "rank": 68,
                "win_rate": 0.09,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.16,
                "grass_win_rate": 0.10,
                "recent_form": 0.10,
                "age": 27
            },
            "Hugo Gaston": {
                "rank": 69,
                "win_rate": 0.08,
                "hard_win_rate": 0.16,
                "clay_win_rate": 0.15,
                "grass_win_rate": 0.09,
                "recent_form": 0.09,
                "age": 24
            },
            "Corentin Moutet": {
                "rank": 70,
                "win_rate": 0.07,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.14,
                "grass_win_rate": 0.08,
                "recent_form": 0.08,
                "age": 25
            },
            "Maxime Cressy": {
                "rank": 71,
                "win_rate": 0.06,
                "hard_win_rate": 0.18,
                "clay_win_rate": 0.10,
                "grass_win_rate": 0.12,
                "recent_form": 0.07,
                "age": 27
            },
            "Otto Virtanen": {
                "rank": 72,
                "win_rate": 0.05,
                "hard_win_rate": 0.16,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.11,
                "recent_form": 0.06,
                "age": 22
            },
            "Luca Van Assche": {
                "rank": 73,
                "win_rate": 0.04,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.10,
                "recent_form": 0.05,
                "age": 20
            },
            "Giulio Zeppieri": {
                "rank": 74,
                "win_rate": 0.03,
                "hard_win_rate": 0.13,
                "clay_win_rate": 0.14,
                "grass_win_rate": 0.09,
                "recent_form": 0.04,
                "age": 22
            },
            "Harold Mayot": {
                "rank": 75,
                "win_rate": 0.02,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.10,
                "recent_form": 0.03,
                "age": 22
            },
            "Titouan Droguet": {
                "rank": 76,
                "win_rate": 0.01,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.09,
                "recent_form": 0.02,
                "age": 23
            },
            "Terence Atmane": {
                "rank": 77,
                "win_rate": 0.01,
                "hard_win_rate": 0.13,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.08,
                "recent_form": 0.01,
                "age": 22
            },
            "Pedro Cachin": {
                "rank": 78,
                "win_rate": 0.01,
                "hard_win_rate": 0.12,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.07,
                "recent_form": 0.01,
                "age": 29
            },
            "Luca Nardi": {
                "rank": 79,
                "win_rate": 0.01,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.11,
                "grass_win_rate": 0.09,
                "recent_form": 0.01,
                "age": 21
            },
            "Giovanni Mpetshi Perricard": {
                "rank": 80,
                "win_rate": 0.01,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.10,
                "grass_win_rate": 0.11,
                "recent_form": 0.01,
                "age": 20
            },
            "Billy Harris": {
                "rank": 81,
                "win_rate": 0.01,
                "hard_win_rate": 0.13,
                "clay_win_rate": 0.11,
                "grass_win_rate": 0.12,
                "recent_form": 0.01,
                "age": 30
            },
            "Aleksandar Kovacevic": {
                "rank": 82,
                "win_rate": 0.01,
                "hard_win_rate": 0.16,
                "clay_win_rate": 0.09,
                "grass_win_rate": 0.10,
                "recent_form": 0.01,
                "age": 26
            },
            "Daniel Elahi Galan": {
                "rank": 83,
                "win_rate": 0.01,
                "hard_win_rate": 0.12,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.08,
                "recent_form": 0.01,
                "age": 28
            },
            "Jaume Munar": {
                "rank": 84,
                "win_rate": 0.01,
                "hard_win_rate": 0.11,
                "clay_win_rate": 0.14,
                "grass_win_rate": 0.07,
                "recent_form": 0.01,
                "age": 27
            },
            "Pavel Kotov": {
                "rank": 85,
                "win_rate": 0.01,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.10,
                "grass_win_rate": 0.09,
                "recent_form": 0.01,
                "age": 25
            },
            "Marton Fucsovics": {
                "rank": 86,
                "win_rate": 0.01,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.08,
                "recent_form": 0.01,
                "age": 32
            },
            "Yibing Wu": {
                "rank": 87,
                "win_rate": 0.01,
                "hard_win_rate": 0.13,
                "clay_win_rate": 0.11,
                "grass_win_rate": 0.10,
                "recent_form": 0.01,
                "age": 24
            },
            "Thiago Monteiro": {
                "rank": 88,
                "win_rate": 0.01,
                "hard_win_rate": 0.12,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.08,
                "recent_form": 0.01,
                "age": 30
            },
            "Roberto Carballes Baena": {
                "rank": 89,
                "win_rate": 0.01,
                "hard_win_rate": 0.10,
                "clay_win_rate": 0.14,
                "grass_win_rate": 0.07,
                "recent_form": 0.01,
                "age": 31
            },
            "Laslo Djere": {
                "rank": 90,
                "win_rate": 0.01,
                "hard_win_rate": 0.11,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.08,
                "recent_form": 0.01,
                "age": 29
            },
            "Christopher O'Connell": {
                "rank": 91,
                "win_rate": 0.01,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.09,
                "grass_win_rate": 0.11,
                "recent_form": 0.01,
                "age": 30
            },
            "Diego Schwartzman": {
                "rank": 92,
                "win_rate": 0.01,
                "hard_win_rate": 0.13,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.09,
                "recent_form": 0.01,
                "age": 32
            },
            "Botic van de Zandschulp": {
                "rank": 93,
                "win_rate": 0.01,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.10,
                "grass_win_rate": 0.10,
                "recent_form": 0.01,
                "age": 29
            },
            "Arthur Rinderknech": {
                "rank": 94,
                "win_rate": 0.01,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.09,
                "grass_win_rate": 0.11,
                "recent_form": 0.01,
                "age": 29
            },
            "Dominik Koepfer": {
                "rank": 95,
                "win_rate": 0.01,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.11,
                "grass_win_rate": 0.09,
                "recent_form": 0.01,
                "age": 30
            },
            "Juan Pablo Varillas": {
                "rank": 96,
                "win_rate": 0.01,
                "hard_win_rate": 0.11,
                "clay_win_rate": 0.13,
                "grass_win_rate": 0.08,
                "recent_form": 0.01,
                "age": 29
            },
            "Yosuke Watanuki": {
                "rank": 97,
                "win_rate": 0.01,
                "hard_win_rate": 0.16,
                "clay_win_rate": 0.08,
                "grass_win_rate": 0.10,
                "recent_form": 0.01,
                "age": 26
            },
            "Matteo Arnaldi": {
                "rank": 98,
                "win_rate": 0.01,
                "hard_win_rate": 0.13,
                "clay_win_rate": 0.12,
                "grass_win_rate": 0.09,
                "recent_form": 0.01,
                "age": 23
            },
            "Brandon Nakashima": {
                "rank": 99,
                "win_rate": 0.01,
                "hard_win_rate": 0.15,
                "clay_win_rate": 0.09,
                "grass_win_rate": 0.10,
                "recent_form": 0.01,
                "age": 23
            },
            "J.J. Wolf": {
                "rank": 100,
                "win_rate": 0.01,
                "hard_win_rate": 0.14,
                "clay_win_rate": 0.10,
                "grass_win_rate": 0.11,
                "recent_form": 0.01,
                "age": 25
            }
        }
        return default_players
    
    def get_player(self, name: str) -> Optional[Dict]:
        """Get player data by name."""
        return self.players.get(name)
    
    def list_players(self) -> List[str]:
        """Get list of all player names."""
        return sorted(self.players.keys())
    
    def search_players(self, query: str) -> List[str]:
        """Search for players by name."""
        query_lower = query.lower()
        return [name for name in self.players.keys() if query_lower in name.lower()]
    
    def add_player(self, name: str, stats: Dict):
        """Add a new player to the database."""
        self.players[name] = stats
        self.save_players()
    
    def update_player(self, name: str, stats: Dict):
        """Update player statistics."""
        if name in self.players:
            self.players[name].update(stats)
            self.save_players()
        else:
            raise ValueError(f"Player {name} not found in database")
    
    def get_head_to_head(self, player1: str, player2: str) -> Dict:
        """Get head-to-head record between two players."""
        # In a real implementation, this would query historical match data
        # For now, return empty or random data
        h2h_key = f"{player1}_vs_{player2}"
        reverse_key = f"{player2}_vs_{player1}"
        
        # Check if we have stored H2H data
        if hasattr(self, 'h2h_records'):
            if h2h_key in self.h2h_records:
                return self.h2h_records[h2h_key]
            elif reverse_key in self.h2h_records:
                rec = self.h2h_records[reverse_key]
                return {'meetings': rec['meetings'], 'wins': rec['meetings'] - rec['wins']}
        
        # Return default (no prior meetings)
        return {'meetings': 0, 'wins': 0}



