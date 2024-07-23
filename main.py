# This Python file uses the following encoding: Latin-1
# Importing the pygame modules
import random
import pygame
import asyncio
from pygame.locals import *
 
# Initiate pygame and giver permissions to use pygames funktions
pygame.init()

# Mobile based resulotion: x = 1080; y = 2400
# Blit options:
# topleft: Die obere linke Ecke des Rechtecks.
# topright: Die obere rechte Ecke des Rechtecks.
# bottomleft: Die untere linke Ecke des Rechtecks.
# bottomright: Die untere rechte Ecke des Rechtecks.
# midtop: Die Mitte der oberen Kante des Rechtecks.
# midbottom: Die Mitte der unteren Kante des Rechtecks.
# midleft: Die Mitte der linken Kante des Rechtecks.
# midright: Die Mitte der rechten Kante des Rechtecks.
# center: Das Zentrum des Rechtecks.

# Get the screen resolution
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h # To get HD resolution on FullHD screen: screen_info.current_w - 640, screen_info.current_h - 360
screen = pygame.display.set_mode((screen_width, screen_height))
Player_Monitor = False
Obstacle_Monitor = False
Jungle_IMAGE_Monitor = False
if screen_width > screen_height:
   Player_Monitor = True
   Obstacle_Monitor = True
   Jungle_IMAGE_Monitor = True
gameDisplay_rect = screen.get_rect()
pygame.display.set_caption('Dragonrace')


def get_font_size(base_size, base_resolution, current_resolution):
    width_ratio = current_resolution[0] / base_resolution[0]
    height_ratio = current_resolution[1] / base_resolution[1]
    scale_factor = (width_ratio + height_ratio) / 2  # Middle value of the scaling factors
    return int(base_size * scale_factor)

base_resolution = (1920, 1080)
base_resolution_image = (screen_width, screen_height)

current_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)

def scale_image(base_image, base_resolution_image, current_resolution, manual_scale=1.0):
    width_ratio = current_resolution[0] / base_resolution_image[0]
    height_ratio = current_resolution[1] / base_resolution_image[1]
    new_width = int(base_image.get_width() * width_ratio * manual_scale)
    new_height = int(base_image.get_height() * height_ratio * manual_scale)
    return pygame.transform.scale(base_image, (new_width, new_height))


start_ticks = pygame.time.get_ticks()
paused_ticks = 0
paused_ticks_single = 0
waiting_for_input = False
start_waiting_for_input = False

Player_move = True
score_allowed = True
highscore_reset = False
obstacle_hard_color = False
Player_move_keyboard = True
music_stop = True
move_info = True
storm_info = True
Jungle_rain = False
collide_player = False
Lifebar_3_3 = True
Lifebar_2_3 = False
Lifebar_1_3 = False
Lifebar_0_3 = False

Timebar_5_5 = False
Timebar_4_5 = False
Timebar_3_5 = False
Timebar_2_5 = False
Timebar_1_5 = False
Timebar_0_5 = False

slow_time = False
spikes = False
Obstacles_allowed = True
smaller_gap = False
bigger_gap = False
first_hit = True
cooldown = False
normal_obstacle_spawn = True
Lifebar_time = 500
Lifebar_activation_time = True
Lifebar_timer_check = True
Lifebar_timer = 0
random_box_timer = random.randrange(25000, 40000, 1000)

#Normal_Background_Sound = pygame.mixer.Sound("Dragonrace Normal 2.0.mp3")
#Thunder_Background_Sound = pygame.mixer.Sound("Dragonrace Thunder 2.0.mp3")

Dragon_IMAGE_Scaled_allowed = True
Dragon_IMAGE_Scaled_Left_allowed = True
Dragon_IMAGE_Scaled_Right_allowed = True
prev_x = 0

# Dragon images
Dragon_IMAGE = pygame.image.load('ALPHA Toothless 10.0.png').convert_alpha()
if Player_Monitor == True:
  neue_breite = Dragon_IMAGE.get_width() / 5 * screen_width / 2120
  neue_hoehe = Dragon_IMAGE.get_height() / 5 * screen_width / 2120
else:
  neue_breite = Dragon_IMAGE.get_width() / 2 * screen_width / 2120
  neue_hoehe = Dragon_IMAGE.get_height() / 2 * screen_width / 2120
Dragon_IMAGE_Scaled = pygame.transform.scale(Dragon_IMAGE, (neue_breite, neue_hoehe))

Dragon_IMAGE_Left = pygame.image.load('ALPHA Toothless left 5.0.png').convert_alpha()
if Player_Monitor == True:
  neue_breite_links = Dragon_IMAGE_Left.get_width() / 5 * screen_width / 2120
  neue_hoehe_links = Dragon_IMAGE_Left.get_height() / 5 * screen_width / 2120
else:
  neue_breite_links = Dragon_IMAGE_Left.get_width() / 2 * screen_width / 2120
  neue_hoehe_links = Dragon_IMAGE_Left.get_height() / 2 * screen_width / 2120
Dragon_IMAGE_Scaled_Left = pygame.transform.scale(Dragon_IMAGE_Left, (neue_breite_links, neue_hoehe_links))

Dragon_IMAGE_Right = pygame.image.load('ALPHA Toothless right 5.0.png').convert_alpha()
if Player_Monitor == True:
  neue_breite_rechts = Dragon_IMAGE_Right.get_width() / 5 * screen_width / 2120
  neue_hoehe_rechts = Dragon_IMAGE_Right.get_height() / 5 * screen_width / 2120
else:
  neue_breite_rechts = Dragon_IMAGE_Right.get_width() / 2 * screen_width / 2120
  neue_hoehe_rechts = Dragon_IMAGE_Right.get_height() / 2 * screen_width / 2120
Dragon_IMAGE_Scaled_Right = pygame.transform.scale(Dragon_IMAGE_Right, (neue_breite_rechts, neue_hoehe_rechts))


# Dragon shadow images
Dragon_IMAGE_shadow = pygame.image.load('ALPHA Toothless shadow.png').convert_alpha()
if Player_Monitor == True:
  neue_breite_shadow = Dragon_IMAGE_shadow.get_width() / 20 * screen_width / 2120
  neue_hoehe_shadow = Dragon_IMAGE_shadow.get_height() / 20 * screen_width / 2120
else:
  neue_breite_shadow = Dragon_IMAGE_shadow.get_width() / 8 * screen_width / 2120
  neue_hoehe_shadow = Dragon_IMAGE_shadow.get_height() / 8 * screen_width / 2120
Dragon_IMAGE_Scaled_shadow = pygame.transform.scale(Dragon_IMAGE_shadow, (neue_breite_shadow, neue_hoehe_shadow))

