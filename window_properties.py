from panda3d.core import WindowProperties

class GameProperties(WindowProperties):
    def __init__(self):
        '''
        Initialization of the GameProperties class. This class inherits from the WindowProperties class.
        The reason for having it inherit instead of just using the WindowProperties class provided by
        Panda3d is because it allows me to have default attributes of the window properties object I create.
        This class only has one method, which allows the cursor to be toggled between visible and invisible.
        This class only creates properties for a window, the actual property change will not be visible until
        win.requestProperties(GameProperties) is called.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None

'''
        super().__init__()
        self.isCursorHidden = False
        self.setCursorHidden(self.isCursorHidden)
        
        #keeps the cursor confined in the window
        self.setMouseMode(WindowProperties.M_confined)
        
        #keeps this window on top
        self.set_z_order(WindowProperties.Z_top)
    
    def updateMouseView(self):
        '''
        This method is responsible for toggling the visibility of the cursor. It first toggles the isCursorHidden attribute,
        then sets the cursorHidden to what is specified by isCursorHidden
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        self.isCursorHidden = not self.isCursorHidden
        self.setCursorHidden(self.isCursorHidden)
        
    