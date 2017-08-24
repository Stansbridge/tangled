import pygame, time
import pygame.locals

class InputHandler(): 
    def __init__(self):
        self.reloadJoysticks()
        self.bindingsKeyboard = {"up":[pygame.locals.K_UP],
                                "down":[pygame.locals.K_DOWN],
                                "left":[pygame.locals.K_LEFT],
                                "right":[pygame.locals.K_RIGHT],
                                "enter":[pygame.locals.K_RETURN, pygame.locals.K_SPACE, pygame.locals.K_x], #i.e. A
                                "back":[pygame.locals.K_z],                                                 #i.e. B
                                "change":[pygame.locals.K_c],                                               #i.e. X
                                "special":[pygame.locals.K_BACKQUOTE],                                      #i.e. Y
                                "start":[pygame.locals.K_ESCAPE],
                                "select":[]}
        self.bindingsJoystick = {"up":[], #These are handled by hardcoded axis events
                                "down":[],
                                "left":[],
                                "right":[],
                                "enter":[0, 5],  #i.e. A
                                "back":[1],      #i.e. B
                                "change":[2, 4], #i.e. X
                                "special":[3],   #i.e. Y
                                "start":[7],
                                "select":[6]}
        self.bindingsMouse = {"up":[],
                            "down":[],
                            "left":[],
                            "right":[],
                            "enter":[0],
                            "back":[2],
                            "change":[1],
                            "special":[],
                            "start":[],
                            "select":[]}
        self.bindingsAxis = {"up":[(1,"-")],
                            "down":[(1,"+")],
                            "left":[(0,"-")],
                            "right":[(0,"+")],
                            "enter":[],
                            "back":[],
                            "change":[],
                            "special":[],
                            "start":[],
                            "select":[]}
        self.inputsPressed = {"up":False,
                            "down":False,
                            "left":False,
                            "right":False,
                            "enter":False,
                            "back":False,
                            "change":False,
                            "special":False,
                            "start":False,
                            "select":False}
        self.inputsTimeout = {"up":0,
                            "down":0,
                            "left":0,
                            "right":0,
                            "enter":0,
                            "back":0,
                            "change":0,
                            "special":0,
                            "start":0,
                            "select":0}
        self.inputsTimer = {"up":0,
                            "down":0,
                            "left":0,
                            "right":0,
                            "enter":0,
                            "back":0,
                            "change":0,
                            "special":0,
                            "start":0,
                            "select":0}
    
    def reloadJoysticks(self): #Aside from being used during the InputHandler init, this can be used for a menu option for if the player connects a joystick after the game has already start.
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joystick = False
        for joystick in joysticks:
            joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
        if self.joystick:
            self.axesNeutral = []
            for axis in range(0, self.joystick.get_numaxes()):
                self.axesNeutral.append(self.joystick.get_axis(axis))
    
    def resetTimeout(self, which): #Call this when you're done with a custom timeout and want to reset it back to the default. You should do this any time the game changes state.
        if which == "all":
            for put in inputsTimeout:
                inputsTimeout[put] = 0
        else:
            try:
                inputsTimeout[which] = 0
            except:
                print("Everything is lava: {0} is not a valid input for InputHandler.reloadTimeout()".format(which))
    
    def setTimeout(self, which, timeout): #Call this to set a new custom timeout.
        if which == "all":
            for put in self.inputsTimeout:
                self.inputsTimeout[put] = timeout
        elif which == "move":
            for put in ["up","down","left","right"]:
                self.inputsTimeout[put] = timeout
        else:
            #try:
            self.inputsTimeout[which] = timeout
            #except:
            #    print("Everything is lava: {0} is not a valid input for InputHandler.setTimeout()".format(which))
    
    def resetTimer(self, which): #For internal use only.
        self.inputsTimer[which] = time.time() + self.inputsTimeout[which]
    
    def inputCheck(self, which): #For internal use only.
        for key in self.bindingsKeyboard[which]:
            if pygame.key.get_pressed()[key]:
                return True
        if self.joystick:
            for button in self.bindingsJoystick[which]:
                if self.joystick.get_button(button):
                    return True
            for axes in self.bindingsAxis[which]:
                if axes[1] == "+" and self.joystick.get_axis(axes[0]) > self.axesNeutral[axes[0]]:
                    return True
                elif axes[1] == "-" and self.joystick.get_axis(axes[0]) < self.axesNeutral[axes[0]]:
                    return True
        for button in self.bindingsMouse[which]:
            if pygame.mouse.get_pressed()[button]:
                return True
        return False
    
    def checkHold(self, which): #Use this one if you just want to know if it's being pressed, or if you want to have a cooldown on this input.
        if self.inputsTimeout[which]:
            if self.inputsTimer[which] < time.time():
                if self.inputCheck(which):
                    self.resetTimer(which)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return self.inputCheck(which)
        return False
    
    def checkPress(self, which): #Use this one if you want to make sure the input has only been pressed once and isn't being held down. Note that this ignores timeouts.
        if not self.inputsPressed[which]:
            if self.inputCheck(which):
                self.inputsPressed[which] = True
                return True
            else:
                return False
        else:
            if self.inputCheck(which):
                self.inputsPressed[which] = True
            else:
                self.inputsPressed[which] = False
            return False
