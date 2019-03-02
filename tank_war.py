import pygame,sys,time
from pygame.locals import *
from random import randint


class Tank_Main:
    width=800
    height=500
    my_tank_missile_list = []
    my_tank = None
    wall=None
    enemy_list = pygame.sprite.Group()
    explode_list=[]
    enemy_missile_list=pygame.sprite.Group()
    def start_game(self):
        pygame.init()
        screen=pygame.display.set_mode((Tank_Main.width,Tank_Main.height),0,32)
        pygame.display.set_caption("Tank War")
        Tank_Main.wall=Wall(screen,100,150,30,200)
        Tank_Main.my_tank=My_Tank(screen)

        if(len(Tank_Main.enemy_list)==0):
            for i in range(1,6):
                Tank_Main.enemy_list.add(Enemy_Tank(screen))

        while True:
            screen.fill((0,0,0))
            for i,text in enumerate(self.show_message(),0):
                screen.blit(text,(0,5+(30*i)))
            Tank_Main.wall.display()
            Tank_Main.wall.hit_other()
            if (len(Tank_Main.enemy_list) < 5):
                Tank_Main.enemy_list.add(Enemy_Tank(screen))
            self.get_event(Tank_Main.my_tank,screen)
            if(Tank_Main.my_tank):
                Tank_Main.my_tank.hit_enemy_missile()
            if(Tank_Main.my_tank and Tank_Main.my_tank.live):
                Tank_Main.my_tank.display()
                Tank_Main.my_tank.move()
            else:
                Tank_Main.my_tank=None
                #sys.exit()
            for enemy in Tank_Main.enemy_list:
                enemy.display()
                enemy.random_move()
                enemy.random_fire()
            for m in Tank_Main.my_tank_missile_list:
                if(m.live):
                    m.display()
                    m.hit_tank()
                    m.move()
                else:
                    Tank_Main.my_tank_missile_list.remove(m)
            for m in Tank_Main.enemy_missile_list:
                if (m.live):
                    m.display()
                    m.move()
                else:
                    Tank_Main.enemy_missile_list.remove(m)
            for explode in Tank_Main.explode_list:
                explode.display()
            time.sleep(0.03)
            pygame.display.update()

    def get_event(self,my_tank,screen):
        for event in pygame.event.get():
            if(event.type==QUIT):
                self.end_game()
            if(event.type==KEYDOWN and (not my_tank) and event.key==K_n):
                Tank_Main.my_tank=My_Tank(screen)
            if(event.type==KEYDOWN and my_tank):
                if(event.key==K_LEFT):
                    my_tank.direction="L"
                    my_tank.stop=False
                    #my_tank.move()
                if(event.key==K_RIGHT):
                    my_tank.direction = "R"
                    my_tank.stop = False
                    #my_tank.move()
                if (event.key == K_UP):
                    my_tank.direction = "U"
                    my_tank.stop = False
                    #my_tank.move()
                if (event.key == K_DOWN):
                    my_tank.direction = "D"
                    my_tank.stop = False
                    #my_tank.move()
                if (event.key == K_ESCAPE):
                    self.end_game()
                if (event.key == K_SPACE):
                    m=my_tank.fire()
                    m.good_missile=True
                    Tank_Main.my_tank_missile_list.append(m)

            if(event.type==KEYUP and my_tank):
                if(event.key==K_LEFT or event.key==K_RIGHT or event.key==K_UP or event.key==K_DOWN):
                    my_tank.stop=True

    def end_game(self):
        sys.exit()

    def show_message(self):
        font=pygame.font.SysFont("gigi",24)
        text_sf1=font.render("Enemy count:%d" %len(Tank_Main.enemy_list),True,(255,0,0))
        text_sf2=font.render("Our missile remains:%d" %len(Tank_Main.my_tank_missile_list),True,(255,0,0))
        return text_sf1,text_sf2

class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.screen=screen

    def display(self):
        if(self.live):
            self.image = self.images[self.direction]
            self.screen.blit(self.image, self.rect)

class Tank(BaseItem):
    width=60
    height=60

    def __init__(self,screen,left,top):
        super().__init__(screen)
        self.direction = "D"
        self.speed=5
        self.stop=False
        self.images={}
        self.images["L"]=pygame.image.load("tank_img\\tank_L.gif")
        self.images["R"]=pygame.image.load("tank_img\\tank_R.gif")
        self.images["U"]=pygame.image.load("tank_img\\tank_U.gif")
        self.images["D"]=pygame.image.load("tank_img\\tank_D.gif")
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.live=True
        self.good_missile=False
        self.oldtop=self.rect.top
        self.oldleft=self.rect.left

    def stay(self):
        self.rect.top=self.oldtop
        self.rect.left=self.oldleft

    def move(self):
        if(not self.stop):
            self.oldleft=self.rect.left
            self.oldtop=self.rect.top
            if(self.direction=="L"):
                if(self.rect.left>0):
                    self.rect.left-=self.speed
                else:
                    self.rect.left=0
            elif(self.direction=="R"):
                if (self.rect.right < Tank_Main.width):
                    self.rect.right += self.speed
                else:
                    self.rect.right=Tank_Main.width
            elif(self.direction=="U"):
                if (self.rect.top > 0):
                    self.rect.top -= self.speed
                else:
                    self.rect.top=0
            elif (self.direction == "D"):
                if (self.rect.bottom < Tank_Main.height):
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom = Tank_Main.height

    def fire(self):
        m=Missile(self.screen,self)
        return m

