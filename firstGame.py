import pygame
pygame.init()
screenWidth = 500
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')


clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound("gun.wav")
hitSound = pygame.mixer.Sound("hit.wav")
bgm = pygame.mixer.music.load('music.mp3')
jump = pygame.mixer.Sound("jump.wav")
pygame.mixer.music.play(-1)
score = 0 # It shows you how many time you hit a goblin

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y, 28, 65)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            elif self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(char, (self.x, self.y))

        self.hitbox = (self.x + 17, self.y, 28, 65)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # get hitbox invisible

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('./barking_cat/BarkingCatDEMO.otf', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, ((screenWidth/2) - 50, (screenHeight/2) - 50))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy():
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.hp = 100
        self.visible = True # this is for eliminating goblin when hp goes 0.

    def draw(self, win):
        self.move()
        if self.visible == True:
            if self.walkCount + 1 >= 22:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//2], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//2], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 20, self.y, 28, 60)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # get hitbox invisible
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 29, 10))
            pygame.draw.rect(win, (125, 255, 125), (self.hitbox[0], self.hitbox[1] - 10, 29 - (100 - self.hp) * 0.29, 10))


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.hp > 0:
            self.hp -= 1
        else:
            self.visible = False
        pass

def redrawWindow():
    win.blit(bg, (0, 0))
    text = font.render("Score: {}".format(score), 1, (0, 0, 0)) # text object
    win.blit(text, (20, 20)) # blit text on win
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# mainloop
font = pygame.font.SysFont("./barking_cat/BarkingCatDEMO.otf", 30, True) # font object
man = player(300, 410, 64, 64)
bullets = []
shootLoop = 0
goblin = enemy(100, 410, 64, 64, 450)
run = True
while run:
    clock.tick(27)

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if bullet.y + bullet.radius > goblin.hitbox[1] and bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                hitSound.play()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        elif man.right:
            facing = 1
        if len(bullets) < 100:
            bullets.append(projectile(round(man.x + (man.width//2)), round(man.y + (man.height//2)), 6, (50,55,80), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x >= man.vel:
        man.x -= man.vel
        man.right = False
        man.left = True
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_UP]:
            jump.play()
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            vector = 1
            if man.jumpCount < 0:
                vector = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * vector
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    if goblin.visible == False:
        text = font.render('WIN', 1, (255, 0, 0))
        win.blit(text, ((screenWidth / 2) - 50, (screenHeight / 2) - 50))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        pygame.quit()
    redrawWindow()
pygame.quit()
