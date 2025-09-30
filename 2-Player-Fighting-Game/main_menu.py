import pygame
from pygame import mixer

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
        
        # Menu options
        self.menu_options = ["ПОЧНИ ИГРУ", "ИЗАЂИ"]
        self.selected_option = 0
        
        # Menu state
        self.menu_active = True
        
        # Load menu music (optional)
        try:
            pygame.mixer.music.load("music/bgmusic.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass  # Continue without music if file not found
    
    def handle_input(self, event):
        """Handle keyboard input for menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.select_option()
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
        # # Draw instructions
        # instruction_text = self.small_font.render("Use UP/DOWN or W/S to navigate, ENTER/SPACE to select", True, self.WHITE)
        # instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        # screen.blit(instruction_text, instruction_rect)
        
        # # Draw player controls info
        # controls_text1 = self.small_font.render("Player 1: WASD + Q/E to attack", True, self.WHITE)
        # controls_text2 = self.small_font.render("Player 2: Arrow Keys + Numpad 1/2 to attack", True, self.WHITE)
        
        # controls_rect1 = controls_text1.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        # controls_rect2 = controls_text2.get_rect(center=(self.screen_width // 2, self.screen_height - 70))
        
        # screen.blit(controls_text1, controls_rect1)
        # screen.blit(controls_text2, controls_rect2)
    
    def is_active(self):
        """Check if menu is still active"""
        return self.menu_active
