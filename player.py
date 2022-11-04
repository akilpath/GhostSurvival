from axe import Axe
from panda3d.core import CollisionCapsule
from panda3d.core import CollisionNode
from game_collision_handler import CollisionHandler

import game
import math
from timer import Timer
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

#player hit sound effect from https://www.fesliyanstudios.com/royalty-free-sound-effects-download/breathing-150
class Player():
    def __init__(self):
        '''
        Initialization for the player class, the player class contains all the attributes related to the player
        such as the direction the player is looking at, the player's speed, position and health. The player class does not have
        its own NodePath, instead it manipulates the camera nodePath. The player class also contains the axe object.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        
        self.speed = 0
        self.acceleration = 15
        self.decceleration = -17
        
        #this attribute represents the last direction the player was moving in, when the user doesn't click
        #any buttons, the player will maintain its current speed in the direction it was last moving in, simulating inertia.
        self.lastMovingDirection = 0
        
        self.posX = 0
        self.posY = -10
        self.posZ = 2
        
        self.heading = 0
        self.pitch = 0
        self.roll = 0
        
        self.playerHealth = 15
        
        #regenTimer is a timer that is used to determine when the player can begin to regenerate health
        self.regenTimer = Timer()
        
        #collision NodePath for the player object. 
        self.cnodePath = game.gameObj.cam.attachNewNode(CollisionNode("playerCollNode"))
        self.cnodePath.node().addSolid(CollisionCapsule(0,0,0,0,0,2,0.5))
        self.cnodePath.show()
        self.playerCollHandler = CollisionHandler()
        game.gameObj.cTrav.addCollider(self.cnodePath, self.playerCollHandler)
        
        #axe object
        self.axe = Axe()
        
        #damage filter, this is an attribute that is assigned an image to put on the screen.
        #this is where the image for the bloody effect that comes on the screen when the player is damaged is stored
        self.damageFilter = None
        
        #sound effects for the player
        self.playerHitSFX = game.gameObj.loader.loadSfx(r"assets/sounds/heavy-breathing.mp3")
        self.playerHitSFX.setLoop(True)
        self.playerHitSFX.setVolume(0.75)
    
    def updatePlayerLoc(self):
        '''
        This method updates the player location and the player heading pitch and roll.
        
        Parameters
        ----------------------------------------------------
        none
        
        Returns
        ----------------------------------------------------
        None
