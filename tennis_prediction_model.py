"""
ATP Tennis Match Prediction Model
This model predicts match outcomes using player statistics, rankings, and historical performance.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TennisPredictionModel:
    """
    A machine learning model for predicting ATP tennis match outcomes.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def fetch_atp_data(self, num_matches=1000):
        """
        Fetch ATP match data. In production, this would connect to a real API.
        For now, we'll create synthetic data based on realistic patterns.
        """
        print("Fetching ATP match data...")
        
        # In a real implementation, you would fetch from:
        # - ATP official API
        # - Tennis Abstract
        # - Web scraping from ATP website
        # For this example, we'll generate realistic synthetic data
        
        np.random.seed(42)
        matches = []
        
        # Generate synthetic match data
        for i in range(num_matches):
            # Player rankings (ATP top 500)
            player1_rank = np.random.randint(1, 500)
            player2_rank = np.random.randint(1, 500)
            
            # Ensure different players
            while abs(player1_rank - player2_rank) < 5:
                player2_rank = np.random.randint(1, 500)
            
            # Surface types
            surface = np.random.choice(['Hard', 'Clay', 'Grass'], p=[0.6, 0.3, 0.1])
            
            # Player stats (win rates, recent form)
            p1_win_rate = max(0.3, min(0.9, 0.5 + (500 - player1_rank) / 1000))
            p2_win_rate = max(0.3, min(0.9, 0.5 + (500 - player2_rank) / 1000))
            
            # Surface-specific win rates
            p1_surface_win_rate = p1_win_rate + np.random.uniform(-0.15, 0.15)
            p2_surface_win_rate = p2_win_rate + np.random.uniform(-0.15, 0.15)
            
            # Recent form (last 10 matches)
            p1_recent_form = np.random.binomial(10, p1_win_rate) / 10
            p2_recent_form = np.random.binomial(10, p2_win_rate) / 10
            
            # Head-to-head (if they've played before)
            h2h_meetings = np.random.randint(0, 5)
            if h2h_meetings > 0:
                p1_h2h_wins = np.random.binomial(h2h_meetings, 0.5)
            else:
                p1_h2h_wins = 0
            
            # Age (affects stamina)
            p1_age = np.random.randint(18, 38)
            p2_age = np.random.randint(18, 38)
            
            # Calculate match outcome based on features
            rank_diff = player2_rank - player1_rank  # Positive if player1 is better
            surface_advantage = p1_surface_win_rate - p2_surface_win_rate
            form_advantage = p1_recent_form - p2_recent_form
            h2h_advantage = (p1_h2h_wins / max(h2h_meetings, 1)) - 0.5 if h2h_meetings > 0 else 0
            age_advantage = (p2_age - p1_age) / 20  # Younger is slightly better
            
            # Probability of player1 winning
            win_prob = 0.5 + 0.3 * np.tanh(rank_diff / 100) + 0.2 * surface_advantage + \
                      0.15 * form_advantage + 0.1 * h2h_advantage + 0.05 * age_advantage
            win_prob = max(0.1, min(0.9, win_prob))
            
            # Determine winner
            player1_won = 1 if np.random.random() < win_prob else 0
            
            matches.append({
                'player1_rank': player1_rank,
                'player2_rank': player2_rank,
                'player1_win_rate': p1_win_rate,
                'player2_win_rate': p2_win_rate,
                'player1_surface_win_rate': p1_surface_win_rate,
                'player2_surface_win_rate': p2_surface_win_rate,
                'player1_recent_form': p1_recent_form,
                'player2_recent_form': p2_recent_form,
                'h2h_meetings': h2h_meetings,
                'player1_h2h_wins': p1_h2h_wins,
                'player1_age': p1_age,
                'player2_age': p2_age,
                'surface': surface,
                'rank_diff': rank_diff,
                'player1_won': player1_won
            })
        
        df = pd.DataFrame(matches)
        print(f"Fetched {len(df)} matches")
        return df
    
    def engineer_features(self, df):
        """
        Create additional features from raw data.
        """
        print("Engineering features...")
        
        # Rank difference (normalized)
        df['rank_diff_normalized'] = (df['player2_rank'] - df['player1_rank']) / 500
        
        # Win rate difference
        df['win_rate_diff'] = df['player1_win_rate'] - df['player2_win_rate']
        df['surface_win_rate_diff'] = df['player1_surface_win_rate'] - df['player2_surface_win_rate']
        
        # Form difference
        df['form_diff'] = df['player1_recent_form'] - df['player2_recent_form']
        
        # Head-to-head advantage
        df['h2h_advantage'] = (df['player1_h2h_wins'] / df['h2h_meetings'].replace(0, 1)) - 0.5
        df['h2h_advantage'] = df['h2h_advantage'].fillna(0)
        
        # Age difference (normalized)
        df['age_diff'] = (df['player2_age'] - df['player1_age']) / 20
        
        # Surface encoding
        df['surface_hard'] = (df['surface'] == 'Hard').astype(int)
        df['surface_clay'] = (df['surface'] == 'Clay').astype(int)
        df['surface_grass'] = (df['surface'] == 'Grass').astype(int)
        
        # Combined strength metric
        df['player1_strength'] = (500 - df['player1_rank']) / 500 + df['player1_win_rate'] + df['player1_recent_form']
        df['player2_strength'] = (500 - df['player2_rank']) / 500 + df['player2_win_rate'] + df['player2_recent_form']
        df['strength_diff'] = df['player1_strength'] - df['player2_strength']
        
        # Experience factor (older players might have more experience)
        df['experience_diff'] = (df['player1_age'] - df['player2_age']) / 20
        
        return df
    
    def prepare_features(self, df):
        """
        Select and prepare features for model training.
        """
        feature_cols = [
            'rank_diff_normalized',
            'win_rate_diff',
            'surface_win_rate_diff',
            'form_diff',
            'h2h_advantage',
            'age_diff',
            'surface_hard',
            'surface_clay',
            'surface_grass',
            'strength_diff',
            'experience_diff',
            'player1_rank',
            'player2_rank'
        ]
        
        X = df[feature_cols].copy()
        y = df['player1_won'].copy()
        
        self.feature_names = feature_cols
        
        return X, y
    
    def train(self, X, y, test_size=0.2):
        """
        Train the prediction model using ensemble methods.
        """
        print("Training model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Create ensemble of models
        rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        # Voting classifier
        self.model = VotingClassifier(
            estimators=[('rf', rf_model), ('gb', gb_model)],
            voting='soft',
            weights=[1.5, 1.0]
        )
        
        # Train
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nModel Performance:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='accuracy')
        print(f"\nCross-validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        self.is_trained = True
        
        return accuracy, X_test, y_test, y_pred, y_pred_proba
    
    def predict_match(self, player1_stats, player2_stats, surface='Hard'):
        """
        Predict the outcome of a single match.
        
        Parameters:
        -----------
        player1_stats : dict
            Dictionary with keys: rank, win_rate, surface_win_rate, recent_form, 
                                  age, h2h_wins (optional), h2h_meetings (optional)
        player2_stats : dict
            Same as player1_stats
        surface : str
            Surface type: 'Hard', 'Clay', or 'Grass'
        
        Returns:
        --------
        dict : Prediction results with probability and predicted winner
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions!")
        
        # Calculate features
        rank_diff_normalized = (player2_stats['rank'] - player1_stats['rank']) / 500
        win_rate_diff = player1_stats['win_rate'] - player2_stats['win_rate']
        surface_win_rate_diff = player1_stats.get('surface_win_rate', player1_stats['win_rate']) - \
                                player2_stats.get('surface_win_rate', player2_stats['win_rate'])
        form_diff = player1_stats['recent_form'] - player2_stats['recent_form']
        
        h2h_meetings = player1_stats.get('h2h_meetings', 0)
        h2h_wins = player1_stats.get('h2h_wins', 0)
        h2h_advantage = (h2h_wins / max(h2h_meetings, 1)) - 0.5 if h2h_meetings > 0 else 0
        
        age_diff = (player2_stats['age'] - player1_stats['age']) / 20
        
        surface_hard = 1 if surface == 'Hard' else 0
        surface_clay = 1 if surface == 'Clay' else 0
        surface_grass = 1 if surface == 'Grass' else 0
        
        player1_strength = (500 - player1_stats['rank']) / 500 + player1_stats['win_rate'] + player1_stats['recent_form']
        player2_strength = (500 - player2_stats['rank']) / 500 + player2_stats['win_rate'] + player2_stats['recent_form']
        strength_diff = player1_strength - player2_strength
        
        experience_diff = (player1_stats['age'] - player2_stats['age']) / 20
        
        # Create feature vector
        features = np.array([[
            rank_diff_normalized,
            win_rate_diff,
            surface_win_rate_diff,
            form_diff,
            h2h_advantage,
            age_diff,
            surface_hard,
            surface_clay,
            surface_grass,
            strength_diff,
            experience_diff,
            player1_stats['rank'],
            player2_stats['rank']
        ]])
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        proba = self.model.predict_proba(features_scaled)[0]
        prediction = self.model.predict(features_scaled)[0]
        
        return {
            'player1_win_probability': proba[1],
            'player2_win_probability': proba[0],
            'predicted_winner': 'Player 1' if prediction == 1 else 'Player 2',
            'confidence': max(proba)
        }
    
    def save_model(self, filepath='tennis_model.pkl'):
        """Save the trained model."""
        import joblib
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='tennis_model.pkl'):
        """Load a trained model."""
        import joblib
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
        self.is_trained = True
        print(f"Model loaded from {filepath}")


def main():
    """
    Main function to train and demonstrate the model.
    """
    print("=" * 60)
    print("ATP Tennis Match Prediction Model")
    print("=" * 60)
    
    # Initialize model
    model = TennisPredictionModel()
    
    # Fetch and prepare data
    df = model.fetch_atp_data(num_matches=2000)
    df = model.engineer_features(df)
    X, y = model.prepare_features(df)
    
    # Train model
    accuracy, X_test, y_test, y_pred, y_pred_proba = model.train(X, y)
    
    # Save model
    model.save_model('tennis_model.pkl')
    
    # Example predictions
    print("\n" + "=" * 60)
    print("Example Predictions")
    print("=" * 60)
    
    # Example 1: Top player vs lower ranked player
    print("\nExample 1: Top 10 player vs Top 50 player (Hard court)")
    player1 = {
        'rank': 5,
        'win_rate': 0.75,
        'surface_win_rate': 0.78,
        'recent_form': 0.8,
        'age': 25,
        'h2h_wins': 2,
        'h2h_meetings': 3
    }
    player2 = {
        'rank': 45,
        'win_rate': 0.55,
        'surface_win_rate': 0.52,
        'recent_form': 0.5,
        'age': 27
    }
    
    result = model.predict_match(player1, player2, surface='Hard')
    print(f"Player 1 Win Probability: {result['player1_win_probability']:.2%}")
    print(f"Player 2 Win Probability: {result['player2_win_probability']:.2%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    # Example 2: Close match
    print("\nExample 2: Two top 20 players (Clay court)")
    player1 = {
        'rank': 12,
        'win_rate': 0.68,
        'surface_win_rate': 0.72,  # Better on clay
        'recent_form': 0.7,
        'age': 28,
        'h2h_wins': 1,
        'h2h_meetings': 2
    }
    player2 = {
        'rank': 15,
        'win_rate': 0.65,
        'surface_win_rate': 0.60,  # Weaker on clay
        'recent_form': 0.65,
        'age': 26
    }
    
    result = model.predict_match(player1, player2, surface='Clay')
    print(f"Player 1 Win Probability: {result['player1_win_probability']:.2%}")
    print(f"Player 2 Win Probability: {result['player2_win_probability']:.2%}")
    print(f"Predicted Winner: {result['predicted_winner']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    print("\n" + "=" * 60)
    print("Model training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()


