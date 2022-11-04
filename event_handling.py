from direct.showbase import DirectObject
from timer import Timer


'''
Code to have in Microbit

from microbit import *
while True:
    gesture = accelerometer.current_gesture()
    print(gesture)
'''
class Handler(DirectObject.DirectObject):
    def __init__(self):
        '''
        Initialization for the Event Handler, this class inherits from DirectObject.DirectObject which allows
        this class to handle events for the game. By default, WASD, escape, and left mouse click buttons are accepted events.
        
        By default, the event handler of Panda3d ignores all events, it needs to be specified which events to accept. The accept method
        takes in what event it is, and a method to call when the event is thrown. The parameters that come after are extra arguments that
        the method you specified might take. 
'''
        super().__init__()
        
        #uncomment to see have each event printed
        #messenger.toggleVerbose()
        
        #event for when WASD is pressed
        self.accept("w", self.changeKeyMap, ["w"])
        self.accept("s", self.changeKeyMap, ["s"])
        self.accept("a", self.changeKeyMap, ["a"])
        self.accept("d", self.changeKeyMap, ["d"])
        
        #events for when WASD is no longer being pressed
        self.accept("w-up", self.changeKeyMap, ["w"])
        self.accept("s-up", self.changeKeyMap, ["s"])
        self.accept("a-up", self.changeKeyMap, ["a"])
        self.accept("d-up", self.changeKeyMap, ["d"])
        
        self.accept("escape", self.changeKeyMap, ["escape"])
        self.accept("escape-up", self.changeKeyMap, ["escape"])
        
        self.accept("mouse1", self.changeKeyMap, ["mouse1"])
        self.accept("mouse1-up", self.changeKeyMap, ["mouse1"])
        
        #dictionary containing a boolean value for WASD, escape and left mouse button
        #
        self.keyMap = {"w": False,
                       "s": False,
                       "a": False,
                       "d": False,
                       "escape": False,
                       "mouse1" : False}
        
        #list for axe hitting ghosts
        #the boolean value for a specific ghost is the same indice as the ghostNumber
        self.ghostAxeList = [False, False]
        
        #list for ghost hitting the player
        #the pair of boolean and timer for a specific ghost is the same indice as the ghostnumber
        self.ghostHitList = [[False, Timer()], [False, Timer()]]
        
        #boolean for checking if the axe has hit any ghost
        self.axeCollision = False
        
        self.ghostToGhostEventList = []
        
        #list representing which ghost a ghost is colliding with
        #if ghost 0 is colliding with ghost 3, it would be represented by this:
        #self.ghostToGhostColliding[0] == 3
        #-1 is the value to represent if the ghost is not colliding with any ghost
        self.ghostToGhostColliding = [-1,-1]

    def translateMicrobitEvent(self, microbitEvent):
        '''
        This method is used to take the data from the microbit and depending on what the data is, it throws an event.
        In my program, if the microbit is face up, that is considered its resting position, when the microbit is facing down,
        that is considered a swing. When the input mode is microbit, there are no events for the left mouse button, so it
        uses the same keyMap entry that the left mouse button would use.
        
        Parameters
        ----------------------------------------------------
        microbitEvent: a variable representing the data coming in from the microbit
        
        Returns
        ----------------------------------------------------
        None
        
'''
        if microbitEvent != None:
            if microbitEvent == "face up":
                self.keyMap["mouse1"] = False
            elif microbitEvent == "face down":
                self.keyMap["mouse1"] = True
    

    def changeKeyMap(self, key):
        '''
        This method is called whenever WASD, escape or left mouse button is clicked. It toggles the keyMap boolean for
        that key. For example if w is pressed, then the key parameter of the method is 'w' and it accesses the boolean at
        self.keyMap["w"]
        
        Parameters
        ----------------------------------------------------
        key: representing which value in the dictionary to change
        
        Returns
        ----------------------------------------------------
        None
'''
        self.keyMap[key] = not self.keyMap[key]
    
    def collisions(self, objectName, objectNum, entry):
        '''
        This method is called whenever a collision event between a ghost and the axe is thrown or a collision
        event between a ghost and player is thrown.
        
        If the object the ghost is colliding with is the axe, it will toggle the axeCollision variable and it will
        toggle the boolean value in ghostAxeList for that ghost.
        If the object the ghost is colliding with is the player, then it will toggle the boolean at that specific ghosts'
        indice
        
        Parameters
        ----------------------------------------------------
        objectName: the name of the object, either "axe" or "player"
        objectNum: an integer representing the ghostNumber of the ghost that is colliding with the axe or the player
        entry: redundant parameter, any event thrown by a collision needs this extra parameter
        
        Returns
        ----------------------------------------------------
        None
        
'''
        if objectName == "axe":
            self.ghostAxeList[objectNum] = not self.ghostAxeList[objectNum]
            self.axeCollision = not self.axeCollision
        if objectName == "player":
            self.ghostHitList[objectNum][0] = not self.ghostHitList[objectNum][0]
            
    def ghostToGhost(self, ghostOne, ghostTwo, entry):
        '''
        This method is called when a ghost collides with another ghost. All it does is change the ghostNumber currently
        stored at the colliding ghost's indice in ghostToGhostColliding
        
        Parameters
        ----------------------------------------------------
        ghostOne: an integer representing the ghostnumber of the colliding ghost
        ghostTwo: an integer representing the ghost number of the ghost the colliding ghost is colliding with.
        entry: redundant, unused parameter.
        
        Returns
        ----------------------------------------------------
        None
'''
        self.ghostToGhostColliding[ghostOne] = ghostTwo
        