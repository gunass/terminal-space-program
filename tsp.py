
import math
import time

_GRAVITY = 9.8
_FPS = 5
_GAME_WIDTH = 100
_GAME_HEIGHT = 30
_icon0 = "|"
_icon1 = "/"
_icon2 = "—"
_icon3 = "\\"

_crashicon = "&"

def vecSum(vector0, vector1):
    return [vector0[0] + vector1[0], vector0[1] + vector1[1]]

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0] * width for i in range(height)]
        self.map[0][0] = _icon0

    def add(self, position, icon):
        xPos = int(position[0])
        yPos = int(position[1])
        self.map = [[0] * self.width for i in range(self.height)]
        if xPos < _GAME_WIDTH and yPos < _GAME_HEIGHT:
            self.map[yPos][xPos] = icon

class Rocket:
    def __init__(self, mass, thrust, fuel, heading):
        self.ms = mass
        self.th = thrust
        self.fl = fuel
        self.xy = [0,0]
        self.hd = heading
        self.vl = [0,0]
        self.ac = [0,-_GRAVITY]
        self.wg = self.ms * _GRAVITY
        self.liftoff = False
        self.icon = _icon0
        
    def getAcceleration(self):
        # If rocket has fuel...
        if self.fl > 0:
            # If lifted off...
            if self.liftoff:
                # Calculate acceleration as normal
                # sinh(heading) is the unit vector of thrust
                # Multiply unit vector by thrust to get full force vector
                # Divide force vector by mass = acceleration
                # Subtract gravity from y-axis: net acceleration in G
                xAccel = ((math.sinh(self.hd) * self.th) / self.ms) / _FPS
                yAccel = (((math.cosh(self.hd) * self.th) / self.ms) - _GRAVITY) / _FPS
                return [xAccel, yAccel]
            else:
                # If not lifted off, just return y: no x acceleration on launchpad
                yAccel = (((math.cosh(self.hd) * self.th) / self.ms) - _GRAVITY) / _FPS
                if yAccel >= 0:
                    return [0, yAccel]
                else:
                    # If this y is negative, force to 0
                    return [0,0]
        # If no fuel, acceleration is only gravity (down)
        # This kills the rocket
        elif self.liftoff:
            return [0,-_GRAVITY / _FPS]
        else:
            return [0,0]
        
    def updateVelocity(self, acc):
        # Simply add acceleration and current velocity
        self.vl = vecSum(self.vl, acc)

    def updatePosition(self):
        # Add velocity per frame to current position
        # Round to nearest integer
        newX = (self.xy[0] + (self.vl[0] / _FPS))
        newY = (self.xy[1] + (self.vl[1] / _FPS))
        if (newX != 0 or self.xy[0] != 0):
            newHD = (newY - self.xy[1]) / (newX - self.xy[0])
            self.hd = newHD
            if newHD > 0.8:
                self.icon = _icon0
            elif newHD > 0.2:
                self.icon = _icon1
            elif newHD > -0.2:
                self.icon = _icon2
            elif newHD > -0.8:
                self.icon = _icon3
            else:
                self.icon = _icon0

        self.xy = [newX, newY]
        
    def tick(self, mp):

        self.updateVelocity(self.getAcceleration())
        self.fl -= 1/_FPS
        self.updatePosition()

        # Debug info
        print("xy = ", self.xy)
        print("vl = ", self.vl)
        print("hd = ", self.hd)

        if self.fl <= 0 and not self.liftoff:
            print("You ran out of fuel on the launchpad!")
            return 0

        if self.xy[0] < 0:
            print("You crashed into the LEFT wall. How?")
            return 0
        if self.xy[1] < 0:
            # Signifies a crash!
            mp.add([self.xy[0], 0], _crashicon)
            printMap(mp)
            print("You crashed into the floor.")
            return 0    

        if self.vl[1] > 0:
            self.liftoff = True    

        mp.add(self.xy, self.icon)
        return 1



game_map = Map(_GAME_WIDTH,_GAME_HEIGHT)
dft_rocket = Rocket(10,400,5,0.3)

def printMap(mp):
    # State of the art rendering
    i = _GAME_HEIGHT-1
    while i >= 0:
        for j in mp.map[i]:
            if j == 0:
                print(' ', end="")
            else:
                print(j, end='')    
        print()
        i -= 1    
    print("—————_______________________________________________________________________________________________")
    
    
def start(map, rocket):
    printMap(map)
    while True:
        time.sleep(1/_FPS)
        if rocket.tick(map):
            print("-----------------------------------------------------------------------------------------")
            printMap(map)
        else:
            print("Mission aborted!")
            break
    
input(                     "Resize your terminal to 100x34 and press enter >")
print(                     "Recommended: M=10, T=550, F=1, G=0.1")
    
rocket_mass = int(input(   "Rocket mass      > "))
rocket_thrust = int(input( "Rocket thrust    > "))
rocket_fuel = int(input(   "Rocket fuel      > "))
rocket_angle = float(input("Launch gradient  > "))

rocket_thrust_ = rocket_thrust / _FPS

start(game_map, Rocket(rocket_mass, rocket_thrust_, rocket_fuel, rocket_angle))    

print("Mass="+str(rocket_mass), 
      "Thrust="+str(rocket_thrust), 
      "Fuel="+str(rocket_fuel), 
      "Angle="+str(rocket_angle))