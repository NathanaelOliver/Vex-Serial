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
    port = 7
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
        stdscr.addstr(2, 0, "x_loc: ")
        stdscr.addstr(3, 0, "y_loc: ")
        stdscr.addstr(4, 0, "theta: ")

        # Simulate updating sensor data
        sensor1_value = 0
        sensor2_value = 0
        sensor3_value = 0

        while True:
            data = ser.readline().decode().split(";")



            # Clear previous sensor values
            stdscr.addstr(2, 7, " " * 10)
            stdscr.addstr(3, 7, " " * 10)
            stdscr.addstr(4, 7, " " * 10)

            # Print updated sensor values
            stdscr.addstr(2, 7, str(data[0]))
            stdscr.addstr(3, 7, str(data[1]))
            stdscr.addstr(4, 7, str(data[2]))

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


upload_code()
# Run the dashboard
curses.wrapper(update_dashboard)
