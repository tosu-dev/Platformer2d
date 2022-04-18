import pygame

class Animation(pygame.sprite.Sprite):

    def __init__(self, image_path:str, default_image_size:int, image_size:int):
        """
        A list of images that can be played to create an animation

        param image_path: path to the animation image
        param default_image_size: original size of images of the animation
        param image_size: new size of images of the animation
        """
        self.image = pygame.image.load(image_path)
        self.image_size = image_size
        self.images = []
        for x in range(0, self.image.get_width(), default_image_size):
            img = self.image.subsurface(pygame.Rect(x, 0, default_image_size, default_image_size))
            img = pygame.transform.scale(img, (self.image_size, self.image_size))
            self.images.append(img)
        self.current_image = 0

    def reset(self):
        """
        Reset the animation
        """
        self.current_image = 0

    def play(self) -> pygame.Surface:
        """
        Go to the next image of the animation
        
        return: the current image of the animation
        """
        self.current_image += 1
        self.current_image %= len(self.images)
        return self.images[self.current_image]
            