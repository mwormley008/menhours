# Auto GUI
# This is a program that grabs information from a specified 
# Excel column and then automates the input of that list into a data entry form
# using autogui



## TODO:
# I think I might be able to use tkinter to confirm when I've made a copy that way I can just automate
# the whole first part of the making a copy step and then once I've done pressed the button 
# that one time it'll do the rest for me
import pyautogui, openpyxl, time, pyperclip, datetime, calendar
import os, re, sys
import pygetwindow as gw
from openpyxl import load_workbook
from pyautogui import write, press, keyUp, keyDown, hotkey
from time import sleep
from datetime import datetime, timedelta, date

from tkinter import Tk, simpledialog, messagebox
from tkinter.filedialog import askopenfilename

def copy_clipboard():
    hotkey('ctrl', 'c')
    time.sleep(.5)
    return pyperclip.paste()

def highlight_line():
    press('numlock')
    keyDown('shiftleft')
    press('end')
    keyUp('shiftleft')
    sleep(1)
    press('numlock')
    sleep(1)

windows = gw.getAllWindows()

qb_window = None



for window in windows:
    if "QuickBooks" in window.title:
        qb_window = window
        break

# Create the Tkinter root window
root = Tk()
root.withdraw()  # Hide the root window



# Focuses the Quickbooks window and goes to the customer:job pane
qb_window.activate()
hotkey('alt', 'j')
time.sleep(.5)

sleep(1)

today = date.today()
print(today)
res = calendar.monthrange(today.year, today.month)[1]
completed_date = f"Completed through {today.month}/{res}/{today.year}"


# starts once you have created a copy of the invoice, which will
# start with highlighting the customer job
# 8 tabs to the first item
# 10 tabs to the first price cell

# get the new invoice number
press('tab', presses=3)
new_inv = copy_clipboard()


# Goes to the contract amount / the first cell of the price column
press('tab', presses=7)
# This is previously billed
press('down', presses=1)
sleep(.5)
prev_billed = copy_clipboard()
sleep(.5)
prev_billed = prev_billed.replace(',', '')
prev_billed = prev_billed[0:-3]

# Goes to the last invoice's completed through which will become the last perioud amount
press('down', presses=2)
last_period = copy_clipboard()
sleep(.5)

# This could become a method or something since I'm doing it multiple times and it would improve 
# Legibility
last_period = last_period.replace(',', '')
last_period = last_period[0:-3]

# Combines the previously billed with the amount billed last perioud for the new previously billed
new_prev_billed = int((prev_billed)) + int((last_period))

# Sets previously retained
new_prev_retained = new_prev_billed * .1

# Alright, at this point we now have all of the information and now we're just going to be writing it to
# The quickbooks fields
press('up', presses=2)
sleep(.5)
press('backspace')
write(str(new_prev_billed))
press('down')
press('backspace')
write(str(new_prev_retained))
press('tab', presses=4)
# Deletes the completed through line, because this is the retention billing program and 
# We won't have done any additional work this perioud
hotkey('ctrl', 'delete')
sleep(1.5)
write('New Ret Due')
press('tab', presses=2)
sleep(.5)
write(str(new_prev_retained))


print_bin = messagebox.askyesno("Confirmation", "Do you want to print this?")

if print_bin:
    sleep(1)
    qb_window.activate()
    hotkey('ctrl', 'p')
    sleep(5)
    press('space') 
else:
    sys.exit()


# This is some code from ChatGPT that lets you find a file by the number
# even if it's not the only thing in the file name
