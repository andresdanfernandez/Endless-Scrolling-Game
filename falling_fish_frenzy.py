import pygame
from sys import exit
import os
from random import randint, choice
from pygame import mixer

pygame.init()
mixer.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Fishsplosion")
clock = pygame.time.Clock()


#Variables
fish_size = (56,56)
largefish_size = (75,56)
font = pygame.font.Font("font/Pixeltype.ttf", 50)
dark_blue = pygame.Color("#145DA0")
red = pygame.Color("#FF0000")
light_blue = pygame.Color("#B2CACF")
score = 0
game_active = False
font = pygame.font.Font("font/Pixeltype.ttf", 50)
failed_catches = 0
frame = 0
miliseconds = 1200
black = (0,0,0)

#Sound/Music
mixer.music.load(os.path.join("audio", "background.mp3"))
mixer.music.set_volume(0.2)
channel = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
explosion_sound = pygame.mixer.Sound(os.path.join("audio", "explosion.mp3"))
explosion_sound.set_volume(0.3)
success_sound = pygame.mixer.Sound(os.path.join("audio", "success.mp3"))
success_sound.set_volume(0.3)
failure_sound = pygame.mixer.Sound(os.path.join("audio", "failure.mp3"))
failure_sound.set_volume(0.3)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("graphics", "barrel.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(145,145))
        self.rect = self.image.get_rect(midbottom = (400,600))

    def player_input(self):
        keys = pygame.key.get_pressed()
        vel = 7

        if keys[pygame.K_RIGHT]:
            if self.rect.right < 800:

                if frame < 10:
                    self.rect.x += vel

                elif frame > 10 and frame <= 20:
                    vel = 8
                    self.rect.x += vel
                
                elif frame > 20 and frame <= 30:
                    vel = 10
                    self.rect.x += vel
                
                elif frame > 30 and frame <= 40:
                    vel = 11
                    self.rect.x += vel
                
                elif frame > 40:
                    vel = 12
                    self.rect.x += vel

        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:

                if frame < 10:
                    self.rect.x -= vel

                elif frame > 10 and frame <= 15:
                    vel = 8
                    self.rect.x -= vel
                
                elif frame > 15 and frame <= 20:
                    vel = 9
                    self.rect.x -= vel
                
                elif frame > 20 and frame <= 25:
                    vel = 10
                    self.rect.x -= vel
                
                elif frame > 25:
                    vel = 11
                    self.rect.x -= vel

    def update(self):
        self.player_input()
     
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if  type == "jellyfish":
            jellyfish_surf = pygame.image.load(os.path.join("graphics", "jellyfish.png")).convert_alpha()
            jellyfish_surf = pygame.transform.scale(jellyfish_surf, fish_size)
            self.frames = [jellyfish_surf]
            y_pos = randint(-50,-10)

        elif type == "turtle":
            turtle_surf = pygame.image.load(os.path.join("graphics", "turtle.png")).convert_alpha()
            turtle_surf = pygame.transform.scale(turtle_surf, fish_size)
            self.frames = [turtle_surf]
            y_pos = randint(-50,-10)

        elif type == "whale":
            whale_surf = pygame.image.load(os.path.join("graphics", "whale.png")).convert_alpha()
            whale_surf = pygame.transform.scale(whale_surf, largefish_size)
            self.frames = [whale_surf]
            y_pos = randint(-50,-10)
        
        elif type == "mantaray":
            mantaray_surf = pygame.image.load(os.path.join("graphics","mantaray.png")).convert_alpha()
            mantaray_surf = pygame.transform.scale(mantaray_surf, fish_size)
            self.frames = [mantaray_surf]
            y_pos = randint(-50,-10)

        elif type == "swordfish":
            swordfish_surf = pygame.image.load(os.path.join("graphics","swordfish.png")).convert_alpha()
            swordfish_surf = pygame.transform.scale(swordfish_surf, largefish_size)
            self.frames = [swordfish_surf]
            y_pos = randint(-50,-10)
        
        elif type == "squid":
            squid_surf = pygame.image.load(os.path.join("graphics", "squid.png")).convert_alpha()
            squid_surf = pygame.transform.scale(squid_surf, fish_size)
            self.frames = [squid_surf]
            y_pos = randint(-50,-10)

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center = (randint(100,700), y_pos))    
    
    def update(self):
        vel = 6
        if frame < 10:
            self.rect.y += vel
        elif frame > 10 and frame <= 20:
            vel = 7
            self.rect.y += vel
        elif frame > 20 and frame <= 30:
            vel = 8
            self.rect.y += vel
        elif frame > 30 and frame <= 40:
            vel = 9
            self.rect.y += vel
        elif frame > 40 and frame <= 50:
            vel = 10
            self.rect.y += vel 
        elif frame > 50 and frame <= 60:
            vel = 11
            self.rect.y += vel
        elif frame > 60 and frame <= 70:
            vel = 12
            self.rect.y += vel
        elif frame > 60 and frame <= 80:
            vel = 14
            self.rect.y += vel
        elif frame > 80:
            vel = 15
            self.rect.y += vel

        self.destroy()
        self.collisions()
    
    def destroy(self):
        global failed_catches
        if self.rect.y >= 615:
            self.kill()
            channel3.play(failure_sound)
            failed_catches += 1
            print("killed")

    def collisions(self):
        global score
        collidelist = pygame.sprite.spritecollide(player.sprite, obstacle_group,False)
        for i in collidelist:
            if i.rect.bottom < player.sprite.rect.top + 20:
                i.kill()
                score += 1
                channel2.play(success_sound)
                return True
            else: return False

