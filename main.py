# This Python file uses the following encoding: Latin-1
# Importing the pygame modules
import random
import pygame
import asyncio
from pygame.locals import *
 
# Initiate pygame and giver permissions to use pygames funktions
pygame.init()

# Get the screen resolution
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
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

start_ticks = pygame.time.get_ticks()

Player_move = True
score_allowed = True
highscore_reset = False
obstacle_hard_color = False

# Dragon images
Dragon_IMAGE = pygame.image.load('ALPHA Toothless 10.0.png').convert_alpha()
if Player_Monitor == True:
  neue_breite = Dragon_IMAGE.get_width() / 5 * screen_width / 2120
  neue_hoehe = Dragon_IMAGE.get_height() / 5 * screen_width / 2120
else:
  neue_breite = Dragon_IMAGE.get_width() / 2 * screen_width / 2120
  neue_hoehe = Dragon_IMAGE.get_height() / 2 * screen_width / 2120
Dragon_IMAGE_Scaled = pygame.transform.scale(Dragon_IMAGE, (neue_breite, neue_hoehe))


# Jungle images
Jungle_IMAGE = pygame.image.load("HFW Dragonrace_Mobile.png").convert_alpha()
if Jungle_IMAGE_Monitor == True:
  neue_breite_Jungle = screen_width
  neue_hoehe_Jungle = screen_height
else:
  neue_breite_Jungle = screen_width * 4
  neue_hoehe_Jungle = screen_height
Jungle_IMAGE_Scaled = pygame.transform.scale(Jungle_IMAGE, (neue_breite_Jungle, neue_hoehe_Jungle))

 
# Create an object to track the time
clock = pygame.time.Clock()

score_background = pygame.Rect(screen_width * 0.1667, screen_height * 0.025, screen_width * 0.6667, screen_height * 0.0625)
highscore_background = pygame.Rect(screen_width * 0.1481, screen_height * 0.5, screen_width * 0.7037, screen_height * 0.0833)
New_personal_best_background = pygame.Rect(screen_width * 0.0278, screen_height * 0.0938, screen_width * 0.9444, screen_height * 0.0563)

if Player_Monitor == True:
  obstacle_spawn_time = 6000 # Spawns objects every 6 seconds at the start
else:
 obstacle_spawn_time = 6000  # Spawns objects every 6 seconds at the start
last_obstacle_spawn_time = 0

text_color = (255, 215, 0)
font_score = pygame.font.Font(None, int(screen_height * 0.0625))
font_highscore = pygame.font.Font(None, int(screen_height * 0.0625))
    

obstacle_speed = screen_height * 0.00167

player_x_spawn = screen_width * 0.2870
player_y_spawn = screen_height * 0.75



  
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
        self.image = pygame.Surface((width_obstacle_left, screen_height * 0.0833))
        self.rect = Rect(0, -screen_height * 0.0833, width_obstacle_left, screen_height * 0.0833) 
        self.image.fill((208,204,204))
        
        
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
        self.image = pygame.Surface((width_obstacle_right, screen_height * 0.0833))
        self.rect = Rect((width_obstacle_right_spawn, -screen_height * 0.0833, width_obstacle_right, screen_height * 0.0833)) 
        self.image.fill((208,204,204))
      

    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.top > screen_height:
            self.kill()
            
    def obstacle_right_kill(self):
        self.kill()
        
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
 
font_restart_text = pygame.font.Font(None,int(screen_height * 0.0667))  
restart_text = font_restart_text.render('Restart', True, color_button_restart) 
          