'''
        game.gameObj.camera.setPos(self.posX,self.posY,self.posZ)
        game.gameObj.camera.setHpr(self.heading,self.pitch,self.roll)
        
    def updateSpeed(self):
        '''
        This method is responsible for updating the speed. This is needed since the player doesn't just have speed, it has acceleration and decceleration.
        This method is called at the beginning of the player update method, depending on if the player is currently trying to move, it will either
        increase or decrease the speed.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        if game.gameObj.inputMode == "mouse":
            #if the input mode is set to mouse, the game will check if any of the WASD keys are being pressed and if the player hasn't exceeded its top speed. If both are true,
            #then it will accelerate the speed
            #if none of the movement keys are being pressed and the player has a speed greater than 0, it will reduce the speed
            if (game.gameObj.events.keyMap["w"] or game.gameObj.events.keyMap["s"] or game.gameObj.events.keyMap["a"] or game.gameObj.events.keyMap["d"]) and self.speed < 14:
                self.speed = self.acceleration*game.gameObj.dt + self.speed
            elif not (game.gameObj.events.keyMap["w"] or game.gameObj.events.keyMap["s"] or game.gameObj.events.keyMap["a"] or game.gameObj.events.keyMap["d"]) and self.speed > 0 :
                self.speed = self.decceleration*game.gameObj.dt + self.speed
        elif game.gameObj.inputMode == "microbit":
            #if the inputMode is set to microbit, acceleration and decceleration work the same as above except there is only two movement keys.
            if (game.gameObj.events.keyMap["w"] or game.gameObj.events.keyMap["s"]) and self.speed < 10:
                self.speed = self.acceleration*game.gameObj.dt + self.speed
            elif not (game.gameObj.events.keyMap["w"] or game.gameObj.events.keyMap["s"]) and self.speed > 0 :
                self.speed = self.decceleration*game.gameObj.dt + self.speed
                
        #if the player speed is less than zero, it sets it to 0. 
        if self.speed < 0:
            self.speed = 0
            
    def updatePlayer(self,task):
        '''
        This is a task that is responsible for updating the player, this is added to the task manager whenver the game is being played.
        This method involves changing the direction the player is looking in, allowing the player to move, checking for damage and updating the axe.
        
        Parameters
        ----------------------------------------------------
        task: task object from direct.task
        
        Returns
        ----------------------------------------------------
        Returns task.cont which indicates the task is finished
        '''
        self.updateSpeed()
        
        #movement forward and backward is the same for both microbit input and mouse input
        #moving forward is always going to be equivalent to the current heading of the player
        #moving right will be in the direction of the heading - 90 degrees
        #moving left will be in the direction of the heading + 90 degrees
        #moving backward will be in the direction of the heading + 180 degrees.
        #moving in the forward direction is the fastest.
        
        if game.gameObj.events.keyMap["w"]:
            theta = self.heading%360
            self.lastMovingDirection = math.radians(theta)
            theta = math.radians(theta)
            newPos = (self.posX - ((self.speed)*math.sin(theta)*game.gameObj.dt), self.posY + (self.speed)*math.cos(theta)*game.gameObj.dt)
            #if the move into this new position is allowed, it will update the x and y of the player
            if self.permissionToMove(newPos):
                self.posX, self.posY = newPos
        if game.gameObj.events.keyMap["s"]:
            theta = (self.heading+180)%360
            self.lastMovingDirection = math.radians(theta)
            theta = math.radians(theta)
            newPos = (self.posX - ((self.speed*0.4)*math.sin(theta)*game.gameObj.dt), self.posY + (self.speed*0.4)*math.cos(theta)*game.gameObj.dt)
            if self.permissionToMove(newPos):
                self.posX, self.posY = newPos
                
        if game.gameObj.inputMode == "mouse":
            #if the inputMode is mouse, then  a and d become keys that allow the player to strafe left and right
            if game.gameObj.events.keyMap["a"]:
                theta = (self.heading+90)%360
                self.lastMovingDirection = math.radians(theta)
                theta = math.radians(theta)
                newPos = (self.posX - ((self.speed*0.4)*math.sin(theta)*game.gameObj.dt), self.posY + (self.speed*0.4)*math.cos(theta)*game.gameObj.dt)
                if self.permissionToMove(newPos) == True:
                    self.posX, self.posY = newPos
            if game.gameObj.events.keyMap["d"]:
                theta = (self.heading-90)%360
                self.lastMovingDirection = math.radians(theta)
                theta = math.radians(theta)
                newPos = (self.posX - ((self.speed*0.4)*math.sin(theta)*game.gameObj.dt), self.posY + (self.speed*0.4)*math.cos(theta)*game.gameObj.dt)
                if self.permissionToMove(newPos) == True:
                    self.posX, self.posY = newPos
        
        #if no keys were pressed, that means no movement occured, which means that the player will maintain its current velocity in its last direction
        if not (game.gameObj.events.keyMap["w"] or game.gameObj.events.keyMap["s"] or game.gameObj.events.keyMap["a"] or game.gameObj.events.keyMap["d"]):
            newPos = (self.posX - ((self.speed*0.4)*math.sin(self.lastMovingDirection)*game.gameObj.dt), self.posY + (self.speed*0.4)*math.cos(self.lastMovingDirection)*game.gameObj.dt)
            if self.permissionToMove(newPos) == True:
                self.posX, self.posY = newPos
        
        #if the input is the mouse, then moving the mouse will move the direction the player is looking in
        if game.gameObj.inputMode == "mouse":  
            mouse = game.gameObj.mouseWatcherNode
            mouseX, mouseY = mouse.getMouseX(), mouse.getMouseY()
            #mouse x and mouseY are coordinates between 0-1.
            #the heading rotation is the change in the mouseX
            #the pitch rotation is the change in the mouseY
            #the reason for it being 0-mouseX is because the heading is one counter clockwise instead of clockwise. So increasing the heading will turn left. 
            headingRot = (0-mouseX)*game.gameObj.sensX*game.gameObj.dt
            self.heading += headingRot
            pitchRot = (mouseY - 0)*game.gameObj.sensY*game.gameObj.dt
            self.pitch += pitchRot
            
            #moves the cursor back to the center of the screen. 
            game.gameObj.win.movePointer(0, game.gameObj.props.getXSize()//2,game.gameObj.props.getYSize()//2)
        
        #if the inputMode is the microbit, then a and d are used to pan left and right. 
        if game.gameObj.inputMode == "microbit":
            if game.gameObj.events.keyMap["a"]:
                self.heading += 180*game.gameObj.dt
            if game.gameObj.events.keyMap["d"]:
                self.heading -= 180*game.gameObj.dt
        
        self.checkDamage()
        self.axe.update()
        self.updatePlayerLoc()
        return task.cont
    
    def permissionToMove(self, newPos):
        '''
        This method is responsible for checking if the position the player wants to move into is outside of the map border.
        
        Parameters
        ----------------------------------------------------
        newPos: a tuple representing the new x and new y the player wants to move into
        
        Returns
        ----------------------------------------------------
        returns a boolean value, true if newPos is within the bounds of the map
'''
        return (game.gameObj.mapBorder[0][0] <= newPos[0] <= game.gameObj.mapBorder[0][1]) and (game.gameObj.mapBorder[1][0] <= newPos[1] <= game.gameObj.mapBorder[1][1])
    
    def checkDamage(self):
        '''
        This method is responsible for checking if the player is taking damage.
        
        It iterates through the ghostHitList list in the game events object to determine which ghost hit the player.
        Each ghost has its own timer which indicates their hit cooldown, this prevents ghosts from spamming hits.
        This method also manages the health regeneration for the player. 
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
        '''
        
        for ghosts in game.gameObj.events.ghostHitList:
            if ghosts[0] == True:
                if ghosts[1].mode == "default":
                    #if the ghost that has hit the player does not have a cooldown, it will cause the player to take damage and it will start the regeneration timer
                    #it will also start the timer for the ghost hit cooldown
                    #plays the heavy breathing sound effect
                    self.playerHealth -= 5
                    self.regenTimer.setTimer(4)
                    self.playerHitSFX.play()
                    ghosts[1].setTimer(3)
                elif ghosts[1].getTimeUntil() < 0:
                    #if the ghost hitting the player has passed its hit cooldown, the player will take damage, reset the regen timer and reset the ghost hit cooldown timer
                    #plays heavy breathing sound effect
                    self.playerHealth -= 5
                    self.regenTimer.setTimer(4)
                    self.playerHitSFX.play()
                    ghosts[1].setTimer(3)
            elif (not ghosts[0]) and ghosts[1].getTimeUntil() < 0:
                #if the ghost isnt colliding with the player and the ghost hit hooldown is over, then it will reset the ghost hit cooldown timer.
                ghosts[1].resetTimer()
                
        if self.playerHealth <= 0:
            #if the player health is below zero, the player dies
            game.gameObj.transitionGameToDeath()
            game.gameObj.taskMgr.remove("updatePlayer")
            self.playerHitSFX.stop()
            try:
                self.damageFilter.destroy()
            except:
                pass
            return
        
        if self.regenTimer.mode == "timing" and self.regenTimer.getTimeUntil() < 0:
            #if the regen timer is going and it has passed the regen cooldown, it will reset the player health, remove the bloody image from the screen
            # and stop the heavy breathing sound effect
            self.playerHealth = 15
            self.damageFilter.destroy()
            self.regenTimer.resetTimer()
            self.playerHitSFX.stop()
            
        if self.playerHealth == 10:
            #if the player health is 10, it will display the first bloody image
            try:
                self.damageFilter.destroy()
            except AttributeError:
                pass
            self.damageFilter = OnscreenImage(image = r"assets/bloodSplatterOne.png", pos = (0,0,0), scale = (1.7778,1,1))
            self.damageFilter.setTransparency(TransparencyAttrib.MAlpha)
            
        if self.playerHealth == 5:
            #if the player health is 5, it will display the second bloody image
            try:
                self.damageFilter.destroy()
            except AttributeError:
                print(e)
                pass
            self.damageFilter = OnscreenImage(image = r"assets/bloodSplatterTwo.png", pos = (0,0,0), scale = (1.7778,1,1))
            self.damageFilter.setTransparency(TransparencyAttrib.MAlpha)


