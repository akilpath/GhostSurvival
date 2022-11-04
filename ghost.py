from panda3d.core import CollisionCapsule
from panda3d.core import CollisionNode
from game_collision_handler import CollisionHandler

import game
import math


class Ghost():
    
    def __init__(self, ghostNumberIn):
        '''
        Initialization for the Ghost Class. Every ghost that is created has a ghost number which indicates which indice
        in any ghost related index to access, it also acts as an identity so other ghosts can understand which ghost it is.
        
        
        Each ghost has its own position and heaidng. It also has its own collision solid, which is set as a child of the ghost NodePath.
        Important attributes of the ghost class are the speed of the ghost and the ghost health. The ghost health
        is dependent on the round the ghost was created in. Each ghost also has a status atribute, which is used to determine if the ghost has been spawned
        in or not. By default every ghost's status is set to unspawned and is also hidden in the scene graph, depending on the ghosts number and the time
        passed in the round counter, the ghost status will change and it will also be shown in the scene.
        
        Parameters
        ----------------------------------------------------
        ghostNumberIn: An integer representing the ghost number. It serves as an identity for the ghost, it allows the ghost to acces its unique
        state in the ghostHitList, ghostAxeList and ghostToGhostColliding list. It is also used for other ghosts to identify which ghost they are colliding with.
        
        Returns
        ----------------------------------------------------
        None
        
'''
        #sets the ghost number
        self.ghostNumber = ghostNumberIn
        
        #creates a NodePath for the ghost, then uses sets the globalGhost as an instance to the ghost NodePath.
        #This allows for the rendering to be better, instead of loading the same ghost model over and over again, it is
        #loaded once at the beginning of the program and every ghost duplicates that same model.
        self.np = game.gameObj.gameRoot.attachNewNode(f"{self.ghostNumber}ghost")
        game.gameObj.globalGhost.instanceTo(self.np)
        
        #information containing the spawn locations for the ghosts.
        ghostSpawn = [(-57,34), (-57,-26), (45,34), (45,-26)]
        
        #the ghost spawn location is determined by its ghost number
        self.posX = ghostSpawn[self.ghostNumber%4][0]
        self.posY = ghostSpawn[self.ghostNumber%4][1]
        self.np.setPos(self.posX,self.posY,2)
        
        #tells the event handler to accept any collision events between this ghost and the axe or this ghost and the player.
        game.gameObj.events.accept(f"{self.ghostNumber}ghostCollNode-into-playerCollNode", game.gameObj.events.collisions, ["player", self.ghostNumber])
        game.gameObj.events.accept(f"{self.ghostNumber}ghostCollNode-out-playerCollNode", game.gameObj.events.collisions, ["player", self.ghostNumber])
        game.gameObj.events.accept(f"axeCollNode-into-{self.ghostNumber}ghostCollNode", game.gameObj.events.collisions, ["axe", self.ghostNumber])
        game.gameObj.events.accept(f"axeCollNode-out-{self.ghostNumber}ghostCollNode", game.gameObj.events.collisions, ["axe", self.ghostNumber])
        
        #creates a collision node path to this collision node
        #adds a collision solid to the node of the cnodePath
        #the type of collision solid the ghosts use are capsules
        self.cnodePath = self.np.attachNewNode(CollisionNode(f"{self.ghostNumber}ghostCollNode"))
        self.cnodePath.node().addSolid(CollisionCapsule(0,0,0,0,0,-1.5,1))
        
        #this command will allow you to see the hitboxes of every ghost
        #self.cnodePath.show()
        
        #creates a collision handler object for the ghost
        #adds the collision node path along with its collision handler to the collision traverser
        #check the CollisionHandler class to understand the collision handler object
        ghostCollHandler = CollisionHandler()
        game.gameObj.cTrav.addCollider(self.cnodePath, ghostCollHandler)
        
        #creates ghost speed, ghost health
        self.speed = 6.5
        self.ghostHealth = game.gameObj.round*2 + 10
        
        #this variable indicates if a ghost is allowed to be hit, prevents multiple axe hits from happening in one swing
        self.allowHit = True
        
        self.status = "unspawned"
        self.np.hide()
    
    def destruct(self):
        '''
        This method is responsible for cleaning up the ghost object.
        
        It removes the NodePath of the ghost from the scene graph, it removes the collision node path from the collision traverser, removes the ghost's update task from
        the task manager and removes the ghost nodepath from the scene graph and any children attached to it. It tells the event handler to ignore collision events between this ghost
        and the axe and between this ghost and the player. Then it sets that entry in the ghosts list in the MyGame class to None, getting rid of the reference to that ghost.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        game.gameObj.cTrav.removeCollider(self.cnodePath)
        game.gameObj.taskMgr.remove(f"{self.ghostNumber}updateGhost")
        self.np.node().removeAllChildren()
        self.np.removeNode()
        game.gameObj.events.ignore(f"axeCollNode-into-{self.ghostNumber}ghostCollNode")
        game.gameObj.events.ignore(f"axeCollNode-out-{self.ghostNumber}ghostCollNode")
        game.gameObj.events.ignore(f"{self.ghostNumber}ghostCollNode-into-playerCollNode")
        game.gameObj.events.ignore(f"{self.ghostNumber}ghostCollNode-out-playerCollNode")
        game.gameObj.ghosts[self.ghostNumber] = None
    
    def permissionToMove(self):
        '''
        This method tells what ever is calling it whether or not the ghost can move. The only times the ghost is not able to move,
        is if it is colliding with the player. If game.gameObj.events.ghostHitList[self.ghostNumber][0] is True, that means the
        ghost is colliding with the player currently, which means it cannot move, so permissionToMove would return False.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        Returns a boolean value, True if the ghost is not colliding with the player and False if it is. 
