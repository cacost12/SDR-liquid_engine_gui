###############################################################
#                                                             #
# PandID.py -- draws an engine schematic and displays data on #
#              engine for real-time visualization             # 
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Standard Imports                                            #
###############################################################
import tkinter as tk


###############################################################
# Project Modules                                             #
###############################################################
import component_template
import solenoid        as SDR_solenoid
import ball_valve      as SDR_ball_valve
import orifice         as SDR_orifice
import pressure_sensor as SDR_pressure_sensor
import temp_sensor     as SDR_temp_sensor
import tank            as SDR_tank
import pipe            as SDR_pipe
import nozzle          as SDR_nozzle
import main


###############################################################
# Engine Window Title                                         #
###############################################################
class Header:

    def __init__(
                self, 
                root,       # window to draw on 
                background, # background color 
                text,       # header text 
                width,      # width of drawing canvas 
                height,     # height of drawing canvas 
                fontsize
                ):

        # Canvas dimensions
        self.width = width
        self.height = height

        # Underline coordinates
        underline_x0 = width/8.0
        underline_y0 = 7*height/8.0
        underline_x1 = 7*underline_x0
        underline_y1 = underline_y0
        underline_start_coords = (underline_x0, underline_y0)
        underline_end_coords   = (underline_x1, underline_y1)

        # Canvas object
        self.canvas = tk.Canvas(
                               root, 
                               width=width, 
                               height=height, 
                               bg=background, 
                               highlightthickness=0
                               )

        # Draw text and underline
        self.canvas.create_line(
                               underline_start_coords, 
                               underline_end_coords,
                               width=1, 
                               fill='white'
                               )

        self.canvas.create_text(
                               width/2.0, 
                               height/2.0, 
                               font=("Arial", fontsize, ''), 
                               fill="white", 
                               text=text
                               )

    # Canvas widget public access
    def getWidget(self):
        return self.canvas


###############################################################
# Engine Schematic Labels                                     #
###############################################################
class Text:

    def __init__(
                self, 
                root,      # Window to draw text on 
                bg_color,  # Background color 
                text,      # Text to display 
                width,     # Width of drawing canvas 
                height,    # Height of frawing canvas 
                fontsize   # Text fontsize
                ):

        # Drawing canvas dimensions 
        self.width = width
        self.height = height

        # Canvas object
        self.canvas = tk.Canvas(
                               root, 
                               width=width, 
                               height=height, 
                               bg=bg_color, 
                               highlightthickness=0
                               )

        # Draw text
        self.canvas.create_text(
                               width/2.0, 
                               height/2.0, 
                               font=("Arial", fontsize, ''),
                               fill="white", 
                               text=text
                               )

    # Canvas widget public access
    def getWidget(self):
        return self.canvas


