# Err.py
"""
Betty Phipps
09/28/2025
Module 4: Properly design and build a solution using threads with locks
Due Sunday September 21
This script stimulates multiple application threads producing errors. It logs
errors to a file, processes "Serious Errors" to a separate file, and displays them.
Threading and locks are used for concurrency and file safety.
"""
import threading
import random
import time

# File names
LOG_FILE = "app.log"
SER_FILE = "SerErr.txt"

# Lock for file operations
file_lock = threading.Lock()


#function to clear a file
def clear_file(filename):
    with file_lock:
        open(filename, "w").close()

#function to append an error message to log file
def append_log(err_type, message):
    with file_lock:
        with open(LOG_FILE, "a") as f:
            f.write(f"{err_type}||{message}\n")

# function to read and clear a file
def read_and_clear(filename):
    with file_lock:
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []
        open(filename, "w").close()
    return [ln.strip() for ln in lines]

# Function for each running application thread
def RunningApplication():
    for _ in range(200):
        n = random.randint(1, 100)
        if 1 <= n <= 15:  # Serious Error
            append_log("Serious Error", "A really bad thing happened")
        elif 16 <= n <= 35:  # Warning (ignored for display)
            append_log("Warning", "Just a warning")
        time.sleep(0.001)
    print("RunningApplication Ended")

# function to process serious errors
def ProcessError(running_done_event):
    while True:
        lines = read_and_clear(LOG_FILE)
        serious = [ln.split("||", 1)[1] for ln in lines if ln.startswith("Serious Error")]
        if serious:
            with file_lock:
                with open(SER_FILE, "a") as f:
                    for msg in serious:
                        f.write(msg + "\n")
        # exit when all running aplication finished and no more lines to process
        if running_done_event.is_set() and not lines:
            break
        time.sleep(0.05)
    print("ProcessError Ended")

# function display serious errors   
def DisplayError(running_done_event):
    while True:
        lines = read_and_clear(SER_FILE)
        for ln in lines:
            print(ln)
        # exit when all running aplication finished and no more lines to display
        if running_done_event.is_set() and not lines:
            break
        time.sleep(0.05)
    print("DisplayError Ended")

# starting threads
def main():
    random.seed(time.time())    #initalize random number generator
    clear_file(LOG_FILE)
    clear_file(SER_FILE)

    # event to singal that all running application threads are done
    running_done_event = threading.Event()

    proc_thread = threading.Thread(target=ProcessError, args=(running_done_event,))
    disp_thread = threading.Thread(target=DisplayError, args=(running_done_event,))
    proc_thread.start()
    disp_thread.start()

    runners = []    #starting multiple running application threads
    for _ in range(10):
        t = threading.Thread(target=RunningApplication)
        runners.append(t)
        t.start()

    # wait for all running application threads
    for t in runners:
        t.join()

    # signal that running application threads are done
    running_done_event.set()
    proc_thread.join()
    disp_thread.join()

if __name__ == "__main__":
    main()
