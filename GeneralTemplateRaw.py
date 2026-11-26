#region VEXcode Generated Robot Configuration
import math
import random
from vexcode_vrc import *
from vexcode_vrc.events import get_Task_func

# Brain should be defined by default
brain=Brain()

ai_vision = AiVision("aiVision", 6)
gps = GPS("GPS", 7)
drivetrain = Drivetrain("drivetrain", 0)

# 'Enum' class for AI Vision GameElements
class GameElements:
    BLUE_BLOCK = 0
    RED_BLOCK = 1

# Color to String Helper
def convert_color_to_string(col):
    if col == RED:
        return "red"
    if col == GREEN:
        return "green"
    if col == BLUE:
        return "blue"
    if col == WHITE:
        return "white"
    if col == YELLOW:
        return "yellow"
    if col == ORANGE:
        return "orange"
    if col == PURPLE:
        return "purple"
    if col == CYAN:
        return "cyan"
    if col == RED_VIOLET:
        return "red_violet"
    if col == VIOLET:
        return "violet"
    if col == BLUE_VIOLET:
        return "blue_violet"
    if col == BLUE_GREEN:
        return "blue_green"
    if col == YELLOW_GREEN:
        return "yellow_green"
    if col == YELLOW_ORANGE:
        return "yellow_orange"
    if col == RED_ORANGE:
        return "red_orange"
    if col == BLACK:
        return "black"
    if col == TRANSPARENT:
        return "transparent"
    return ""

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      Generalized Template for VEX Virtual
#	Author:       45519X RefleX
#	Created:      January 26, 2026
#   NOTE: There are different types of bots for each
#   of the different playgrounds. If you want to use
#   this template for something other than Push Back, 
#   you will need to replace the robot configuration
#   code located in the region above this message.
# 
# ------------------------------------------

#region helpers

def motorSetup():
    # set up the motor velocities
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)

# starting position heading offset from field/global heading
global headingOffset
headingOffset = gps.heading() - drivetrain.heading(DEGREES)
headingOffset = (headingOffset + 180) % 360 - 180 #normalization

#endregion helpers

#region classes
class posData:
    # initialize position variables
    def __init__(self, x, y, theta=0):
        self.x = x 
        self.y = y
        self.theta = theta

class heroBot:
    # initialize the robot
    def __init__(self):
        self.position = posData(0,0,0) # start position at zero
        self.dx = self.dy = self.dis = self.target_ang = 0 #initialize calculation variables

    def printReadings(self):
        while True:
            # print location and heading values to brain screen to help debugging
            brain.screen.clear_screen()
            brain.screen.print(f"X: {gps.x_position(MM)} Y: {gps.y_position(MM)} H: {gps.heading()} DH: {drivetrain.heading(DEGREES)}")
            wait(10, MSEC)

    def updatePos(self, x, y):
        self.position = posData(gps.x_position(MM), gps.y_position(MM), drivetrain.heading(DEGREES)) #current position
        #calculate differences in x and y
        self.dx = x - self.position.x
        self.dy = y - self.position.y

        #calculate distance to target using Pythagreom therom
        self.dis = math.sqrt(self.dx ** 2 + self.dy ** 2)
        #find angle to point towards the target in degrees based on positional difference with atan2
        self.target_ang = (math.degrees(math.atan2(self.dx, self.dy))) % 360

    def turnTo(self, angle, waitt = True):
        # turns to a specific heading including our offset
        turnAmount = (angle - headingOffset) % 360
        drivetrain.turn_to_heading(turnAmount, DEGREES, waitt)
    
    def moveTo(self, x, y, error = 0):
        self.updatePos(x, y) # calculate distances and target angle
        # move the robot to the point
        turnAmount = (self.target_ang - headingOffset) % 360
        drivetrain.turn_to_heading(turnAmount, DEGREES)
        drivetrain.drive_for(FORWARD, self.dis - error, MM)
    
    # create custom functions relating to the bot here
    @staticmethod
    def spinIntake():
        # put spinning the intake motor here
        wait(1, SECONDS)

# create robot class
bot = heroBot()

#endregion classes

#region functionality functions
def something():
    #create a reusable function here
    wait(1, SECONDS)

#endregion functionality functions

# "main" is our actual route
def main():
    motorSetup() # setup motors

    # moving to a specific coordinate in mm
    bot.moveTo(-1200, -1200)

    # moving to a coordinate accounting for error (subtract 100mm)
    bot.moveTo(0, -600, 100)

    # moving to a coordinate accounting for error (add 100mm)
    bot.moveTo(-750, 0, -100)

    # turn to zero degrees (north)
    bot.turnTo(0)

    #south
    bot.turnTo(180)  

    #random angle
    bot.turnTo(97)

    # run your custom bot function
    bot.spinIntake()

    # run your custom function
    something()

# VR threads
vr_thread(main) # main program

# to see the brain screen: click the speed gauge icon in the top left
# X = x position
# Y = y position
# H = GPS sensor heading
# DH = drivetrain inertial sensor heading
vr_thread(bot.printReadings) # print values to screen