# Game functions
def display_score():
    score_surf = font.render((f"Score: {score}"),True, (0,0,0))
    score_surf = pygame.transform.scale(score_surf, (250,60))
    score_rect = score_surf.get_rect(center = (400,45))
    screen.blit(score_surf,score_rect)

def check_failed():
    if failed_catches >= 3:
        return False
    else:
        return True

def gameover_screen():
        global score
        screen.fill((light_blue))
        gameover_surf = font.render(("Fishsplosion"),False,(red))
        gameover_surf = pygame.transform.scale(gameover_surf, (600, 150))
        gameover_rect = gameover_surf.get_rect(center = (400,100))
        scoreover_surf = font.render((f"Final Score: {score}"),False,(black))
        scoreover_surf = pygame.transform.scale(scoreover_surf, (300,65))
        scoreover_rect = scoreover_surf.get_rect(center = (400,215))
        smallexpo_surf = pygame.image.load(os.path.join("graphics", "explosion.png")).convert_alpha()
        smallexpo_surf = pygame.transform.scale(smallexpo_surf, (250,300)) 
        smallexpo_rect = smallexpo_surf.get_rect(midbottom = (400,600))
        continue_surf = font.render(("Press space to retry"),False,(0,0,0))
        continue_rect = continue_surf.get_rect(center = (400,280))

        jellyfish_surf = pygame.image.load(os.path.join("graphics", "jellyfish.png")).convert_alpha()
        jellyfish_surf = pygame.transform.scale(jellyfish_surf, fish_size)
        jellyfish_rect = jellyfish_surf.get_rect(center = (150,200))

        mantaray_surf = pygame.image.load(os.path.join("graphics", "mantaray.png")).convert_alpha()            
        mantaray_surf = pygame.transform.scale(mantaray_surf, fish_size)
        mantaray_rect = mantaray_surf.get_rect(center = (210,530))

        swordfish_surf = pygame.image.load(os.path.join("graphics", "swordfish.png")).convert_alpha()
        swordfish_surf = pygame.transform.scale(swordfish_surf, largefish_size)
        swordfish_rect = swordfish_surf.get_rect(center = (670,195))

        turtle_surf = pygame.image.load(os.path.join("graphics", "turtle.png")).convert_alpha()
        turtle_surf = pygame.transform.scale(turtle_surf, fish_size)
        turtle_rect = turtle_surf.get_rect(center = (725,545))

        whale_surf = pygame.image.load(os.path.join("graphics", "whale.png")).convert_alpha()
        whale_surf = pygame.transform.scale(whale_surf, largefish_size)
        whale_rect = whale_surf.get_rect(center = (615,380))

        squid_surf = pygame.image.load(os.path.join("graphics", "squid.png")).convert_alpha()
        squid_surf = pygame.transform.scale(squid_surf, fish_size)
        squid_rect = squid_surf.get_rect(center = (80,400))  


        screen.blit(jellyfish_surf,jellyfish_rect)
        screen.blit(mantaray_surf,mantaray_rect)
        screen.blit(swordfish_surf,swordfish_rect)
        screen.blit(turtle_surf,turtle_rect)
        screen.blit(whale_surf,whale_rect)
        screen.blit(squid_surf,squid_rect)
        screen.blit(smallexpo_surf,smallexpo_rect)
        screen.blit(gameover_surf,gameover_rect) 
        screen.blit(scoreover_surf,scoreover_rect)
        screen.blit(continue_surf,continue_rect)

