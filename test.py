import curses
import time
import socket
import serial
import os
import subprocess

def upload_code():
	build_process = subprocess.Popen("pros build", shell=True)
	build_process.wait()

	upload_process = subprocess.Popen("pros upload", shell=True)
	upload_process.wait()

def update_dashboard(stdscr):

    ser = serial.Serial('/dev/ttyACM1', 9600)
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()

    # Turn off echoing of keys, and enter cbreak mode,
    # where no buffering is performed on keyboard input
    curses.noecho()
    curses.cbreak()

    # Clear the screen and hide the cursor
    stdscr.clear()
    curses.curs_set(0)

    try:
        # Define the dashboard layout
        stdscr.addstr(0, 0, "Dashboard", curses.A_BOLD)
        
        while True:
            data = ser.readline().decode().split(";")
            for i in range(len(data)):
                stdscr.addstr(2+i, 0, " " *40)
                stdscr.addstr(2+i, 0, data[i])

            # Refresh the screen
            stdscr.refresh()

            # Wait for a while before updating again
            time.sleep(.001)

    except KeyboardInterrupt:
        pass

    finally:
        # Clean up
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        pass

upload_code()
# Run the dashboard
curses.wrapper(update_dashboard)
