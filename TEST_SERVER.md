# How to Start the Server

## Fixed Issues
- ✅ Fixed syntax error with `global` declaration
- ✅ Server should now start properly

## Starting the Server

### Method 1: Using the Batch File (Easiest)
Double-click `start_server.bat` in Windows Explorer

### Method 2: Using Command Line
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```
   cd "C:\Users\flame\OneDrive\Desktop\New folder"
   ```
3. Run:
   ```
   python app.py
   ```

### Method 3: Using Python Script
```
python start_server.py
```

## What to Expect

When the server starts, you should see:
```
======================================================================
ATP Tennis Match Prediction Web Application
======================================================================
Starting server...
Open your browser and navigate to: http://127.0.0.1:5000
======================================================================
```

Then open your browser and go to: **http://127.0.0.1:5000**

## Troubleshooting

### If the site still cannot be reached:

1. **Check if the server is running**
   - Look for the Flask output in the terminal
   - You should see: "Running on http://127.0.0.1:5000"

2. **Check for errors**
   - Look for any error messages in the terminal
   - Common issues:
     - Port 5000 already in use
     - Missing dependencies
     - Import errors

3. **Try a different port**
   - If port 5000 is busy, edit `app.py` and change:
     ```python
     app.run(debug=True, host='0.0.0.0', port=5000)
     ```
     to:
     ```python
     app.run(debug=True, host='0.0.0.0', port=5001)
     ```
     Then use: http://127.0.0.1:5001

4. **Check Windows Firewall**
   - Windows Firewall might be blocking the connection
   - Try temporarily disabling it to test

5. **Check if Python is in PATH**
   - Run: `python --version`
   - If it doesn't work, try: `py --version` or `python3 --version`

## Quick Test

To verify everything works, run:
```python
python -c "from app import app; print('Server can start!')"
```

If this works, the server should start fine.