Dragon_IMAGE_Left_shadow = pygame.image.load('ALPHA Toothless left shadow.png').convert_alpha()
if Player_Monitor == True:
  neue_breite_links_shadow = Dragon_IMAGE_Left_shadow.get_width() / 20 * screen_width / 2120
  neue_hoehe_links_shadow = Dragon_IMAGE_Left_shadow.get_height() / 20 * screen_width / 2120
else:
  neue_breite_links_shadow = Dragon_IMAGE_Left_shadow.get_width() / 8 * screen_width / 2120
  neue_hoehe_links_shadow = Dragon_IMAGE_Left_shadow.get_height() / 8 * screen_width / 2120
Dragon_IMAGE_Scaled_Left_shadow = pygame.transform.scale(Dragon_IMAGE_Left_shadow, (neue_breite_links_shadow, neue_hoehe_links_shadow))

Dragon_IMAGE_Right_shadow = pygame.image.load('ALPHA Toothless right shadow.png').convert_alpha()
if Player_Monitor == True:
  neue_breite_rechts_shadow = Dragon_IMAGE_Right_shadow.get_width() / 20 * screen_width / 2120
  neue_hoehe_rechts_shadow = Dragon_IMAGE_Right_shadow.get_height() / 20 * screen_width / 2120
else:
  neue_breite_rechts_shadow = Dragon_IMAGE_Right_shadow.get_width() / 8 * screen_width / 2120
  neue_hoehe_rechts_shadow = Dragon_IMAGE_Right_shadow.get_height() / 8 * screen_width / 2120
Dragon_IMAGE_Scaled_Right_shadow = pygame.transform.scale(Dragon_IMAGE_Right_shadow, (neue_breite_rechts_shadow, neue_hoehe_rechts_shadow))


# Jungle images
Jungle_IMAGE = pygame.image.load("HFW Dragonrace_Mobile.png").convert_alpha()
if Jungle_IMAGE_Monitor == True:
  neue_breite_Jungle = screen_width
  neue_hoehe_Jungle = screen_height
else:
  neue_breite_Jungle = screen_width * 4
  neue_hoehe_Jungle = screen_height
Jungle_IMAGE_Scaled = pygame.transform.scale(Jungle_IMAGE, (neue_breite_Jungle, neue_hoehe_Jungle))

Jungle_IMAGE_rain = pygame.image.load("HFW Dragonrace_Mobile_rain.png").convert_alpha()
if Jungle_IMAGE_Monitor == True:
  neue_breite_Jungle_rain = screen_width
  neue_hoehe_Jungle_rain = screen_height
else:
  neue_breite_Jungle_rain = screen_width * 4
  neue_hoehe_Jungle_rain = screen_height
Jungle_IMAGE_Scaled_rain = pygame.transform.scale(Jungle_IMAGE_rain, (neue_breite_Jungle_rain, neue_hoehe_Jungle_rain))


# Cloud images
Cloud_IMAGE = pygame.image.load("Dragonrace normal cloud 6.0.png").convert_alpha()
if Player_Monitor == True:
  neue_breite_Cloud = screen_width
  neue_hoehe_Cloud = screen_height
else:
  neue_breite_Cloud = screen_width
  neue_hoehe_Cloud = screen_height
Cloud_IMAGE_Scaled = pygame.transform.scale(Cloud_IMAGE, (neue_breite_Cloud, neue_hoehe_Cloud))

Red_Cloud_IMAGE = pygame.image.load("Dragonrace red cloud 6.0.png").convert_alpha()
if Player_Monitor == True:
  neue_breite_red_Cloud = screen_width
  neue_hoehe_red_Cloud = screen_height
else:
  neue_breite_red_Cloud = screen_width
  neue_hoehe_red_Cloud = screen_height
Red_Cloud_IMAGE_Scaled = pygame.transform.scale(Red_Cloud_IMAGE, (neue_breite_red_Cloud, neue_hoehe_red_Cloud))


# Lifebar images
Lifebar_3_3_IMAGE = pygame.image.load("Lifebar 3-3 8.0.png")
manual_scale = 0.099
Lifebar_3_3_IMAGE_Scaled = scale_image(Lifebar_3_3_IMAGE, base_resolution_image, current_resolution, manual_scale)

Lifebar_2_3_IMAGE = pygame.image.load("Lifebar 2-3 8.0.png")
manual_scale = 0.099
Lifebar_2_3_IMAGE_Scaled = scale_image(Lifebar_2_3_IMAGE, base_resolution_image, current_resolution, manual_scale)

Lifebar_1_3_IMAGE = pygame.image.load("Lifebar 1-3 8.0.png")
manual_scale = 0.099
Lifebar_1_3_IMAGE_Scaled = scale_image(Lifebar_1_3_IMAGE, base_resolution_image, current_resolution, manual_scale)

Lifebar_0_3_IMAGE = pygame.image.load("Lifebar 0-3 8.0.png")
manual_scale = 0.099
Lifebar_0_3_IMAGE_Scaled = scale_image(Lifebar_0_3_IMAGE, base_resolution_image, current_resolution, manual_scale)


# Timebar images
Timebar_5_5_IMAGE = pygame.image.load("Timebar_5-5.png")
manual_scale = 0.076
Timebar_5_5_IMAGE_Scaled = scale_image(Timebar_5_5_IMAGE, base_resolution_image, current_resolution, manual_scale)

Timebar_4_5_IMAGE = pygame.image.load("Timebar_4-5.png")
manual_scale = 0.076
Timebar_4_5_IMAGE_Scaled = scale_image(Timebar_4_5_IMAGE, base_resolution_image, current_resolution, manual_scale)

Timebar_3_5_IMAGE = pygame.image.load("Timebar_3-5.png")
manual_scale = 0.076
Timebar_3_5_IMAGE_Scaled = scale_image(Timebar_3_5_IMAGE, base_resolution_image, current_resolution, manual_scale)

Timebar_2_5_IMAGE = pygame.image.load("Timebar_2-5.png")
manual_scale = 0.076
Timebar_2_5_IMAGE_Scaled = scale_image(Timebar_2_5_IMAGE, base_resolution_image, current_resolution, manual_scale)

Timebar_1_5_IMAGE = pygame.image.load("Timebar_1-5_2.0.png")
manual_scale = 0.076
Timebar_1_5_IMAGE_Scaled = scale_image(Timebar_1_5_IMAGE, base_resolution_image, current_resolution, manual_scale)

Timebar_0_5_IMAGE = pygame.image.load("Timebar_0-5_2.0.png")
manual_scale = 0.076
Timebar_0_5_IMAGE_Scaled = scale_image(Timebar_0_5_IMAGE, base_resolution_image, current_resolution, manual_scale)


# Powerup images
Box_bigger_gap_IMAGE = pygame.image.load("Dragonrace_box_bigger_gap.png")
manual_scale = 1
Box_bigger_gap_IMAGE_Scaled = scale_image(Box_bigger_gap_IMAGE, base_resolution_image, current_resolution, manual_scale)

