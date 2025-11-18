# ATP Rankings API Documentation

This application includes functionality to automatically fetch and update ATP rankings from the official [ATP Tour website](https://www.atptour.com/en/rankings/singles).

## Features

- **Automatic Daily Updates**: Rankings are automatically updated every 24 hours in the background
- **Manual Update API**: Update rankings on-demand via API endpoint
- **Status Checking**: Check when rankings were last updated

## API Endpoints

### 1. Update Rankings

**Endpoint**: `/api/rankings/update`  
**Methods**: `GET` or `POST`  
**Description**: Fetches current ATP rankings from the official website and updates the player database.

**Response** (Success):
```json
{
  "success": true,
  "message": "Rankings updated successfully",
  "stats": {
    "updated": 95,
    "added": 5,
    "total_players": 100,
    "rankings_fetched": 100
  },
  "last_update": "2025-01-15T10:30:00",
  "players_fetched": 100
}
```

**Response** (Error):
```json
{
  "error": "Failed to fetch rankings from ATP website",
  "last_update": "2025-01-14T10:30:00"
}
```

**Example Usage**:
```bash
# Using curl
curl http://localhost:5000/api/rankings/update

# Using Python requests
import requests
response = requests.get('http://localhost:5000/api/rankings/update')
print(response.json())
```

### 2. Check Rankings Status

**Endpoint**: `/api/rankings/status`  
**Method**: `GET`  
**Description**: Returns the last update time and whether an update is needed.

**Response**:
```json
{
  "last_update": "2025-01-15T10:30:00",
  "needs_update": false
}
```

**Example Usage**:
```bash
curl http://localhost:5000/api/rankings/status
```

## Manual Update Script

You can also update rankings manually using the provided script:

```bash
python update_rankings.py
```

This script will:
1. Fetch the current top 100 ATP rankings
2. Update the player database
3. Display update statistics

## Automatic Updates

The application automatically updates rankings every 24 hours in the background. The update thread starts when the Flask application is launched.

To disable automatic updates, you can comment out the auto-update thread initialization in `app.py`.

## How It Works

1. **Fetching**: The `ATPRankingsFetcher` class attempts to fetch rankings from:
   - ATP API endpoints (primary method)
   - HTML scraping (fallback method)

2. **Updating**: The `PlayerDatabase.update_rankings()` method:
   - Updates existing players' ranks
   - Adds new players with default statistics
   - Handles name variations and case differences

3. **Statistics**: Default win rates and statistics are calculated based on ranking position for new players.

## Troubleshooting

### Rankings Not Updating

If rankings fail to update:

1. **Check Internet Connection**: Ensure the server has internet access
2. **ATP Website Changes**: The ATP website structure may have changed. Check the `atp_rankings_fetcher.py` file
3. **Rate Limiting**: The ATP website may be rate-limiting requests. Wait a few minutes and try again
4. **Manual Update**: Use the manual update script: `python update_rankings.py`

### API Returns Empty Results

If the API returns empty results:

1. Check the server logs for error messages
2. Verify the ATP website is accessible: https://www.atptour.com/en/rankings/singles
3. The website structure may have changed - you may need to update the fetcher code

## Notes

- Rankings are fetched from the official ATP Tour website
- The application respects the website's structure and uses appropriate headers
- Updates are performed in a thread-safe manner
- Failed updates don't affect existing player data

