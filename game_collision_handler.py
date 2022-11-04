from panda3d.core import CollisionHandlerEvent

class CollisionHandler(CollisionHandlerEvent):
    def __init__(self):
        '''
        Initialization for the Collision handler object. There are many different ways to handle collisions
        in panda3d, one way of doing it is having collisions throw events, I chose this way. This class inherits from
        the CollisionHandlerEvent class, this class has no methods, all it does is create a collisionHandler for an object.
        The specifications for CollisionHandlerEvent are the same for every object I use, so I just had it be part of the initialization
        of the Collision Handler
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        super().__init__()
        #this is notation for events
        #whenever a collision is detected, it is going to send out an event according to this string
        #%fn represents the from object
        #%in represents the into object
            
        self.addInPattern('%fn-into-%in')
        self.addAgainPattern('%fn-again-%in')
        self.addOutPattern('%fn-out-%in')
    
    