Box_life_IMAGE = pygame.image.load("Dragonrace_box_life.png")
manual_scale = 1
Box_life_IMAGE_Scaled = scale_image(Box_life_IMAGE, base_resolution_image, current_resolution, manual_scale)

Box_smaller_gap_IMAGE = pygame.image.load("Dragonrace_box_smaller_gap.png")
manual_scale = 1
Box_smaller_gap_IMAGE_Scaled = scale_image(Box_smaller_gap_IMAGE, base_resolution_image, current_resolution, manual_scale)

Box_slow_time_IMAGE = pygame.image.load("Dragonrace_box_slow_time.png")
manual_scale = 1
Box_slow_time_IMAGE_Scaled = scale_image(Box_slow_time_IMAGE, base_resolution_image, current_resolution, manual_scale)

Box_spikes_IMAGE = pygame.image.load("Dragonrace_box_spikes.png")
manual_scale = 1
Box_spikes_IMAGE_Scaled = scale_image(Box_spikes_IMAGE, base_resolution_image, current_resolution, manual_scale)

 
# Create an object to track the time
clock = pygame.time.Clock()

score_background = pygame.Rect(screen_width * 0.1667, screen_height * 0.025, screen_width * 0.6667, screen_height * 0.0625)
highscore_background = pygame.Rect(screen_width * 0.1481, screen_height * 0.5, screen_width * 0.7037, screen_height * 0.0833)
New_personal_best_background = pygame.Rect(screen_width * 0.0278, screen_height * 0.0938, screen_width * 0.9444, screen_height * 0.0563)
move_info_background = pygame.Rect(screen_width * 0.0278, screen_height * 0.0938 * 5.35, screen_width * 0.9444, screen_height * 0.0563)
storm_info_background = pygame.Rect(screen_width * 0.0278, screen_height * 0.0938 * 5.35 * 1.1, screen_width * 0.9444, screen_height * 0.0563)

if Player_Monitor == True:
  obstacle_spawn_time = 6000 # Spawns objects every 6 seconds at the start
else:
 obstacle_spawn_time = 6000  # Spawns objects every 6 seconds at the start
last_obstacle_spawn_time = 0

text_color = (255, 215, 0)
move_info_text_color = (0, 255, 0)
storm_info_text_color = (0, 255, 0)
if Player_Monitor == False:
    base_font_size_score = 75
    scaled_font_size_score = get_font_size(base_font_size_score, base_resolution, current_resolution)
    font_score = pygame.font.SysFont(None, scaled_font_size_score)
    
    base_font_size_highscore = 75
    scaled_font_size_highscore = get_font_size(base_font_size_highscore, base_resolution, current_resolution)
    font_highscore = pygame.font.SysFont(None, scaled_font_size_highscore)

    base_font_size_info = 60
    scaled_font_size_info = get_font_size(base_font_size_info, base_resolution, current_resolution)
    font_info = pygame.font.SysFont(None, scaled_font_size_info)
else:
    base_font_size_score = 75
    scaled_font_size_score = get_font_size(base_font_size_score, base_resolution, current_resolution)
    font_score = pygame.font.SysFont(None, scaled_font_size_score)
    
    base_font_size_highscore = 75
    scaled_font_size_highscore = get_font_size(base_font_size_highscore, base_resolution, current_resolution)
    font_highscore = pygame.font.SysFont(None, scaled_font_size_highscore)

    base_font_size_info = 60
    scaled_font_size_info = get_font_size(base_font_size_info, base_resolution, current_resolution)
    font_info = pygame.font.SysFont(None, scaled_font_size_info)   

obstacle_speed = screen_height * 0.00167

player_x_spawn = screen_width / 2 - screen_width * 0.4259 / 2.5 * 0.95 / 0.75
player_y_spawn = screen_height * 0.75

start_box_timer = 0
box_claimed_timer = float("inf")
all_boxes_size = int(manual_scale * 90)
# Powerup classes
class Life_box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randrange(0, screen_width - all_boxes_size)
        self.y = -all_boxes_size
        self.size = all_boxes_size
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.speed = obstacle_speed * 4
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 0.35
        self.image = Box_life_IMAGE_Scaled
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Scale image

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Check for collision with the left or right wall
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.size:
            self.direction_x *= -1
            
        if self.rect.top > screen_height:
            self.kill()
            
    def Life_box_pause(self):
      self.speed = 0

           
        
class Bigger_gap_box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randrange(0, screen_width - all_boxes_size)
        self.y = -all_boxes_size
        self.size = all_boxes_size
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.speed = obstacle_speed * 4
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 0.35
        self.image = Box_bigger_gap_IMAGE_Scaled
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Scale image

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Check for collision with the left or right wall
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.size:
            self.direction_x *= -1
            
        if self.rect.top > screen_height:
            self.kill()

    def Bigger_gap_box_pause(self):
        self.speed = 0

        

class Smaller_gap_box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randrange(0, screen_width - all_boxes_size)
        self.y = -all_boxes_size
        self.size = all_boxes_size
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.speed = obstacle_speed * 4
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 0.35
        self.image = Box_smaller_gap_IMAGE_Scaled
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Scale image

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Check for collision with the left or right wall
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.size:
            self.direction_x *= -1
            
        if self.rect.top > screen_height:
            self.kill()

    def Smaller_gap_box_pause(self):
        self.speed = 0

        

class Slow_time_box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randrange(0, screen_width - all_boxes_size)
        self.y = -all_boxes_size
        self.size = all_boxes_size
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.speed = obstacle_speed * 4
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 0.35
        self.image = Box_slow_time_IMAGE_Scaled
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Scale image

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Check for collision with the left or right wall
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.size:
            self.direction_x *= -1
            
        if self.rect.top > screen_height:
            self.kill()

    def Slow_time_box_pause(self):
        self.speed = 0

        

class Spikes_box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randrange(0, screen_width - all_boxes_size)
        self.y = -all_boxes_size
        self.size = all_boxes_size
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.speed = obstacle_speed * 4
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 0.35
        self.image = Box_spikes_IMAGE_Scaled
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Scale image

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Check for collision with the left or right wall
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.size:
            self.direction_x *= -1
            
        if self.rect.top > screen_height:
            self.kill()

    def Spikes_box_pause(self):
        self.speed = 0


  
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        if Player_Monitor == True:
          self.image = pygame.Surface((screen_width * 0.4259 / 2.5 * 0.95, screen_height * 0.05 * 1.3))
          self.rect = Rect(player_x_spawn, player_y_spawn, screen_width * 0.4259 / 2.5 * 0.95, screen_height * 0.05 * 1.3)  
        else:
          self.image = pygame.Surface((screen_width * 0.4259 * 0.95, screen_height * 0.05 * 1.3))
          self.rect = Rect(player_x_spawn, player_y_spawn, screen_width * 0.4259 * 0.95, screen_height * 0.05 * 1.3)
        self.image.fill(255)
        self.dragging = False
        
    def moveRight(self, speed):
        self.rect.x += speed * speed/10
 
    def moveLeft(self, speed):
        self.rect.x -= speed * speed/10
 
    def moveForward(self, speed):
        self.rect.y += speed * speed/10
 
    def moveBack(self, speed):
        self.rect.y -= speed * speed/10
    
    def update(self, pos):
        if self.dragging:
          mouse_x, mouse_y = pos
          self.rect.x = mouse_x + self.offset_x
          self.rect.y = mouse_y + self.offset_y 

    def clamp_ip(self, rect):
        self.rect.clamp_ip(rect)
        
    def player_spawn(self, player_x_spawn, player_y_spawn):
        self.rect.x = player_x_spawn
        self.rect.y = player_y_spawn

