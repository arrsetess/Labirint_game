from pygame import *

win_width = 700
win_hight = 500

window = display.set_mode((win_width,win_hight))
display.set_caption('Maze')

class GameSprite(sprite.Sprite):
    def init(self, image_name, x, y, width, height):
        super().init()
        img = image.load(image_name)
        self.image = transform.scale(img,(width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def init(self, image_name, x, y, width, height, speed_x, speed_y):
        super().init(image_name, x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def move(self):
        #self.rect.x += self.speed_x
        #self.rect.y += self.speed_y
        if self.rect.x <= win_width - 75 and self.speed_x > 0 or self.rect.x >= 0 and self.speed_x < 0:
            self.rect.x += self.speed_x

        if self.rect.y <= win_hight - 75 and self.speed_y > 0 or self.rect.y >= 0 and self.speed_y < 0:
            self.rect.y += self.speed_y

        platform_touched = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for platform in platform_touched:
                self.rect.right = min(self.rect.right, platform.rect.left)

        elif self.speed_x < 0:
            for platform in platform_touched:
                self.rect.left = max(self.rect.left, platform.rect.right)

        elif self.speed_y > 0:
            for platform in platform_touched:
                self.rect.bottom = min(self.rect.bottom, platform.rect.top)

        elif self.speed_y < 0:
            for platform in platform_touched:
                self.rect.top = max(self.rect.top, platform.rect.bottom)
    
    def fire(self):
        bullet = Bullet(image_name = 'bullet.png',x=self.rect.right,y=self.rect.centery, width= 10,height= 10, speed = 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    direction = 'left'
    def init(self, image_name, x, y, width, height, speed):
        super().init( image_name, x, y, width, height)
        self.speed = speed
    def move(self, left, right):
        if self.rect.x >= right:
            self.direction = 'left'
        elif self.rect.x <= left:
            self.direction = 'right'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def init(self, image_name, x, y, width, height, speed):
        super().init(image_name, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()
        
font.init()
font = font.SysFont('Arial', 60)
def lose():
    window.fill((255, 0, 100))
    win_text = font.render('ПРОИГРЫШ', True, (0, 0, 0))
    window.blit(win_text, (180, 220))

def win():
    window.fill((0, 255, 100))
    win_text = font.render('ПОБЕДА', True, (0, 0, 0))
    window.blit(win_text, (180, 220))

background = GameSprite(image_name='forest.jpg', x=0, y=0, width=win_width, height=win_hight)

platform = GameSprite(image_name='wall.jpg', x=300,y=250,width=100,height=250)

platform_1 = GameSprite(image_name='wall.jpg', x=500,y=0,width=100,height=250)

platform_2 = GameSprite(image_name='wall.jpg', x=100,y=0,width=100,height=250)

bullets = sprite.Group()


walls = sprite.Group()
walls.add(platform)
walls.add(platform_1)
walls.add(platform_2)

player = Player(image_name = 'player_sprite.png', x=35,y=400,width=75,height=75, speed_x = 0,speed_y =0)

enemy = Enemy(image_name = 'enemy_sprite.png', x = win_width - 150, y=50,width=100,height=100,speed=2)

enemy_2 = Enemy(image_name = 'enemy_sprite.png', x = win_width - 10, y=300, width=100,height=100,speed=2)

win_1 = GameSprite(image_name='win.png', x=550,y=415, width=100,height=100)

clock = time.Clock()
FPS = 119

run = T
run = True
end = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.speed_y = -3
            elif e.key == K_s:
                player.speed_y= 3
            elif e.key == K_d:
                player.speed_x = 3
            elif e.key == K_a:
                player.speed_x = -3
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.speed_y = 0
            elif e.key == K_s:
                player.speed_y= 0
            elif e.key == K_d:
                player.speed_x = 0
            elif e.key == K_a:
                player.speed_x = 0

    if not end:
        background.draw()
        platform.draw()
        platform_1.draw()
        platform_2.draw()
        player.draw()
        win_1.draw()
        enemy.draw()
        enemy.move(left = 200, right = 400)
        enemy_2.draw()
        enemy_2.move(left = 400, right = 600)
        player.move() 
        bullets.draw(window)
        bullets.update()

        sprite.groupcollide(bullets, walls, True, False)

        if sprite.spritecollide(enemy, bullets, True):
            enemy.rect.x = 800
            enemy.rect.y = 800
            enemy.kill()

        if sprite.spritecollide(enemy_2, bullets, True):
            enemy_2.rect.x = 800
            enemy_2.rect.y = 800
            enemy_2.kill()

        if player.rect.colliderect(win_1.rect):
            win()
            end =  True
        
        if player.rect.colliderect(enemy.rect):
            lose()
            end = True
        
        if player.rect.colliderect(enemy_2.rect):
            lose()
            end = True
    display.update()
    clock.tick(FPS)