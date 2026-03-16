import pyxel
import math

W, H = 160, 120
FOV = 1
HALF_FOV = FOV / 2
NUM_RAYS = W
MAX_DEPTH = 20

MOVE_SPEED = 0.05
ROT_SPEED = 0.05

TEX_SIZE = 16   # taille texture

WORLD_MAP = [
    "##########",
    "#........#",
    "#........#",
    "#........#",
    "#........#",
    "#........#",
    "#........#",
    "#........#",
    "#........#",
    "##########",
]

monsters = []

def wall(x, y):
    if x < 0 or y < 0:
        return True
    if y >= len(WORLD_MAP) or x >= len(WORLD_MAP[0]):
        return True
    return WORLD_MAP[int(y)][int(x)] == "#"

class Monster:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.monster_here = False
        self.distance = 0
        self.monster_draw = ()

    def ismonster(self,x,y):
        return self.x-0.05 < x < self.x+0.05 and self.y-0.05 < y < self.y+0.05
    
    def update(self):
        self.monster_here = False
        self.distance = math.sqrt((self.x-self.player.x)**2 + (self.y-self.player.y)**2)
        if self.x < self.player.x:
            self.x += MOVE_SPEED - 0.01
        elif self.x > self.player.x:
            self.x -= MOVE_SPEED - 0.01
        if self.y < self.player.y:
            self.y += MOVE_SPEED - 0.01
        elif self.y > self.player.y:
            self.y -= MOVE_SPEED - 0.01
    def draw(self):
        try:
            if self.monster_draw[0] > -8 and self.monster_draw[0] < 128:
                pyxel.blt(self.monster_draw[0],self.monster_draw[1],self.monster_draw[2],self.monster_draw[3],self.monster_draw[4],self.monster_draw[5],self.monster_draw[6],self.monster_draw[7],self.monster_draw[8],self.monster_draw[9])
        except:
            pass

    def prepare_draw(self, ray):
        start_angle = self.player.angle - HALF_FOV
        step = FOV / NUM_RAYS
        
        ray_angle = start_angle + ray * step
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        depth = 0
        hit_x, hit_y = 0, 0
            
            
        while depth < MAX_DEPTH:
            depth += 0.02
            x = self.player.x + cos_a * depth
            y = self.player.y + sin_a * depth
                
            if self.ismonster(x,y) and self.monster_here == False:
                hit_x, hit_y = x, y
                self.monster_here = True
                break
        
                
        if hit_x != 0 and hit_y != 0:
            monster_height = min(int(100 / depth), H)/10
            self.monster_draw = (ray-8,50,0,16,0,16,16,0,0,monster_height)


class Player:
    def __init__(self):
        self.x = 3.5
        self.y = 3.5
        self.angle = 0
        self.energie = 100
        self.attack = False
        self.over_kill = False

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.angle -= ROT_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.angle += ROT_SPEED
        

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        nx, ny = self.x, self.y

        if pyxel.btn(pyxel.KEY_Z):
            nx += cos_a * MOVE_SPEED
            ny += sin_a * MOVE_SPEED

        if pyxel.btn(pyxel.KEY_S):
            nx -= cos_a * MOVE_SPEED
            ny -= sin_a * MOVE_SPEED

        if pyxel.btn(pyxel.KEY_Q):
            nx += sin_a * MOVE_SPEED
            ny -= cos_a * MOVE_SPEED

        if pyxel.btn(pyxel.KEY_D):
            nx -= sin_a * MOVE_SPEED
            ny += cos_a * MOVE_SPEED
        
        if pyxel.btn(pyxel.KEY_UP) and self.energie > 0 and self.over_kill == False:
            self.attack = True
        
        if self.attack == True:
            if self.energie <= 0:
                self.over_kill = True
            self.energie -= 1
        elif self.energie < 100:
            self.energie += 1
        print(self.energie)
        if self.over_kill == True and self.energie == 100:
            self.over_kill = False
        
        for monster in monsters:
            if abs(monster.x - self.x) < 0.5 and abs(monster.y - self.y) < 0.5:
                pass #Player DIE
        
        self.attack = False
        
        if not wall(nx, self.y):
            self.x = nx
        if not wall(self.x, ny):
            self.y = ny

    

class App:
    def __init__(self):
        pyxel.init(W, H, title="Test 3D")

        pyxel.mouse(False)
        pyxel.load("res.pyxres")
        
        self.player = Player()
        monsters.append(Monster(4,8,self.player))

        pyxel.run(self.update, self.draw)


    def update(self):
        self.player.update()
        for monster in monsters:
            monster.update()


    def draw_world(self):

        start_angle = self.player.angle - HALF_FOV
        step = FOV / NUM_RAYS
        
        for ray in range(NUM_RAYS):
            ray_angle = start_angle + ray * step
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            depth = 0
            hit_x, hit_y = 0, 0

            while depth < MAX_DEPTH:
                depth += 0.02
                x = self.player.x + cos_a * depth
                y = self.player.y + sin_a * depth
                
                if wall(x, y):
                    hit_x, hit_y = x, y
                    break
            
            distance = math.sqrt((hit_x-self.player.x)**2 + (hit_y-self.player.y)**2)
            wall_height = min(int(100 / depth), H) # le int change les profondeurs
    
            hit_tile_x = int(hit_x)
            hit_tile_y = int(hit_y)
    
            dx = hit_x - hit_tile_x
            dy = hit_y - hit_tile_y
    
            if abs(dx - 0.5) > abs(dy - 0.5):
                tex_x = int((hit_y % 1) * TEX_SIZE)
            else:
                tex_x = int((hit_x % 1) * TEX_SIZE)
    
            y_start = H // 2 - wall_height // 2
            
            
            for monster in monsters:
                for y in range(wall_height):
                    tex_y = int((y / wall_height) * TEX_SIZE)
                    color = pyxel.image(0).pget(tex_x, tex_y)
    
                    pyxel.pset(ray, y_start + y, color)
                monster.prepare_draw(ray)
    
    def draw(self):
        pyxel.cls(0)

        # ciel / sol
        pyxel.rect(0, 0, W, H//2, 1)
        pyxel.rect(0, H//2, W, H//2, 3)

        self.draw_world()
        for monster in monsters:
            monster.draw()
        pyxel.pset(80,60,6)


App()