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
        self.inputsPressed = {"up":time.time(),
                            "down":time.time(),
                            "left":time.time(),
                            "right":time.time(),
                            "enter":time.time(),
                            "back":time.time(),
                            "change":time.time(),
                            "special":time.time(),
                            "start":time.time(),
                            "select":time.time()}
        self.inputsTimeout = {"up":INPUT_TIMEOUT_DEFAULT, #These aren't set in stone for a reason - you should be changing them on-the-fly to create custom cooldowns for certain actions.
                            "down":INPUT_TIMEOUT_DEFAULT,
                            "left":INPUT_TIMEOUT_DEFAULT,
                            "right":INPUT_TIMEOUT_DEFAULT,
                            "enter":INPUT_TIMEOUT_DEFAULT,
                            "back":INPUT_TIMEOUT_DEFAULT,
                            "change":INPUT_TIMEOUT_DEFAULT,
                            "special":INPUT_TIMEOUT_DEFAULT,
                            "start":INPUT_TIMEOUT_DEFAULT,
                            "select":INPUT_TIMEOUT_DEFAULT}
    
    def reloadJoysticks(self): #Aside from being used during the InputHandler init, this can be used for a menu option for if the player connects a joystick after the game has already start.
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joystick = False
        for joystick in joysticks:
            joystick.init()
        if pygame.joystick.get_count() > 0 and not me.name.startswith("windows"):
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
    
    #To use the check functions, you still need to pass the event yourself as the InputHandler can't poll for them. Use `for event in pygame.event.get():` to do this.
    def checkHold(self, event): #Use this one if you don't care how often the input is being pressed.
        returned = False
        if event.type == pygame.locals.KEYDOWN: #Keyboard key pressed
            for keysID, keys in self.bindingsKeyboard.items():
                if event.key in keys:
                    returned = keysID
                    self.inputsPressed[keysID] = time.time() + self.inputsTimeout[keysID]
                    pygame.event.clear(pygame.locals.KEYDOWN)
                    break
        elif event.type == pygame.locals.JOYBUTTONDOWN: #Gamepad button pressed
            for buttonsID, buttons in self.bindingsJoystick.items():
                if event.button in buttons:
                    returned = buttonsID
                    self.inputsPressed[buttonsID] = time.time() + self.inputsTimeout[buttonsID]
                    pygame.event.clear(pygame.locals.JOYBUTTONDOWN)
                    break
        elif event.type == pygame.locals.JOYAXISMOTION: #Gamepad d-pad or joystick moved (note: these bindings are hardcoded)
            if event.axis == 0: #X axis
                if event.value > 0:
                    returned = "right"
                elif event.value < 0:
                    returned = "left"
            elif event.axis == 1: #Y axis
                if event.value > 0:
                    returned = "up"
                elif event.value < 0:
                    returned = "down"
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            for buttonsID, buttons in self.bindingsMouse.items():
                if event.button in buttons:
                    returned = buttonsID
                    self.inputsPressed[buttonsID] = time.time() + self.inputsTimeout[buttonsID]
                    pygame.event.clear(pygame.locals.MOUSEBUTTONDOWN)
                    break
        return returned
    
    def checkPress(self, event): #Use this one if you want to make sure the input has only been pressed once and isn't being held down.
        returned = False
        if event.type == pygame.locals.KEYDOWN:
            for keysID, keys in self.bindingsKeyboard.items():
                if event.key in keys:
                    if self.inputsPressed[keysID] <= time.time():
                        returned = keysID
                    self.inputsPressed[keysID] = time.time() + self.inputsTimeout[keysID]
                    pygame.event.clear(pygame.locals.KEYDOWN)
                    break
        elif event.type == pygame.locals.JOYBUTTONDOWN:
            for buttonsID, buttons in self.bindingsJoystick.items():
                if event.button in buttons:
                    if self.inputsPressed[buttonsID] <= time.time():
                        returned = buttonsID
                    self.inputsPressed[buttonsID] = time.time() + self.inputsTimeout[buttonsID]
                    pygame.event.clear(pygame.locals.JOYBUTTONDOWN)
                    break
        elif event.type == pygame.locals.JOYAXISMOTION:
            inputAxis = False
            if event.axis == 0: #X axis
                if event.value > 0:
                    inputAxis = "right"
                elif event.value < 0:
                    inputAxis = "left"
            elif event.axis == 1: #Y axis
                if event.value > 0:
                    inputAxis = "up"
                elif event.value < 0:
                    inputAxis = "down"
            if inputAxis:
                if self.inputsPressed[inputAxis] <= time.time():
                    self.inputsPressed[inputAxis] = time.time() + self.inputsTimeout[buttonsID]
                    returned = inputAxis
            pygame.event.clear(pygame.locals.JOYAXISMOTION)
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            for buttonsID, buttons in self.bindingsMouse.items():
                if event.button in buttons:
                    if self.inputsPressed[buttonsID] <= time.time():
                        returned = buttonsID
                    self.inputsPressed[buttonsID] = time.time() + self.inputsTimeout[buttonsID]
                    pygame.event.clear(pygame.locals.MOUSEBUTTONDOWN)
                    break
        return returned
