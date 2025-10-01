import pygame
from pygame import mixer

# Controller button mappings for PlayStation controllers
CONTROLLER_BUTTONS = {
    'CROSS': 0,      # X button
    'CIRCLE': 1,     # O button
    'SQUARE': 2,     # Square button
    'TRIANGLE': 3,   # Triangle button
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

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load background image
        self.background = pygame.image.load("menu/DjokoiVlajkoPoster.png").convert_alpha()
        # Scale background to fit screen
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        
        # Load font
        self.font = pygame.font.Font("fonts/Tiny5-Regular.ttf", 40)
        self.small_font = pygame.font.Font("fonts/Tiny5-Regular.ttf", 30)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (240, 2, 5)
        self.BLACK = (50, 15, 12)
        self.GREEN = (0, 255, 0)
        
        # Menu options
        self.menu_options = ["ПОЧНИ ИГРУ", "ИЗАЂИ"]
        self.selected_option = 0
        
        # Menu state
        self.menu_active = True
        
        # Controller support
        self.controller = None
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
        
        # Load menu music (optional)
        try:
            pygame.mixer.music.load("music/bgmusic.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass  # Continue without music if file not found
    
    def handle_input(self, event):
        """Handle keyboard and controller input for menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.select_option()
        elif event.type == pygame.JOYBUTTONDOWN and self.controller:
            # Controller button input
            if event.button == CONTROLLER_BUTTONS['CROSS']:  # X button to select
                return self.select_option()
            elif event.button == CONTROLLER_BUTTONS['CIRCLE']:  # O button to go back (if needed)
                pass  # Could add back functionality here
        elif event.type == pygame.JOYAXISMOTION and self.controller:
            # Controller stick input for navigation
            if event.axis == CONTROLLER_AXES['LEFT_Y']:
                deadzone = 0.5
                if event.value < -deadzone:  # Up
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.value > deadzone:  # Down
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        return None
    
    def select_option(self):
        """Handle option selection"""
        if self.menu_options[self.selected_option] == "ПОЧНИ ИГРУ":
            self.menu_active = False
            return "start_game"
        elif self.menu_options[self.selected_option] == "ИЗАЂИ":
            return "quit"
        return None
    
    def draw(self, screen):
        """Draw the main menu"""
        # Draw background
        screen.blit(self.background, (0, 0))
        

        # Draw menu options centered in the middle of the bottom half of the screen

        # Calculate the starting y position so that the options are vertically centered in the bottom half
        options_height = len(self.menu_options) * 40
        bottom_half_top = self.screen_height // 2
        start_y = bottom_half_top + (self.screen_height // 4) - (options_height // 2)

        for i, option in enumerate(self.menu_options):
            y_pos = start_y + i * 60
            if i == self.selected_option:
                # Highlight selected option
                text = self.font.render(option, True, self.RED)
                # Add a background rectangle for selected option
                text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
                pygame.draw.rect(screen, self.BLACK, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
                pygame.draw.rect(screen, self.WHITE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10), 2)
            else:
                text = self.font.render(option, True, self.WHITE)
                text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
            
            screen.blit(text, text_rect)
        
        # Draw controller connection status in the top right corner
        controller_count = pygame.joystick.get_count()
        padding = 20
        if controller_count > 0:
            controller_text = self.small_font.render(f"Број џојстика: {controller_count}", True, self.GREEN)
            controller_rect = controller_text.get_rect(topright=(self.screen_width - padding, padding))
            screen.blit(controller_text, controller_rect)
        else:
            no_controller_text = self.small_font.render("Нема џојстика - удара се по тастатури", True, self.YELLOW)
            no_controller_rect = no_controller_text.get_rect(topright=(self.screen_width - padding, padding))
            screen.blit(no_controller_text, no_controller_rect)

    
    def is_active(self):
        """Check if menu is still active"""
        return self.menu_active
