import pygame
from pygame import mixer
class Fighter():
    def __init__(self,player,x,y,Flip,data,spritesheet,animationstep,sound,misssound):
        self.player=player
        self.size=data[0]
        self.img_scale=data[1]
        self.ofset=data[2]
        self.flip=Flip
        self.anm_list=self.loadimage(spritesheet, animationstep)   
        # 0:Still 1:Run 2:Jump 3:Attack1 4:Attack2 5:Damage 6:Die 7:fall
        self.action=0
        self.frame=0
        self.image=self.anm_list[self.action][self.frame]
        self.update_time=pygame.time.get_ticks()
        self.rect=pygame.Rect(x,y,120,180)
        self.vely=0
        self.running=False
        self.jump=False
        self.attacking=False
        self.attack_type=0
        self.attack_sound = sound
        self.attack_misssound = misssound
        self.attack_cooldown=0
        self.hit=False
        self.health=100
        self.alive=True

    def loadimage(self,spritesheet,animationstep):
        anm_list=[]
        for y, animate in enumerate(animationstep):
            temp_img_list=[]
            for x in range(animate):
                temp_img=spritesheet.subsurface(x*self.size,y*self.size,self.size,self.size)
                
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size*self.img_scale,self.size*self.img_scale)))
            anm_list.append(temp_img_list)
        return anm_list

    def move(self,sc_width,sc_height,surface,target,round_over):
        SPEED=5
        gravity=2
        dx=0
        dy=0
        self.running=False
        self.attack_type=0

        key=pygame.key.get_pressed()
        if self.attacking==False and self.alive==True and round_over==False:
            # movement for p1
            if self.player==1:
                if key[pygame.K_d]:
                    dx=SPEED
                    self.running=True
                    
                if key[pygame.K_a] and dx<360:
                    dx=-SPEED
                    self.running=True
                # jump
                if key[pygame.K_w] and self.jump==False:
                    self.vely=-30
                    self.jump=True

                # attack
                if key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(target)
                    if key[pygame.K_q]:
                        self.attack_type=1
                    if key[pygame.K_e]:
                        self.attack_type=2


            if self.player==2:
                if key[pygame.K_RIGHT]:
                    dx=SPEED
                    self.running=True
                if key[pygame.K_LEFT] and dx<360:
                    dx=-SPEED
                    self.running=True
                # jump
                if key[pygame.K_UP] and self.jump==False:
                    self.vely=-30
                    self.jump=True

                # attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    if key[pygame.K_KP1]:
                        self.attack_type=1
                    if key[pygame.K_KP2]:
                        self.attack_type=2

        self.vely+=gravity
        dy+=self.vely

        if self.rect.left + dx < 0:
            dx=-self.rect.left
        if self.rect.right + dx > sc_width:
            dx= sc_width - self.rect.right
        if self.rect.bottom + dy >sc_height - 70:
            self.vely=0
            self.jump=False
            dy=sc_height - 70 - self.rect.bottom

        # facing
        if key[pygame.K_a]:
            self.flip=True
        if target.rect.centerx > self.rect.centerx:
            self.flip=False
        else:
            self.flip=True
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1        

        self.rect.x += dx
        self.rect.y +=dy

    def update(self):
        # check performed action 
        if self.health<=0:
            self.health=0
            self.alive=False
            self.update_action(6) 
        elif self.hit==True:
            self.update_action(5)   
        elif self.attacking==True:
            if self.attack_type==1:
                self.update_action(3)
            if self.attack_type==2:
                self.update_action(4)
        elif self.jump==True:
            self.update_action(2)
        elif self.running==True:
            self.update_action(1)
        else:
            self.update_action(0)

            
        cooldown=70
        self.image=self.anm_list[self.action][self.frame]
        if pygame.time.get_ticks() - self.update_time>cooldown:
            self.frame+=1
            self.update_time=pygame.time.get_ticks()
        if self.frame>=len(self.anm_list[self.action]):
            if self.alive==False:
                self.frame=len(self.anm_list[self.action])-1
            else:
                self.frame=0
                if self.action==3 or self.action==4:
                    self.attacking=False
                    self.attack_cooldown=25
                if self.action==5:
                    self.hit=False
                    self.attacking=False
                    self.attack_cooldown=25

    def attack(self,target):
        if self.attack_cooldown==0:
            self.attacking=True
            self.attack_misssound.play()
            attack_rect=pygame.Rect(self.rect.centerx - (self.rect.width*self.flip), self.rect.y,self.rect.width,self.rect.height)
            if attack_rect.colliderect(target.rect):
                self.attack_sound.play()
                target.health-=10
                target.hit=True

            # pygame.draw.rect(surface,(0,255,0),attack_rect)
    
    def update_action(self,new_action):
        #if new action if sifferent to previous one
        if new_action!=self.action:
            self.action=new_action
            #updated animantion
            self.frame=0
            self.update_time=pygame.time.get_ticks()

    def draw(self,surface):
        img=pygame.transform.flip(self.image,self.flip,False)
        # pygame.draw.rect(surface,(255,0,0),self.rect )
        surface.blit(img, (self.rect.x - (self.ofset[0]-self.img_scale),self.rect.y - (self.ofset[1]-self.img_scale)))