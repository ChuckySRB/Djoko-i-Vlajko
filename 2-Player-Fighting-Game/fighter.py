import pygame
from pygame import mixer

# Controller button mappings for PlayStation controllers
# These are standard mappings that work with most PlayStation controllers
CONTROLLER_BUTTONS = {
    'CROSS': 0,      # X button (jump)
    'CIRCLE': 1,     # O button (attack 2)
    'SQUARE': 2,     # Square button (attack 1)
    'TRIANGLE': 3,   # Triangle button (special)
    'L1': 4,         # L1 button
    'R1': 5,         # R1 button
    'L2': 6,         # L2 button
    'R2': 7,         # R2 button
    'SHARE': 8,      # Share button
    'OPTIONS': 9,    # Options button
    'L3': 10,        # Left stick press
    'R3': 11,        # Right stick press
    'PS': 12,        # PS button
    'TOUCHPAD': 13   # Touchpad button
}

# Controller axis mappings
CONTROLLER_AXES = {
    'LEFT_X': 0,     # Left stick X axis
    'LEFT_Y': 1,     # Left stick Y axis
    'RIGHT_X': 2,    # Right stick X axis
    'RIGHT_Y': 3,    # Right stick Y axis
    'L2_TRIGGER': 4, # L2 trigger
    'R2_TRIGGER': 5  # R2 trigger
}

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
        self.attack_hit_this_attack=False  # Track if this attack already hit
        
        # Controller support
        self.controller_id = player - 1  # Player 1 uses controller 0, Player 2 uses controller 1
        self.controller = None
        if self.controller_id < pygame.joystick.get_count():
            self.controller = pygame.joystick.Joystick(self.controller_id)
            self.controller.init()

    def get_controller_input(self):
        """Get controller input for the fighter"""
        input_data = {
            'left': False,
            'right': False,
            'jump': False,
            'attack1': False,
            'attack2': False
        }
        
        if self.controller is None:
            return input_data
            
        try:
            # Get button states
            buttons = [self.controller.get_button(i) for i in range(self.controller.get_numbuttons())]
            
            # Get axis states
            axes = [self.controller.get_axis(i) for i in range(self.controller.get_numaxes())]
            
            # Left stick movement (with deadzone)
            deadzone = 0.3
            if len(axes) > CONTROLLER_AXES['LEFT_X']:
                left_x = axes[CONTROLLER_AXES['LEFT_X']]
                if left_x > deadzone:
                    input_data['right'] = True
                elif left_x < -deadzone:
                    input_data['left'] = True
            
            # Jump button (Cross/X button)
            if len(buttons) > CONTROLLER_BUTTONS['CROSS']:
                input_data['jump'] = buttons[CONTROLLER_BUTTONS['CROSS']]
            
            # Attack buttons
            if len(buttons) > CONTROLLER_BUTTONS['SQUARE']:
                input_data['attack1'] = buttons[CONTROLLER_BUTTONS['SQUARE']]
            if len(buttons) > CONTROLLER_BUTTONS['CIRCLE']:
                input_data['attack2'] = buttons[CONTROLLER_BUTTONS['CIRCLE']]
                
        except pygame.error:
            # Controller disconnected
            self.controller = None
            
        return input_data

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
            # Check for controller input first, then keyboard
            controller_input = self.get_controller_input()
            
            # movement for p1
            if self.player==1:
                # Controller input
                if controller_input['right']:
                    dx=SPEED
                    self.running=True
                if controller_input['left'] and dx<360:
                    dx=-SPEED
                    self.running=True
                if controller_input['jump'] and self.jump==False:
                    self.vely=-30
                    self.jump=True
                if controller_input['attack1']:
                    self.attack(target)
                    self.attack_type=1
                if controller_input['attack2']:
                    self.attack(target)
                    self.attack_type=2
                
                # Keyboard input (fallback)
                if key[pygame.K_d]:
                    dx=SPEED
                    self.running=True
                if key[pygame.K_a] and dx<360:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_w] and self.jump==False:
                    self.vely=-30
                    self.jump=True
                if key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(target)
                    if key[pygame.K_q]:
                        self.attack_type=1
                    if key[pygame.K_e]:
                        self.attack_type=2

            if self.player==2:
                # Controller input
                if controller_input['right']:
                    dx=SPEED
                    self.running=True
                if controller_input['left'] and dx<360:
                    dx=-SPEED
                    self.running=True
                if controller_input['jump'] and self.jump==False:
                    self.vely=-30
                    self.jump=True
                if controller_input['attack1']:
                    self.attack(target)
                    self.attack_type=1
                if controller_input['attack2']:
                    self.attack(target)
                    self.attack_type=2
                
                # Keyboard input (fallback)
                if key[pygame.K_RIGHT]:
                    dx=SPEED
                    self.running=True
                if key[pygame.K_LEFT] and dx<360:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_UP] and self.jump==False:
                    self.vely=-30
                    self.jump=True
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
                    self.attack_hit_this_attack=False  # Reset hit flag when attack ends
                    self.attack_cooldown=25
                if self.action==5:
                    self.hit=False
                    self.attacking=False
                    self.attack_cooldown=25

    def attack(self,target):
        if self.attack_cooldown==0:
            self.attacking=True
            self.attack_hit_this_attack=False  # Reset hit flag for new attack
            self.attack_misssound.play()
            # Attack rectangle will be created and checked in update() method
            # so it follows the player during the entire attack animation
    
    def get_attack_rect(self):
        """Create attack rectangle that follows the player's current position"""
        if not self.attacking:
            return None
            
        # Create larger attack rectangle
        attack_width = self.rect.width * 1.5  # 50% larger width
        attack_height = self.rect.height * 1.2  # 20% larger height
        
        # Position the attack rectangle based on player's facing direction
        if self.flip:
            attack_x = self.rect.centerx - attack_width
        else:
            attack_x = self.rect.centerx
            
        return pygame.Rect(attack_x, self.rect.y, attack_width, attack_height)
    
    def check_attack_hit(self, target):
        """Check if attack hits target during attack animation"""
        if not self.attacking or self.attack_hit_this_attack:
            return False
        
        # Only allow damage during first 2 frames of attack animation
        if self.action == 3 or self.action == 4:  # Attack actions
            if self.frame > 1:  # Only first 2 frames (0 and 1) can deal damage
                return False
            
        attack_rect = self.get_attack_rect()
        if attack_rect and attack_rect.colliderect(target.rect):
            self.attack_sound.play()
            target.health -= 10
            target.hit = True
            self.attack_hit_this_attack = True  # Mark that this attack already hit
            return True
        return False
    
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
        
        # Draw attack rectangle for debugging (uncomment to see attack hitbox)
        # if self.attacking:
        #     attack_rect = self.get_attack_rect()
        #     if attack_rect:
        #         pygame.draw.rect(surface, (0, 255, 0), attack_rect, 2)