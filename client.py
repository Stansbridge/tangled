import pygame
import pygame.locals
import socket
import select
import random
import time
import logging
import zmq
import pdb
import bson
import uuid
import webbrowser
from pyre import Pyre, pyre_event
from pyre import zhelper
from collections import namedtuple
from enum import Enum

from map import *
from network import Network
from player import *
from sprite import *
from screen import MainMenu
from level import SaveLevel
from tile import Tileset
from music import LevelMusic
from controls import InputHandler

white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)

width = 1024
height = 1024

font = 'assets/fonts/alterebro-pixel-font.ttf'
level_tileset_path = 'assets/tilesets/main.png'
player_animation_tileset_path = 'assets/tilesets/player.png'
red_flag = "assets/tilesets/Red Flag.png"
blue_flag = "assets/tilesets/Blue Flag.png"

projectile_paths = [
                    'assets/images/spells/arrow.png',
                    'assets/images/spells/fireball.png',
                    'assets/images/spells/frostbolt.png',
                    'assets/images/spells/icicle.png',
                    'assets/images/spells/lightning_bolt.png',
                    'assets/images/spells/poisonball.png'
                    ]
projectile_images = []

for path in projectile_paths:
    projectile_images.append(pygame.image.load(path))

#buttons = {"A":1, "B":2, "X":0, "Y":3, "L":4, "R":5, "Start":9, "Select":8} #Use these for the PiHut SNES controller
buttons = {"A":0, "B":1, "X":2, "Y":3, "L":4, "R":5, "Start":7, "Select":6} #Use these for the iBuffalo SNES controller

error_message = "Everything is lava"

class GameState(Enum):
    MENU = 0
    PLAY = 1
    HELP = 2
    CHARACTER = 3
    QUIT = 4
    MUTE = 5