def update_health():
        if failed_catches == 0:
            screen.blit(heart_surf, heart_rect)
            screen.blit(heart_surf2, heart_rect2)
            screen.blit(heart_surf3, heart_rect3)
        elif failed_catches == 1:
            screen.blit(heart_surf2, heart_rect2)
            screen.blit(heart_surf3, heart_rect3)
        else:
            screen.blit(heart_surf3, heart_rect3)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#Backgrounds
waves_surf = pygame.image.load(os.path.join("graphics", "waves.png")).convert_alpha()
waves_surf = pygame.transform.scale(waves_surf,(850,300)).convert_alpha()
waves_rect = waves_surf.get_rect(midbottom =(350,715))

waves_surf2 = pygame.image.load(os.path.join("graphics", "waves.png")).convert_alpha()
waves_surf2 = pygame.transform.scale(waves_surf2,(850,300)).convert_alpha()
waves_rect2 = waves_surf2.get_rect(midbottom = (520,725))

explosion_surf = pygame.image.load(os.path.join("graphics", "explosion.png")).convert_alpha()
explosion_surf = pygame.transform.scale(explosion_surf, (450,550))
explosion_rect = explosion_surf.get_rect(midbottom = (400,600))

#Health Bar
heart_surf = pygame.image.load(os.path.join("graphics", "heart.png")).convert_alpha()
heart_surf = pygame.transform.scale(heart_surf, (40,40))
heart_rect = heart_surf.get_rect(center = (650, 35))

heart_surf2 = pygame.image.load(os.path.join("graphics", "heart.png")).convert_alpha()
heart_surf2 = pygame.transform.scale(heart_surf2, (40,40))
heart_rect2 = heart_surf.get_rect(center = (690, 35))

heart_surf3 = pygame.image.load(os.path.join("graphics", "heart.png")).convert_alpha()
heart_surf3 = pygame.transform.scale(heart_surf3, (40,40))
heart_rect3 = heart_surf.get_rect(center = (730, 35))

#Obstacle Spawner
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,miliseconds)

