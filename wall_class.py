import pygame

class Field:
    """
    Class for making the field
    
    Attributes:
        x,y : position of the top left corner of each rectangle
        width, height : dimension of the rectangle
        r_top_left, r_top_right, r_bot_left, r_bot_right : radius of each corner of the field, 
               these have to be smaller than half the size of the height
               
    This class actually makes an rectangle, we can use it to make one big field with inside it four block on each
    corner to shape de field and to make goals
    
    """
    def __init__(self,x,y,width,height, color, r_top_left=0, r_top_right=0, r_bot_left=0, r_bot_right=0):
        self.rect = pygame.Rect(x, y, width, height) #door dit te gebruiken zal de botsing functie in ball_class makkelijker zijn
        self.color = color
        self.r_top_left = r_top_left 
        self.r_top_right = r_top_right
        self.r_bot_left = r_bot_left
        self.r_bot_right = r_bot_right
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect, 
            border_top_left_radius=self.r_top_left,
            border_top_right_radius=self.r_top_right,
            border_bottom_left_radius=self.r_bot_left,
            border_bottom_right_radius=self.r_bot_right)

        
field = Field(80, 60, 520, 300, color=(255,255,255))


block_top_left     = Field(80,  60,  60, 100, color=(0,0,0), r_bot_right=20)
block_bottom_left  = Field(80,  260, 60, 100, color=(0,0,0), r_top_right=20)
block_top_right    = Field(540, 60,  60, 100, color=(0,0,0), r_bot_left=20)
block_bottom_right = Field(540, 260, 60, 100, color=(0,0,0), r_top_left=20)


"""
in game loop:
field.draw(screen)
block_top_left.draw(screen)
block_bottom_left.draw(screen)
block_top_right.draw(screen)
block_bottom_right.draw(screen)
"""