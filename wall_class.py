import pygame

class Field:
    """
    Class for making the field
    
    Attributes:
        x,y : position of the top left corner of each rectangle
        width, height : dimension of the rectangle
        r_top_left, r_top_right, r_bot_left, r_bot_right : radius of each corner of the field, 
               these have to be smaller than half the size of the height
               
    This class actually makes an rectangle, we can use it to make four block on each
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

class Triangle:
    
    """
    Class for making the little triangle that we used so we do,'t have 90° angles

    Attributes:
        point : list of three tuples indacting de position of the triangle
                the fist coordinate is de right angle, then we go clockwise
                als we point niet willen gebruiken kunnen we ook x,y,width,height
                en dan  self.points = [(x, y + height),(x + width, y + height),(x + width//2, y)]
        color : color of the triangles
        
    """
    def __init__(self, points, color):
        self.points = points
        self.color = color
        
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)

#to actually draw the field (hypotetical at the moment, maybe use variables) :

triangle_top_left = Triangle([(100,0),(150,0),(100,150)], (0,0,0))
triangle_bottom_left = Triangle([...],(0,0,0))
triangle_top_right = Triangle([...],(0,0,0))
triangle_bottom_right = Triangle([...],(0,0,0))

block_top_left     = Field(0,  0,  100, 300, color=(0,0,0), r_bot_right=20)
block_bottom_left  = Field(0,  500, 100, 300, color=(0,0,0), r_top_right=20)
block_top_right    = Field(900, 0,  100, 300, color=(0,0,0), r_bot_left=20)
block_bottom_right = Field(900, 500 , 100, 300, color=(0,0,0), r_top_left=20)


    

"""
in game loop:

block_top_left.draw(screen)
block_bottom_left.draw(screen)
block_top_right.draw(screen)
block_bottom_right.draw(screen)
triangle_top_left.draw(screen)
triangle_bottom_left.draw(screen)
triangle_top_right.draw(screen)
triangle_bottom_right.draw(screen)

"""