"""
Flask Web Application for ATP Tennis Match Prediction
"""

from flask import Flask, render_template, request, jsonify
from tennis_prediction_model import TennisPredictionModel
from player_database import PlayerDatabase
import os

app = Flask(__name__)

# Initialize model and database
model = TennisPredictionModel()
db = PlayerDatabase()

# Load or train model on startup
def initialize_model():
    """Load existing model or train a new one."""
    if os.path.exists('tennis_model.pkl'):
        try:
            print("Loading existing model...")
            model.load_model('tennis_model.pkl')
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}. Training new model...")
            train_model()
    else:
        print("No existing model found. Training new model...")
        train_model()

def train_model():
    """Train the prediction model."""
    print("Training model (this may take a minute)...")
    df = model.fetch_atp_data(num_matches=1500)
    df = model.engineer_features(df)
    X, y = model.prepare_features(df)
    model.train(X, y)
    model.save_model('tennis_model.pkl')
    print("Model trained and saved!")

# Initialize on import
initialize_model()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/players', methods=['GET'])
def get_players():
    """Get list of all players."""
    players = db.list_players()
    players_data = []
    for player_name in players:
        stats = db.get_player(player_name)
        players_data.append({
            'name': player_name,
            'rank': stats['rank'],
            'win_rate': stats['win_rate'],
            'age': stats['age']
        })
    # Sort by rank
    players_data.sort(key=lambda x: x['rank'])
    return jsonify(players_data)

@app.route('/api/player/<player_name>', methods=['GET'])
def get_player(player_name):
    """Get detailed player information."""
    stats = db.get_player(player_name)
    if not stats:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify({
        'name': player_name,
        'rank': stats['rank'],
        'age': stats['age'],
        'win_rate': stats['win_rate'],
        'hard_win_rate': stats['hard_win_rate'],
        'clay_win_rate': stats['clay_win_rate'],
        'grass_win_rate': stats['grass_win_rate'],
        'recent_form': stats['recent_form']
    })

@app.route('/api/predict', methods=['POST'])
def predict_match():
    """Make a match prediction."""
    try:
        data = request.json
        player1_name = data.get('player1')
        player2_name = data.get('player2')
        surface = data.get('surface', 'Hard')
        
        if not player1_name or not player2_name:
            return jsonify({'error': 'Both players must be selected'}), 400
        
        if player1_name == player2_name:
            return jsonify({'error': 'Cannot select the same player twice'}), 400
        
        # Get player stats
        p1_stats = db.get_player(player1_name)
        p2_stats = db.get_player(player2_name)
        
        if not p1_stats or not p2_stats:
            return jsonify({'error': 'One or both players not found'}), 404
        
        # Prepare stats for prediction
        surface_map = {
            'Hard': 'hard_win_rate',
            'Clay': 'clay_win_rate',
            'Grass': 'grass_win_rate'
        }
        
        p1_prediction_stats = {
            'rank': p1_stats['rank'],
            'win_rate': p1_stats['win_rate'],
            'surface_win_rate': p1_stats[surface_map[surface]],
            'recent_form': p1_stats['recent_form'],
            'age': p1_stats['age']
        }
        
        p2_prediction_stats = {
            'rank': p2_stats['rank'],
            'win_rate': p2_stats['win_rate'],
            'surface_win_rate': p2_stats[surface_map[surface]],
            'recent_form': p2_stats['recent_form'],
            'age': p2_stats['age']
        }
        
        # Get head-to-head if available
        h2h = db.get_head_to_head(player1_name, player2_name)
        if h2h['meetings'] > 0:
            p1_prediction_stats['h2h_wins'] = h2h['wins']
            p1_prediction_stats['h2h_meetings'] = h2h['meetings']
        
        # Make prediction
        result = model.predict_match(p1_prediction_stats, p2_prediction_stats, surface)
        
        return jsonify({
            'player1': player1_name,
            'player2': player2_name,
            'surface': surface,
            'player1_win_probability': result['player1_win_probability'],
            'player2_win_probability': result['player2_win_probability'],
            'predicted_winner': result['predicted_winner'],
            'confidence': result['confidence'],
            'h2h': h2h
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("ATP Tennis Match Prediction Web Application")
    print("="*70)
    print("Starting server...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

