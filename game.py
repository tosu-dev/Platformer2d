import pygame
import sys
import time
import random
from player import Player
from camera import Camera
from tiles import *
from constants import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.map = TileMap(
            "data\\tilemap\\map.csv",
            "assets\\tiles and background_foreground\\tileset.png",
            zoom = 4)
        self.player = Player(spawn=(64*13, 64*13))
        self.camera = Camera(
            SCREEN_SIZE, 
            self.player.position,
            "follow player")
        self.bg_image = pygame.image.load(
            "assets\\tiles and background_foreground\\bg_0.png"
            ).convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image, 
            (int(SCREEN_SIZE[0]*1.5), int(SCREEN_SIZE[1]*1.5)))
        
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
        
        self.game_running = False
        self.delta_time = 0
        self.gravity_force = 0.2
        self.axis_value = 0


    def draw_bg(self):
        self.screen.blit(self.bg_image, 
            (-100 + self.camera.position.x // 5, 
            -100 + self.camera.position.y // 5))


    def run(self):
        self.game_running = True
        prev_time = time.time()
        while self.game_running:
            # delta time
            self.delta_time = (time.time() - prev_time) * TARGET_FPS
            prev_time = time.time()

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # joystick
                if self.joystick:
                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis == 0:
                            if abs(event.value) > 0.1:
                                if event.value < 0:
                                    self.player.keys["LEFT"] = True
                                elif event.value > 0:
                                    self.player.keys["RIGHT"] = True
                                self.axis_value = abs(event.value)
                            else:
                                self.axis_value = 0
                                self.player.keys["LEFT"] = False
                                self.player.keys["RIGHT"] = False
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0 and not self.player.is_jumping:
                            self.player.jump()
                        if event.button == 0 and not self.player.is_jumping and self.player.double_jump_available:
                            self.player.double_jump()
                    if event.type == pygame.JOYBUTTONUP:
                        if event.button == 0 and self.player.is_jumping:
                            self.player.velocity.y *= 0.25
                            self.player.is_jumping = False
                else:
                    # keyboard
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.camera.shake_timer = 30

                        if event.key == pygame.K_y:
                            if self.camera.state == "scroll":
                                self.camera.state = "follow player"
                            elif self.camera.state == "follow player":
                                self.camera.state = "scroll"

                        if event.key == pygame.K_LEFT:
                            self.player.keys["LEFT"] = True
                        if event.key == pygame.K_RIGHT:
                            self.player.keys["RIGHT"] = True
                        if event.key == pygame.K_UP:
                            self.player.jump()
                        if event.key == pygame.K_x:
                            self.player.dash()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.player.keys["LEFT"] = False
                        if event.key == pygame.K_RIGHT:
                            self.player.keys["RIGHT"] = False
                        if event.key == pygame.K_UP and self.player.is_jumping:
                            self.player.velocity.y *= 0.25
                            self.player.is_jumping = False
                    self.axis_value = 0
                    if self.player.keys["LEFT"] ^ self.player.keys["RIGHT"]:
                        self.axis_value = 1
                        



            # UPDATE
            self.player.update(self.axis_value, self.delta_time, self.map.tiles)
            
            # camera
            if self.camera.state == "follow player":
                self.camera.follow_player(self.player)
            elif self.camera.state == "scroll":
                self.camera.scroll(5, 0)

            if self.camera.shake_timer > 0:
                self.camera.shake(5)
                self.camera.shake_timer -= 1

            # camera border
            if self.camera.position.x >= 0:
                self.camera.position.x = 0
                if self.camera.state == "follow player":
                    self.camera.follow_player_y(self.player)
            elif self.camera.position.x <= -2200:
                self.camera.position.x = -2200
                if self.camera.state == "follow player":
                    self.camera.follow_player_y(self.player)
            

            # DRAW
            self.draw_bg()
            self.player.draw(self.screen, self.camera)
            self.map.draw(self.screen, self.camera)


            pygame.display.update()
            self.clock.tick(FPS)