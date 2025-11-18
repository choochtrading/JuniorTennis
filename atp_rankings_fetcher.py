"""
ATP Rankings Fetcher
Fetches current ATP rankings from the official ATP Tour website
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Optional
import time
from datetime import datetime

class ATPRankingsFetcher:
    """Fetches ATP rankings from the official website."""
    
    def __init__(self):
        self.base_url = "https://www.atptour.com"
        self.rankings_url = "https://www.atptour.com/en/rankings/singles"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_rankings(self, top_n: int = 100) -> List[Dict]:
        """
        Fetch ATP rankings from the official website.
        
        Args:
            top_n: Number of top players to fetch (default: 100)
            
        Returns:
            List of player dictionaries with rank, name, and points
        """
        try:
            # Method 1: Try ATP API endpoint (most reliable)
            api_urls = [
                f"https://www.atptour.com/-/ajax/rankings/overview/rankDate/ATP/latest/rankType/RANKING/limit/{top_n}/offset/0",
                f"https://www.atptour.com/-/ajax/rankings/overview/rankDate/latest/rankType/RANKING/limit/{top_n}/offset/0",
                f"https://www.atptour.com/api/rankings/singles?limit={top_n}"
            ]
            
            for api_url in api_urls:
                try:
                    response = requests.get(api_url, headers=self.headers, timeout=15)
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            players = []
                            
                            # Parse the JSON response - ATP API structure may vary
                            rankings = None
                            if 'rankings' in data:
                                rankings = data['rankings']
                            elif 'items' in data:
                                rankings = data['items']
                            elif isinstance(data, list):
                                rankings = data
                            elif 'players' in data:
                                rankings = data['players']
                            
                            if rankings:
                                for idx, player in enumerate(rankings[:top_n], 1):
                                    player_name = self._extract_player_name(player)
                                    if player_name:
                                        players.append({
                                            'rank': idx,
                                            'name': player_name,
                                            'points': player.get('points', player.get('rankingPoints', 0)),
                                            'age': player.get('age', None),
                                            'country': player.get('country', {}).get('code', '') if isinstance(player.get('country'), dict) else ''
                                        })
                                
                                if players:
                                    return players
                        except (json.JSONDecodeError, KeyError, TypeError):
                            continue
                except requests.RequestException:
                    continue
            
            # Method 2: Try scraping the HTML page
            return self._scrape_rankings_html(top_n)
            
        except Exception as e:
            print(f"Error fetching rankings: {e}")
            return []
    
    def _extract_player_name(self, player_data: Dict) -> Optional[str]:
        """Extract player name from player data."""
        # Try different possible field names
        if 'player' in player_data:
            player = player_data['player']
            if isinstance(player, dict):
                first_name = player.get('firstName', '')
                last_name = player.get('lastName', '')
                return f"{first_name} {last_name}".strip()
        elif 'firstName' in player_data and 'lastName' in player_data:
            first_name = player_data.get('firstName', '')
            last_name = player_data.get('lastName', '')
            return f"{first_name} {last_name}".strip()
        elif 'name' in player_data:
            return player_data['name']
        elif 'playerName' in player_data:
            return player_data['playerName']
        
        return None
    
    def _scrape_rankings_html(self, top_n: int = 100) -> List[Dict]:
        """Fallback method to scrape rankings from HTML."""
        try:
            response = requests.get(self.rankings_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            players = []
            
            # Look for rankings table
            # The ATP website structure may vary, so we try multiple selectors
            table = soup.find('table') or soup.find('div', class_='rankings-table')
            
            if table:
                rows = table.find_all('tr')[1:top_n+1]  # Skip header row
                
                for idx, row in enumerate(rows, 1):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        # Extract player name (usually in second cell or link)
                        name_cell = cells[1]
                        link = name_cell.find('a')
                        if link:
                            player_name = link.get_text(strip=True)
                        else:
                            player_name = name_cell.get_text(strip=True)
                        
                        if player_name:
                            players.append({
                                'rank': idx,
                                'name': player_name,
                                'points': 0,
                                'age': None,
                                'country': ''
                            })
            
            return players[:top_n]
            
        except Exception as e:
            print(f"Error scraping HTML: {e}")
            return []
    
    def fetch_rankings_with_retry(self, top_n: int = 100, max_retries: int = 3) -> List[Dict]:
        """Fetch rankings with retry logic."""
        for attempt in range(max_retries):
            try:
                players = self.fetch_rankings(top_n)
                if players:
                    return players
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return []


def get_current_rankings(top_n: int = 100) -> List[Dict]:
    """
    Convenience function to get current ATP rankings.
    
    Args:
        top_n: Number of top players to fetch
        
    Returns:
        List of player dictionaries
    """
    fetcher = ATPRankingsFetcher()
    return fetcher.fetch_rankings_with_retry(top_n)


if __name__ == "__main__":
    # Test the fetcher
    print("Fetching ATP rankings...")
    fetcher = ATPRankingsFetcher()
    rankings = fetcher.fetch_rankings_with_retry(100)
    
    print(f"\nFetched {len(rankings)} players:")
    for player in rankings[:10]:  # Show first 10
        print(f"{player['rank']}. {player['name']}")

