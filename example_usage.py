"""
Example usage of the ATP Tennis Prediction Model
"""

from tennis_prediction_model import TennisPredictionModel
import pandas as pd

def example_predictions():
    """Demonstrate various prediction scenarios."""
    
    # Initialize and load model
    model = TennisPredictionModel()
    
    # Train model (or load existing)
    print("Training model...")
    df = model.fetch_atp_data(num_matches=1500)
    df = model.engineer_features(df)
    X, y = model.prepare_features(df)
    model.train(X, y)
    
    print("\n" + "="*70)
    print("PREDICTION EXAMPLES")
    print("="*70)
    
    # Scenario 1: Dominant player vs underdog
    print("\n[Scenario 1] Top 5 player vs Top 100 player (Hard Court)")
    print("-" * 70)
    top_player = {
        'rank': 3,
        'win_rate': 0.80,
        'surface_win_rate': 0.82,
        'recent_form': 0.85,
        'age': 24
    }
    underdog = {
        'rank': 95,
        'win_rate': 0.45,
        'surface_win_rate': 0.42,
        'recent_form': 0.40,
        'age': 29
    }
    
    result = model.predict_match(top_player, underdog, surface='Hard')
    print(f"Top Player Win Probability: {result['player1_win_probability']:.1%}")
    print(f"Underdog Win Probability: {result['player2_win_probability']:.1%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"\nBetting Odds:")
    print(f"  Top Player:    Decimal {result['player1_odds']['decimal']:.2f} | American {result['player1_odds']['american']:+d} | Fractional {result['player1_odds']['fractional']}")
    print(f"  Underdog:      Decimal {result['player2_odds']['decimal']:.2f} | American {result['player2_odds']['american']:+d} | Fractional {result['player2_odds']['fractional']}")
    
    # Scenario 2: Close match between top players
    print("\n[Scenario 2] Two Top 10 players (Clay Court)")
    print("-" * 70)
    player1 = {
        'rank': 7,
        'win_rate': 0.72,
        'surface_win_rate': 0.78,  # Strong on clay
        'recent_form': 0.75,
        'age': 26,
        'h2h_wins': 3,
        'h2h_meetings': 5
    }
    player2 = {
        'rank': 9,
        'win_rate': 0.70,
        'surface_win_rate': 0.65,  # Weaker on clay
        'recent_form': 0.70,
        'age': 28,
        'h2h_wins': 2,
        'h2h_meetings': 5
    }
    
    result = model.predict_match(player1, player2, surface='Clay')
    print(f"Player 1 Win Probability: {result['player1_win_probability']:.1%}")
    print(f"Player 2 Win Probability: {result['player2_win_probability']:.1%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"\nBetting Odds:")
    print(f"  Player 1:      Decimal {result['player1_odds']['decimal']:.2f} | American {result['player1_odds']['american']:+d} | Fractional {result['player1_odds']['fractional']}")
    print(f"  Player 2:      Decimal {result['player2_odds']['decimal']:.2f} | American {result['player2_odds']['american']:+d} | Fractional {result['player2_odds']['fractional']}")
    
    # Scenario 3: Grass court specialist
    print("\n[Scenario 3] Grass Court Specialist vs All-Court Player (Grass)")
    print("-" * 70)
    grass_specialist = {
        'rank': 25,
        'win_rate': 0.58,
        'surface_win_rate': 0.75,  # Excellent on grass
        'recent_form': 0.60,
        'age': 27
    }
    all_court = {
        'rank': 20,
        'win_rate': 0.65,
        'surface_win_rate': 0.55,  # Average on grass
        'recent_form': 0.65,
        'age': 25
    }
    
    result = model.predict_match(grass_specialist, all_court, surface='Grass')
    print(f"Grass Specialist Win Probability: {result['player1_win_probability']:.1%}")
    print(f"All-Court Player Win Probability: {result['player2_win_probability']:.1%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"\nBetting Odds:")
    print(f"  Grass Specialist: Decimal {result['player1_odds']['decimal']:.2f} | American {result['player1_odds']['american']:+d} | Fractional {result['player1_odds']['fractional']}")
    print(f"  All-Court Player: Decimal {result['player2_odds']['decimal']:.2f} | American {result['player2_odds']['american']:+d} | Fractional {result['player2_odds']['fractional']}")
    
    # Scenario 4: Young rising star vs veteran
    print("\n[Scenario 4] Young Rising Star vs Experienced Veteran (Hard Court)")
    print("-" * 70)
    rising_star = {
        'rank': 15,
        'win_rate': 0.68,
        'surface_win_rate': 0.70,
        'recent_form': 0.80,  # Hot streak
        'age': 21
    }
    veteran = {
        'rank': 18,
        'win_rate': 0.65,
        'surface_win_rate': 0.68,
        'recent_form': 0.55,  # Slumping
        'age': 34
    }
    
    result = model.predict_match(rising_star, veteran, surface='Hard')
    print(f"Rising Star Win Probability: {result['player1_win_probability']:.1%}")
    print(f"Veteran Win Probability: {result['player2_win_probability']:.1%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"\nBetting Odds:")
    print(f"  Rising Star:    Decimal {result['player1_odds']['decimal']:.2f} | American {result['player1_odds']['american']:+d} | Fractional {result['player1_odds']['fractional']}")
    print(f"  Veteran:        Decimal {result['player2_odds']['decimal']:.2f} | American {result['player2_odds']['american']:+d} | Fractional {result['player2_odds']['fractional']}")
    
    # Scenario 5: Head-to-head advantage
    print("\n[Scenario 5] Lower Ranked Player with H2H Advantage (Clay)")
    print("-" * 70)
    lower_ranked = {
        'rank': 30,
        'win_rate': 0.60,
        'surface_win_rate': 0.65,
        'recent_form': 0.65,
        'age': 26,
        'h2h_wins': 4,
        'h2h_meetings': 5  # Dominant head-to-head
    }
    higher_ranked = {
        'rank': 12,
        'win_rate': 0.70,
        'surface_win_rate': 0.68,
        'recent_form': 0.70,
        'age': 28,
        'h2h_wins': 1,
        'h2h_meetings': 5
    }
    
    result = model.predict_match(lower_ranked, higher_ranked, surface='Clay')
    print(f"Lower Ranked Player Win Probability: {result['player1_win_probability']:.1%}")
    print(f"Higher Ranked Player Win Probability: {result['player2_win_probability']:.1%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"\nBetting Odds:")
    print(f"  Lower Ranked:  Decimal {result['player1_odds']['decimal']:.2f} | American {result['player1_odds']['american']:+d} | Fractional {result['player1_odds']['fractional']}")
    print(f"  Higher Ranked: Decimal {result['player2_odds']['decimal']:.2f} | American {result['player2_odds']['american']:+d} | Fractional {result['player2_odds']['fractional']}")
    print(f"Note: H2H advantage can overcome ranking difference!")
    
    print("\n" + "="*70)
    print("Examples complete!")
    print("="*70)


if __name__ == "__main__":
    example_predictions()