'''
        return not game.gameObj.events.ghostHitList[self.ghostNumber][0]

    def move(self):
        '''
        This method is responsible for the movement of the ghost in general
        
        This method gets the ghost number of whichever ghost the currentghost is colliding with (if it is not colliding with any ghost then the value is -1).
        It then calculates the direction the player is in relative to the current ghost. This method will either move the ghost towards the player or away
        from the ghost it is colliding with. It also makes sure the ghost is always turning towards the player.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        ghostCollidingWith = game.gameObj.events.ghostToGhostColliding[self.ghostNumber]
        theta = math.atan2(game.gameObj.player.posY - self.posY, game.gameObj.player.posX - self.posX)
        
        #if the ghost is colliding with another ghost and the current ghost is the one further away from the player, it will move away from the ghost it is colliding with
        if ghostCollidingWith != -1:
            #when a ghost dies, its value does not disappear from the ghostToGhostColliding list in the handler class, so this makes sure that
            #the ghost this ghost is colliding with still exists.
            if game.gameObj.ghosts[ghostCollidingWith] != None:
                distSq = self.distSq((self.posX,self.posY), (game.gameObj.ghosts[ghostCollidingWith].posX,game.gameObj.ghosts[ghostCollidingWith].posY))
                distToPlayerSq = self.distSq((self.posX,self.posY), (game.gameObj.player.posX, game.gameObj.player.posY))
                colliderToPlayerSq = self.distSq((game.gameObj.ghosts[ghostCollidingWith].posX,game.gameObj.ghosts[ghostCollidingWith].posY), (game.gameObj.player.posX, game.gameObj.player.posY))
                #if this ghost is the further one away from the player and the distance between the colliding ghost is less than 1
                if distToPlayerSq >= colliderToPlayerSq and distSq <= 1:
                    tempTheta = math.atan2(game.gameObj.ghosts[ghostCollidingWith].posY - self.posY, game.gameObj.ghosts[ghostCollidingWith].posX - self.posX)
                    self.posX += math.cos(tempTheta+math.pi)*0.01
                    self.posY += math.sin(tempTheta+math.pi)*0.01
                    self.np.setPos(self.posX,self.posY,2)
                    return
            else:
                game.gameObj.events.ghostToGhostColliding[self.ghostNumber] = -1
        #if the ghost is allowed to move, it will move in the direction of the player at the ghost speed. 
        if self.permissionToMove():
            self.posX += math.cos(theta)*self.speed*game.gameObj.dt
            self.posY += math.sin(theta)*self.speed*game.gameObj.dt
            self.np.setPos(self.posX,self.posY,2)
        self.np.setH(math.degrees(theta)+90)
        
        
    def update(self, task):
        '''
        This is a task that is ran for every ghost in the game. The task is responsible for updating the ghost throughout the game.
        It spawns the ghost in, it calls the move function and reduces the ghost health when the ghost dies.
        
        Parameters
        ----------------------------------------------------
        task: task object from direct.task
        
        Returns
        ----------------------------------------------------
        returns task.cont which indicates that the task needs to be called again. 
'''
        
        if self.status == "moving":
            #if the ghost is spawned in, it calls the move() method
            #if the axe is colliding with the ghost and the ghost is allowed to take a hit it will take damage
            #having the animate attribute from axe in there allows hits to only be counted if the person is swinging their axe
            self.move()
            if game.gameObj.events.ghostAxeList[self.ghostNumber] == True and self.allowHit == True and game.gameObj.player.axe.animate == True:
                self.ghostHealth -= 5
                    
                #plays the hit sound effect
                game.gameObj.globalGhostHitSFX.play()
                self.allowHit = False
                
            if not game.gameObj.events.ghostAxeList[self.ghostNumber] and not self.allowHit:
                #if the axe is no longer colliding with the player and allowHit is also False, it is going to reset allowHit
                self.allowHit = True
            if self.ghostHealth <= 0:
                #adds the kill to ghostKills, plays death soundeffect and destroys this ghost
                game.gameObj.ghostKills += 1
                game.gameObj.globalGhostDeathSFX.play()
                self.destruct()
        elif self.status == "unspawned":
            #ghosts spawn in groups of four, there is a 5 second interval between group spawns. 
            if game.gameObj.roundSpawnTimer.getTimePassed() > (self.ghostNumber // 4)*5:
                self.status = "moving"
                self.np.show()
        return task.cont
    
    def distSq(self, pointOne, pointTwo):
        """
        This function returns the distance between one point and another. This function uses the pythagorean theorem, except it does not
        take the square root of the sum of the squares since it takes more processing power for square roots.
        
        Parameters
        ----------------------------------------------------
        pointOne: A tuple where the first indice is the x value and the second indice is the y value
        pointTwo: A tuple where the first indice is the x value and the second indice is the y value
        
        Returns
        ----------------------------------------------------
        Returns a floating point value that represents the distance squared between the two points
        """
        return (pointTwo[0]-pointOne[0])**2 + (pointTwo[1]-pointOne[1])**2