import pydirectinput
import pyautogui # Added back JUST for initial position
import time
import sys
import keyboard
import math

# --- Configuration ---
INTER_CLICK_DELAY = 0.2  # Seconds between clicks (after click, before next move starts)
PRE_CLICK_DELAY = 0.2    # Seconds to wait AFTER move finishes, BEFORE clicking
MOVE_DURATION = 0.08     # Seconds the mouse cursor takes to travel between points
STEPS_PER_SECOND = 80    # How many small moves per second for smoothing (TUNABLE)

# --- MODIFIED: Delay now happens after the 8th click ---
POST_SEQUENCE_DELAY = 1.0 # Seconds after the 8th click before looping
INITIAL_WAIT_SECONDS = 3 # Wait time before starting the first loop
EXIT_KEY = 'q' # Key to press to stop the script

# --- Hardcoded Click Locations ---
# --- MODIFIED: Added an 8th location ---
CLICK_LOCATIONS = [
    (280, 568),  # 1st Click Location
    (650, 430),  # 2nd Click Location
    (457, 563),  # 3rd Click Location
    (650, 430),  # 4th Click Location
    (640, 563),  # 5th Click Location
    (650, 430),  # 6th Click Location
    (870, 700),  # 7th Click Location
    (880, 700),  # 8th Click Location - REPLACE WITH YOUR VALUES
]
# --------------------------------

# Global variable to track mouse position
current_mouse_x = 0
current_mouse_y = 0

def check_for_exit():
    """Checks if the exit key is pressed and exits if it is."""
    if keyboard.is_pressed(EXIT_KEY):
        print(f"\n'{EXIT_KEY}' pressed. Stopping script.")
        sys.exit(0)

def smooth_move(target_x, target_y, duration):
    """Manually moves the mouse smoothly over a given duration."""
    global current_mouse_x, current_mouse_y
    start_x, start_y = current_mouse_x, current_mouse_y

    if duration <= 0:
        pydirectinput.moveTo(target_x, target_y)
        current_mouse_x, current_mouse_y = target_x, target_y
        return

    total_steps = max(1, math.ceil(duration * STEPS_PER_SECOND))
    sleep_time = duration / total_steps
    dx = (target_x - start_x) / total_steps
    dy = (target_y - start_y) / total_steps

    print(f"  -> Moving smoothly to ({target_x}, {target_y}) over {duration}s...")

    for step in range(total_steps):
        check_for_exit()

        intermediate_x = start_x + dx * (step + 1)
        intermediate_y = start_y + dy * (step + 1)

        pydirectinput.moveTo(int(intermediate_x), int(intermediate_y))
        current_mouse_x, current_mouse_y = int(intermediate_x), int(intermediate_y)

        check_for_exit()
        time.sleep(sleep_time)

    if current_mouse_x != target_x or current_mouse_y != target_y:
         check_for_exit()
         pydirectinput.moveTo(target_x, target_y)
         current_mouse_x, current_mouse_y = target_x, target_y


def perform_click_sequence(locations):
    """Moves smoothly, waits, clicks, waits, then repeats."""
    global current_mouse_x, current_mouse_y

    if not locations:
        print("No locations provided to click.")
        return

    num_locations = len(locations) # This will now be 8
    for i, (x, y) in enumerate(locations):
        try:
            check_for_exit()

            smooth_move(x, y, MOVE_DURATION)

            check_for_exit()

            print(f"     Pausing for {PRE_CLICK_DELAY}s before click...")
            start_pre_click_delay = time.time()
            while time.time() - start_pre_click_delay < PRE_CLICK_DELAY:
                 check_for_exit()
                 time.sleep(0.02)

            check_for_exit()

            print(f"     Clicking at current location ({x}, {y})...")
            pydirectinput.click()
            print(f"     Clicked ({x}, {y}).")

            # Wait INTER_CLICK_DELAY AFTER click, except after the last one
            if i < num_locations - 1: # This condition correctly handles 8 locations
                print(f"     Pausing for {INTER_CLICK_DELAY} seconds (before next move)...")
                start_inter_click_delay = time.time()
                while time.time() - start_inter_click_delay < INTER_CLICK_DELAY:
                    check_for_exit()
                    time.sleep(0.02)

        except SystemExit:
             raise
        except Exception as e:
            if "permission" in str(e).lower() and "keyboard" in str(e).lower():
                 print(f"\nError: {e}")
                 print("The 'keyboard' library might require root/admin privileges.")
            else:
                print(f"\nAn error occurred during click sequence: {e}")
            sys.exit(1)


