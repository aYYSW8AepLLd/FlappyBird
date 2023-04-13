import pygame
import random
 
FPS = 30
FPSCLOCK = pygame.time.Clock()
WINDOW_W ,WINDOW_H = 288,512
BLUE_BIRD_LIST = [
    'assets/sprites/bluebird-upflap.png',
    'assets/sprites/bluebird-midflap.png',
    'assets/sprites/bluebird-downflap.png'
]

pygame.mixer.init()
SOUNDS = {
    'die':pygame.mixer.Sound('assets/audio/die.wav'),
    'hit':pygame.mixer.Sound('assets/audio/hit.wav'),
    'point':pygame.mixer.Sound('assets/audio/point.wav'),
    'swoosh':pygame.mixer.Sound('assets/audio/swoosh.wav'),
    'wing':pygame.mixer.Sound('assets/audio/wing.wav')
}
           
class Bird(pygame.sprite.Sprite):
    def __init__(self,filename_list):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_list = []
        for filename in filename_list:
            self.image_list.append(pygame.image.load(filename))
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect()
        self.last_time = 0

    def update(self,birdx,birdy,bird_angle = 0):
        x,y,w,h = self.image.get_rect()
        self.rect = (birdx,birdy,w / 2,h / 2)

        ms = pygame.time.get_ticks()
        if ms > self.last_time + 100:
            self.last_time = ms
            self.image_index += 1
            if self.image_index >= len(self.image_list):
                self.image_index = 0
        self.image = pygame.transform.rotate(self.image_list[self.image_index],bird_angle)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,pipe_y,posi = 0):
        pygame.sprite.Sprite.__init__(self)
        self.pipe_y = pipe_y
        if posi == 0:
            self.image = pygame.image.load("assets/sprites/pipe-green.png")
        else:
            self.image = pygame.transform.flip(pygame.image.load("assets/sprites/pipe-green.png"),False,True)
            
        x,y,w,h = self.image.get_rect()
        self.rect = x,pipe_y,w,h
        self.scored = False
    def update(self,pipe_x):
        x,y,w,h = self.image.get_rect()
        self.rect = (pipe_x,self.pipe_y,w,h)