Player = player()   

class Obstacle_Left(pygame.sprite.Sprite):
    def __init__(self, width_obstacle_left):
        super().__init__() 
        self.rect = Rect(0, -screen_height * 0.0833, width_obstacle_left - screen_width * 0.4259 / 2.5 * 0.05, screen_height * 0.0833) 
        if obstacle_hard_color == False:
          self.image = Cloud_IMAGE_Scaled
          self.image = pygame.transform.scale(self.image, (width_obstacle_left, screen_height * 0.0833))  # Scale image
        else:
          self.image = Red_Cloud_IMAGE_Scaled
          self.image = pygame.transform.scale(self.image, (width_obstacle_left, screen_height * 0.0833))  # Scale image
        
    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.top > screen_height:
            self.kill()
            
    def obstacle_left_kill(self):
        self.kill()


class Obstacle_Right(pygame.sprite.Sprite):
    def __init__(self, width_obstacle_right):
        super().__init__()
        width_obstacle_right_spawn = screen_width - width_obstacle_right
        self.rect = Rect((width_obstacle_right_spawn, -screen_height * 0.0833, width_obstacle_right, screen_height * 0.0833)) 
        if obstacle_hard_color == False:
          self.image = Cloud_IMAGE_Scaled
          self.image = pygame.transform.scale(self.image, (width_obstacle_right, screen_height * 0.0833))  # Scale image
        else:
          self.image = Red_Cloud_IMAGE_Scaled
          self.image = pygame.transform.scale(self.image, (width_obstacle_right, screen_height * 0.0833))  # Scale image

    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.top > screen_height:
            self.kill()
            
    def obstacle_right_kill(self):
        self.kill()


life_box_group = pygame.sprite.Group()
smaller_gap_box_group = pygame.sprite.Group()
bigger_gap_box_group = pygame.sprite.Group()
slow_time_box_group = pygame.sprite.Group()
spikes_box_group = pygame.sprite.Group()
        
all_sprites = pygame.sprite.Group(Player)
Obstacles = pygame.sprite.Group()
obstacles_left = pygame.sprite.Group()
obstacles_right = pygame.sprite.Group()

color_button_restart = (100,255,255)   
# Light shade of the button 
color_button_restart_light = (170,170,170)   
# Dark shade of the button 
color_button_restart_dark = (100,100,100) 

# Position of the buttons
width_button_restart = screen_width * 0.4444 
height_button_restart = screen_height * 0.6667
 
if Player_Monitor == False:
  base_font_size_restart_text = 75
  scaled_font_size_restart_text = get_font_size(base_font_size_restart_text, base_resolution, current_resolution)
  font_restart_text = pygame.font.SysFont(None, scaled_font_size_restart_text)
else:
  base_font_size_restart_text = 75
  scaled_font_size_restart_text = get_font_size(base_font_size_restart_text, base_resolution, current_resolution)
  font_restart_text = pygame.font.SysFont(None, scaled_font_size_restart_text)
restart_text = font_restart_text.render('Restart', True, color_button_restart) 

#waiting_for_input = True
#while waiting_for_input:  # With that the game on the website does not load before you interact with it
#    for event in pygame.event.get():
#        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP: 
#            start_ticks = pygame.time.get_ticks()
#            last_obstacle_spawn_time = pygame.time.get_ticks()
#            waiting_for_input = False
#    if pygame.time.get_ticks() > 5000: 
#        start_ticks = pygame.time.get_ticks()
#        last_obstacle_spawn_time = pygame.time.get_ticks()
#        waiting_for_input = False
            
run = True
            
#pygame.mixer.music.load("Dragonrace Normal 2.0.mp3")
#pygame.mixer.music.play(-1)

