from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_weight - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_weight:
            self.rect.x = randint(80, win_weight - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_weight = 1000
win_height = 800
window = display.set_mode((win_weight, win_height))
display.set_caption('Шутер')
shyter = transform.scale(image.load('galaxy.jpg'), (win_weight, win_height))

ship = Player('rocket.png', 5, win_weight - 290, 80, 90, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_weight - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

font.init()
font1 = font.SysFont(None, 36)
font2 = font.SysFont(None, 36)
font3 = font.SysFont(None, 100)
font4 = font.SysFont(None, 100)


bullets = sprite.Group()
finish = True
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                ship.fire()
    if finish == True:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides :
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_weight - 80), 40, 80, 50, randint(1, 5))
            monsters.add(monster)
        bullets.update()
        window.blit(shyter,(0, 0))
        monsters.update()
        text_lose = font1.render("Попущено:" + str(lost), 1, (255, 255, 255))
        text_win = font2.render("Попадено:" + str(score), 1, (255, 255, 255))
        lose = font3.render("ТЫ ПРОИГРАЛ!", 1, (255, 255, 255))
        win = font4.render("УРА! ТЫ ВЫИГРАЛ!", 1, (255, 255, 255)) 
        ship.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        if score == 100:
            window.blit(win, (170, 350))
            finish = False
        window.blit(text_win, (15, 40))
        if lost == 50:
            window.blit(lose, (200, 350))
            finish = False
        window.blit(text_lose, (10, 10))

        display.update()
    
