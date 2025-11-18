"""
Cleanup script to remove players not in top 100
Run this to remove all players with rank > 100 or rank == 999
"""

from player_database import PlayerDatabase

def main():
    print("="*70)
    print("Database Cleanup - Removing players not in top 100")
    print("="*70)
    
    db = PlayerDatabase()
    
    # Count before cleanup
    total_before = len(db.players)
    invalid_players = [
        (name, stats.get('rank', 999))
        for name, stats in db.players.items()
        if stats.get('rank', 999) > 100 or stats.get('rank', 999) == 999
    ]
    
    print(f"\nCurrent database status:")
    print(f"  - Total players: {total_before}")
    print(f"  - Players with rank > 100 or rank 999: {len(invalid_players)}")
    
    if invalid_players:
        print(f"\nPlayers to be removed:")
        for name, rank in invalid_players[:10]:  # Show first 10
            print(f"  - {name} (rank: {rank})")
        if len(invalid_players) > 10:
            print(f"  ... and {len(invalid_players) - 10} more")
    
    # Perform cleanup
    print("\nPerforming cleanup...")
    cleanup_stats = db.cleanup_rankings()
    
    print("\nCleanup Results:")
    print(f"  - Players removed: {cleanup_stats['removed']}")
    print(f"  - Players remaining: {cleanup_stats['remaining']}")
    print(f"  - Initial count: {cleanup_stats['initial_count']}")
    
    # Show top 10 players
    players = db.list_players()
    players_with_rank = [(name, db.get_player(name)['rank']) for name in players]
    players_with_rank.sort(key=lambda x: x[1])
    
    print(f"\nTop 10 players in database:")
    for name, rank in players_with_rank[:10]:
        print(f"  {rank}. {name}")
    
    print("\n✓ Cleanup completed successfully!")
    print("="*70)

if __name__ == "__main__":
    main()