class Score(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image_list = []
       self.image_list.append(pygame.image.load("assets/sprites/0.png"))
       self.image_list.append(pygame.image.load("assets/sprites/1.png"))
       self.image_list.append(pygame.image.load("assets/sprites/2.png"))
       self.image_list.append(pygame.image.load("assets/sprites/3.png"))
       self.image_list.append(pygame.image.load("assets/sprites/4.png"))
       self.image_list.append(pygame.image.load("assets/sprites/5.png"))
       self.image_list.append(pygame.image.load("assets/sprites/6.png"))
       self.image_list.append(pygame.image.load("assets/sprites/7.png"))
       self.image_list.append(pygame.image.load("assets/sprites/8.png"))
       self.image_list.append(pygame.image.load("assets/sprites/9.png"))

       self.image_index = 0
       self.image = self.image_list[self.image_index]
       self.rect = self.image.get_rect()
    def update(self,num,scorex,scorey):
       self.image_index = num
       self.image = self.image_list[self.image_index]
       x,y,w,h = self.image.get_rect()
       self.rect = (scorex,scorey,w,h)
        



def Welcome():
    
    pygame.init()

    window = pygame.display.set_mode((WINDOW_W ,WINDOW_H))
    pygame.display.set_caption("Flappy Bird")

    bk = pygame.image.load("assets/sprites/background-day.png")
    window.blit(bk,(0,0))

    message = pygame.image.load("assets/sprites/message.png")
    msgw,msgh = message.get_size()
    msgx = (WINDOW_W - msgw) / 2
    msgy = (WINDOW_H - msgh) / 2
    window.blit(message,(msgx,msgy))
    
    base = pygame.image.load("assets/sprites/base.png")
    basew,baseh = base.get_size()
    base_x = WINDOW_W - basew
    base_y = WINDOW_H - baseh
    window.blit(base,(base_x,base_y))

    bird = Bird(BLUE_BIRD_LIST)
    group = pygame.sprite.Group()
    group.add(bird)
    group.draw(window)
    
    pygame.display.flip()
    
    birdx,birdy = 80,300
    bird_dir = 0
    while True:
        
        window.blit(bk,(0,0))
        
        base_x -= 3
        if base_x <= WINDOW_W - basew:
            base_x = 0
        window.blit(base,(base_x,base_y))
        window.blit(message,(msgx,msgy))

        if bird_dir == 0:
            birdy -= 3
        if bird_dir == 1:
            birdy += 3

        if birdy <= 290:
            bird_dir = 1
        if birdy >= 310:
            bird_dir = 0
        bird.update(birdx,birdy)
        group.draw(window)
        pygame.display.update()
        
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                exit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
                SOUNDS['wing'].play()
                sprites = {"window":window}
                sprites["backgroud"] = bk
                sprites["base"] = base
                sprites["bird"] = bird
                sprites["group"] = group
                sprites["birdx"] = birdx
                sprites['birdy'] = birdy
                sprites["base_x"] = base_x
                sprites["base_y"] = base_y
                return sprites
        FPSCLOCK.tick(FPS)


       
def MainGame(sprites):
    basew,baseh = sprites["base"].get_size()
    base_x = WINDOW_W - basew
    base_y = WINDOW_H - baseh

    bird_dir = 0
    birdx,birdy = sprites["birdx"],sprites['birdy']
    bird_last_y = birdy
    bird_speed = 9
    bird_speed_acc = 0
    bird_distance = 100
    bird_angle = 0

    
    pipe_group = pygame.sprite.Group()
    
    last_time = 0

    score = 0
    
    
    score_group = pygame.sprite.Group()
    while True:
        base_x -= 3
        if base_x <= WINDOW_W - basew:
              base_x = 0
      
        if bird_last_y - birdy > 0:
            if bird_last_y - birdy > 50:
                bird_speed_acc = -1
            if bird_last_y - birdy > 60:
                bird_speed_acc = -2
            if bird_last_y - birdy > 70:
                bird_speed_acc = -3
            if bird_last_y - birdy > 80:
                bird_speed_acc = -4
              
        else:
            bird_speed_acc = 0
        if bird_dir == 0:
            birdy -= bird_speed + bird_speed_acc
            if birdy <= bird_last_y - bird_distance:
                bird_dir = 1
            bird_angle += 9
            if bird_angle > 25:
                bird_angle = 25
        if bird_dir == 1:
            birdy += bird_speed
            bird_angle -= 4
            if bird_angle < -40:
                bird_angle = -40

        
        sprites["window"].blit(sprites["backgroud"],(0,0))

        ms = pygame.time.get_ticks()
        if ms > last_time + 2000:
            last_time = ms

            h = random.randint(10,200)
            pipe_up = Pipe(-50 - h,1)
            pipe_up.update(WINDOW_W)
            pipe_down = Pipe(base_y - h,0)
            pipe_down.update(WINDOW_W)

            pipe_group.add(pipe_up,pipe_down)
        for pipe in pipe_group.sprites():
            pipex,pipey,pipew,pipeh = pipe.rect
            if pipex + pipew < birdx and not pipe.scored:
                score += 1
                SOUNDS['point'].play()
                pipe.scored = True
            if pipex < 0 - pipe.rect[2]:
                pipe_group.remove(pipe)
            else:
                pipex -= 3
                pipe.update(pipex)
                
            rel_score = int(score / 2)
            score_group.empty()
            score_x = 100
            score_y = 50
            for s in str(rel_score):
                score_sprite = Score()
                score_group.add(score_sprite)
                score_x += 25
                score_sprite.update(int(s),score_x,score_y)
   
        check = CheckGameOver({"bird":sprites["bird"],"base_y":base_y,'pipe_group':pipe_group})
        if check:
            SOUNDS['hit'].play()
            SOUNDS['die'].play()
            sprites["base_x"] = base_x
            sprites["base_y"] = base_y
            sprites["pipe_group"] = pipe_group
            sprites['birdx'] = birdx
            sprites['birdy'] = birdy
            sprites['bird_angle'] = bird_angle
            return sprites
        
        pipe_group.draw(sprites["window"])
        sprites["bird"].update(birdx,birdy,bird_angle)
      

      
        sprites["group"].draw(sprites["window"])
        score_group.draw(sprites["window"])
        sprites["window"].blit(sprites["base"],(base_x,base_y))
      


        pygame.display.update()
        for i in pygame.event.get():
              if i.type == pygame.QUIT:
                  pygame.quit()
                  exit()
              if i.type == pygame.KEYDOWN and (i.key == pygame.K_SPACE or i.key == pygame.K_UP):
                 SOUNDS['wing'].play()
                 bird_dir = 0
                 bird_last_y = birdy
                 bird_angle = 20
        FPSCLOCK.tick(FPS)
      

def CheckGameOver(p):
    birdx,birdy,birdw,birdh = p["bird"].rect
    if birdy >= p["base_y"] - birdh:

        return True
        
    for pipe in p['pipe_group'].sprites():
        checkpipe = pygame.sprite.collide_mask(p['bird'],pipe)
        if checkpipe != None:
            return True
    return False

def GameOver(sprites):
    base_x,base_y = sprites["base_x"],sprites["base_y"]
    birdx,birdy,bird_angle = sprites['birdx'],sprites['birdy'],sprites['bird_angle']
    go = pygame.image.load('assets/sprites/gameover.png')
    w,h = go.get_size()
    while True:
        birdy += 1
        if birdy >= base_y - sprites['bird'].rect[3]:
            birdy = base_y - sprites['bird'].rect[3]
        bird_angle -= 10
        if bird_angle < -90:
            bird_angle = -90
        
        sprites["window"].blit(sprites["backgroud"],(0,0))
        sprites["pipe_group"].draw(sprites['window'])
        sprites["window"].blit(sprites["base"],(base_x,base_y))
        sprites['bird'].update(birdx,birdy,bird_angle)
        sprites['group'].draw(sprites['window'])
        sprites["window"].blit(go,((WINDOW_W - w) / 2,100))
        
        pygame.display.update()
        for i in pygame.event.get():
            
              if i.type == pygame.QUIT:
                  pygame.quit()
                  exit()
              if i.type == pygame.KEYDOWN and (i.key == pygame.K_SPACE or i.key == pygame.K_UP):
                  sprites['pipe_group'].empty()
                  sprites['pipe_group'].update()
                  sprites['pipe_group'].draw(sprites['window'])
                  sprites['bird'].update(sprites['birdx'],sprites['birdy'],20)
                  sprites['group'].draw(sprites["window"])
                  pygame.display.update()
                  return sprites
                
sprites = Welcome()
while True:
    sprites = MainGame(sprites)
    sprites = GameOver(sprites)
