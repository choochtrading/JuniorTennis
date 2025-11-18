# Quick Start Guide

## Getting Started

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Interface

#### Option A: Web Interface (Recommended) 🌐
```bash
python app.py
```
Then open your browser and navigate to: **http://127.0.0.1:5000**

The web interface provides:
- Beautiful, user-friendly design
- Easy player selection with dropdowns
- Real-time player information
- Visual prediction results with probability bars
- Head-to-head statistics
- Responsive design for mobile devices

#### Option B: Command-Line Interface
```bash
python interactive_predictor.py
```

### Step 3: Make Predictions!

The interactive tool will guide you through:
1. Selecting Player 1 (by number or name)
2. Selecting Player 2 (by number or name)
3. Choosing the surface (Hard, Clay, or Grass)
4. Viewing the prediction results

## Example Session

```
======================================================================
ATP TENNIS MATCH PREDICTOR
======================================================================

Main Menu:
  1. Predict a match
  2. View all players
  3. View player details
  4. Exit

Your choice (1-4): 1

Select Player 1:
Options:
  1. Enter player number from list
  2. Enter player name (partial match OK)
  3. View all players
  4. Cancel

Your choice (1-4): 2
Enter player name (or partial name): Djokovic

Found 1 matches:
  Select number (1-1): 1

PLAYER: NOVAK DJOKOVIC
Rank:              1
Age:               37
Overall Win Rate:  85.0%
Recent Form:       83.0%
Surface-Specific Win Rates:
  Hard Court:      87.0%
  Clay Court:      82.0%
  Grass Court:     88.0%

Select Novak Djokovic? (y/n): y

Select Player 2:
...
[Similar process for Player 2]

Select Surface:
  1. Hard Court
  2. Clay Court
  3. Grass Court

Your choice (1-3): 1

======================================================================
MATCH PREDICTION
======================================================================
Player 1: Novak Djokovic
Player 2: Carlos Alcaraz
Surface:  Hard Court
======================================================================

----------------------------------------------------------------------
PREDICTION RESULTS
----------------------------------------------------------------------
Novak Djokovic            Win Probability: 58.23%
Carlos Alcaraz            Win Probability: 41.77%
----------------------------------------------------------------------

Predicted Winner: Player 1
Confidence Level: 58.2%
======================================================================
```

## Tips

### Web Interface
- **Player Selection**: Use the dropdown menus to select players (sorted by rank)
- **Player Info**: Player statistics appear automatically when you select a player
- **Surface Selection**: Click on Hard, Clay, or Grass buttons to choose the court surface
- **Results**: Predictions show win probabilities with visual bars and highlight the predicted winner

### Command-Line Interface
- **Player Selection**: You can type partial names (e.g., "Djok" for Djokovic)
- **View Players**: Use option 2 in the main menu to see all available players
- **Player Details**: Use option 3 to view detailed statistics for any player
- **Multiple Predictions**: After each prediction, you can make another without restarting

## Available Players

The database includes top ATP players such as:
- Novak Djokovic
- Carlos Alcaraz
- Daniil Medvedev
- Jannik Sinner
- Andrey Rublev
- Stefanos Tsitsipas
- Casper Ruud
- Alexander Zverev
- And more...

You can add more players by editing the `PlayerDatabase` class or the `players.json` file.


