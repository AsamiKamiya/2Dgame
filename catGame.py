from collections import deque, namedtuple
from random import randint
import pyxel
from time import sleep
 
Point = namedtuple("Point", ["w", "h"]) 
 
# direction_cat
RIGHT = Point(-16, 16)
LEFT = Point(16, 16)

class App:
    def __init__(self):
        # make window
        pyxel.init(128, 128, caption="cat game")
        # load picture data.
        pyxel.load("pictures.pyxres")
        # init direction
        self.direction = RIGHT
        # Score
        self.score = 0
        # Starting Point
        self.player_x = 42
        self.player_y = 100
        self.player_xy = 0
        self.player_vy = 0
        self.gravity = 0.1
        # make items
        self.fruit = [(randint(0, 104), i * 60 , True) for i in range(5)]
        self.star =  [(i * 60, randint(0, 104), True) for i in range(1)]
        self.bomb =  [(i * 60, randint(0, 104), True) for i in range(1)]
        self.enemy = [(i * 60, 0, True) for i in range(1)]
        self.shots = []
        # flgs
        self.speed = 0
        self.counter = 0
        self.GAME_OVER = False
        self.START_FLG = False

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)
 
    def update(self):
        # quit
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # player moving
        self.update_player()

        # item moving
        if self.START_FLG: 
            for i, v in enumerate(self.fruit):
                self.fruit[i] = self.update_fruit(*v)
        
            for i, v in enumerate(self.star):
                self.star[i] = self.update_star(*v)
        
            for i, v in enumerate(self.bomb):
                self.bomb[i] = self.update_bomb(*v)

            for i, v in enumerate(self.enemy):
                self.enemy[i] = self.update_enemy(*v)
        
        if pyxel.btn(pyxel.KEY_0):
            self.START_FLG = True

        if self.GAME_OVER :
            if pyxel.btn(pyxel.KEY_R):
                self.START_FLG = False
                self.GAME_OVER = False
        
        # jump
        self.player_vy += self.gravity
        self.player_y += self.player_vy
        if self.player_y > 100:
            self.player_y = 100
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player_vy = -2

        
    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2 - self.speed, 0)
            self.direction = LEFT
 
        if pyxel.btn(pyxel.KEY_RIGHT) :
            self.player_x = min(self.player_x + 2 + self.speed, pyxel.width - 16)
            self.direction = RIGHT
 
    def draw(self):
        if self.START_FLG == False:
            pyxel.cls(0)
            pyxel.text(40, 40, "GAME START", pyxel.frame_count % 16)
            pyxel.blt(
                50,
                50,
                0,
                0,
                0,
                self.direction[0],
                self.direction[1],
                10,
            )
            pyxel.blt(
                66,
                50,
                0,
                16,
                0,
                self.direction[0],
                self.direction[1],
                10,
            )
            return

        # draw gameover
        if self.GAME_OVER:
            pyxel.text(40, 40, "GAME OVER", pyxel.frame_count % 16)
            pyxel.blt(self.player_x, self.player_y-10, 0, 32, 16, 16, 16, 0)
            self.speed = 0
            self.counter = 0
            self.score = 0
            pyxel.stop()
            return

        # draw map
        pyxel.bltm(0,0,0,0,0,16,16)
 
        if self.START_FLG :
            # draw fruits
            for x, y, is_active in self.fruit:
                if is_active:
                    pyxel.blt(x, y, 0, 16, 0, 16, 16, 0)

            # draw star
            for x, y, is_active in self.star:
                if is_active:
                    pyxel.blt(x, y, 0, 32, 0, 16, 16, 0)
            
            # draw bomb
            for x, y, is_active in self.bomb:
                if is_active:
                    pyxel.blt(x, y, 0, 48, 0, 16, 16, 7)

            # draw enemy
            for x, y, is_active in self.enemy:
                if is_active:
                    pyxel.blt(x, y, 0, 56, 40, 8, 8, 7)
    
            # draw cat
            if self.speed == 0 :
                pyxel.blt(
                    self.player_x,
                    self.player_y,
                    0,
                    16 if self.player_xy > 0 else 0,
                    0,
                    self.direction[0],
                    self.direction[1],
                    10,
                )
            if self.speed ==  2 :
                pyxel.blt(
                    self.player_x,
                    self.player_y,
                    0,
                    16 if self.player_xy > 0 else 0,
                    0,
                    self.direction[0],
                    self.direction[1],
                    10,
                )
                pyxel.text(self.player_x + 10,
                    self.player_y, "!!", pyxel.frame_count % 16)
        # draw score
        s = "Score {:>4}".format(self.score)
        if self.speed == 0 :
            pyxel.text(5, 4, s, 1)
            pyxel.text(4, 4, s, 7)
        if self.speed == 2 :
            pyxel.text(4, 4, s, pyxel.frame_count % 16)

 
    def update_fruit(self, x, y, is_active):
        if is_active and abs(y - self.player_y) < 12 and abs(x - self.player_x) < 12:
            is_active = False
            self.score += 100
            self.player_xy = min(self.player_xy, -8)
            self.counter += 1
        
        if self.counter > 3:
            self.counter = 0
            self.speed = 0
 
        y += 2
 
        if y > 100:
            y -= 240
            x = randint(0, 104)
            is_active = True
 
        return (x, y, is_active)
    
    def update_star(self, x, y, is_active):
        if is_active and abs(y - self.player_y) < 12 and abs(x - self.player_x) < 12:
            is_active = False
            self.player_xy = min(self.player_xy, -8)
            self.speed = 2
 
        y += 1
 
        if y > 100:
            y -= 240
            x = randint(0, 104)
            is_active = True
 
        return (x, y, is_active)

    def update_bomb(self, x, y, is_active):
        if is_active and abs(y - self.player_y) < 12 and abs(x - self.player_x) < 12:
            is_active = False
            self.player_xy = min(self.player_xy, -8)
            self.GAME_OVER = True
        y += 2
 
        if y > 100:
            y -= 240
            x = randint(0, 104)
            is_active = True
 
        return (x, y, is_active)
    
    def update_enemy(self, x, y, is_active):
        if is_active and abs(y - self.player_y) < 12 and abs(x - self.player_x) < 6:
            is_active = False
            self.player_xy = min(self.player_xy, -8)
            self.GAME_OVER = True
 
        x -= 2
 
        if x < -40:
            x += 240
            y = 108
            is_active = True
 
        return (x, y, is_active)
       
 
App()