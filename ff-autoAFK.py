# OS Info Imports
import platform
from time import sleep
import threading

# GUI Imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import *

# Logic HotKey/Keypress Imports
#from pynput import keyboard
import pyautogui
#import pygetwindow as gw # This is depreciated for MacOS, will be using PyWinCtl
import pywinctl as gw

# Define global hooking variables w/ default values and get platform information
getPlatform = platform.system()
FFmainHandle = [0]
present = ''
hookLabel = ''

# Define global variable holding default key presses
keyPress = ['w', 'a', 's', 'd', 'space', 'space', 'space', '1', '2', '3', '4', 'i', 'esc', 'm', 'esc', 'l', 'esc', 'k', 'esc', 'b', 'esc']
on = True


# ------------- FFXIV AFK Logic ------------- #


# Func thats called if custom key actions are submitted
def updateKeys():
    global keyPress
    global customActionsEntry
    q = customActionsEntry.get()
    if q == '' or q == ' ':
        messagebox.showinfo('ff-autoAFK', 'No input found, using default instead')
        return
    else:
        q = q.split(',')
        keyPress = q
        return keyPress

# Kill functionality for AFK sequence
def kill():
    global on
    on = False

def afkThread():
    x = threading.Thread(target=startAFKSeq, args=(), daemon=True)
    x.start()

# Main Function that runs the AFK key presses
def startAFKSeq():
    global on
    global FFmainHandle
    if FFmainHandle == []:
        messagebox.showinfo('AFK Control', 'No Final Fantasy XIV Window Found.. Exiting.')
    else:
        t = FFmainHandle[0]
        t.activate()
        i = 0
        z = len(keyPress)
        while on:
            if z == i:
                i = 0
            else:
                pyautogui.keyDown(keyPress[i])
                sleep(1)
                pyautogui.keyUp(keyPress[i])
                sleep(1)
                i += 1

# Main Func to Grab Window Title & set present text
def getHandle():
    global getPlatform
    global FFmainHandle
    global present
    global hookLabel
    if getPlatform == 'Windows':
        FFmainHandle = gw.getWindowsWithTitle("FINAL FANTASY XIV")
    else:
        FFmainHandle = gw.getWindowsWithTitle("FINAL FANTASY XIV ONLINE")
    if FFmainHandle == []:
        present = 'No Hook Present'
        if hookLabel == '':
            return
        else:
            hookLabel.config(text=present)
    else:
        present = 'FF Hook Present'
        if hookLabel == '':
            return
        else:
            hookLabel.config(text=present)

# Func to call MessageBox for Custom Actions
def customActionsFunc():
    messagebox.showinfo('Custom Actions Help', 'If no actions are present in the custom actions; will use default.\nThis includes movement, # key presses, and default FF hotkeys to open menus then close them.\nPlease make sure it is as follows: 1,2,3,a,b,c\nThere is no spaces.\nMake Sure to keep FFXIV Focused; will work on updating it in the background.')


# ------------------ GUI~ ------------------- #


# Parent GUI Window Creation
rootWin = Tk()
rootWin.title('ff-autoAFK')
frame = ttk.Frame(rootWin, padding=15)
rootWin.geometry('320x180')
frame.grid()

# Call getHandle to get present value of FFXIV Window hook
getHandle()

# Create Label with Hook Status
hookLabel = ttk.Label(frame, text=present)

# Button to Test Ability to Hook to Final Fantasy XIV 
testHookButton = ttk.Button(frame, text="Test Hook", command=getHandle)

# Input Custom Actions
customActionsLabel = ttk.Label(frame, text="Custom Actions")
customActionsEntry = ttk.Entry(frame, show='')
customActionsSubmitButton = ttk.Button(frame, text='Submit', command=updateKeys)
customActionsExpLabel = ttk.Label(frame, text="Input as: w,w,w,a,a,1,2,3")

# Help Window Button
customActionsHelpButton = ttk.Button(frame, text="Help", command=customActionsFunc)

# Button to Run the AFK program
runButton = ttk.Button(frame, text='Run', command=afkThread)

# Label for Stop Button
stopLabel = ttk.Label(frame, text='Click the button to stop')

# Button to stop the afk sequence
stopButton = ttk.Button(frame, text='Stop', command=kill)

# Quit Button
quitButton = ttk.Button(frame, text="Quit", command=rootWin.destroy)

# Grid Positions
hookLabel.grid(row=0, column=0)
testHookButton.grid(row=1, column=0)
customActionsLabel.grid(row=0, column=1)
customActionsEntry.grid(row=1, column=1)
customActionsExpLabel.grid(row=2, column=1)
customActionsSubmitButton.grid(row=1, column=2)
customActionsHelpButton.grid(row=2, column=2)
runButton.grid(row=3, column=1)
stopLabel.grid(row=4, column=1)
stopButton.grid(row=5, column=1)
quitButton.grid(row=2, column=0)

# GUI Loop for input
rootWin.mainloop()
