import pygame
import os
import csv
from camera import Camera


class Tile(pygame.sprite.Sprite):
    def __init__(self, default_size:int, x:int, y:int, num_tile:int, spritesheet:str, zoom:int=1):
        """
        A square image with an hitbox

        param default_size: Default size of a tile
        param x: x coordinate of the tile
        param y: y coordinate of the tile
        param num_tile: Number of the tile in the spritesheet
        param spritesheet: Path to the spritesheet image
        param zoom: Zoom the size of the tile
        """
        pygame.sprite.Sprite.__init__(self)
        self.default_size = default_size
        self.zoom = zoom
        self.size = self.default_size * self.zoom
        self.image = pygame.image.load(spritesheet).convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.zoom, self.image.get_height()*self.zoom))
        self.left = (num_tile % (self.image.get_width()//self.size)) * self.size
        self.top = (num_tile // (self.image.get_width()//self.size)) * self.size
        self.area = (
                self.left, self.top,
                self.size, self.size
            )
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.rect.width, self.rect.height = self.size, self.size

    def draw(self, surface:pygame.Surface, camera:Camera):
        """
        Draw the tile on a surface depending of the camera position

        param surface: Surface to draw
        param camera: The camera
        """
        surface.blit(self.image, (self.rect.x + camera.position.x, self.rect.y + camera.position.y), self.area)


class TileMap():
    def __init__(self, filename:str, spritesheet:str, zoom:int=1):
        """
        A map of tiles

        param filename: Path to the map file
        param spritesheet: Path to the spritesheet file
        param zoom: Zoom the size of tiles
        """
        self.zoom = zoom
        self.spritesheet = spritesheet
        self.tiles = []
        self.load_tiles(filename)
        
    def load_map(self, filename:str) -> list:
        """
        Load the map 

        param filename: Path to the map file
        """
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename:str):
        """
        Load tiles of the map
        
        param filename: Path to the map file
        """
        map = self.load_map(filename)
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] != '-1':
                    tile = Tile(16, 0, 0, int(map[y][x]), self.spritesheet, zoom=self.zoom)
                    tile.rect.x = x*tile.size
                    tile.rect.y = y*tile.size
                    self.tiles.append(tile)

    def draw(self, surface:pygame.Surface, camera:Camera):
        """
        Draw the tile on a surface depending of the camera position
        param surface: Surface to draw
        param camera: The camera
        """
        for tile in self.tiles:
            tile.draw(surface, camera)