###############################################################
#                                                             #
# pipe.py -- Piping engine display component                  #
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


###############################################################
# Project Imports                                             #
###############################################################
import component_template as SDR_component_template


###############################################################
# Application Notes                                           #
###############################################################

# The following class makes it simple to connect different GUI 
# P&ID objects together with pipes. The PIPE Class operates on 
# five main parameters: pipe_top, pipe_right, pipe_buttom,
#                       pipe_left, fill

# All 5 parameters are of the data type boolean and control the 
# type of pipe and whether fluid is running through it
# (respectively)

# The booleans correspond to which side gets a pipe:
# pipe_top:   12:00
# pipe_right:  3:00
# pipe_buttom: 6:00
# pipe_left:   9:00

#        ln1

#  ln4    P    ln2

#        ln3

# By modulating these input parameters, any pipe can be designed 
# to fit the GUI P&ID.

# Additionally, all components are linked together with a singly 
# linked list (which functions more as a map). This allows for a 
# traversal of the list to enable mass flow indicators on the GUI 
# P&ID sketch.


###############################################################
#                                                             #
# OBJECT:                                                     #
# 		Pipe                                                  #
#                                                             #
# DESCRIPTION:                                                #
# 		Container of fluid on engine display, used to connect #
#       components such as valves, tanks, and the chamber     #
#                                                             #
###############################################################
class Pipe:

    def __init__(
                self       , 
                root       , # GUI window to draw on
                bg_color   , # Background color 
                width      , # Canvas dimensions  
                height     , 
                pipe_top   , # booleans indicating which sides 
                pipe_right , # have pipes connected 
                pipe_buttom, 
                pipe_left  , 
                fluidColor , # Fluid color code 
                fill         # boolean indicating whether pipe is
                ):           # filled or not

		#######################################################
		# Initialization                                      #
		#######################################################

		# Instantiate canvas to draw on
        self.canvas = Canvas(
                            root         , 
                            width=width  , 
                            height=height, 
                            bg=bg_color  , 
                            highlightthickness=0
                            )

		# Canvas dimensions
        self.width = width
        self.height = height

		# Pipe attachments
        self.line1 = pipe_top
        self.line2 = pipe_right
        self.line3 = pipe_buttom
        self.line4 = pipe_left

        self.top =    None
        self.right =  None
        self.bottom = None
        self.left =   None

		# Fluid variables
        self.state = False
        self.fluidColor = fluidColor

		#######################################################
		# Central pipe                                        #
		#######################################################

        if (fill):
            self.pipe_fluid_canvas = self.canvas.create_rectangle(
                                                  7*width /16.0, 
                                                  7*height/16.0, 
                                                  9*width /16.0, 
                                                  9*height/16.0,
                                                  fill=fluidColor )
        else:
            self.pipe_fluid_canvas = self.canvas.create_rectangle(
                                                  7*width/16.0, 
                                                  7*height/16.0, 
                                                  9*width /16.0, 
                                                  9*height/16.0,
                                                  fill='black')

		#######################################################
		# Top connecting pipe                                 #
		#######################################################

        if ( pipe_top ):
            left_wall = [
						(7*width/16.0, 0            ), 
						(7*width/16.0, 7*height/16.0)
                        ]
            self.canvas.create_line(
                                   left_wall, 
                                   width = 1, 
                                   fill='white'
                                   )
            right_wall= [
                        (9*width/16.0, 0            ), 
                        (9*width/16.0, 7*height/16.0)
                        ]
            self.canvas.create_line(
                                   right_wall, 
                                   width = 1 , 
                                   fill='white'
                                   )
			# Draw fluid in top connecting pipe
            if ( fill ):
                self.fluid_top = self.canvas.create_rectangle(
                                           (7*width /16.0)+1, 
                                            0               , 
                                           (9*width /16.0)-1,
                                           (7*height/16.0)+1,
                                           fill=fluidColor  , 
                                           outline = ""      )
            else:
                self.fluid_top = self.canvas.create_rectangle(
                                           (7*width /16.0)+1, 
                                            0               , 
                                           (9*width /16.0)-1,
                                           (7*height/16.0)+1,
                                           fill='black'     , 
                                           outline = ""      )
		# No top connecting pipe, close the top off
        else:
            top_wall = [
                       (7*width/16.0, 7*height/16.0), 
                       (9*width/16.0, 7*height/16.0)
                       ]

            self.canvas.create_line(
                                   top_wall , 
                                   width = 1, 
                                   fill='white'
                                   )

		#######################################################
		# Right connecting pipe                               #
		#######################################################

        if ( pipe_right ):
            bottom_wall = [
                          (9*width/16.0, 7*height/16.0), 
                          (  width     , 7*height/16.0)
                          ]
            top_wall =    [
                          (9*width/16.0, 9*height/16.0), 
                          (  width     , 9*height/16.0)
                          ]
            self.canvas.create_line(
                                   bottom_wall, 
                                   width = 1  , 
                                   fill='white'
                                   )
            self.canvas.create_line(
                                   top_wall , 
                                   width = 1, 
                                   fill='white'
                                   )
			# Draw fluid in right connecting pipe
            if ( fill ):
                self.fluid_right = self.canvas.create_rectangle(
                                  (9*width /16.0)  , 
                                  (7*height/16.0)+1, 
                                  (   width     )  ,
                                  (9*height/16.0)-1,
                                  fill=fluidColor  , 
                                  outline=""                   )
            else:
                self.fluid_right = self.canvas.create_rectangle(
                                   (9*width /16.0)  , 
                                   (7*height/16.0)+1, 
                                   (  width      )  ,
                                   (9*height/16.0)-1,
                                   fill='black'     , 
                                   outline = ""                )
		# No top connecting pipe, close the right off
        else:
            right_wall= [
                        (9*width/16.0, 7*height/16.0), 
                        (9*width/16.0, 9*height/16.0)
                        ]
            self.canvas.create_line(
                                   right_wall, 
                                   width = 1 , 
                                   fill='white'
                                   )

        if (pipe_buttom):
            xy = [
                 (7*width/16.0, 9*height/16.0), 
                 (7*width/16.0,   height     )
                 ]

            self.canvas.create_line(
                                   xy, 
                                   width=1, 
                                   fill='white'
                                   )

            xy2 = [
                  (9*width/16.0, 9*height/16.0), 
                  (9*width/16.0,   height     )
                  ]

            self.canvas.create_line(
                                    xy2, 
                                    width=1, 
                                    fill='white'
                                    )

            if (fill):
                self.fluid_buttom = self.canvas.create_rectangle(
                                    (7*width /16.0)+1, 
                                    (9*height/16.0)  , 
                                    (9*width /16.0)-1,
                                    (  height     )  ,
                                    fill=fluidColor  , 
                                    outline=""
                                                                )
            else:
                self.fluid_buttom = self.canvas.create_rectangle(
                                    (7*width /16.0)+1, 
                                    (9*height/16.0)  , 
                                    (9*width /16.0)-1,
                                    (  height    )   ,
                                    fill='black'     , 
                                    outline=""
                                                                )
        else:
            xy = [
                 (7*width/16.0, 9*height/16.0), 
                 (9*width/16.0, 9*height/16.0)
                 ]

            self.canvas.create_line(
                                   xy          , 
                                   width=1     , 
                                   fill='white'
                                   )

        if (pipe_left):
            xy = [
                 (  0         , 7*height/16.0), 
                 (7*width/16.0, 7*height/16.0)
                 ]

            self.canvas.create_line(
                                   xy          , 
                                   width=1     , 
                                   fill='white'
                                   )

            xy2 = [
                  (  0         , 9*height/16.0), 
                  (7*width/16.0, 9*height/16.0)
                  ]

            self.canvas.create_line(
                                   xy2         , 
                                   width=1     , 
                                   fill='white'
                                   )

            if (fill):
                self.fluid_left = self.canvas.create_rectangle(
                                   (  0          )  , 
                                   (7*height/16.0)+1, 
                                   (7*width /16.0)+1,
                                   (9*height/16.0)-1,
                                   fill=fluidColor, 
                                   outline=""
                                                              )

            else:
                self.fluid_left = self.canvas.create_rectangle(
                                   (  0          )  , 
                                   (7*height/16.0)+1, 
                                   (7*width /16.0)+1,
                                   (9*height/16.0)-1,
                                   fill='black', 
                                   outline=""
                                                              )

        else:
            xy = [
                 (7*width/16.0, 7*height/16.0), 
                 (7*width/16.0, 9*height/16.0)
                 ]

            self.canvas.create_line(
                                   xy, 
                                   width=1, 
                                   fill='white'
                                   )


    # function used to populate map to establish relations between 
    # this pipe and components around it
    def setNeighbors(
                    self  , 
                    top   , 
                    right , 
                    bottom, 
                    left
                    ):

        self.top =    top
        self.right =  right
        self.bottom = bottom
        self.left =   left

    def setState(self, fluid):
        self.state = fluid
        if (fluid):
            self.canvas.itemconfig(
                                  self.pipe_fluid_canvas, 
                                  fill=self.fluidColor
                                  )

            if (self.line1):
                self.canvas.itemconfig(
                                  self.fluid_top, 
                                  fill=self.fluidColor
                                      )

            if (self.line2):
                self.canvas.itemconfig(
                                  self.fluid_right, 
                                  fill=self.fluidColor
                                      )

            if (self.line3):
                self.canvas.itemconfig(
                                  self.fluid_buttom, 
                                  fill=self.fluidColor
                                      )

            if (self.line4):
                self.canvas.itemconfig(
                                  self.fluid_left, 
                                  fill=self.fluidColor
                                      )

        else:
            self.canvas.itemconfig(
                                  self.pipe_fluid_canvas, 
                                  fill='black'
                                  )

            if (self.line1):
                self.canvas.itemconfig(
                                  self.fluid_top, 
                                  fill='black'
                                      )
            if (self.line2):
                self.canvas.itemconfig(
                                  self.fluid_right, 
                                  fill='black'
                                      )

            if (self.line3):
                self.canvas.itemconfig(
                                  self.fluid_buttom, 
                                  fill='black'
                                      )

            if (self.line4):
                self.canvas.itemconfig(
                                  self.fluid_left, 
                                  fill='black'
                                      )


    def getState(self):
        return self.state

    def getWidget(self):
        return self.canvas


###############################################################
# END OF FILE                                                 #
###############################################################
