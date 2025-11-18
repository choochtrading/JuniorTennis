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


