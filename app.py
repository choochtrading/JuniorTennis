"""
Flask Web Application for ATP Tennis Match Prediction
"""

from flask import Flask, render_template, request, jsonify
from tennis_prediction_model import TennisPredictionModel
from player_database import PlayerDatabase
from atp_rankings_fetcher import ATPRankingsFetcher
from datetime import datetime, timedelta
import os
import threading
import time

app = Flask(__name__)

# Initialize model and database
model = TennisPredictionModel()
db = PlayerDatabase()
rankings_fetcher = ATPRankingsFetcher()

# Track last rankings update
last_rankings_update = None
rankings_update_lock = threading.Lock()

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

# Try to update rankings on startup (optional - can be disabled)
def initial_rankings_update():
    """Update rankings on startup if database is empty or old."""
    global last_rankings_update
    try:
        # First, fix any None values in existing database
        fixed_count = 0
        for name, stats in db.players.items():
            updated = False
            if stats.get('age') is None:
                stats['age'] = 25
                updated = True
            if stats.get('win_rate') is None:
                stats['win_rate'] = 0.5
                updated = True
            if stats.get('recent_form') is None:
                stats['recent_form'] = 0.5
                updated = True
            if stats.get('hard_win_rate') is None:
                stats['hard_win_rate'] = stats.get('win_rate', 0.5)
                updated = True
            if stats.get('clay_win_rate') is None:
                stats['clay_win_rate'] = stats.get('win_rate', 0.5)
                updated = True
            if stats.get('grass_win_rate') is None:
                stats['grass_win_rate'] = stats.get('win_rate', 0.5)
                updated = True
            if stats.get('rank') is None:
                stats['rank'] = 100
                updated = True
            if updated:
                fixed_count += 1
        
        if fixed_count > 0:
            db.save_players()
            print(f"Fixed {fixed_count} players with None values in database.")
        
        # Check if we need to update
        players = db.list_players()
        if len(players) == 0 or last_rankings_update is None:
            print("Performing initial rankings update...")
            rankings_data = rankings_fetcher.fetch_rankings_with_retry(100)
            if rankings_data:
                db.update_rankings(rankings_data)
                db.cleanup_rankings()  # Clean up any players ranked 999
                last_rankings_update = datetime.now()
                print(f"Initial rankings update complete. Loaded {len(rankings_data)} players.")
    except Exception as e:
        print(f"Could not perform initial rankings update: {e}")
        print("You can manually update rankings using: python update_rankings.py")
        print("Or via API: GET /api/rankings/update")

# Perform initial update in background
initial_update_thread = threading.Thread(target=initial_rankings_update, daemon=True)
initial_update_thread.start()

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
        
        # Helper function to safely get stat with default
        def safe_get(stats, key, default):
            value = stats.get(key)
            return default if value is None else value
        
        # Safely extract all stats with defaults
        p1_rank = safe_get(p1_stats, 'rank', 100)
        p1_win_rate = safe_get(p1_stats, 'win_rate', 0.5)
        p1_surface_win_rate = safe_get(p1_stats, surface_map[surface], p1_win_rate)
        p1_recent_form = safe_get(p1_stats, 'recent_form', 0.5)
        p1_age = safe_get(p1_stats, 'age', 25)
        
        p2_rank = safe_get(p2_stats, 'rank', 100)
        p2_win_rate = safe_get(p2_stats, 'win_rate', 0.5)
        p2_surface_win_rate = safe_get(p2_stats, surface_map[surface], p2_win_rate)
        p2_recent_form = safe_get(p2_stats, 'recent_form', 0.5)
        p2_age = safe_get(p2_stats, 'age', 25)
        
        p1_prediction_stats = {
            'rank': p1_rank,
            'win_rate': p1_win_rate,
            'surface_win_rate': p1_surface_win_rate,
            'recent_form': p1_recent_form,
            'age': p1_age
        }
        
        p2_prediction_stats = {
            'rank': p2_rank,
            'win_rate': p2_win_rate,
            'surface_win_rate': p2_surface_win_rate,
            'recent_form': p2_recent_form,
            'age': p2_age
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
    'h2h': h2h,
    'player1_odds': result['player1_odds'],
    'player2_odds': result['player2_odds'],
})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rankings/update', methods=['POST', 'GET'])
def update_rankings():
    """Update ATP rankings from official website."""
    global last_rankings_update
    
    try:
        with rankings_update_lock:
            print("Fetching latest ATP rankings...")
            rankings_data = rankings_fetcher.fetch_rankings_with_retry(100)
            
            if not rankings_data:
                return jsonify({
                    'error': 'Failed to fetch rankings from ATP website',
                    'last_update': last_rankings_update.isoformat() if last_rankings_update else None
                }), 500
            
            # Update database with new rankings (automatically keeps only top 100)
            update_stats = db.update_rankings(rankings_data)
            
            # Clean up any remaining players with rank > 100 or rank 999
            cleanup_stats = db.cleanup_rankings()
            
            last_rankings_update = datetime.now()
            
            return jsonify({
                'success': True,
                'message': 'Rankings updated successfully',
                'stats': update_stats,
                'cleanup': cleanup_stats,
                'last_update': last_rankings_update.isoformat(),
                'players_fetched': len(rankings_data),
                'total_players': len(db.players)
            })
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'last_update': last_rankings_update.isoformat() if last_rankings_update else None
        }), 500

