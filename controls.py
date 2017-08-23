import pygame, time
import pygame.locals

INPUT_TIMEOUT_DEFAULT = 0.15

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
                            "enter":[1],
                            "back":[3],
                            "change":[4,5,8],
                            "special":[9],
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
    
    def reloadJoysticks(self): #Aside from being used during the InputHandler init, this can be used for a menu option for if the player connects a joystick after the game has already start.
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joystick = False
        for joystick in joysticks:
            joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
    
    def reloadTimeout(self, which): #Call this when you're done with a custom timeout and want to reset it back to the default. You should do this any time the game changes state.
        if which == "all":
            for put in inputsTimeout:
                inputsTimeout[put] = INPUT_TIMEOUT_DEFAULT
        else:
            try:
                inputsTimeout[which] = INPUT_TIMEOUT_DEFAULT
            except:
                print(client.error_message + ": Tried to reset an input's timeout, but it was " + str(which) + " and not a valid input")
    
    def update(self, event): #Run this every frame with the event from `for event in pygame.event.get():` so that the InputHandler knows what's going on.
        if event.type == pygame.locals.KEYDOWN:
            for keysID, keys in self.bindingsKeyboard.items():
                if event.key in keys:
                    self.inputsPressed[keysID] = ("key",event.key)
            pygame.event.clear(pygame.locals.KEYDOWN)
        elif event.type == pygame.locals.JOYBUTTONDOWN:
            for keysID, keys in self.bindingsJoystick.items():
                if event.button in keys:
                    self.inputsPressed[keysID] = ("button",event.button)
            pygame.event.clear(pygame.locals.JOYBUTTONDOWN)
        elif event.type == pygame.locals.JOYAXISMOTION:
            if event.axis == 0: #X axis
                if event.value > 0:
                    self.inputsPressed["right"] = ("axis",event.axis)
                elif event.value < 0:
                    self.inputsPressed["left"] = ("axis",event.axis)
                else:
                    if self.inputsPressed["right"] == ("axis",event.axis):
                        self.inputsPressed["right"] = False
                    if self.inputsPressed["left"] == ("axis",event.axis):
                        self.inputsPressed["left"] = False
            elif event.axis == 1: #Y axis
                if event.value > 0:
                    self.inputsPressed["down"] = ("axis",event.axis)
                elif event.value < 0:
                    self.inputsPressed["up"] = ("axis",event.axis)
                else:
                    if self.inputsPressed["down"] == ("axis",event.axis):
                        self.inputsPressed["down"] = False
                    if self.inputsPressed["up"] == ("axis",event.axis):
                        self.inputsPressed["up"] = False
            pygame.event.clear(pygame.locals.JOYAXISMOTION)
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            for keysID, keys in self.bindingsMouse.items():
                if event.button in keys:
                    self.inputsPressed[keysID] = ("mouse",event.button)
            pygame.event.clear(pygame.locals.MOUSEBUTTONDOWN)
        elif event.type == pygame.locals.KEYUP:
            for pressed in self.inputsPressed:
                if self.inputsPressed[pressed] == ("key",event.key):
                    self.inputsPressed[pressed] = False
            pygame.event.clear(pygame.locals.KEYUP)
        elif event.type == pygame.locals.JOYBUTTONUP:
            for pressed in self.inputsPressed:
                if self.inputsPressed[pressed] == ("button",event.button):
                    self.inputsPressed[pressed] = False
            pygame.event.clear(pygame.locals.JOYBUTTONUP)
        elif event.type == pygame.locals.MOUSEBUTTONUP:
            for pressed in self.inputsPressed:
                if self.inputsPressed[pressed] == ("mouse",event.button):
                    self.inputsPressed[pressed] = False
            pygame.event.clear(pygame.locals.MOUSEBUTTONUP)
        print(self.inputsPressed)
    
    def checkHold(self, which): #Use this one if you don't care how often the input is being pressed.
        try:
            return self.inputsPressed[which]
        except:
            print("Everything is lava: {0} is not a valid input for InputHandler.checkHold()".format(which))
            return False
    
    def checkPress(self, which): #Use this one if you want to make sure the input has only been pressed once and isn't being held down.
        try:
            if self.inputsPressed[which]:
                self.inputsPressed[which] = False
                return True
            else:
                return False
        except:
            print("Everything is lava: {0} is not a valid input for InputHandler.checkHold()".format(which))
            return False
