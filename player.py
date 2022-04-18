from pickle import FALSE
import pygame
from animation import Animation
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, spawn):
        pygame.sprite.Sprite.__init__(self)
        self.image_size = 64
        self.image = pygame.image.load("assets\\herochar sprites\\herochar_idle_anim_strip_4.png")
        self.image = self.image.subsurface(pygame.Rect(0, 0, 16, 16))
        self.image =  pygame.transform.scale(self.image, (self.image_size, self.image_size))
        self.position = vector(spawn)
        self.hitbox = pygame.Rect(
            self.position.x, self.position.y, 
            self.image_size-36, self.image_size-8)
        self.keys = {"LEFT":False, "RIGHT":False}
        self.on_ground = False
        self.is_jumping = False
        self.nb_jump = 1
        self.gravity = 0.6
        self.friction = -0.1
        self.acceleration = vector(0, self.gravity)
        self.velocity = vector(0, 0)
        self.movement = vector(0, 0)
        self.facing_right = True
        self.air_timer = 6
        self.wall_jump_timer = 20

        self.is_dashing = False
        self.dash_timer = 5

        self.animation_timer = 1
        self.current_animation = "idle"
        self.animations = {
            "idle" : Animation("assets\\herochar sprites\\herochar_idle_anim_strip_4.png", 16, 64),
            "run" : Animation("assets\\herochar sprites\\herochar_run_anim_strip_6.png", 16, 64),
            "jump" : Animation("assets\\herochar sprites\\herochar_jump_up_anim_strip_3.png", 16, 64),
            "down" : Animation("assets\\herochar sprites\\herochar_jump_down_anim_strip_3.png", 16, 64),
            "double jump" : Animation("assets\\herochar sprites\\herochar_jump_double_anim_strip_3.png", 16, 64),
            "land": Animation("assets\\herochar sprites\\herochar_before_or_after_jump_srip_2.png", 16, 64)
        }
        
        
    def horizontal_movement(self, axis_value, delta_time):
        self.acceleration.x = 0
        if self.keys["LEFT"]:
            self.acceleration.x -= 0.8
            if not self.keys["RIGHT"]:
                self.facing_right = False
        if self.keys["RIGHT"]:
            self.acceleration.x += 0.8
            if not self.keys["LEFT"]:
                self.facing_right = True
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * delta_time
        self.limit_velocity(0)
        self.movement.x = (self.velocity.x * delta_time + (self.acceleration.x * 0.5) * (delta_time**2)) * axis_value
        self.position.x += self.movement.x
        self.hitbox.x = self.position.x

    def vertical_movement(self, delta_time):
        self.velocity.y += self.acceleration.y * delta_time
        if self.velocity.y > 20:
            self.velocity.y = 20
        self.movement.y = self.velocity.y * delta_time + (self.acceleration.x * 0.5) * (delta_time**2)
        self.position.y += self.movement.y
        self.hitbox.y = self.position.y
        if self.movement.y >= 0:
            self.is_jumping = False

    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def jump(self):
        if self.air_timer > 0:
            if self.air_timer > 0:
                self.nb_jump -= 1
                self.air_timer = 0
                self.is_jumping = True
                self.velocity.y -= 15
                self.on_ground = False

    def dash(self):
        self.is_dashing = True
            

    def get_tiles_hit(self, tiles):
        hits = []
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles):
        tiles_hit = self.get_tiles_hit(tiles)
        for tile in tiles_hit:
            if self.velocity.x > 0: # right
                self.position.x = tile.rect.left - self.hitbox.w
                self.hitbox.x = self.position.x
            elif self.velocity.x < 0: # left
                self.position.x = tile.rect.right
                self.hitbox.x = self.position.x
    
    def check_collisions_y(self, tiles):
        self.on_ground = False
        self.hitbox.bottom += 1
        tiles_hit = self.get_tiles_hit(tiles)
        for tile in tiles_hit:
            if self.velocity.y > 0: # bot
                self.on_ground = True
                self.is_jumping = False
                self.nb_jump = 2
                self.velocity.y = 0
                self.position.y = tile.rect.top - self.hitbox.h
                self.hitbox.y = self.position.y
                self.air_timer = 6
            elif self.velocity.y < 0: # top
                self.velocity.y = 0
                self.position.y = tile.rect.bottom
                self.hitbox.y = self.position.y

    def draw_hitbox(self, surface, camera):
        pygame.draw.rect(surface, (255,0,0), 
            pygame.Rect(
            self.hitbox.x+camera.position.x, self.hitbox.y+camera.position.y, 
            self.hitbox.width, self.hitbox.height
            ), 
            2)

    def draw(self, surface, camera):
        # left
        if self.facing_right == False:
            surface.blit(pygame.transform.flip(self.image, True, False),
                (self.position.x-16 + camera.position.x, 
                self.position.y-8 + camera.position.y)
            )
        # right
        else:
            surface.blit(self.image, 
                (self.position.x-16 + camera.position.x, 
                self.position.y-8 + camera.position.y)
            )

    def update_animation(self, axis_value):
        self.animation_timer -= 1
        if axis_value == 0 and self.on_ground:
            new_animation = "idle"
        elif axis_value != 0 and self.on_ground:
            new_animation = "run"
        elif self.nb_jump == 1 and self.is_jumping:
            new_animation = "jump"
        elif self.movement.y > 0:
            new_animation = "down"
        else:
            new_animation = "idle"
        if self.current_animation != new_animation:
            self.animations[self.current_animation].reset()
        self.current_animation = new_animation

    def play_animation(self):
        if self.animation_timer == 0:
            if self.current_animation == "idle":
                self.animation_timer = 10
            else:
                self.animation_timer = 5
            self.image = self.animations[self.current_animation].play()
            
    def update(self, axis_value, delta_time, tiles):
        self.air_timer -= 1
        self.update_animation(axis_value)
        self.play_animation()
        self.horizontal_movement(axis_value, delta_time)
        self.check_collisions_x(tiles)
        self.vertical_movement(delta_time)
        self.check_collisions_y(tiles)