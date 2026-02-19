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
    "#..##....#",
    "#........#",
    "#....#...#",
    "#........#",
    "#...##...#",
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Verifie si le monstre est au cordonne approximative
    def isThere(self,x,y):
        #return self.x+0.001 > x and self.x-0.001 < x and self.y+0.001 > y and self.y-0.001 < y
        return int(x) == self.x and int(y) == self.y

class Player:
    def __init__(self):
        self.x = 3.5
        self.y = 3.5
        self.angle = 0

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

        # collisions
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
        monsters.append(Monster(5,9))

        pyxel.run(self.update, self.draw)


    def update(self):
        self.player.update()


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
                
                # Detecte mais ne fait rien pour le moment
                for monster in monsters:
                    if monster.isThere(x,y):
                        pass

                if wall(x, y):
                    hit_x, hit_y = x, y
                    break

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

            for y in range(wall_height):
                tex_y = int((y / wall_height) * TEX_SIZE)
                color = pyxel.image(0).pget(tex_x, tex_y)

                pyxel.pset(ray, y_start + y, color)

    def draw(self):
        pyxel.cls(0)

        # ciel / sol
        pyxel.rect(0, 0, W, H//2, 1)
        pyxel.rect(0, H//2, W, H//2, 3)

        self.draw_world()


App()
