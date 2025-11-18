"""
Manual script to update ATP rankings
Run this script to fetch and update rankings from the official ATP website
"""

from atp_rankings_fetcher import ATPRankingsFetcher
from player_database import PlayerDatabase
from datetime import datetime

def main():
    print("="*70)
    print("ATP Rankings Updater")
    print("="*70)
    print(f"Starting update at {datetime.now()}\n")
    
    # Initialize fetcher and database
    fetcher = ATPRankingsFetcher()
    db = PlayerDatabase()
    
    # Fetch rankings
    print("Fetching current ATP rankings from official website...")
    rankings = fetcher.fetch_rankings_with_retry(100)
    
    if not rankings:
        print("ERROR: Failed to fetch rankings. Please check your internet connection.")
        print("The ATP website may have changed its structure or is temporarily unavailable.")
        return
    
    print(f"Successfully fetched {len(rankings)} players\n")
    
    # Show top 10
    print("Top 10 players fetched:")
    for player in rankings[:10]:
        print(f"  {player['rank']}. {player['name']}")
    print()
    
    # Update database (automatically keeps only top 100)
    print("Updating player database...")
    stats = db.update_rankings(rankings)
    
    # Clean up any remaining players with rank > 100
    print("Cleaning up players not in top 100...")
    cleanup_stats = db.cleanup_rankings()
    
    print("\nUpdate Statistics:")
    print(f"  - Players updated: {stats['updated']}")
    print(f"  - New players added: {stats['added']}")
    print(f"  - Players removed: {cleanup_stats.get('removed', 0)}")
    print(f"  - Total players in database: {stats['total_players']}")
    print(f"  - Rankings fetched: {stats['rankings_fetched']}")
    print()
    print("✓ Rankings updated successfully!")
    print("✓ Only top 100 players are now in the database")
    print("="*70)

if __name__ == "__main__":
    main()