class My_Tank(Tank):

    def __init__(self,screen):
        super().__init__(screen,400,400)
        self.stop=True
        self.live=True
        self.speed=8
    def hit_enemy_missile(self):
        hit_list=pygame.sprite.spritecollide(self,Tank_Main.enemy_missile_list,False)
        for m in hit_list:
            m.live=False
            Tank_Main.enemy_missile_list.remove(m)
            self.live=False
            explode=Explode(self.screen,self.rect)
            Tank_Main.explode_list.append(explode)

class Enemy_Tank(Tank):

    def __init__(self,screen):
        super().__init__(screen,randint(1,6)*100,200,)
        self.images = {}
        self.images["L"] = pygame.image.load("tank_img\\ene_L.gif")
        self.images["R"] = pygame.image.load("tank_img\\ene_R.gif")
        self.images["U"] = pygame.image.load("tank_img\\ene_U.gif")
        self.images["D"] = pygame.image.load("tank_img\\ene_D.gif")
        self.image = self.images[self.direction]
        self.step=8
        self.speed=3
        self.get_random_direction()

    def get_random_direction(self):
        r = randint(0, 4)
        if (r == 4):
            self.stop = True
        elif (r == 1):
            self.direction = "L"
            self.stop=False
        elif (r == 2):
            self.direction = "R"
            self.stop = False
        elif (r == 3):
            self.direction = "U"
            self.stop = False
        elif (r == 0):
            self.direction = "D"
            self.stop = False

    def random_move(self):
        if(self.live):
            if(self.step==0):
                self.get_random_direction()
                self.step=6
            else:
                self.move()
                self.step-=1

    def random_fire(self):
        r=randint(0,50)
        if(r==10 or r==20 or r==30):
            m=self.fire()
            Tank_Main.enemy_missile_list.add(m)
        else:
            return

class Missile(BaseItem):
    width=15
    height=15
    def __init__(self,screen,tank):
        super().__init__(screen)
        self.tank=tank
        self.direction = tank.direction
        self.speed = 12
        self.images = {}
        self.images["L"] = pygame.image.load("tank_img\\missile_L.gif")
        self.images["R"] = pygame.image.load("tank_img\\missile_R.gif")
        self.images["U"] = pygame.image.load("tank_img\\missile_U.gif")
        self.images["D"] = pygame.image.load("tank_img\\missile_D.gif")
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left +(tank.width- self.width)//2
        self.rect.top = tank.rect.top + (tank.height-self.height)//2
        self.live = True

    def move(self):
        if(self.live):
            if(self.direction=="L"):
                if(self.rect.left>0):
                    self.rect.left-=self.speed
                else:
                    self.live=False
            elif(self.direction=="R"):
                if (self.rect.right < Tank_Main.width):
                    self.rect.right += self.speed
                else:
                    self.live = False
            elif(self.direction=="U"):
                if (self.rect.top > 0):
                    self.rect.top -= self.speed
                else:
                    self.live = False
            elif (self.direction == "D"):
                if (self.rect.bottom < Tank_Main.height):
                    self.rect.bottom += self.speed
                else:
                    self.live = False

    def hit_tank(self):
        if(self.good_missile):
           hit_list= pygame.sprite.spritecollide(self,Tank_Main.enemy_list,False)
           for e in hit_list:
                e.live=False
                Tank_Main.enemy_list.remove(e)
                self.live=False
                explode=Explode(self.screen,e.rect)
                Tank_Main.explode_list.append(explode)



class Explode(BaseItem):

    def __init__(self,screen,rect):
        super().__init__(screen)
        self.live=True
        self.images=[pygame.image.load("tank_img\\explode1.gif"),pygame.image.load("tank_img\\explode2.gif"),pygame.image.load("tank_img\\explode3.gif")]
        self.step=0
        self.rect=rect

    def display(self):
        if(self.live):
            if(self.step==len(self.images)):
                self.live=False
            else:
                self.image=self.images[self.step]
                self.screen.blit(self.image,self.rect)
                self.step+=1
        else:
            pass

class Wall(BaseItem):
    def __init__(self,screen,left,top,width,height):
        super().__init__(screen)
        self.rect=Rect(left,top,width,height)
        self.color=(255,0,0)
    def display(self):
        self.screen.fill(self.color,self.rect)
    def hit_other(self):
        if(Tank_Main.my_tank):
            is_hit=pygame.sprite.collide_rect(self,Tank_Main.my_tank)
            if(is_hit):
                Tank_Main.my_tank.stop=True
                Tank_Main.my_tank.stay()
        if(Tank_Main.enemy_list):
            hit_list = pygame.sprite.spritecollide(self,Tank_Main.enemy_list,False)
            for  e in hit_list:
                e.stop=True
                e.stay()
        if(Tank_Main.enemy_missile_list):
            hit2_list= pygame.sprite.spritecollide(self,Tank_Main.enemy_missile_list,False)
            for e in hit2_list:
                e.live=False
        if(Tank_Main.my_tank_missile_list):
            hit3_list=pygame.sprite.spritecollide(self,Tank_Main.my_tank_missile_list,False)
            for e in hit3_list:
                e.live=False


tank=Tank_Main()
tank.start_game()



