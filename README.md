## SPDA.ThreadsWithLocks
Apply parallel and distributed computing to computational problems and analyze the scalability and efficiency of the solutions.

# Error loggin with threads
The script generates 10 application threads (`RunningApplication`) that produce random errors. Serious errors are captured in `SerErr.txt` and displayed by the `DisplayError` thread.

## Features
1. **Clear files:** Clears log files at the start.
2. **Append errors:** Adds errors to `app.log`.
3. **RunningApplication:** Generates random errors (serious or warning).
4. **ProcessError:** Moves all serious errors to `SerErr.txt`.
5. **DisplayError:** Prints serious errors to the console.
6. **Thread synchronization:** Uses locks and events to prevent race conditions.

# run
python err.py