###############################################################
# Engine Object                                               #
###############################################################
class Engine_Display:

    def __init__(self, gridLen):

		#######################################################
		# Display Settings                                    #
		#######################################################

		# Window dimensions
        width  = gridLen * 8
        height = gridLen * 12

		# Window Configuration
        self.win = tk.Tk()
        self.win.title("P&ID Diagram")
        self.win.geometry(str(width) + "x" + str(height))
        self.win.configure(bg='black')
        self.win.protocol("WM_DELETE_WINDOW",
                           self.close_window_callback)

        # Fluid Color Hex Code 
        fluidColor = '#41d94d'


		#######################################################
		# Component Initializations                           #
		#######################################################

        # Header 
        self.header = Header(self.win, 'black', 'P&ID', width, gridLen, 24)

        # Tanks 
        self.gn2 = SDR_tank.Tank(self.win, 'black', 'GN2', '#1d2396', gridLen, gridLen)
        self.lox = SDR_tank.Tank(self.win, 'black', 'LOx', '#1d2396', gridLen, gridLen)
        self.k   = SDR_tank.Tank(self.win, 'black', 'K'  , '#1d2396', gridLen, gridLen)

        # Solenoids 
        self.one   = SDR_solenoid.Solenoid(self.win, 'black', 1, gridLen, gridLen, False, True, True, False)
        self.two   = SDR_solenoid.Solenoid(self.win, 'black', 2, gridLen, gridLen, False, True, False, False)
        self.three = SDR_solenoid.Solenoid(self.win, 'black', 3, gridLen, gridLen, False, False, True, True)
        self.four  = SDR_solenoid.Solenoid(self.win, 'black', 4, gridLen, gridLen, False, True, False, False)
        self.five  = SDR_solenoid.Solenoid(self.win, 'black', 5, gridLen, gridLen, False, True, True, False)
        self.six   = SDR_solenoid.Solenoid(self.win, 'black', 6, gridLen, gridLen, False, False, True, True)

        # Ball Valves 
        self.s1 = SDR_solenoid.Solenoid(self.win, 'black', 7, gridLen, gridLen, True, False, True, False)
        self.s2 = SDR_solenoid.Solenoid(self.win, 'black', 8, gridLen, gridLen, True, False, True, False)

        # Orifices 
        self.o1 = SDR_orifice.Orifice(self.win, 'black', gridLen, gridLen, True, False, True, False)
        self.o2 = SDR_orifice.Orifice(self.win, 'black', gridLen, gridLen, True, False, True, False)

        # Pressure Sensors
        self.ps1 = SDR_pressure_sensor.PressureSensor(self.win, 'black', gridLen, gridLen, False, True, False, False)
        self.ps2 = SDR_pressure_sensor.PressureSensor(self.win, 'black', gridLen, gridLen, False, False, False, True)
        self.ps3 = SDR_pressure_sensor.PressureSensor(self.win, 'black', gridLen, gridLen, False, True, True, True)

		# Temperature Sensors
        self.tp1 = SDR_temp_sensor.TempSensor(self.win, 'black', gridLen, gridLen, True, False, False, False)

        # Text boxes
        self.t1 = Text(self.win, 'black', 'K Fill', gridLen, gridLen, 12)
        self.t2 = Text(self.win, 'black', 'K Drain', gridLen, gridLen, 12)
        self.t3 = Text(self.win, 'black', 'LOx\nFill/Drain', gridLen, gridLen, 12)

        # Pipes 
        self.p1 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p2 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, True, '#41d94d', False)
        self.p3 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p4 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p5 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, True, '#41d94d', False)
        self.p6 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p7 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, False, '#41d94d', False)
        self.p8 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, True, '#41d94d', False)
        self.p9 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p10 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, True, '#41d94d', False)
        self.p11 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p12 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p13 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, False, '#41d94d', False)
        self.p14 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, False, '#41d94d', False)
        self.p15 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p16 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, True, '#41d94d', False)
        self.p17 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, True, '#41d94d', False)
        self.p18 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, False, False, True, True, '#41d94d', False)
        self.p19 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, True, '#41d94d', False)
        self.p20 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, False, True, True, True, '#41d94d', False)
        self.p21 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, True, '#41d94d', False)
        self.p22 = SDR_pipe.Pipe(self.win, 'black', gridLen, gridLen, True, False, False, True, '#41d94d', False)

        # Nozzle  
        self.n = SDR_nozzle.Nozzle(self.win, 'black', gridLen, gridLen * 1.5)

        #self.s2.setNeighbors(None, self.five, self.p19, self.p16)
        #self.s1.setNeighbors(self.p13, None, None, self.o2)


		#######################################################
		# Component Placement                                 #
		#######################################################

        # Header 
        self.header.getWidget().place(x=gridLen * 0, y=gridLen * 0)

		# Tanks
        self.gn2.getWidget().place(x=gridLen * 3, y=gridLen * 1)
        self.lox.getWidget().place(x=gridLen * 1, y=gridLen * 5)
        self.k.getWidget().place(x=gridLen * 6, y=gridLen * 5)

		# Solenoids
        self.one.getWidget().place(x=gridLen * 1, y=gridLen * 2)
        self.one.setIn ( self.one.inlet_pipe_right  )
        self.one.setOut( self.one.inlet_pipe_bottom )
        self.two.getWidget().place(x=gridLen * 0, y=gridLen * 4)
        self.two.setIn( self.two.inlet_pipe_right )
        self.three.getWidget().place(x=gridLen * 6, y=gridLen * 2)
        self.three.setIn ( self.three.inlet_pipe_left   )
        self.three.setOut( self.three.inlet_pipe_bottom )
        self.four.getWidget().place(x=gridLen * 5, y=gridLen * 4)
        self.four.setIn( self.four.inlet_pipe_right )
        self.five.getWidget().place(x=gridLen * 2, y=gridLen * 8)
        self.five.setIn( self.five.inlet_pipe_right )
        self.five.setOut( self.five.inlet_pipe_bottom )
        self.six.getWidget().place(x=gridLen * 4, y=gridLen * 8)
        self.six.setIn ( self.six.inlet_pipe_left   )
        self.six.setOut( self.six.inlet_pipe_bottom )

		# Ball Valves
        self.s1.getWidget().place(x=gridLen * 6, y=gridLen * 8)
        self.s2.getWidget().place(x=gridLen * 1, y=gridLen * 8)

		# Orifices
        self.o1.getWidget().place(x=gridLen * 1, y=gridLen * 6)
        self.o2.getWidget().place(x=gridLen * 6, y=gridLen * 7)

		# Pressure Sensors
        self.ps1.getWidget().place(x=gridLen * 0, y=gridLen * 3)
        self.ps2.getWidget().place(x=gridLen * 7, y=gridLen * 3)
        self.ps3.getWidget().place(x=gridLen * 5, y=gridLen * 9)

		# Temperature Sensors
        self.tp1.getWidget().place(x=gridLen * 5, y=gridLen * 10)

		# Text Boxes
        self.t1.getWidget().place(x=gridLen * 7, y=gridLen * 4)
        self.t2.getWidget().place(x=gridLen * 7, y=gridLen * 6)
        self.t3.getWidget().place(x=gridLen * 0, y=gridLen * 7)

		# Pipes
        self.p1.getWidget().place(x=gridLen * 2, y=gridLen * 2)
        self.p2.getWidget().place(x=gridLen * 3, y=gridLen * 2)
        self.p3.getWidget().place(x=gridLen * 4, y=gridLen * 2)
        self.p4.getWidget().place(x=gridLen * 5, y=gridLen * 2)
        self.p5.getWidget().place(x=gridLen * 1, y=gridLen * 3)
        self.p6.getWidget().place(x=gridLen * 3, y=gridLen * 3)
        self.p7.getWidget().place(x=gridLen * 6, y=gridLen * 3)
        self.p8.getWidget().place(x=gridLen * 1, y=gridLen * 4)
        self.p9.getWidget().place(x=gridLen * 3, y=gridLen * 4)
        self.p10.getWidget().place(x=gridLen * 6, y=gridLen * 4)
        self.p11.getWidget().place(x=gridLen * 3, y=gridLen * 5)
        self.p12.getWidget().place(x=gridLen * 3, y=gridLen * 6)
        self.p13.getWidget().place(x=gridLen * 6, y=gridLen * 6)
        self.p14.getWidget().place(x=gridLen * 1, y=gridLen * 9)
        self.p15.getWidget().place(x=gridLen * 3, y=gridLen * 7)
        self.p16.getWidget().place(x=gridLen * 1, y=gridLen * 7)
        self.p17.getWidget().place(x=gridLen * 3, y=gridLen * 8)
        #self.p18.getWidget().place(x=gridLen * 6, y=gridLen * 8)
        self.p19.getWidget().place(x=gridLen * 2, y=gridLen * 9)
        self.p20.getWidget().place(x=gridLen * 3, y=gridLen * 9)
        self.p21.getWidget().place(x=gridLen * 4, y=gridLen * 9)
        self.p22.getWidget().place(x=gridLen * 6, y=gridLen * 9)

		# Nozzle
        self.n.getWidget().place(x=gridLen * 3, y=gridLen * 10)


		#######################################################
		# Configure Connections                               #
		#######################################################

        #SET ALL VIRTUAL COMPONENTS (linked list)
        self.head = self.gn2

        #row 1
        self.gn2.setNeighbors(None, None, self.p2, None)

        #row 2
        self.one.setNeighbors(None, None, self.p5, None)
        self.p1.setNeighbors(None, None, None, self.one)
        self.p2.setNeighbors(None, self.p3, self.p6, self.p1)
        self.p3.setNeighbors(None, self.p4, None, None)
        self.p4.setNeighbors(None, self.three, None, None)
        self.three.setNeighbors(None, None, self.p7, None)

        #row 3
        self.ps1.setNeighbors(None, None, None, None)
        self.p5.setNeighbors(None, None, self.p8, self.ps1)
        self.p6.setNeighbors(None, None, self.p9, None)
        self.p7.setNeighbors(None, self.ps2, self.p10, None)
        self.ps2.setNeighbors(None, None, None, None)

        #row 4
        self.two.setNeighbors(None, None, None, None)
        self.p8.setNeighbors(None, None, self.lox, self.two)
        self.p9.setNeighbors(None, None, self.p11, None)
        self.four.setNeighbors(None, None, None, None)
        self.p10.setNeighbors(None, None, self.k, self.four)

        #row5
        self.lox.setNeighbors(None, None, self.o1, None)
        self.p11.setNeighbors(None, None, self.p12, None)
        self.k.setNeighbors(None, None, self.p13, None)

        #row 6
        self.o1.setNeighbors(None, None, self.p16, None)
        self.p12.setNeighbors(None, None, self.p15, None)
        self.p13.setNeighbors(None, None, self.o2, None)

        #row 7
        self.p15.setNeighbors(None, None, self.p17, None)
        self.p16.setNeighbors(None, None, self.s2, None)
        self.o2.setNeighbors(None, None, self.s1, None)
        self.s2.setNeighbors(None, None, self.p14, None)

        #row 8
        self.five.setNeighbors(None, None, self.p19, None)
        self.six.setNeighbors(None, None, self.p21, None)
        self.p17.setNeighbors(None, self.six, None, self.five)
        self.s1.setNeighbors(None, None, None, self.p22)
        #self.p18.setNeighbors(None, None, self.p22, None)

        #row 9
        self.p14.setNeighbors(None, self.p19, None, None)
        self.p19.setNeighbors(None, self.p20, None, self.p14)
        self.p20.setNeighbors(None, None, self.n, None)
        self.p21.setNeighbors(self.six, self.ps3, None, self.p20)
        self.ps3.setNeighbors(self.p22, None, self.tp1, self.p21)
        self.p22.setNeighbors(None, None, None, self.ps3)

        #row 10
        self.n.setNeighbors(None, None, None, None)
        self.tp1.setNeighbors(None, None, None, None)

    def close_window_callback(self):
        self.win.destroy()

    def defaultState(self):
        self.p1.setState(False)
        self.p2.setState(False)
        self.p3.setState(False)
        self.p4.setState(False)
        self.p5.setState(False)
        self.p6.setState(False)
        self.p7.setState(False)
        self.p8.setState(False)
        self.p9.setState(False)
        self.p10.setState(False)
        self.p11.setState(False)
        self.p12.setState(False)
        self.p13.setState(False)
        self.p14.setState(False)
        self.p15.setState(False)
        self.p16.setState(False)
        self.p17.setState(False)
        self.p18.setState(False)
        self.p19.setState(False)
        self.p20.setState(False)
        self.p21.setState(False)
        self.p22.setState(False)

        self.one.setPipes(False, False, False, False)
        self.two.setPipes(False, False, False, False)
        self.three.setPipes(False, False, False, False)
        self.four.setPipes(False, False, False, False)
        self.five.setPipes(False, False, False, False)
        self.six.setPipes(False, False, False, False)

        self.ps1.setPipes(False)
        self.ps2.setPipes(False)
        self.ps3.setPipes(False)

        self.o1.setPipes(False)
        self.o2.setPipes(False)

        self.s1.setPipes(False, False, False, False)
        self.s2.setPipes(False, False, False, False)

        self.tp1.setPipes(False)



    def getHead(self):
        return self.gn2

    def updatePipeStatus(self):
        self.defaultState()

        head = self.getHead()

        listMultiplePaths = []
        visited = []
        listMultiplePaths.append(head)

        # Basic traversal method
        while(len(listMultiplePaths) > 0):
            if(type(head) is SDR_pipe.Pipe):
                head.setState(True)

            if (head.top is not None and head.top not in visited):
                if(type(head.top) is SDR_solenoid.Solenoid and head.top.getState()):
                    listMultiplePaths.append(head.top)
                    visited.append(head.top)
                elif(type(head.top) is not SDR_solenoid.Solenoid and type(head.top) is not SDR_ball_valve.Ball_Valve):
                    listMultiplePaths.append(head.top)
                    visited.append(head.top)
                elif (type(head.top) is SDR_ball_valve.Ball_Valve and head.top.getPercentage() > 0):
                    listMultiplePaths.append(head.top)
                    visited.append(head.top)
            if (head.right is not None and head.right not in visited):
                if (type(head.right) is SDR_solenoid.Solenoid and head.right.getState()):
                    listMultiplePaths.append(head.right)
                    visited.append(head.right)
                elif (type(head.right) is not SDR_solenoid.Solenoid and type(head.right) is not SDR_ball_valve.Ball_Valve):
                    listMultiplePaths.append(head.right)
                    visited.append(head.right)
                elif (type(head.right) is SDR_ball_valve.Ball_Valve and head.right.getPercentage() > 0):
                    listMultiplePaths.append(head.right)
                    visited.append(head.right)
            if (head.bottom is not None and head.bottom not in visited):
                if (type(head.bottom) is SDR_solenoid.Solenoid and head.bottom.getState()):
                    listMultiplePaths.append(head.bottom)
                    visited.append(head.bottom)
                elif (type(head.bottom) is not SDR_solenoid.Solenoid and type(head.bottom) is not SDR_ball_valve.Ball_Valve):
                    listMultiplePaths.append(head.bottom)
                    visited.append(head.bottom)
                elif (type(head.bottom) is SDR_ball_valve.Ball_Valve and head.bottom.getPercentage() > 0):
                    listMultiplePaths.append(head.bottom)
                    visited.append(head.bottom)
            if (head.left is not None and head.left not in visited):
                if (type(head.left) is SDR_solenoid.Solenoid and head.left.getState()):
                    listMultiplePaths.append(head.left)
                    visited.append(head.left)
                elif (type(head.left) is not SDR_solenoid.Solenoid and type(head.left) is not SDR_ball_valve.Ball_Valve):
                    listMultiplePaths.append(head.left)
                    visited.append(head.left)
                elif (type(head.left) is SDR_ball_valve.Ball_Valve and head.left.getPercentage() > 0):
                    listMultiplePaths.append(head.left)
                    visited.append(head.left)

            listMultiplePaths.pop(0)
            if(len(listMultiplePaths) > 0):
                head = listMultiplePaths[0]
            else:
                break

        #edge checks for components with pipes (excluding pipes)
        if(self.p1.getState()):
            self.one.setFill(False, True, False, False)
        if(self.p4.getState()):
            self.three.setFill(False, False, False, True)
        if(self.p5.getState()):
            self.one.setFill(False, False, True, False)
            self.ps1.setFill(False, True, False, False)
        if(self.p7.getState()):
            self.three.setFill(False, False, True, False)
            self.ps2.setFill(False, False, False, True)
        if(self.p8.getState()):
            self.two.setFill(False, True, False, False)
            self.o1.setFill(True, False, True, False)
        if(self.p10.getState()):
            self.four.setFill(False, True, False, False)
