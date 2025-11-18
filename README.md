# ATP Tennis Match Prediction Model

A machine learning model for predicting outcomes of ATP (Association of Tennis Professionals) tour matches using player statistics, rankings, and historical performance data.

## Features

- **Comprehensive Feature Engineering**: Uses player rankings, win rates, surface-specific performance, recent form, head-to-head records, age, and more
- **Ensemble Learning**: Combines Random Forest and Gradient Boosting classifiers for robust predictions
- **Surface-Specific Predictions**: Accounts for Hard, Clay, and Grass court surfaces
- **Easy-to-Use API**: Simple interface for making match predictions

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Tool (Recommended)

The easiest way to use the predictor is through the interactive tool:

```bash
python interactive_predictor.py
```

This will launch an interactive menu where you can:
- **Select players** from a database of ATP players
- **Choose match surface** (Hard, Clay, or Grass)
- **View predictions** with win probabilities and confidence levels
- **Browse player statistics** and rankings

The tool includes a database of top ATP players with realistic statistics. You can:
- Select players by number or by typing their name (partial matches work)
- View detailed player information including rankings, win rates, and surface-specific performance
- Get instant match predictions with detailed statistics

### Training the Model

Run the main script to train the model on synthetic ATP match data:

```bash
python tennis_prediction_model.py
```

This will:
- Generate synthetic match data (in production, you would use real ATP data)
- Engineer features from the raw data
- Train an ensemble model
- Evaluate performance
- Save the trained model to `tennis_model.pkl`
- Show example predictions

**Note:** The interactive tool will automatically train a model if one doesn't exist, so you can skip this step if you only want to use the interactive interface.

### Making Predictions Programmatically

```python
from tennis_prediction_model import TennisPredictionModel

# Load or train model
model = TennisPredictionModel()
model.load_model('tennis_model.pkl')  # Or train a new one

# Define player statistics
player1_stats = {
    'rank': 5,
    'win_rate': 0.75,
    'surface_win_rate': 0.78,  # Win rate on specific surface
    'recent_form': 0.8,  # Win rate in last 10 matches
    'age': 25,
    'h2h_wins': 2,  # Optional: head-to-head wins
    'h2h_meetings': 3  # Optional: total head-to-head meetings
}

player2_stats = {
    'rank': 45,
    'win_rate': 0.55,
    'surface_win_rate': 0.52,
    'recent_form': 0.5,
    'age': 27
}

# Predict match outcome
result = model.predict_match(player1_stats, player2_stats, surface='Hard')

print(f"Player 1 Win Probability: {result['player1_win_probability']:.2%}")
print(f"Player 2 Win Probability: {result['player2_win_probability']:.2%}")
print(f"Predicted Winner: {result['predicted_winner']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Model Features

The model uses the following features:

1. **Ranking Difference**: Normalized difference between player rankings
2. **Win Rate Difference**: Overall win rate comparison
3. **Surface Win Rate Difference**: Surface-specific performance
4. **Recent Form**: Performance in last 10 matches
5. **Head-to-Head**: Historical matchup record
6. **Age Difference**: Player age comparison
7. **Surface Type**: Hard, Clay, or Grass court
8. **Combined Strength**: Composite metric combining multiple factors
9. **Experience Factor**: Age-based experience metric

## Model Architecture

- **Random Forest Classifier**: 200 trees, max depth 15
- **Gradient Boosting Classifier**: 200 estimators, learning rate 0.1
- **Voting Classifier**: Soft voting with weighted ensemble

## Files

- **`tennis_prediction_model.py`**: Core ML model and prediction engine
- **`interactive_predictor.py`**: Interactive command-line tool for easy predictions
- **`player_database.py`**: Player database management with top ATP players
- **`example_usage.py`**: Example scripts showing various prediction scenarios
- **`tennis_model.pkl`**: Trained model (created after first training)

## Player Database

The tool includes a database of top ATP players with realistic statistics:
- Current rankings
- Overall and surface-specific win rates
- Recent form indicators
- Age information

You can easily add more players or update statistics by modifying the `PlayerDatabase` class or the `players.json` file.

## Data Sources

Currently uses synthetic data for demonstration. In production, you would integrate with:

- ATP Official API
- Tennis Abstract
- Web scraping from ATP website
- Historical match databases

## Performance

The model typically achieves:
- Accuracy: ~70-75% on test data
- Cross-validation: Stable performance across folds

## Future Improvements

- Integration with real ATP data APIs
- More sophisticated feature engineering
- Deep learning models (LSTM for sequence data)
- Real-time data updates
- Tournament-specific adjustments
- Weather and location factors
- Injury and fatigue tracking

## License

This project is for educational and research purposes.

