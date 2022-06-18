###############################################################
#                                                             #
# valve.py -- contains objects for individual valve control   #
#             buttons                                         #
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Standard Imports                                            #
###############################################################
from tkinter import *
import tkinter as tk


###############################################################
# Global variables                                            #
###############################################################
pad      = 10
width    = 60
height   = 60
sl_width = 500


###############################################################
# Valve state indication light                                #
###############################################################
class RelayLED:

    def __init__(
                self, 
                root, 
                background, 
                onB, offB, 
                title, 
                width, 
                height
                ):

		#######################################################
		# class attributes                                    #
		#######################################################

		# Canvas dimensions
        self.width = width
        self.height = height

		# Color hex codes
        self.on = onB
        self.off = offB

		#######################################################
		# drawing objects                                     #
		#######################################################

		# tk canvas object	
        self.canvas = Canvas(root, width=width, height=height, bg=background, highlightthickness=0)

		# indicator circle
        self.state = self.canvas.create_oval((width / 4.0) + 1, (height / 4.0) + 1, (3 * width / 4.0) - 1, (3 * height / 4.0) - 1,
                                               fill=offB)

    def setState(self, state):
        if(state):
            self.canvas.itemconfig(self.state, fill=self.on)
        else:
            self.canvas.itemconfig(self.state, fill=self.off)

    def getWidget(self):
        return self.canvas


###############################################################
# Solenoid state control buttons                              #
###############################################################
class Buttons:
    def __init__(self, root, text, symbol):

        self.symbol = symbol

        self.switch = tk.Frame(root, background = 'black')
        #self.switch_label = tk.LabelFrame(self.switch, text = self.title)
        self.led = RelayLED(self.switch, 'black', '#41d94d', '#ed3b3b', text, width, height)
        self.state = 0
        self.off_button = tk.Button(self.switch, text="OFF", width=12, command=self.actionOff, bg='#ed3b3b', fg='white', activebackground='#d42f2f', activeforeground='white')
        self.on_button = tk.Button(self.switch, text="ON", width=12, command=self.actionOn, bg='#41d94d', fg='white', activebackground='#28bd33', activeforeground='white')
        self.off_button.pack(side="right")
        self.led.getWidget().pack(side="right")
        self.on_button.pack(side="right")
        self.switch.pack(side='left', padx=4*pad)

    def actionOff(self):
        self.led.setState(False)
        self.symbol.setState(False)
        print("1 (OFF)")

    def actionOn(self):
        print("1 (ON)")

    def setLedState(self, state):
        self.led.setState(state)

    def getFrame(self):
        return self.switch


###############################################################
# Ball valve state control buttons                            #
###############################################################
class BV_button:
    def __init__(self, root, text):
        self.switch = tk.Frame(root, background = 'black')
        self.led = RelayLED(self.switch, 'black', '#41d94d', '#ed3b3b', text, width, height)
        self.state = 0
        self.off_button = tk.Button(self.switch, text="OFF", width=12, command=self.actionOff, bg='#ed3b3b', fg='white', activebackground='#d42f2f', activeforeground='white')
        self.on_button = tk.Button(self.switch, text="ON", width=12, command=self.actionOn, bg='#41d94d', fg='white', activebackground='#28bd33', activeforeground='white')
        self.off_button.pack(side="right")
        self.led.getWidget().pack(side="right")
        self.on_button.pack(side="right")
        self.switch.pack(side='left', padx=4*pad)

    def actionOff(self):
        self.led.setState(False)
        self.symbol.setState(False)

    def actionOn(self):
        print("1 (ON)")

    def setLedState(self, state):
        self.led.setState(state)

    def getFrame(self):
        return self.switch

        serialNum = int(self.state.get())
        self.lR.config(bg="red")
        print(str(serialNum))

###############################################################
# END OF FILE                                                 #
###############################################################
