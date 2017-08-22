import pygame, time
import pygame.locals

INPUT_TIMEOUT_DEFAULT = 150

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
        self.bindingsJoystick = {"up":[],
                                "down":[],
                                "left":[],
                                "right":[],
                                "enter":[0, 5],  #i.e. A
                                "back":[1],      #i.e. B
                                "change":[2, 4], #i.e. X
                                "special":[3],   #i.e. Y
                                "start":[7],
                                "select":[6]}
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
        self.inputsTimeout = {"up":INPUT_TIMEOUT_DEFAULT,
                            "down":INPUT_TIMEOUT_DEFAULT,
                            "left":INPUT_TIMEOUT_DEFAULT,
                            "right":INPUT_TIMEOUT_DEFAULT,
                            "enter":INPUT_TIMEOUT_DEFAULT,
                            "back":INPUT_TIMEOUT_DEFAULT,
                            "change":INPUT_TIMEOUT_DEFAULT,
                            "special":INPUT_TIMEOUT_DEFAULT,
                            "start":INPUT_TIMEOUT_DEFAULT,
                            "select":INPUT_TIMEOUT_DEFAULT}
    
    def reloadJoysticks(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joystick = False
        for joystick in joysticks:
            joystick.init()
        if pygame.joystick.get_count() > 0 and not me.name.startswith("windows"):
            self.joystick = pygame.joystick.Joystick(0)
   
    def checkHold(self, event):
        if event.type == pygame.locals.KEYDOWN:
            for keysID, keys in self.bindingsKeyboard.items():
                if event.key in keys:
                    self.inputsPressed[keysID] = time.time() + self.inputsTimeout[keysID]
                    return keysID
        elif event.type == pygame.locals.JOYBUTTONDOWN:
            for buttonsID, buttons in self.bindingsJoystick.items():
                if event.button in buttons:
                    self.inputsPressed[keysID] = time.time() + self.inputsTimeout[buttonsID]
                    return buttonsID
        return False
    
    def checkPress(self, event):
        if event.type == pygame.locals.KEYDOWN:
            for keysID, keys in self.bindingsKeyboard.items():
                if event.key in keys:
                    if self.inputsPressed[keysID] <= time.time():
                        return keysID
                    self.inputsPressed[keysID] = time.time() + self.inputsTimeout[keysID]
        elif event.type == pygame.locals.JOYBUTTONDOWN:
            for buttonsID, buttons in self.bindingsJoystick.items():
                if event.button in buttons:
                    if self.inputsPressed[buttonsID] <= time.time():
                        return buttonsID
                    self.inputsPressed[buttonsID] = time.time() + self.inputsTimeout[buttonsID]
        return False