if __name__ == "__main__":
    click_locations = CLICK_LOCATIONS

    # --- MODIFIED: Check for exactly 8 locations ---
    if not click_locations or len(click_locations) != 8:
        print("Error: CLICK_LOCATIONS list is not defined correctly.")
        print("Please ensure it contains exactly EIGHT (x, y) tuples.") # Updated message
        sys.exit(1)
    # ---------------------------------------------

    print("Getting initial mouse position...")
    try:
        current_mouse_x, current_mouse_y = pyautogui.position()
        print(f"Mouse starting at: ({current_mouse_x}, {current_mouse_y})")
    except Exception as e:
        print(f"\nWarning: Could not get initial mouse position using pyautogui: {e}")
        print("Assuming starting position (0, 0). First move might be long.")
        current_mouse_x, current_mouse_y = 0, 0
    # ----------------------------------------------------------

    print("-" * 30)
    print("Using pydirectinput library with manual smooth movement.")
    print("Using hardcoded coordinates:")
    # This loop automatically handles printing 8 locations now
    for i, (x, y) in enumerate(click_locations):
        print(f"  Click #{i+1}: ({x}, {y})")
    print("-" * 30)
    # This print statement automatically adapts using len()
    print(f"Will click these {len(click_locations)} locations in a loop.")
    print(f"Mouse move duration: {MOVE_DURATION}s")
    print(f"Steps per second for move: {STEPS_PER_SECOND}")
    print(f"Delay BEFORE click (after move): {PRE_CLICK_DELAY}s")
    print(f"Delay BETWEEN clicks (after click): {INTER_CLICK_DELAY}s")
    print(f"Delay AFTER sequence: {POST_SEQUENCE_DELAY}s")
    print("\n!!! IMPORTANT !!!")
    print(f"The script will start clicking in {INITIAL_WAIT_SECONDS} seconds.")
    print(f"Press and hold '{EXIT_KEY}' to STOP the script at any time.")
    print("You can also press Ctrl+C in the terminal.")
    print("NOTE: The corner mouse Fail-Safe is NOT available with pydirectinput.")
    print("-" * 30)

    try:
        # Initial wait loop with exit check
        start_time = time.time()
        while time.time() - start_time < INITIAL_WAIT_SECONDS:
            check_for_exit()
            remaining = INITIAL_WAIT_SECONDS - (time.time() - start_time)
            print(f"Starting in {remaining:.1f} seconds... (Press '{EXIT_KEY}' to cancel)", end='\r')
            time.sleep(0.05)
        print("\nStarting clicks now!" + " "*30)

        loop_count = 0
        # Infinite loop
        while True:
            check_for_exit()

            loop_count += 1
            print(f"\n--- Starting Loop #{loop_count} ---")

            perform_click_sequence(click_locations) # Handles 8 locations now

            print(f"--- Sequence Complete ---")
            print(f"Pausing for {POST_SEQUENCE_DELAY} seconds before next loop...")
            start_delay_time = time.time()
            while time.time() - start_delay_time < POST_SEQUENCE_DELAY:
                check_for_exit()
                time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nScript interrupted by user (Ctrl+C).")
    except SystemExit as e:
        pass
    except Exception as e:
        if "permission" in str(e).lower() and "keyboard" in str(e).lower():
             print(f"\nError: {e}")
             print("The 'keyboard' library might require root/admin privileges.")
        else:
            print(f"\nAn unexpected error occurred in the main loop: {e}")
    finally:
        print("Script finished.")