#        if(self.p14.getState()):
#            self.o1.setFill(False, False, True, False)
        if(self.p15.getState()):
            self.five.setFill(False, True, False, False)
            self.six.setFill(False, False, False, True)
            if(self.six.getState()):
                self.six.setFill(False, False, True, False)
#                self.o2.setFill(False, False, True, True)
            if(self.five.getState()):
                self.five.setFill(False, False, True, False)
#                self.s2.setFill(False, True, False, False)
#                if(self.s2.getPercentage() > 0):
#                    self.s2.setFill(False, False, True, False)
        if(self.p13.getState()):
            self.s1.setFill(True, False, False, False)
            self.o2.setFill(True, False, True, False)
            if( self.s1.getState() ):
                self.s1.setFill(True, False, True, False)
            #    self.o2.setFill(False, True, True, False)
        if ( self.p14.getState() ):
            if ( self.s2.getState() ):
                self.s2.setFill(True, False, True, False)
            else:
                self.s2.setFill(False, False, True, False)
        if(self.p16.getState()):
            self.s2.setFill(True, False, False, False)
            if( self.s2.getState() ):
                self.s2.setFill(False, False, True, False)
        if ( self.p19.getState() ):
            self.five.setFill(False, True, True, False)
        if ( self.p21.getState() ):
            self.ps3.setFill(False, True, True, True)
            self.tp1.setFill(True, False, False, False)
            if ( self.six.getState() ):
                self.six.setFill(False, False, True, True)
            else:
                self.six.setFill(False, False, True, False)
        if(self.p22.getState()):
            self.ps3.setFill(False, True, True, True)
            self.tp1.setFill(True, False, False, False)
            self.s1.setFill(False, False, True, False)

    def getWindow(self):
        return self.win

###############################################################
# END OF FILE                                                 #
###############################################################