while True:
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                # Spawns random enemy
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(["jellyfish","turtle","whale","mantaray","swordfish","squid"])))
                    if frame < 10:
                        miliseconds = 1200
                        pygame.time.set_timer(obstacle_timer,miliseconds)
                    elif frame > 10 and frame <= 20:
                        miliseconds = 1000
                        pygame.time.set_timer(obstacle_timer,miliseconds)
                    elif frame > 20 and frame <= 30:
                        miliseconds = 950
                        pygame.time.set_timer(obstacle_timer,miliseconds) 
                    elif frame > 30 and frame <= 40:
                        miliseconds = 850
                        pygame.time.set_timer(obstacle_timer,miliseconds)
                    elif frame >= 40:
                        miliseconds = 750
                        pygame.time.set_timer(obstacle_timer,miliseconds)
            else:
                # Restart Game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    obstacle_group.empty()
                    player.sprite.rect.midbottom = (400,600)
                    score = 0
                    failed_catches = 0
                    frame = 0
                    mixer.music.play()
                    channel.play(explosion_sound)

    if game_active:
        screen.fill((light_blue))
        screen.blit(explosion_surf,explosion_rect)
        screen.blit(waves_surf,waves_rect)
        screen.blit(waves_surf2,waves_rect2)
        
        update_health()
        
        display_score()

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = check_failed()

        #Game Timer
        frame += 1 / 60

    else:
        # Initial game screen
        if frame == 0:
            channel.play(explosion_sound)
            screen.fill((light_blue))
            gameover_surf = font.render(("Fishsplosion"),False,(red))
            gameover_surf = pygame.transform.scale(gameover_surf, (600, 150))
            gameover_rect = gameover_surf.get_rect(center = (400,100))
            smallexpo_surf = pygame.image.load(os.path.join("graphics", "explosion.png")).convert_alpha()
            smallexpo_surf = pygame.transform.scale(smallexpo_surf, (250,300)) 
            smallexpo_rect = smallexpo_surf.get_rect(midbottom = (400,600))
            continue_surf = font.render(("Press space to play"),False,(black))
            continue_rect = continue_surf.get_rect(center = (400,200))
            arrowkeys_surf = font.render(("Use arrow keys to move"),False,(black))
            arrowkeys_rect = arrowkeys_surf.get_rect(midbottom = (400,275))

            jellyfish_surf = pygame.image.load(os.path.join("graphics", "jellyfish.png")).convert_alpha()
            jellyfish_surf = pygame.transform.scale(jellyfish_surf, fish_size)
            jellyfish_rect = jellyfish_surf.get_rect(center = (150,200))

            mantaray_surf = pygame.image.load(os.path.join("graphics", "mantaray.png")).convert_alpha()
            mantaray_surf = pygame.transform.scale(mantaray_surf, fish_size)
            mantaray_rect = mantaray_surf.get_rect(center = (210,530))

            swordfish_surf = pygame.image.load(os.path.join("graphics", "swordfish.png")).convert_alpha()
            swordfish_surf = pygame.transform.scale(swordfish_surf, largefish_size)
            swordfish_rect = swordfish_surf.get_rect(center = (670,195))

            turtle_surf = pygame.image.load(os.path.join("graphics", "turtle.png")).convert_alpha()
            turtle_surf = pygame.transform.scale(turtle_surf, fish_size)
            turtle_rect = turtle_surf.get_rect(center = (725,545))

            whale_surf = pygame.image.load(os.path.join("graphics", "whale.png")).convert_alpha()
            whale_surf = pygame.transform.scale(whale_surf, largefish_size)
            whale_rect = whale_surf.get_rect(center = (615,380))

            squid_surf = pygame.image.load(os.path.join("graphics", "squid.png")).convert_alpha()
            squid_surf = pygame.transform.scale(squid_surf, fish_size)
            squid_rect = squid_surf.get_rect(center = (80,400))  

            screen.blit(gameover_surf,gameover_rect)
            screen.blit(smallexpo_surf,smallexpo_rect)
            screen.blit(continue_surf,continue_rect)
            screen.blit(arrowkeys_surf,arrowkeys_rect)
            screen.blit(jellyfish_surf,jellyfish_rect)
            screen.blit(mantaray_surf,mantaray_rect)
            screen.blit(swordfish_surf,swordfish_rect)
            screen.blit(turtle_surf,turtle_rect)
            screen.blit(whale_surf,whale_rect)
            screen.blit(squid_surf,squid_rect)

        else:
            mixer.music.stop()
            gameover_screen()

    pygame.display.update()
    clock.tick(60)
