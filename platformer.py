import pygame
from sys import exit
import time
import os
pygame.init()
x = 1024
y = 512
c = pygame.time.Clock()
s = pygame.display.set_mode((x, y))
p = pygame.Rect(512, 512-100, 50, 100)
p_img = pygame.image.load(os.path.join("..","python","platformer","assets","mario.jpeg"))
p_img = pygame.transform.scale(p_img, (50, 100))
jump_vel = -15  # Jump velocity (negative for upward)
gravity = 0.8   # Gravity acceleration
move_speed = 5
p_vel_y = 0     # Player's vertical velocity
p_vel_x = 0     # Player's horizontal velocity
on_ground = True  # Track if player is on ground
tile_size = 32
sponge_w=128
sponge_h=256
max_hp = 100
current_hp = max_hp
tile_img = pygame.image.load(os.path.join("..","python","platformer","assets","wall.jpeg"))
tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
spike_img = pygame.image.load(os.path.join("..","python","platformer","assets","spike.jpeg"))
spike_img = pygame.transform.scale(spike_img, (tile_size, tile_size))
pygame.display.set_icon(p_img)
boss_img = pygame.image.load(os.path.join("..","python","platformer","assets","sponge-boss.jpeg"))
boss_img = pygame.transform.scale(boss_img, (sponge_w, sponge_h))
font = pygame.font.SysFont("Arial", 24)
hp_bar = font.render(f"HP: {current_hp}/{max_hp}", True, (255, 0, 0))
hp_bar = pygame.transform.scale(hp_bar, (150, 30))
def draw():
    s.fill("#3ea6ff")  # Fill with a blue color (RGB values)
    s.blit(p_img, (p.x, p.y))  # Draw the player image at the player's position
    s.blit(hp_bar, (10, 10))
    for tile in tiles:
        s.blit(tile.img, (tile.x, tile.y))
    for spike in spikes:
        s.blit(spike.img, spike)
    for boss in bosses:
        s.blit(boss.img, (boss.x, boss.y))
class sponge_boss(pygame.Rect):
    def __init__(self, x, y, img):
        pygame.Rect.__init__(self, x, y, sponge_w, sponge_h)
        self.img = img
class Tile(pygame.Rect):
    def __init__(self, x, y, img):
        pygame.Rect.__init__(self, x, y, tile_size, tile_size)
        self.img = img
def create_map():
    for i in range(5):
        tile = Tile(200+512+i * tile_size, p.y + tile_size*0.0001, tile_img)
        tiles.append(tile)
    for i in range(5):
        tile = Tile(400+512+i * tile_size, 350, tile_img)
        tiles.append(tile)
    for i in range(5):
        tile = Tile(600+512+i * tile_size, 300, tile_img)
        tiles.append(tile)
    for i in range(5):
        tile = Tile(800+512+i * tile_size, 250, tile_img)
        tiles.append(tile)
    for  i in range(1):
        spike = Tile(232+512+i * tile_size, p.y + tile_size*0.0001, spike_img)
        spikes.append(spike)
    for  i in range(1):
        spike = Tile(432+512+i * tile_size, 350, spike_img)
        spikes.append(spike)
    for i in range(10):
        if i == 3 or i == 7 or i == 9:
            spike = Tile(1000+512+i * tile_size, 400, spike_img)
            spikes.append(spike)
        else:
            tile = Tile(1000+512+i * tile_size, 400, tile_img)
            tiles.append(tile)
def collisions():
    for tile in tiles:
        if p.colliderect(tile):
           return tile
    for spike in spikes:
        if p.colliderect(spike):
            return spike
    for boss in bosses:
        if p.colliderect(boss):
            return boss
            current_hp -= 1
            hp_bar = font.render(f"HP: {current_hp}/{max_hp}", True, (255, 0, 0))
            hp_bar = pygame.transform.scale(hp_bar, (150, 30))
    return None

def col_x():
    for tile in tiles:
        if p.colliderect(tile):
            if p_vel_x > 0:  # Moving right
                p.x = tile.x - p.width
            elif p_vel_x < 0:  # Moving left
                p.x = tile.x + tile.width

def col_y():
    global p_vel_y, on_ground
    for tile in tiles:
        if p.colliderect(tile):
            if p_vel_y > 0:  # Falling down
                p.y = tile.y - p.height
                p_vel_y = 0
                on_ground = True
            elif p_vel_y < 0:  # Moving up
                p.y = tile.y + tile.height
                p_vel_y = 0
    for boss in bosses:
        if p.colliderect(boss):
            if p_vel_y > 0:  # Falling down
                p.y = boss.y - p.height
                p_vel_y = 0
                on_ground = True
            elif p_vel_y < 0:  # Moving up
                p.y = boss.y + boss.height
                p_vel_y = 0
def move():
    global p_vel_y, on_ground
    # Apply gravity
    p_vel_y += gravity
    p.y += p_vel_y
    
    # Check if player is on ground (bottom of screen)
    if p.y >= y - p.height:
        p.y = y - p.height
        p_vel_y = 0
        on_ground = True
    for spike in spikes:
        if p.colliderect(spike):
            time.sleep(1)
            pygame.quit()
            exit()
def move_pl_x(vel_x):
    global camera_x
    camera_x += vel_x
    move_map_x(vel_x)
def move_map_x(vel_x):
    for tile in tiles:
        tile.x += vel_x
    for spike in spikes:
        spike.x += vel_x
    for boss in bosses:
        boss.x += vel_x
pygame.display.set_caption("really bad platformer")
tiles = []
spikes = []
bosses = []
boss_spawned = False
camera_x = 0
create_map()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    p_vel_x = 0  # Reset horizontal velocity
    if keys[pygame.K_d]:
        col_x()
        if collisions() is None:
            move_pl_x(-move_speed)
        else:
            move_pl_x(0)
    if keys[pygame.K_a]:
        col_x()
        if collisions() is None:
            move_pl_x(move_speed)
        else:
            move_pl_x(0)
    if keys[pygame.K_w] and on_ground:
        p_vel_y = jump_vel
        on_ground = False
    if collisions() in bosses and bosses:
        current_hp -= 1
        hp_bar = font.render(f"HP: {current_hp}/{max_hp}", True, (255, 0, 0))
        hp_bar = pygame.transform.scale(hp_bar, (150, 30))
        if current_hp <= 0:
            time.sleep(1)
            pygame.quit()
            exit()
    if camera_x < -2048:
        print("You win!")
        time.sleep(1)
        pygame.quit()
        exit()
    
    # Apply horizontal movement
    p.x += p_vel_x
    col_x()  # Check horizontal collisions
    
    # Apply vertical movement
    move()
    col_y()  # Check vertical collisions
    
    if not boss_spawned and camera_x < -1288:
        boss = sponge_boss(p.x + 200, y - sponge_h, boss_img)
        bosses.append(boss)
        boss_spawned = True
    
    # Screen boundary checks
    if p.x < 0:
        p.x = 0
    if p.x > x - p.width:
        p.x = x - p.width
    draw()
    pygame.display.update()

    c.tick(60)
