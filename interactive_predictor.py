"""
Interactive ATP Tennis Match Predictor
Allows users to select players and get match predictions
"""

from tennis_prediction_model import TennisPredictionModel
from player_database import PlayerDatabase
import os
import sys

class InteractivePredictor:
    """Interactive tool for predicting tennis matches."""
    
    def __init__(self):
        self.model = TennisPredictionModel()
        self.db = PlayerDatabase()
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load existing model or train a new one."""
        if os.path.exists('tennis_model.pkl'):
            try:
                print("Loading existing model...")
                self.model.load_model('tennis_model.pkl')
                print("Model loaded successfully!\n")
            except:
                print("Error loading model. Training new model...")
                self._train_model()
        else:
            print("No existing model found. Training new model...")
            self._train_model()
    
    def _train_model(self):
        """Train the prediction model."""
        print("This may take a minute...")
        df = self.model.fetch_atp_data(num_matches=1500)
        df = self.model.engineer_features(df)
        X, y = self.model.prepare_features(df)
        self.model.train(X, y)
        self.model.save_model('tennis_model.pkl')
        print("\nModel trained and saved!\n")
    
    def display_players(self):
        """Display all available players."""
        players = self.db.list_players()
        print("\n" + "="*70)
        print("AVAILABLE PLAYERS")
        print("="*70)
        for i, player in enumerate(players, 1):
            stats = self.db.get_player(player)
            print(f"{i:2d}. {player:30s} | Rank: {stats['rank']:3d} | "
                  f"Win Rate: {stats['win_rate']:.1%} | Age: {stats['age']}")
        print("="*70 + "\n")
        return players
    
    def select_player(self, prompt: str) -> str:
        """Interactive player selection."""
        while True:
            print(f"\n{prompt}")
            print("Options:")
            print("  1. Enter player number from list")
            print("  2. Enter player name (partial match OK)")
            print("  3. View all players")
            print("  4. Cancel")
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == '1':
                players = self.db.list_players()
                try:
                    num = int(input(f"Enter player number (1-{len(players)}): "))
                    if 1 <= num <= len(players):
                        selected = players[num - 1]
                        self._display_player_info(selected)
                        confirm = input(f"\nSelect {selected}? (y/n): ").strip().lower()
                        if confirm == 'y':
                            return selected
                    else:
                        print("Invalid number!")
                except ValueError:
                    print("Please enter a valid number!")
            
            elif choice == '2':
                query = input("Enter player name (or partial name): ").strip()
                matches = self.db.search_players(query)
                if not matches:
                    print(f"No players found matching '{query}'")
                elif len(matches) == 1:
                    selected = matches[0]
                    self._display_player_info(selected)
                    confirm = input(f"\nSelect {selected}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        return selected
                else:
                    print(f"\nFound {len(matches)} matches:")
                    for i, name in enumerate(matches, 1):
                        stats = self.db.get_player(name)
                        print(f"  {i}. {name} (Rank: {stats['rank']})")
                    try:
                        num = int(input(f"\nSelect number (1-{len(matches)}): "))
                        if 1 <= num <= len(matches):
                            return matches[num - 1]
                        else:
                            print("Invalid number!")
                    except ValueError:
                        print("Please enter a valid number!")
            
            elif choice == '3':
                self.display_players()
            
            elif choice == '4':
                return None
            
            else:
                print("Invalid choice! Please enter 1-4.")
    
    def _display_player_info(self, player_name: str):
        """Display detailed player information."""
        stats = self.db.get_player(player_name)
        if not stats:
            print(f"Player {player_name} not found!")
            return
        
        print("\n" + "="*70)
        print(f"PLAYER: {player_name.upper()}")
        print("="*70)
        print(f"Rank:              {stats['rank']}")
        print(f"Age:               {stats['age']}")
        print(f"Overall Win Rate:  {stats['win_rate']:.1%}")
        print(f"Recent Form:       {stats['recent_form']:.1%}")
        print(f"\nSurface-Specific Win Rates:")
        print(f"  Hard Court:      {stats['hard_win_rate']:.1%}")
        print(f"  Clay Court:      {stats['clay_win_rate']:.1%}")
        print(f"  Grass Court:     {stats['grass_win_rate']:.1%}")
        print("="*70)
    
    def select_surface(self) -> str:
        """Select match surface."""
        print("\nSelect Surface:")
        print("  1. Hard Court")
        print("  2. Clay Court")
        print("  3. Grass Court")
        
        while True:
            choice = input("\nYour choice (1-3): ").strip()
            if choice == '1':
                return 'Hard'
            elif choice == '2':
                return 'Clay'
            elif choice == '3':
                return 'Grass'
            else:
                print("Invalid choice! Please enter 1-3.")
    
    def prepare_player_stats(self, player_name: str, surface: str) -> dict:
        """Prepare player statistics for prediction."""
        stats = self.db.get_player(player_name)
        if not stats:
            raise ValueError(f"Player {player_name} not found!")
        
        surface_map = {
            'Hard': 'hard_win_rate',
            'Clay': 'clay_win_rate',
            'Grass': 'grass_win_rate'
        }
        
        return {
            'rank': stats['rank'],
            'win_rate': stats['win_rate'],
            'surface_win_rate': stats[surface_map[surface]],
            'recent_form': stats['recent_form'],
            'age': stats['age']
        }
    
    def predict_match(self, player1_name: str, player2_name: str, surface: str):
        """Make and display match prediction."""
        print("\n" + "="*70)
        print("MATCH PREDICTION")
        print("="*70)
        print(f"Player 1: {player1_name}")
        print(f"Player 2: {player2_name}")
        print(f"Surface:  {surface} Court")
        print("="*70)
        
        # Get player stats
        p1_stats = self.prepare_player_stats(player1_name, surface)
        p2_stats = self.prepare_player_stats(player2_name, surface)
        
        # Get head-to-head (if available)
        h2h = self.db.get_head_to_head(player1_name, player2_name)
        if h2h['meetings'] > 0:
            p1_stats['h2h_wins'] = h2h['wins']
            p1_stats['h2h_meetings'] = h2h['meetings']
            print(f"\nHead-to-Head: {player1_name} leads {h2h['wins']}-{h2h['meetings'] - h2h['wins']} "
                  f"({h2h['meetings']} meetings)")
        
        # Make prediction
        result = self.model.predict_match(p1_stats, p2_stats, surface)
        
        # Display results
        print("\n" + "-"*70)
        print("PREDICTION RESULTS")
        print("-"*70)
        print(f"{player1_name:30s} Win Probability: {result['player1_win_probability']:6.2%}")
        print(f"{player2_name:30s} Win Probability: {result['player2_win_probability']:6.2%}")
        print("-"*70)
        print(f"\nPredicted Winner: {result['predicted_winner']}")
        print(f"Confidence Level: {result['confidence']:.1%}")
        print("\n" + "-"*70)
        print("PREDICTED BETTING ODDS")
        print("-"*70)
        print(f"{player1_name:30s} Decimal: {result['player1_odds']['decimal']:>6.2f} | American: {result['player1_odds']['american']:>+6d} | Fractional: {result['player1_odds']['fractional']:>8s}")
        print(f"{player2_name:30s} Decimal: {result['player2_odds']['decimal']:>6.2f} | American: {result['player2_odds']['american']:>+6d} | Fractional: {result['player2_odds']['fractional']:>8s}")
        print("="*70 + "\n")
        
        return result
    
    def run(self):
        """Main interactive loop."""
        print("\n" + "="*70)
        print("ATP TENNIS MATCH PREDICTOR")
        print("="*70)
        print("Welcome! This tool predicts ATP tennis match outcomes.")
        print("="*70)
        
        while True:
            print("\nMain Menu:")
            print("  1. Predict a match")
            print("  2. View all players")
            print("  3. View player details")
            print("  4. Exit")
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == '1':
                # Predict match
                print("\n" + "="*70)
                print("SELECT PLAYERS FOR PREDICTION")
                print("="*70)
                
                player1 = self.select_player("Select Player 1:")
                if player1 is None:
                    continue
                
                player2 = self.select_player("Select Player 2:")
                if player2 is None:
                    continue
                
                if player1 == player2:
                    print("\nError: Cannot select the same player twice!")
                    continue
                
                surface = self.select_surface()
                
                self.predict_match(player1, player2, surface)
                
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                self.display_players()
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                player = self.select_player("Select player to view:")
                if player:
                    self._display_player_info(player)
                    input("\nPress Enter to continue...")
            
            elif choice == '4':
                print("\nThank you for using ATP Tennis Match Predictor!")
                print("Goodbye!\n")
                break
            
            else:
                print("Invalid choice! Please enter 1-4.")


def main():
    """Main entry point."""
    try:
        predictor = InteractivePredictor()
        predictor.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()



