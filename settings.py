import json

class Settings():
    def __init__(self):
        '''
        This is the settings class, this class contains all the attributes that are stored in the json file that is loaded.
        There is only one settings object created in my game, and that same one is manipulated throughout the program.
        When the settings object is created, it loads the settings file into its own attributes. 
'''
        with open(r"config/settings.json") as file:
            data = json.load(file)
            self.sensitivityX = data["sensitivityX"]
            self.sensitivityY = data["sensitivityY"]
            self.input = data["input"]
    
    def update(self, sensXIn = None, sensYIn = None, inputIn = None):
        '''
        This method allows me to update any of the settings. Depending on whichever setting I want to change,
        I can send it through this function and it will update the settings attribute.
        
        Parameters
        ----------------------------------------------------
        sensXIn: Default: None, This parameter represents the x sensitivity I want to change to
        sensYIn: Default: None, this parameter represents the y sensitivity I want to change to
        inputIn: Default: None, this parameter represents the input mode I want to change to, can either be "mouse" or "microbit"
'''
        
        if sensXIn != None:
            self.sensitivityX = sensXIn
        if sensYIn != None:
            self.sensitivityY = sensYIn
        if inputIn != None:
            self.input = inputIn
    
    def saveSettings(self):
        '''
        This method is called whenever gameQuit() is called from the MyGame class, it saves all the attributes of settings to the
        json file.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        with open(r"config/settings.json", "w") as file:
            data = {"input": self.input, "sensitivityX": self.sensitivityX, "sensitivityY": self.sensitivityY}
            json.dump(data,file)