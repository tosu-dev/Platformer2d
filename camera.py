import pygame
import random
from constants import SCREEN_SIZE

from player import Player
vector = pygame.math.Vector2

class Camera:

    def __init__(self, screen_size:tuple, position:pygame.math.Vector2, state:str):
        """
        Create a camera with a position

        param screen_size: tuple (screen_width:int, screen_height:int)
        """
        self.screen_width, self.screen_height = screen_size
        self.position = vector(-position.x+SCREEN_SIZE[0]//2, -position.y+SCREEN_SIZE[1]//2)
        self.state = state
        self.shake_timer = 0

    def shake(self, shake_force):
        """
        Shake the camera during the shake timer with a certain force

        param shake_force: The force of the shake (pixels)
        """
        self.position.x += random.randint(-shake_force, shake_force)
        self.position.y += random.randint(-shake_force, shake_force)

    def scroll(self, speed_x:int, speed_y:int):
        """
        Scroll the camera position at a certain speed

        param speed_x: Speed on x axis (pixels)
        param speed_y: Speed on y axis (pixels)
        """
        self.position.x += speed_x
        self.position.y += speed_y

    def follow_player_x(self, player:Player):
        """
        Follow a player on the x axis

        param player: The player to follow
        """
        self.position.x += (self.screen_width//2 - player.position.x - self.position.x) // 10

    def follow_player_y(self, player:Player):
        """
        Follow a player on the y axis

        param player: The player to follow
        """
        self.position.y += (self.screen_height//2 - player.position.y - self.position.y) // 10
    
    def follow_player(self, player:Player):
        """
        Follow a player one x and y axis

        param player: The player to follow
        """
        self.follow_player_x(player)
        self.follow_player_y(player)
