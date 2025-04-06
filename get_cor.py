# coordinate_finder.py
import pyautogui
import time
import sys

print("Move your mouse cursor to the desired click locations.")
print("Press Ctrl+C to quit.")

try:
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {str(x).ljust(4)} Y: {str(y).ljust(4)}"
        print(position_str, end='\r') # '\r' moves cursor to line start
        time.sleep(0.1) # Update 10 times per second
except KeyboardInterrupt:
    print("\nDone.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Ensure pyautogui is installed and permissions are set if needed.")
