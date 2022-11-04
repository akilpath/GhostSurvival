import time

class Timer():
    def __init__(self):
        '''
        This class is the timer class. It is a simple class using only the time module of python.
        I ended up needing to add cooldowns for ghost hits so I created a timer class to make it easier.
        The timer class only has 3 attributes, delay, which represents the future time,
        it is equal to the delay you want added to the current time when the delay was set
        originTime: which is the value returned by time.time(), this is set to be whenever the timer is started.
        and mode: which indicates if a timer is currently timing or not.
        
        Parameters
        ----------------------------------------------------
        None
        
        Returns
        ----------------------------------------------------
        None
'''
        self.delay = 0
        self.mode = "default"
        self.originTime = None
    
    def setTimer(self, delay):
        '''
        This method allows for a delay for the timer to be created, it updates the delay attribute, resets originTime and changes
        mode to timing.
        
        Parameters
        ----------------------------------------------------
        delay: represents a value to delay by, can be an integer or a float
        
        Returns
        ----------------------------------------------------
        None
'''
        self.delay = time.time()+delay
        self.originTime = time.time()
        self.mode = "timing"
    
    def resetTimer(self):
        '''
        Resets a timer back to the default mode, with no delay and no originTime
'''
        self.delay = 0
        self.originTime = 0
        self.mode = "default"
        
    def getTimeUntil(self):
        '''
        This method gets the time until the delay, this would represent the timer acting as an actual timer.
        
        Returns
        ----------------------------------------------------
        returns the difference between the delayTime and the current time. 
'''
        return self.delay-time.time()
    
    def getTimePassed(self):
        '''
        This method returns the time passed, this method allows the timer object to act more as a stopwatch
        
        Returns
        ----------------------------------------------------
        returns the difference between the current time and the origintime. 
'''
        return time.time() - self.originTime