async def main():
    global run
    global score_allowed
    global start_ticks
    global Player_Monitor
    global Obstacle_Monitor
    global Jungle_IMAGE_Monitor
    global Player_move
    global highscore_reset
    global last_obstacle_spawn_time
    global obstacle_spawn_time
    global obstacle_speed
    global obstacle_hard_color
    global Player_move_keyboard
    global Dragon_IMAGE_Scaled_allowed
    global Dragon_IMAGE_Scaled_Left_allowed
    global Dragon_IMAGE_Scaled_Right_allowed
    global prev_x
    global Normal_Background_Sound
    global Thunder_Background_Sound
    global music_stop
    global move_info
    global storm_info
    global Jungle_rain
    global collide_player
    global Lifebar_3_3
    global Lifebar_2_3
    global Lifebar_1_3
    global Lifebar_0_3
    global Timebar_5_5
    global Timebar_4_5
    global Timebar_3_5
    global Timebar_2_5
    global Timebar_1_5
    global Timebar_0_5
    global first_hit
    global Lifebar_activation_time
    global Lifebar_timer
    global Lifebar_timer_check
    global Lifebar_time
    global cooldow
    global start_box_timer
    global box_claimed_timer
    global slow_time
    global normal_obstacle_spawn
    global spikes
    global Obstacles_allowed
    global random_box_timer
    global smaller_gap
    global bigger_gap
    global waiting_for_input
    global paused_ticks
    global paused_ticks_single
    global start_waiting_for_input

    # Creating an infinite loop to run the game
    while run:
   
        #if 2000 < pygame.time.get_ticks() - start_ticks < 2100:
        #   waiting_for_input = True    
        #if 8000 < pygame.time.get_ticks() - start_ticks < 8100:
        #   waiting_for_input = True         
        #if 14000 < pygame.time.get_ticks() - start_ticks < 14100:
        #   waiting_for_input = True

        #if waiting_for_input:
        #   pause_start = pygame.time.get_ticks()
        #   pygame.mixer_music.pause()
        #   start_waiting_for_input = True
        #else:
        #   if start_waiting_for_input == True:
        #     pygame.mixer_music.unpause()
        #     start_waiting_for_input = False
        #while waiting_for_input:  # With that the game on the website does not load before you interact with it
        #    for event in pygame.event.get():
        #        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP: 
        #            paused_ticks = pygame.time.get_ticks() - pause_start + paused_ticks # Takes the ammount of pause time
        #            start_box_timer = start_box_timer + paused_ticks
        #            paused_ticks_single = pygame.time.get_ticks() - pause_start
        #           last_obstacle_spawn_time = last_obstacle_spawn_time + paused_ticks_single
        #            waiting_for_input = False
        #print("After_waiting_for_input")
        
        if score_allowed == True:
          score = (pygame.time.get_ticks() - start_ticks - paused_ticks) // 1000    
          
        if pygame.time.get_ticks() - last_obstacle_spawn_time > obstacle_spawn_time:
            # If 150 score is reached the area to fly through gets smaller
            if score <= 150:
                if normal_obstacle_spawn == True:
                    if Obstacle_Monitor == True:
                      width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                      width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
    
                      while width_obstacle_left + width_obstacle_right > screen_width * 0.5370 * 1.5 - screen_width * 0.4259 / 2.5 * 0.05:
                        width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                        width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                    else:
                      width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
                      width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
    
                      while width_obstacle_left + width_obstacle_right > screen_width * 0.5370 - screen_width * 0.4259 / 2.5 * 0.05:
                        width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
                        width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
            else:
                Jungle_rain = True
                if music_stop == True:
                  #pygame.mixer.music.stop()
                  #pygame.mixer.music.load("Dragonrace Thunder 2.0.mp3")
                  #pygame.mixer.music.play(-1)
                  music_stop = False
                obstacle_hard_color = True
                if normal_obstacle_spawn == True:
                    if Obstacle_Monitor == True:
                      width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                      width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
    
                      while not screen_width * 0.5370 * 1.2 - screen_width * 0.4259 / 2.5 * 0.05 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 * 1.5 - screen_width * 0.4259 / 2.5 * 0.05:
                        width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                        width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                    else:
                      width_obstacle_left = random.randrange(int(screen_width * 0.0370) , int(screen_width * 0.5370))
                      width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
    
                      while not screen_width * 0.5370 * 0.7 - screen_width * 0.4259 / 2.5 * 0.05 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 - screen_width * 0.4259 / 2.5 * 0.05:
                        width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
                        width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
           
            obstacle_left = Obstacle_Left(width_obstacle_left)
            obstacle_right = Obstacle_Right(width_obstacle_right)
            Obstacles.add(obstacle_left, obstacle_right)
            obstacles_left.add(obstacle_left)
            obstacles_right.add(obstacle_right)
            
            #print("New_obstacle_loaded")
            
            if Player_Monitor == True:
              obstacle_spawn_time = obstacle_spawn_time - 140 # Objects spawn faster after spawning
            else:
              obstacle_spawn_time = obstacle_spawn_time - 140 # Objects spawn faster after spawning
            if Player_Monitor == True:
              obstacle_speed = obstacle_speed + screen_height * 0.00001667 * 5 * 1.5 # Objects get faster after spawning
            else:
              obstacle_speed = obstacle_speed + screen_height * 0.00001667 * 5 * 1.5 # Objects get faster after spawning
            last_obstacle_spawn_time = pygame.time.get_ticks()
            
            if slow_time == False:
                if Player_Monitor == True:
                  if obstacle_spawn_time < 800: # Limits the spawn speed on 0.8 seconds
                    obstacle_spawn_time = 800
                else:
                  if obstacle_spawn_time < 800: # Limits the spawn speed on 0.8 seconds
                    obstacle_spawn_time = 800
       
                if obstacle_speed > screen_height * 0.005 * 1.5: # Limits the speed
                  obstacle_speed = screen_height * 0.005 * 1.5      
            else:
                if Player_Monitor == True:
                  if obstacle_spawn_time < 1600: # Limits the spawn speed on 1.6 seconds
                    obstacle_spawn_time = 1600
                else:
                  if obstacle_spawn_time < 1600: # Limits the spawn speed on 1.6 seconds
                    obstacle_spawn_time = 1600
       
                if obstacle_speed > screen_height * 0.005 * 1.5 / 2: # Limits the speed
                  obstacle_speed = screen_height * 0.005 * 1.5 / 2  
        
        # Set FPS to 60
        clock.tick(60)
      
        # Read the previous high score from the file
        try:
            with open('highscore.txt', 'r') as f:
                highscore = int(f.read())
        except FileNotFoundError:
            highscore = 0

        # Compare the current score with the high score
        if score > highscore:
            # Update the high score when the current score is higher
            with open('highscore.txt', 'w') as f:
                f.write(str(score))
            
        if highscore_reset == True:
          with open('highscore.txt', 'w') as f:
            f.write(str(0))
            highscore_reset = False
    

        score_text = font_score.render("Score:" + str(score), True, text_color)
        New_personal_best_text = font_score.render("New personal best!", True, text_color)
        move_info_text = font_info.render("Move with WASD, mouse or finger.", True, move_info_text_color)
        storm_info_text = font_info.render("A storm is coming, dodge the clouds!", True, storm_info_text_color)

        if Jungle_rain == True:
           screen.blit(Jungle_IMAGE_Scaled_rain, (0,0))
        else:
           screen.blit(Jungle_IMAGE_Scaled, (0,0)) 

        if Dragon_IMAGE_Scaled_allowed == True:
          screen.blit(Dragon_IMAGE_Scaled_shadow, Player.rect.bottomright)
        if Dragon_IMAGE_Scaled_Left_allowed == True:
          screen.blit(Dragon_IMAGE_Scaled_Left_shadow, Player.rect.bottomright)
        if Dragon_IMAGE_Scaled_Right_allowed == True:
          screen.blit(Dragon_IMAGE_Scaled_Right_shadow, Player.rect.bottomright)
 
        if Dragon_IMAGE_Scaled_allowed == True:
          screen.blit(Dragon_IMAGE_Scaled, Player.rect.topleft)
        if Dragon_IMAGE_Scaled_Left_allowed == True:
          screen.blit(Dragon_IMAGE_Scaled_Left, Player.rect.topleft)
        if Dragon_IMAGE_Scaled_Right_allowed == True:
          screen.blit(Dragon_IMAGE_Scaled_Right, Player.rect.topleft)
         
          
        #all_sprites.update()
        all_sprites.add(Player)
        #all_sprites.draw(screen)
        if Obstacles_allowed == True:
          Obstacles.draw(screen)
        else:
          obstacles_left.draw(screen)
          obstacles_right.draw(screen)
        
        if start_box_timer == 0:
          start_box_timer = pygame.time.get_ticks()


        life_box = Life_box()
        smaller_gap_box = Smaller_gap_box()
        bigger_gap_box = Bigger_gap_box()
        slow_time_box = Slow_time_box()
        spikes_box = Spikes_box()

        #random_box_timer = random.randrange(500, 1000, 500)
        if pygame.time.get_ticks() - start_box_timer  > random_box_timer:
           #print(random_box_timer)
           #print(pygame.time.get_ticks() - start_box_timer)
           random_box_timer = random.randrange(25000, 40000, 1000)
           start_box_timer = pygame.time.get_ticks()
           random_box = random.randint(1,5)
           if random_box == 1:
             life_box_group.add(life_box)
           if random_box == 2:
             slow_time_box_group.add(slow_time_box)
           if random_box == 3:
             bigger_gap_box_group.add(bigger_gap_box)
           if random_box == 4:
             smaller_gap_box_group.add(smaller_gap_box)
           if random_box == 5:
             spikes_box_group.add(spikes_box)

        pygame.draw.rect(screen, (170, 169, 173), score_background)
    
        screen.blit(score_text, (screen_width * 0.2315, screen_height * 0.0375))
        if score >= highscore:
          pygame.draw.rect(screen, (170, 169, 173), New_personal_best_background)
          screen.blit(New_personal_best_text, (screen_width * 0.0463, screen_height * 0.1021))
          
        if pygame.time.get_ticks() - start_ticks > 7000:
          move_info = False
          storm_info = False
        
        if move_info == True and storm_info == True:
          pygame.draw.rect(screen, (170, 169, 173), move_info_background)
          screen.blit(move_info_text, (screen_width * 0.0463, screen_height * 0.1021 * 5))    
          pygame.draw.rect(screen, (170, 169, 173), storm_info_background)
          screen.blit(storm_info_text, (screen_width * 0.0463, screen_height * 0.1021 * 5.5))  
        
        if Lifebar_3_3 == True:
            screen.blit(Lifebar_3_3_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Lifebar_3_3_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 1.5))

        if Lifebar_2_3 == True:
            screen.blit(Lifebar_2_3_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Lifebar_2_3_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 1.5))

        if Lifebar_1_3 == True:
            screen.blit(Lifebar_1_3_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Lifebar_1_3_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 1.5))

        if Lifebar_0_3 == True:
            screen.blit(Lifebar_0_3_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Lifebar_0_3_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 1.5))
          

        if Timebar_5_5 == True:
            screen.blit(Timebar_5_5_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Timebar_5_5_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 2 * 1.9))

        if Timebar_4_5 == True:
            screen.blit(Timebar_4_5_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Timebar_4_5_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 2 * 1.9))
          
        if Timebar_3_5 == True:
            screen.blit(Timebar_3_5_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Timebar_3_5_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 2 * 1.9))
      
        if Timebar_2_5 == True:
            screen.blit(Timebar_2_5_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Timebar_2_5_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 2 * 1.9))
          
        if Timebar_1_5 == True:
            screen.blit(Timebar_1_5_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Timebar_1_5_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 2 * 1.9))

        if Timebar_0_5 == True:
            screen.blit(Timebar_0_5_IMAGE_Scaled, (screen_width * 0.1667 + screen_width * 0.6667 - Timebar_0_5_IMAGE_Scaled.get_width(), screen_height * 0.01667 * 2 * 1.9))
              

        if Lifebar_timer_check == True:  # If 550 milliseconds have past the game allows a player hit
          if pygame.time.get_ticks() - Lifebar_timer > 550:
            Lifebar_timer = pygame.time.get_ticks()
            first_hit = True
            cooldown = True
            Lifebar_activation_time = True

        if Obstacles_allowed == True:
          Obstacles.update()
        else:
          obstacles_left.update()
          obstacles_right.update()

        
        # Powerup effects
        for life_box in life_box_group:
            if pygame.sprite.collide_rect(Player, life_box):
               #print("Life_collision_start")
               #item_equip = pygame.mixer.Sound("item equip.mp3")
               #item_equip.set_volume(0.3)
               #print("Life_sound_loaded")
               #item_equip.play()
               #print("Life_sound_played")
               life_box_group.remove(life_box)
               #print("Life_box_from_group_removed")
               if Lifebar_3_3 == False and Lifebar_2_3 == True and Lifebar_1_3 == False and Lifebar_0_3 == False:
                 Lifebar_3_3 = True
                 Lifebar_2_3 = False
                 Lifebar_1_3 = False
                 Lifebar_0_3 = False
                 
               if Lifebar_3_3 == False and Lifebar_2_3 == False and Lifebar_1_3 == True and Lifebar_0_3 == False:
                 Lifebar_3_3 = False
                 Lifebar_2_3 = True
                 Lifebar_1_3 = False
                 Lifebar_0_3 = False
         
        for smaller_gap_box in smaller_gap_box_group:
            if pygame.sprite.collide_rect(Player, smaller_gap_box):
               #item_equip = pygame.mixer.Sound("item equip.mp3")
               #item_equip.set_volume(0.3)
               #item_equip.play()
               smaller_gap_box_group.remove(smaller_gap_box)
               box_claimed_timer = pygame.time.get_ticks()
               normal_obstacle_spawn = False
               smaller_gap = True
        if normal_obstacle_spawn == False and smaller_gap == True:
           if Obstacle_Monitor == True:
             width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
             width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
    
             while not screen_width * 0.5370 * 1.4 - screen_width * 0.4259 / 2.5 * 0.05 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 * 1.5 - screen_width * 0.4259 / 2.5 * 0.05:
               width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
               width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
           else:
             width_obstacle_left = random.randrange(int(screen_width * 0.0370) , int(screen_width * 0.5370))
             width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
    
             while not screen_width * 0.5370 * 0.9 - screen_width * 0.4259 / 2.5 * 0.05 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 - screen_width * 0.4259 / 2.5 * 0.05:
               width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
               width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
         
        for bigger_gap_box in bigger_gap_box_group:
            if pygame.sprite.collide_rect(Player, bigger_gap_box):
               #item_equip = pygame.mixer.Sound("item equip.mp3")
               #item_equip.set_volume(0.3)
               #item_equip.play()
               bigger_gap_box_group.remove(bigger_gap_box)
               box_claimed_timer = pygame.time.get_ticks()
               normal_obstacle_spawn = False
               bigger_gap = True
        if normal_obstacle_spawn == False and bigger_gap == True:
           if Obstacle_Monitor == True:
             width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
             width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
    
             while not screen_width * 0.5370 * 0.4 - screen_width * 0.4259 / 2.5 * 0.05 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 * 0.75 - screen_width * 0.4259 / 2.5 * 0.05:
               width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
               width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
           else:
             width_obstacle_left = random.randrange(int(screen_width * 0.0370) , int(screen_width * 0.5370))
             width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
    
             while not screen_width * 0.5370 * 0.2 - screen_width * 0.4259 / 2.5 * 0.05 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 * 0.5 - screen_width * 0.4259 / 2.5 * 0.05:
               width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
               width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
         
        for slow_time_box in slow_time_box_group:
            if pygame.sprite.collide_rect(Player, slow_time_box):
               #item_equip = pygame.mixer.Sound("item equip.mp3")
               #item_equip.set_volume(0.3)
               #item_equip.play()
               slow_time_box_group.remove(slow_time_box)
               box_claimed_timer = pygame.time.get_ticks()
               slow_time = True
               obstacle_speed = obstacle_speed / 2
               obstacle_spawn_time = obstacle_spawn_time * 2
           
        for spikes_box in spikes_box_group:
            if pygame.sprite.collide_rect(Player, spikes_box):
               #item_equip = pygame.mixer.Sound("item equip.mp3")
               #item_equip.set_volume(0.3)
               #item_equip.play()
               spikes_box_group.remove(spikes_box)
               box_claimed_timer = pygame.time.get_ticks()
               spikes = True
               Obstacles_allowed = False
        if spikes == True:
          for obstacle_left in obstacles_left: 
           if pygame.sprite.collide_rect(Player, obstacle_left):
             obstacle_left.obstacle_left_kill() 
           
          for obstacle_right in obstacles_right:
           if pygame.sprite.collide_rect(Player, obstacle_right):
             obstacle_right.obstacle_right_kill() 
         
        #print("Life_box_finished")
        life_box_group.update()
        #print("Life_box_group_update")
        life_box_group.draw(screen)
        #print("Life_box_group_draw")
        smaller_gap_box_group.update()
        smaller_gap_box_group.draw(screen)
        bigger_gap_box_group.update()
        bigger_gap_box_group.draw(screen)
        slow_time_box_group.update()
        slow_time_box_group.draw(screen)
        spikes_box_group.update()
        spikes_box_group.draw(screen)


        if pygame.time.get_ticks() - box_claimed_timer > 0:
           Timebar_5_5 = True
           Timebar_4_5 = False
           Timebar_3_5 = False
           Timebar_2_5 = False
           Timebar_1_5 = False
           Timebar_0_5 = False
        if pygame.time.get_ticks() - box_claimed_timer > 3000:
           Timebar_5_5 = False
           Timebar_4_5 = True
           Timebar_3_5 = False
           Timebar_2_5 = False
           Timebar_1_5 = False
           Timebar_0_5 = False
        if pygame.time.get_ticks() - box_claimed_timer > 6000:
           Timebar_5_5 = False
           Timebar_4_5 = False
           Timebar_3_5 = True
           Timebar_2_5 = False
           Timebar_1_5 = False
           Timebar_0_5 = False
        if pygame.time.get_ticks() - box_claimed_timer > 9000:
           Timebar_5_5 = False
           Timebar_4_5 = False
           Timebar_3_5 = False
           Timebar_2_5 = True
           Timebar_1_5 = False
           Timebar_0_5 = False
        if pygame.time.get_ticks() - box_claimed_timer > 12000:
           Timebar_5_5 = False
           Timebar_4_5 = False
           Timebar_3_5 = False
           Timebar_2_5 = False
           Timebar_1_5 = True
           Timebar_0_5 = False
        if pygame.time.get_ticks() - box_claimed_timer > 15000:
           Timebar_5_5 = False
           Timebar_4_5 = False
           Timebar_3_5 = False
           Timebar_2_5 = False
           Timebar_1_5 = False
           Timebar_0_5 = False
           box_claimed_timer = float("inf")
           if slow_time == True:
             obstacle_speed = obstacle_speed * 2
             obstacle_spawn_time = obstacle_spawn_time / 2
             slow_time = False
             for obstacle in Obstacles:
                for obstacle in obstacles_left:
                    obstacle.obstacle_left_kill()
                for obstacle in obstacles_right:
                    obstacle.obstacle_right_kill()                
           if normal_obstacle_spawn == False:
             normal_obstacle_spawn = True
             smaller_gap = False
             bigger_gap = False
           if spikes == True:
             spikes = False
             Obstacles_allowed = True


        if spikes == False:
            for obstacle in Obstacles:
                # If the player encounters with the obstacle and they have 0 lifes the game is paused
                if pygame.sprite.collide_rect(Player, obstacle):
                  if Lifebar_activation_time == True:
                    collide_player = True
                  if collide_player == True and Lifebar_activation_time == True:
                    Lifebar_timer_check = True
                    Lifebar_timer = pygame.time.get_ticks()
                    if first_hit == True and cooldown == True:
                      Lifebar_time = 0
                      first_hit = False
                      cooldown = False
                    else:
                      Lifebar_time = 500
                      first_hit = False
                    Lifebar_activation_time = False
                    collide_player = False
                
                  if pygame.time.get_ticks() - Lifebar_timer > Lifebar_time and Lifebar_3_3 == True and Lifebar_2_3 == False and Lifebar_1_3 == False and Lifebar_0_3 == False:
                     Lifebar_3_3 = False
                     Lifebar_2_3 = True
                     Lifebar_1_3 = False
                     Lifebar_0_3 = False
                     Lifebar_activation_time = True
                     Lifebar_timer = float("inf")
                     first_hit = False
                     Lifebar_time = 500
                 
                  if pygame.time.get_ticks() - Lifebar_timer > Lifebar_time and Lifebar_3_3 == False and Lifebar_2_3 == True and Lifebar_1_3 == False and Lifebar_0_3 == False:
                     Lifebar_3_3 = False
                     Lifebar_2_3 = False
                     Lifebar_1_3 = True
                     Lifebar_0_3 = False
                     Lifebar_activation_time = True
                     Lifebar_timer = float("inf")
                     first_hit = False
                     Lifebar_time = 500
                 
                  if pygame.time.get_ticks() - Lifebar_timer > Lifebar_time and Lifebar_3_3 == False and Lifebar_2_3 == False and Lifebar_1_3 == True and Lifebar_0_3 == False:
                     Lifebar_3_3 = False
                     Lifebar_2_3 = False
                     Lifebar_1_3 = False
                     Lifebar_0_3 = True
                     collide_player = True

                 
                  if collide_player == True:
                      box_claimed_timer = float("inf")

                      for life_box in life_box_group:
                          life_box.Life_box_pause()
                      for smaller_gap_box in smaller_gap_box_group:
                          smaller_gap_box.Smaller_gap_box_pause()
                      for bigger_gap_box in bigger_gap_box_group:
                          bigger_gap_box.Bigger_gap_box_pause()
                      for slow_time_box in slow_time_box_group:
                          slow_time_box.Slow_time_box_pause()
                      for spikes_box in spikes_box_group:
                          spikes_box.Spikes_box_pause()
                  
                      Lifebar_activation_time = False
                      Lifebar_timer_check = False
                      score_allowed = False
                      Player_move = False
                      obstacle_speed = 0
                      obstacle_spawn_time = float('inf')
                      #pygame.mixer.music.stop()
              
                      # Stores the (x,y) coordinates into the variable as a tuple 
                      mouse = pygame.mouse.get_pos() 
                      # Checks if a mouse is clicked 
                      for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP: 
                
                          # If the mouse is clicked on the restart button the game is restarted 
                          if width_button_restart/2 <= mouse[0] <= width_button_restart/2+screen_width * 0.5556 and height_button_restart/2 <= mouse[1] <= height_button_restart/2+screen_height * 0.0833: 
                            for obstacle in obstacles_left:
                              obstacle.obstacle_left_kill()
                            for obstacle in obstacles_right:
                              obstacle.obstacle_right_kill()
                            Player.player_spawn(screen_width / 2 - screen_width * 0.4259 / 2.5 * 0.95 / 0.75, screen_height * 0.75)
                            #pygame.mixer.music.load("Dragonrace Normal 2.0.mp3")
                            #pygame.mixer.music.play(-1)
                            music_stop = True
                            score_allowed = True
                            Player_move = True
                            Jungle_rain = False
                            obstacle_hard_color = False
                            Lifebar_3_3 = True
                            Lifebar_2_3 = False
                            Lifebar_1_3 = False
                            Lifebar_0_3 = False
                        
                            Timebar_5_5 = False
                            Timebar_4_5 = False
                            Timebar_3_5 = False
                            Timebar_2_5 = False
                            Timebar_1_5 = False
                            Timebar_0_5 = False

                            slow_time = False
                            normal_obstacle_spawn = True
                            spikes = False
                            smaller_gap = False
                            bigger_gap = False
                            Obstacles_allowed = True
                            Lifebar_timer_check = True
                            first_hit = True
                            cooldown = False
                            waiting_for_input = False
                            start_waiting_for_input = False
                        
                            life_box_group.empty()
                            smaller_gap_box_group.empty()
                            bigger_gap_box_group.empty()
                            slow_time_box_group.empty()
                            spikes_box_group.empty()

                            paused_ticks = 0
                            paused_ticks_single = 0
                            random_box_timer = random.randrange(25000, 40000, 1000)
                            Lifebar_time = 0
                            Lifebar_activation_time = True
                            start_ticks = pygame.time.get_ticks()
                            start_box_timer = 0
                            last_obstacle_spawn_time = pygame.time.get_ticks()
                            obstacle_speed = screen_height * 0.00167
                            if Player_Monitor == True:
                              obstacle_spawn_time = 6000 # Spawns objects every 6 seconds
                            else:
                              obstacle_spawn_time = 6000  # Spawns objects every 6 seconds
                            # Reset dragging state for all sprites
                            for sprite in all_sprites:
                                sprite.dragging = False
                            Player_move_keyboard = True
                      
         
                      # If mouse is hovered on the restart button it changes to lighter shade  
                      if width_button_restart/2 <= mouse[0] <= width_button_restart/2+screen_width * 0.5556 and height_button_restart/2 <= mouse[1] <= height_button_restart/2+screen_height * 0.0833: 
                        pygame.draw.rect(screen,color_button_restart_light,[width_button_restart/2,height_button_restart/2,screen_width * 0.5556,screen_height * 0.0833]) 
          
                      else: 
                        pygame.draw.rect(screen,color_button_restart_dark,[width_button_restart/2,height_button_restart/2,screen_width * 0.5556,screen_height * 0.0833]) 
      
                      # Superimposing the restart text onto the button 
                      screen.blit(restart_text , (width_button_restart/2+screen_width * 0.0694,height_button_restart/2+screen_height * 0.0208))
          
                      pygame.draw.rect(screen, (51, 2, 209), highscore_background)

                      highscore_text = font_highscore.render("Highscore:" + str(highscore), True, text_color) 
                      screen.blit(highscore_text, (screen_width * 0.1759, screen_height * 0.5208))
              

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False   
            if Player_move:
                if event.type == pygame.MOUSEBUTTONDOWN:  # Changes the positon of the player with the mouse
                    for sprite in all_sprites:
                        if sprite.rect.collidepoint(event.pos):
                            sprite.dragging = True
                            mouse_x, mouse_y = event.pos
                            sprite.offset_x = sprite.rect.x - mouse_x
                            sprite.offset_y = sprite.rect.y - mouse_y
                            Player_move_keyboard = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    for sprite in all_sprites:
                        sprite.dragging = False
                        Player_move_keyboard = True
                elif event.type == pygame.MOUSEMOTION:
                    for sprite in all_sprites:
                        if sprite.dragging:
                            sprite.rect.x = event.pos[0] + sprite.offset_x
                            sprite.rect.y = event.pos[1] + sprite.offset_y

        # Looks if the player is moving left or right
        current_x = Player.rect.x
        if current_x < prev_x - screen_width * 0.00463:  # Moves left
            Dragon_IMAGE_Scaled_allowed = False
            Dragon_IMAGE_Scaled_Left_allowed = True
            Dragon_IMAGE_Scaled_Right_allowed = False
        elif current_x > prev_x + screen_width * 0.00463:  # Moves right
            Dragon_IMAGE_Scaled_allowed = False
            Dragon_IMAGE_Scaled_Left_allowed = False
            Dragon_IMAGE_Scaled_Right_allowed = True
        elif current_x == prev_x:
            Dragon_IMAGE_Scaled_allowed = True
            Dragon_IMAGE_Scaled_Left_allowed = False
            Dragon_IMAGE_Scaled_Right_allowed = False            
    
        # Update the previous position
        prev_x = current_x
        Player.clamp_ip(screen.get_rect())

                        
        if Player_move == True:
          if Player_move_keyboard == True:
            key = pygame.key.get_pressed()
            
            if key[pygame.K_a] == False:
              Dragon_IMAGE_Scaled_Left_allowed = False
              Dragon_IMAGE_Scaled_allowed = True
            if key[pygame.K_d] == False:
              Dragon_IMAGE_Scaled_Right_allowed = False
              Dragon_IMAGE_Scaled_allowed = True


            if key[pygame.K_a] == True:
              Dragon_IMAGE_Scaled_allowed = False
              Dragon_IMAGE_Scaled_Left_allowed = True
              Dragon_IMAGE_Scaled_Right_allowed = False
              Player.moveLeft(screen_height * 0.0074 * 1.5)
            if key[pygame.K_d] == True:
              Dragon_IMAGE_Scaled_allowed = False
              Dragon_IMAGE_Scaled_Left_allowed = False
              Dragon_IMAGE_Scaled_Right_allowed = True
              Player.moveRight(screen_height * 0.0074 * 1.5)
            if key[pygame.K_w] == True:
              Player.moveBack(screen_height * 0.0111 * 1.25)
            if key[pygame.K_s] == True:           
              Player.moveForward(screen_height * 0.0056 * 1.5)
              
            if key[pygame.K_a] == True and key[pygame.K_d] == True:
              Dragon_IMAGE_Scaled_allowed = True
              Dragon_IMAGE_Scaled_Left_allowed = False
              Dragon_IMAGE_Scaled_Right_allowed = False
          
        Player.clamp_ip(screen.get_rect())
        #print(pygame.time.get_ticks() - Lifebar_timer)
        #print(first_hit)
        #print(Lifebar_time)
        #print("Fully_loaded")
        # Updating the display surface
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())