"""
Simple script to start the Flask server
Run this to start the web application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        print("Starting ATP Tennis Prediction Server...")
        print("=" * 70)
        
        # Import and run the app
        from app import app
        
        print("\nServer is starting...")
        print("Once started, open your browser and navigate to:")
        print("  http://127.0.0.1:5000")
        print("\nPress Ctrl+C to stop the server\n")
        print("=" * 70 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

