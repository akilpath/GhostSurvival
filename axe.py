from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from game_collision_handler import CollisionHandler

import game

class Axe():
    def __init__(self):
        '''
        Creates the axe object, this is the object that is used by the MyGame class.
        During initialization, the axe object creates and sets up its own NodePath with the axe. This class
        mainly only changes the movement of the axe (animation)
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        #Creating the nodepath of the axe, then inserting it into the scene graph under the cam
        #Cam is child of camera, cam is the perspective lens Panda3D uses
        #The reason the axe is put under the cam instead of the camera is because when I want to remove the axe,
        #I can call self.cam.removeChildren()
        self.np  = game.gameObj.loader.loadModel("assets/axe.x")
        self.np.reparentTo(game.gameObj.cam)
        self.np.setTexture(game.gameObj.textures)
        self.np.setLight(game.gameObj.pLight)
        self.np.setLight(game.gameObj.aLight)
        self.np.setScale(1.2)
        
        #variables for the axe position
        self.posX = 1
        self.posY = 0.4
        self.posZ = -0.9
        
        #Axe collision node path
        self.cnodePath = self.np.attachNewNode(CollisionNode("axeCollNode"))
        self.cnodePath.node().addSolid(CollisionSphere(-0.21,1.45,-0.25,0.07))
        #self.cnodePath.show()
        self.axeCollHandler = CollisionHandler()
        game.gameObj.cTrav.addCollider(self.cnodePath, self.axeCollHandler)

        self.np.setPos(self.posX,self.posY,self.posZ)
        self.np.setHpr(10,40,0)
        
        #variable used to indicate if the axe is in animation
        self.animate = False
        
        #variable used to indicate if the axe is not being animated, is moving forward, or is returning
        self.animprocess = 0
        
        
    def updateAxeLoc(self):
        '''
        This method updates the axe location
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        self.np.setPos(self.posX,self.posY,self.posZ)
    
    def animateAxe(self):
        '''
        Method called for animating the axe. For animprocess, 1 represents the axe going forward,
        2 represents the axe coming back, and 0 represents no animation.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        if self.animprocess == 1:
            if game.gameObj.events.axeCollision == True:
                #if the axe has collided with the ghost, it can begin to move back to the player
                self.animprocess = 2
            if self.posY < 2:
                self.posY += 5*game.gameObj.dt
            if self.posX > 0.5:
                self.posX -= 2*game.gameObj.dt
            if self.posZ < -0.5:
                self.posZ += 2*game.gameObj.dt
            if self.posY >= 2 and self.posX <= 0.5 and self.posZ >= -0.5:
                #if the axe has reached its maximum distance from the player, it begins to come back
                self.animprocess = 2
        elif self.animprocess == 2:
            if self.posY > 0.4:
                self.posY -= 3*game.gameObj.dt
            if self.posX < 1:
                self.posX += 2*game.gameObj.dt
            if self.posZ > -0.9:
                self.posZ -= 2*game.gameObj.dt
            if self.posX >= 0.9 and self.posY <= 0.4 and self.posZ <= -0.9:
                #if the axe has came back to the player, reset the anim process, set animate to False
                self.posX = 0.9
                self.posY = 0.4
                self.posZ = -0.9
                self.animprocess = 0
                self.animate = False
                
                #this needs to be here to prevent a glitch from happening, a ghost may destruct midway through collision
                #causing axeCollision to not be updated
                game.gameObj.events.axeCollision = False
        self.updateAxeLoc()
        
        
    def update(self):
        '''
        Update method of the axe, this is called each time the player update method is ran.
        If the left mouse button is clicked or being clicked, it triggers the animation.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
        
'''
        if game.gameObj.events.keyMap["mouse1"] and not self.animate:
            self.animate = True
            self.animprocess = 1
        if self.animate == True:
            self.animateAxe()