@app.route('/api/rankings/status', methods=['GET'])
def rankings_status():
    """Get status of rankings update."""
    global last_rankings_update
    
    # Count players by rank
    top_100_count = sum(1 for stats in db.players.values() if stats.get('rank', 999) <= 100)
    invalid_count = sum(1 for stats in db.players.values() if stats.get('rank', 999) > 100)
    
    return jsonify({
        'last_update': last_rankings_update.isoformat() if last_rankings_update else None,
        'needs_update': last_rankings_update is None or (datetime.now() - last_rankings_update) > timedelta(days=1),
        'total_players': len(db.players),
        'top_100_players': top_100_count,
        'invalid_rankings': invalid_count
    })

@app.route('/api/rankings/cleanup', methods=['POST', 'GET'])
def cleanup_rankings():
    """Remove all players not in the top 100 and fix None values."""
    try:
        cleanup_stats = db.cleanup_rankings()
        
        # Also fix any remaining None values in all stats
        fixed_count = 0
        for name, stats in db.players.items():
            updated = False
            if stats.get('age') is None:
                stats['age'] = 25
                updated = True
            if stats.get('win_rate') is None:
                stats['win_rate'] = 0.5
                updated = True
            if stats.get('recent_form') is None:
                stats['recent_form'] = 0.5
                updated = True
            if stats.get('hard_win_rate') is None:
                stats['hard_win_rate'] = stats.get('win_rate', 0.5)
                updated = True
            if stats.get('clay_win_rate') is None:
                stats['clay_win_rate'] = stats.get('win_rate', 0.5)
                updated = True
            if stats.get('grass_win_rate') is None:
                stats['grass_win_rate'] = stats.get('win_rate', 0.5)
                updated = True
            if stats.get('rank') is None:
                stats['rank'] = 100
                updated = True
            if updated:
                fixed_count += 1
        
        if fixed_count > 0:
            db.save_players()
        
        return jsonify({
            'success': True,
            'message': 'Cleanup completed',
            'stats': cleanup_stats,
            'stats_fixed': fixed_count
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

def auto_update_rankings():
    """Background thread to auto-update rankings daily."""
    global last_rankings_update
    while True:
        try:
            # Wait 24 hours
            time.sleep(24 * 60 * 60)
            
            print(f"[{datetime.now()}] Auto-updating ATP rankings...")
            rankings_data = rankings_fetcher.fetch_rankings_with_retry(100)
            
            if rankings_data:
                with rankings_update_lock:
                    db.update_rankings(rankings_data)
                    db.cleanup_rankings()  # Clean up any players ranked 999
                    last_rankings_update = datetime.now()
                    print(f"[{datetime.now()}] Rankings updated successfully. Total players: {len(db.players)}")
            else:
                print(f"[{datetime.now()}] Failed to fetch rankings. Will retry in 24 hours.")
                
        except Exception as e:
            print(f"[{datetime.now()}] Error in auto-update: {e}")

if __name__ == '__main__':
    # Start auto-update thread for daily rankings updates
    update_thread = threading.Thread(target=auto_update_rankings, daemon=True)
    update_thread.start()
    print("Auto-update thread started (will update rankings daily)")
    
    print("\n" + "="*70)
    print("ATP Tennis Match Prediction Web Application")
    print("="*70)
    print("Starting server...")
    print("\n✓ Server will be available at: http://127.0.0.1:5001")
    print("✓ Open your browser and navigate to the URL above")
    print("\nAPI Endpoints:")
    print("  - GET/POST /api/rankings/update - Update rankings from ATP website")
    print("  - GET /api/rankings/status - Check rankings update status")
    print("  - GET/POST /api/rankings/cleanup - Remove players not in top 100")
    print("="*70 + "\n")
    try:
        app.run(debug=True, host='127.0.0.1', port=5001, use_reloader=False)
    except OSError as e:
        if "address already in use" in str(e).lower() or "address already in use" in str(e):
            print(f"\n❌ ERROR: Port 5001 is already in use!")
            print("   Try one of these solutions:")
            print("   1. Close the other application using port 5001")
            print("   2. Change the port in app.py (line 268) to another port (e.g., 3000, 8000, 8888)")
            print(f"\n   Error details: {e}")
        else:
            raise