class GameClient():
    game_state = GameState.MENU

    def __init__(self):
        self.network = Network()
        self.setup_pygame()
        me = Player(self.screen, self.map, self.network)
        self.players = PlayerManager(me, self.network)

        self.network.node.shout('players:whois', bson.dumps({}))

        red = Sprite(self.screen, self.map, pygame.image.load(red_flag))
        blue = Sprite(self.screen, self.map, pygame.image.load(blue_flag))
        self.flags = {
            'red': red,
            'blue': blue
        }
        self.scores = {
            "red": 0,
            "blue": 0
        }
        self.map.set_centre_player(self.players.me)
        self.menu = MainMenu(self.screen, self.players)

    def setup_pygame(self):
        # Initialise screen/display
        self.screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

        # Initialise fonts.
        pygame.font.init()

        # Initialise music
        pygame.mixer.init()

        # Initialise the joystick.
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in joysticks:
            joystick.init()

        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.locals.QUIT,
            pygame.locals.JOYAXISMOTION,
            pygame.locals.KEYDOWN, pygame.locals.MOUSEBUTTONDOWN,  pygame.locals.JOYBUTTONDOWN])

        self.levels = {
            "main": SaveLevel('./assets/maps/CAPFLAG MAP NAT')
        }

        self.map = Map(
            self.screen,
            self.levels.get("main"),
            Tileset(level_tileset_path, (16, 16), (32, 32)),
            LevelMusic('assets/music/whizzersgame.mp3')
        )
        self.map.music.load_music()

    def set_state(self, new_state):
        if(new_state and new_state != self.game_state):
            self.game_state = new_state

            if(self.game_state.value == GameState.PLAY.value):
                pygame.key.set_repeat(50, 50)
            else:
                pygame.key.set_repeat(0, 0)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        tickspeed = 60
        last_direction = None
        self.toMove = False # Flag for when player moves - reduces network stress
        self.cast = False # Flag for when player casts spell.
        self.status_time = 0
        me = self.players.me
        first_time = False
        inputHandler = InputHandler() #Handles the inputs. They can get stage fright sometimes.

        if me.mute == "False":
            LevelMusic.play_music_repeat()

        try:
            while running:
                self.screen.fill((white))
                clock.tick(tickspeed)
                if clock.get_fps() > 0:
                    framedelta = 1 / clock.get_fps()
                else:
                    framedelta = 1
                
                if(self.game_state.value == GameState.MENU.value):
                    self.menu.render((self.map.screen.get_width() * 0.45, self.map.screen.get_height()*0.4))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
                            running = False
                            break

                        self.set_state(self.menu.update(event))
                elif(self.game_state.value == GameState.QUIT.value):
                    running = False
                    break
                elif(self.game_state.value == GameState.HELP.value):
                    webbrowser.open_new_tab("https://github.com/neontribe/untangled-2017/wiki")
                    self.game_state = GameState.MENU
                elif(self.game_state.value == GameState.MUTE.value):
                    if me.mute == "False":
                        me.set_mute("True", True)
                        LevelMusic.stop_music()
                    elif me.mute == "True":
                        me.set_mute("False", True)
                        LevelMusic.play_music_repeat()
                    self.game_state = GameState.MENU
                else:
                    #Handle movement.
                    if last_direction == None:
                        last_direction = Movement.DOWN
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
                            running = False
                            break
                    if inputHandler.checkPress("start"):
                        pass #Pause menu will be activated here once we readd it
                    elif inputHandler.checkHold("up"):
                        me.move(Movement.UP)
                        last_direction = Movement.UP
                        self.toMove = True
                    elif inputHandler.checkHold("down"):
                        me.move(Movement.DOWN)
                        last_direction = Movement.DOWN
                        self.toMove = True
                    elif inputHandler.checkHold("left"):
                        me.move(Movement.LEFT)
                        last_direction = Movement.LEFT
                        self.toMove = True
                    elif inputHandler.checkHold("right"):
                        me.move(Movement.RIGHT)
                        last_direction = Movement.RIGHT
                        self.toMove = True
                    elif inputHandler.checkPress("change"):
                        me.change_spell()
                    #elif inputHandler.checkHold("enter"):
                    #    if me.can_fire_ability:
                    #        self.cast = me.attack(last_direction)
                    elif inputHandler.checkPress("special") and me.can_step_ability:
                        me.step = 2
                        me.steptime = time.time()
                        me.can_step_ability = False

                    if self.cast == True:
                        me.can_fire_ability = False
                        me.firetime = time.time()
                    elif time.time() - me.firetime > 0.5:
                        me.can_fire_ability = True

                    if time.time() - me.steptime >30:
                        me.can_step_ability = True
                    elif time.time() - me.steptime >3:
                        me.step = 1

                    if time.time() - me.switch_time > 0.1:
                        me.can_switch_spell = True

                    if time.time() - me.swim_timer > 0.3:
                        me.can_swim = True
                    if time.time() - me.sand_timer > 0.1:
                        me.can_sand = True
                    if time.time() - me.move_timer > 0.075:
                        me.can_move = True

                    self.map.render()
                    for flag in self.flags.values():
                        flag.render()

                    me.render(True)

                    for spell in me.cast_spells:
                        spell.render()

                    self.players.set(self.network.node.peers())

                    # check network
                    events = self.network.get_events()
                    if events:
                        try:
                            for event in self.network.get_events():
                                if event.type == 'ENTER':
                                    # Force update on first join.
                                    self.toMove = True

                                    auth_status = event.headers.get('AUTHORITY')
                                    if auth_status == 'TRUE':
                                        self.players.authority_uuid = str(event.peer_uuid)
                                        self.network.authority_uuid = str(event.peer_uuid)
                                        self.players.remove(event.peer_uuid)
                                elif event.type == "SHOUT":
                                    if event.group == "player:name":
                                        new_name = bson.loads(event.msg[0])
                                        player = self.players.get(event.peer_uuid)
                                        if new_name['name']:
                                            player.set_name(new_name['name'])
                                    elif event.group == "world:position":
                                        new_position = bson.loads(event.msg[0])
                                        network_player = self.players.get(event.peer_uuid)
                                        network_player.set_position(Position(**new_position))
                                    elif event.group == "world:combat":
                                        new_spell_properties = bson.loads(event.msg[0])
                                        network_spell_caster = self.players.get(event.peer_uuid)
                                        network_spell_caster.current_spell = new_spell_properties.get('current_spell')
                                        network_spell_caster.cast_spells.append(Spell(network_spell_caster, (0, 0), projectile_images[network_spell_caster.current_spell]))
                                        network_spell_caster.cast_spells[-1].set_properties(SpellProperties(**new_spell_properties))
                                    elif event.group == "ctf:teams":
                                        team_defs = bson.loads(event.msg[0])
                                        self.players.set_teams(team_defs)
                                    elif event.group == "ctf:gotflag":
                                        flag_info = bson.loads(event.msg[0])
                                        team = flag_info["team"]
                                        uuid = flag_info["uuid"]
                                        flag = self.flags[team]
                                        if uuid == str(self.network.node.uuid()):
                                            flag.set_player(self.players.me)
                                        else:
                                            network_player = self.players.get(uuid)
                                            flag.set_player(network_player)
                                    elif event.group == 'ctf:dropflag':
                                        flag_info = bson.loads(event.msg[0])
                                        flag = self.flags[flag_info['team']]
                                        flag.set_player(None)
                                        flag.set_position((flag_info['x'], flag_info['y']))
                                    elif event.group == "players:whois":
                                        self.network.node.shout("player:name", bson.dumps(
                                            {
                                                "name": self.players.me.name
                                            }
                                        ))
                                    elif event.group == "ctf:status":
                                        msg = bson.loads(event.msg[0])
                                        status = msg['status']
                                        self.status_message = status
                                        self.status_time = time.time()
                                    elif event.group == "ctf:scores":
                                        scores = bson.loads(event.msg[0])
                                        self.scores = scores
                                elif event.type == 'WHISPER':
                                    msg = bson.loads(event.msg[0])
                                    if self.players.authority_uuid == str(event.peer_uuid):
                                        if msg['type'] == 'teleport':
                                            me.set_position((msg['x'], msg['y']))
                                            self.toMove = True
                                        elif msg['type'] == 'die':
                                            me.die()

                        except Exception as e:
                            import traceback
                            # traceback.print_exc()
                            pass

                    # if there are other peers we can start sending to groups.
                    if self.toMove == True:
                        self.network.node.shout("world:position", bson.dumps(me.get_position()._asdict()))
                        self.toMove = False
                    if self.cast == True:
                        self.network.node.shout("world:combat", bson.dumps(me.cast_spells[-1].get_properties()._asdict()))
                        self.cast = False


                    for playerUUID, player in self.players.others.items():
                        try:
                            player.render()

                            for spell in player.cast_spells:
                                spell.render()
                                hit_me = spell.hit_target_player(me)
                                if hit_me:
                                    player.cast_spells.remove(spell)
                                    me.deplete_health(spell.damage)

                        except PlayerException as e:
                            # PlayerException due to no initial position being set for that player
                            pass

                    score_shift = 220
                    for team, score in self.scores.items():
                        colour = (0, 0, 200) if team == 'blue' else (200, 0, 0)
                        display_rect = Rect((score_shift, 0), (200, 75))

                        typeface = self.menu.fonts['large']
                        score_text = typeface.render(str(score), False, (255, 255, 255))

                        text_bounds = score_text.get_rect()
                        text_bounds.center = display_rect.center

                        pygame.draw.rect(self.screen, colour, display_rect)
                        self.screen.blit(score_text, text_bounds.topleft)

                        score_shift += 200

                    if time.time() - self.status_time < 5:
                        typeface = self.menu.fonts['large']
                        status_text = typeface.render(self.status_message, False, (255, 255, 255))
                        text_bounds = status_text.get_rect()
                        text_bounds.center = self.screen.get_rect().center
                        pygame.draw.rect(self.screen, (0, 0, 0), text_bounds)
                        self.screen.blit(status_text, text_bounds.topleft)

                    self.players.minimap_render(self.screen)

                pygame.display.update()
        finally:
            self.network.stop()

if __name__ == '__main__':
    logger = logging.getLogger("pyre")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False

    g = GameClient()
    g.run()