run = True

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

    # Creating an infinite loop to run the game
    while run:
            
        if pygame.time.get_ticks() - last_obstacle_spawn_time > obstacle_spawn_time:
            # Wenn 200 score erreicht ist wird der Bereich wo man durchfliegt kleiner
            if score < 200:
                if Obstacle_Monitor == True:
                  width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                  width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
    
                  while width_obstacle_left + width_obstacle_right > screen_width * 0.5370 * 1.5:
                    width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                    width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                else:
                  width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
                  width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
    
                  while width_obstacle_left + width_obstacle_right > screen_width * 0.5370:
                    width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
                    width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
            else:
                if Obstacle_Monitor == True:
                  width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                  width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
    
                  while not screen_width * 0.5370 * 1.2 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370 * 1.5:
                    width_obstacle_left = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                    width_obstacle_right = random.randrange(int(screen_width * 0.0370 * 1.5), int(screen_width * 0.5370 * 1.5))
                else:
                  width_obstacle_left = random.randrange(int(screen_width * 0.0370) , int(screen_width * 0.5370))
                  width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
    
                  while not screen_width * 0.5370 * 0.7 < width_obstacle_left + width_obstacle_right < screen_width * 0.5370:
                    width_obstacle_left = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
                    width_obstacle_right = random.randrange(int(screen_width * 0.0370), int(screen_width * 0.5370))
           
            obstacle_left = Obstacle_Left(width_obstacle_left)
            obstacle_right = Obstacle_Right(width_obstacle_right)
            Obstacles.add(obstacle_left, obstacle_right)
            obstacles_left.add(obstacle_left)
            obstacles_right.add(obstacle_right)
            
            if Player_Monitor == True:
              obstacle_spawn_time = obstacle_spawn_time -320 # Objekte werden nach dem spawnen schneller gespawnt
            else:
              obstacle_spawn_time = obstacle_spawn_time - 40 # Objekte werden nach dem spawnen schneller gespawnt
            if Player_Monitor == True:
              obstacle_speed = obstacle_speed + screen_height * 0.00001667 * 3 * 1.5 # Objekte werden nach dem spawnen schneller
            else:
              obstacle_speed = obstacle_speed + screen_height * 0.00001667 * 1.5 # Objekte werden nach dem spawnen schneller
            last_obstacle_spawn_time = pygame.time.get_ticks()
            
            if Player_Monitor == True:
              if obstacle_spawn_time < 2000: # Begrenzt die Spawngeschwindigkeit bei max 2 Sekunden
                obstacle_spawn_time = 2000
            else:
              if obstacle_spawn_time < 1000: # Begrenzt die Spawngeschwindigkeit bei max 1 Sekunde
                obstacle_spawn_time = 1000
       
            if obstacle_speed > screen_height * 0.005: # Begrentzt die Geschwindigkeit
              obstacle_speed = screen_height * 0.005            
        
        # FPS auf 60 setzten
        dt = clock.tick(60)

        if score_allowed == True:

          score = (pygame.time.get_ticks() - start_ticks) // 1000
      
        # Den bisherigen Highscore aus der Datei lesen
        try:
            with open('highscore.txt', 'r') as f:
                highscore = int(f.read())
        except FileNotFoundError:
            highscore = 0

        # Den aktuellen Score mit dem Highscore vergleichen
        if score > highscore:
            # Den Highscore aktualisieren, wenn der aktuelle Score hoeher ist
            with open('highscore.txt', 'w') as f:
                f.write(str(score))
            
        if highscore_reset == True:
          with open('highscore.txt', 'w') as f:
            f.write(str(0))
            highscore_reset = False
    

        score_text = font_score.render("Score:" + str(score), True, text_color)
        New_personal_best_text = font_score.render("New personal best!", True, text_color)

        screen.blit(Jungle_IMAGE_Scaled, (0,0))  
        screen.blit(Dragon_IMAGE_Scaled, Player.rect.topleft)

        #all_sprites.update()
        all_sprites.add(Player)
        #all_sprites.draw(screen)
        Obstacles.draw(screen)
        pygame.draw.rect(screen, (170, 169, 173), score_background)
    
        screen.blit(score_text, (screen_width * 0.2315, screen_height * 0.0375))
        if score >= highscore:
          pygame.draw.rect(screen, (170, 169, 173), New_personal_best_background)
          screen.blit(New_personal_best_text, (screen_width * 0.0463, screen_height * 0.1021))


        Obstacles.update()
      

        for obstacle in Obstacles:
            # Wenn der Spieler mit dem Obstacle aufeinandertrifft Wird das Spiel Pausiert
            if pygame.sprite.collide_rect(Player, obstacle):
              score_allowed = False
              Player_move = False
              obstacle_speed = 0
              obstacle_spawn_time = float('inf')
              #checks if a mouse is clicked 
              for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP: 
                
                  #if the mouse is clicked on the restart button the game is restarted 
                  if width_button_restart/2 <= mouse[0] <= width_button_restart/2+screen_width * 0.5556 and height_button_restart/2 <= mouse[1] <= height_button_restart/2+screen_height * 0.0833: 
                    for obstacle in obstacles_left:
                      obstacle.obstacle_left_kill()
                    for obstacle in obstacles_right:
                      obstacle.obstacle_right_kill()
                    Player.player_spawn(screen_width * 0.2870, screen_height * 0.75)
                    score_allowed = True
                    Player_move = True
                    start_ticks = pygame.time.get_ticks()
                    last_obstacle_spawn_time = pygame.time.get_ticks()
                    obstacle_speed = screen_height * 0.00167
                    if Player_Monitor == True:
                      obstacle_spawn_time = 10000 # Spawnt Objekte am Anfang alle 10 Sekunden
                    else:
                      obstacle_spawn_time = 4000  # Spawnt Objekte am Anfang alle 4 Sekunden
      
              # stores the (x,y) coordinates into the variable as a tuple 
              mouse = pygame.mouse.get_pos() 
         
              # if mouse is hovered on the restart button it changes to lighter shade  
              if width_button_restart/2 <= mouse[0] <= width_button_restart/2+screen_width * 0.5556 and height_button_restart/2 <= mouse[1] <= height_button_restart/2+screen_height * 0.0833: 
                pygame.draw.rect(screen,color_button_restart_light,[width_button_restart/2,height_button_restart/2,screen_width * 0.5556,screen_height * 0.0833]) 
          
              else: 
                pygame.draw.rect(screen,color_button_restart_dark,[width_button_restart/2,height_button_restart/2,screen_width * 0.5556,screen_height * 0.0833]) 
      
              # superimposing the restart text onto the button 
              screen.blit(restart_text , (width_button_restart/2+screen_width * 0.0694,height_button_restart/2+screen_height * 0.0208))
          
              pygame.draw.rect(screen, (51, 2, 209), highscore_background)

              highscore_text = font_highscore.render("Highscore:" + str(highscore), True, text_color) 
              screen.blit(highscore_text, (screen_width * 0.1759, screen_height * 0.5208))

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False   
          if Player_move == True:
           if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.dragging = True
                        mouse_x, mouse_y = event.pos
                        sprite.offset_x = sprite.rect.x - mouse_x
                        sprite.offset_y = sprite.rect.y - mouse_y
           elif event.type == pygame.MOUSEBUTTONUP:
                    for sprite in all_sprites:
                        sprite.dragging = False
           elif event.type == pygame.MOUSEMOTION:
                    for sprite in all_sprites:
                        if sprite.dragging:
                            sprite.update(event.pos)
                        
        if Player_move == True:
            key = pygame.key.get_pressed()
            if key[pygame.K_a] == True:
              Player.moveLeft(screen_height * 0.0074 * 1.5)
            if key[pygame.K_d] == True:
              Player.moveRight(screen_height * 0.0074 * 1.5)
            if key[pygame.K_w] == True:
              Player.moveBack(screen_height * 0.0111 * 1.25)
            if key[pygame.K_s] == True:
              Player.moveForward(screen_height * 0.0056 * 1.5)
 
        Player.clamp_ip(screen.get_rect())
        # Updating the display surface
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())