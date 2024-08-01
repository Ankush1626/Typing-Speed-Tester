import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()  # clears the screen
    # adds string to the stdscr(prints it)
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()  # refresh the screen
    stdscr.getkey()  # wait for user input to press any key


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)  # Display the target text
    stdscr.addstr(7, 0, f"WPM: {wpm}")  # Display WPM at a fixed position

    # Determine screen width to handle line wrapping
    max_y, max_x = stdscr.getmaxyx()

    for idx, char in enumerate(current):
        # Calculate the position in terms of rows and columns
        j = idx // max_x  # Line number
        i = idx % max_x   # Column number

        if j >= max_y - 1:
            break  # Stop if text goes beyond screen height

        if idx < len(target):
            correct_char = target[idx]
            if char == ' ' and target[idx] != ' ':
                stdscr.addstr(j, i, char, curses.color_pair(2) | curses.A_REVERSE)
            elif char == ' ' and target[idx] == ' ':
                stdscr.addstr(j, i, char, curses.color_pair(1))
            elif char == correct_char:
                stdscr.addstr(j, i, char, curses.color_pair(1))
            else:
                stdscr.addstr(j, i, char, curses.color_pair(2))
        else:
            stdscr.addstr(j, i, char, curses.color_pair(2))

def load_text():
    with open("text.txt", "r") as f:
        lines=f.readlines()
        return random.choice(lines).strip() #.strip() removes any leading or trailing backspace or new line \n character which is always present in text but is not shown to us

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    correct_chars = 0  # Track the number of correct characters
    wpm = 0
    start_time = time.time()
    time_limit = 60  # Time limit in seconds
    stdscr.nodelay(True)  # Keep the code running even if no key is pressed

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        time_remaining = time_limit - time_elapsed

        # Calculate correct characters
        correct_chars = sum(1 for i, char in enumerate(current_text) if i < len(target_text) and char == target_text[i])

        wpm = round((correct_chars / (time_elapsed / 60)) / 5)  # /5 because a word has avg of 5 letters

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.addstr(8, 0, f"Time remaining: {max(int(time_remaining), 0)} seconds")  # Display remaining time
        stdscr.refresh()

        if "".join(current_text) == target_text or time_remaining <= 0:
            stdscr.nodelay(False)  # Stop the nodelay to show end screen
            return ("" if "".join(current_text) == target_text else "Time's up!", wpm)
        
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ASCII value of ESC key
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):  # Value of backspace in different OS
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        status_message, final_wpm = wpm_test(stdscr)
        stdscr.clear()
        stdscr.addstr(9, 0, status_message if status_message else "You completed the text!")
        stdscr.addstr(10, 0, f"Final WPM: {final_wpm}")
        stdscr.addstr(11, 0, "Double press any key to continue or ESC to exit...")
        stdscr.refresh()
        
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break

        key = stdscr.getkey()
        
        if ord(key) == 27:
            break




wrapper(main)
