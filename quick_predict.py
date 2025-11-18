"""
Quick prediction script for specific matches
"""

from tennis_prediction_model import TennisPredictionModel
from player_database import PlayerDatabase

def quick_predict(player1_name: str, player2_name: str, surface: str):
    """Make a quick prediction for a match."""
    # Load model
    model = TennisPredictionModel()
    model.load_model('tennis_model.pkl')
    
    # Load database
    db = PlayerDatabase()
    
    # Get player stats
    surface_map = {
        'Hard': 'hard_win_rate',
        'Clay': 'clay_win_rate',
        'Grass': 'grass_win_rate'
    }
    
    p1_data = db.get_player(player1_name)
    p2_data = db.get_player(player2_name)
    
    if not p1_data:
        print(f"Error: {player1_name} not found in database!")
        return
    if not p2_data:
        print(f"Error: {player2_name} not found in database!")
        return
    
    p1_stats = {
        'rank': p1_data['rank'],
        'win_rate': p1_data['win_rate'],
        'surface_win_rate': p1_data[surface_map[surface]],
        'recent_form': p1_data['recent_form'],
        'age': p1_data['age']
    }
    
    p2_stats = {
        'rank': p2_data['rank'],
        'win_rate': p2_data['win_rate'],
        'surface_win_rate': p2_data[surface_map[surface]],
        'recent_form': p2_data['recent_form'],
        'age': p2_data['age']
    }
    
    # Get head-to-head
    h2h = db.get_head_to_head(player1_name, player2_name)
    if h2h['meetings'] > 0:
        p1_stats['h2h_wins'] = h2h['wins']
        p1_stats['h2h_meetings'] = h2h['meetings']
    
    # Make prediction
    result = model.predict_match(p1_stats, p2_stats, surface)
    
    # Display results
    print("\n" + "="*70)
    print("MATCH PREDICTION")
    print("="*70)
    print(f"Player 1: {player1_name}")
    print(f"Player 2: {player2_name}")
    print(f"Surface:  {surface} Court")
    print("="*70)
    
    if h2h['meetings'] > 0:
        print(f"\nHead-to-Head: {player1_name} leads {h2h['wins']}-{h2h['meetings'] - h2h['wins']} "
              f"({h2h['meetings']} meetings)")
    
    print("\n" + "-"*70)
    print("PREDICTION RESULTS")
    print("-"*70)
    print(f"{player1_name:30s} Win Probability: {result['player1_win_probability']:6.2%}")
    print(f"{player2_name:30s} Win Probability: {result['player2_win_probability']:6.2%}")
    print("-"*70)
    print(f"\nPredicted Winner: {result['predicted_winner']}")
    print(f"Confidence Level: {result['confidence']:.1%}")
    print("="*70 + "\n")
    
    # Show player stats comparison
    print("PLAYER STATISTICS COMPARISON")
    print("-"*70)
    print(f"{'Statistic':<25} {player1_name[:20]:<20} {player2_name[:20]}")
    print("-"*70)
    print(f"{'Rank':<25} {p1_stats['rank']:<20} {p2_stats['rank']}")
    print(f"{'Overall Win Rate':<25} {p1_stats['win_rate']:<20.1%} {p2_stats['win_rate']:.1%}")
    print(f"{surface + ' Win Rate':<25} {p1_stats['surface_win_rate']:<20.1%} {p2_stats['surface_win_rate']:.1%}")
    print(f"{'Recent Form':<25} {p1_stats['recent_form']:<20.1%} {p2_stats['recent_form']:.1%}")
    print(f"{'Age':<25} {p1_stats['age']:<20} {p2_stats['age']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        quick_predict(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        # Default: Casper Ruud vs Tommy Paul on Clay
        quick_predict("Casper Ruud", "Tommy Paul", "Clay")


