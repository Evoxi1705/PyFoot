from base_classes import *
from constants import *
from wall_class import *
import pygame 

walls = [block_top_left, block_bottom_left, block_top_right, block_bottom_right, block_top, block_bottom]
triangles = [triangle_bottom_left, triangle_top_left, triangle_bottom_right, triangle_top_right]

class Ball(DynamicObject):
    """
    Represents the ball in the game world.

    Handles physics, bouncing, collision with players and triangles, and goal detection.

    Attributes:
        radius (int): Radius of the ball in pixels.
        bounce_factor (float): Velocity multiplier applied after a bounce.
        friction (float): Deceleration rate when ball rolls on the ground.
        goal_timer (int): Countdown in milliseconds for the GOAL inscription display.
    """
    def __init__(self,pos,velocity,radius,bounce_factor=BOUNCE_FACTOR):
        super().__init__(pos, velocity, radius*2, radius*2)
        self.radius = radius
        self.bounce_factor = bounce_factor
        self.friction = FRICTION_BALL
        self.goal_timer = 0
        self.image = pygame.image.load("media/fireball-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
    
    def update(self, dt, field, player, level,triangles):
        """
        Updates the ball's physics, collisions, and goal state each frame.

        Args:
            dt (float): Delta time in seconds since the last frame.
            field: The field object defining the play area boundaries.
            player (Player): The human-controlled character.
            bot (Bot): The AI-controlled character.
            triangles (list): List of Triangle objects for bounce detection.
        """

        self._apply_gravity(dt)      
        self._apply_movement(dt)     
        self._apply_friction(dt, field)
        self._handle_borders(field)
        self.bounce_triangle(triangles)
        self.ball_player_collision(player)
        self.ball_player_collision(level)
        
    def draw(self, screen):
        """Renders the ball as a circle onto the provided Pygame surface."""
        screen.blit(self.image, (self.pos.x, self.pos.y)) 
  
        
    def _handle_borders(self, field): 
        """ Keeps the object inside the game world. """
        if self.get_bottom() > field.get_bottom():
            self.pos.y = field.get_bottom() - self.height 
            self.velocity.y = -abs(self.velocity.y) * self.bounce_factor

        if self.get_top() < field.get_top():
            self.pos.y = field.get_top()
            self.velocity.y = abs(self.velocity.y) * self.bounce_factor

        if self.get_right() > field.get_right():
            if self.get_top() < BH or self.get_bottom() > SCREEN_HEIGHT - BH:
                self.pos.x = field.get_right() - self.width
                self.velocity.x = -abs(self.velocity.x) * self.bounce_factor

        if self.get_left() < field.get_left():
            if self.get_top() < BH or self.get_bottom() > SCREEN_HEIGHT - BH:
                self.pos.x = field.get_left()
                self.velocity.x = abs(self.velocity.x) * self.bounce_factor
        
    def bounce_triangle(self, triangles):
        """
        Resolves collision between the ball and triangle corner pieces.
        Uses closest-point-on-segment math to compute the bounce normal.

        Args:
            triangles (list): List of Triangle objects to check against.
        """
        cx = self.pos.x + self.radius
        cy = self.pos.y + self.radius
        
        for triangle in triangles:
          x, y, s = triangle.pos.x, triangle.pos.y, triangle.size
          
          if triangle.corner == "bottom-left":
              p1, p2 = (x, y), (x + s, y + s)
          elif triangle.corner == "bottom-right":
              p1, p2 = (x + s, y), (x, y + s)
          elif triangle.corner == "top-left":
              p1, p2 = (x + s, y), (x, y + s)
          elif triangle.corner == "top-right":
              p1, p2 = (x, y + s), (x + s, y)
          
          edge_x = p2[0] - p1[0]
          edge_y = p2[1] - p1[1]    
        
          edge_length_sqrt = edge_x**2 + edge_y**2
        
          t = ((cx - p1[0]) * edge_x + (cy - p1[1]) * edge_y) / edge_length_sqrt
          if t < 0:
              t = 0
          if t > 1:
              t = 1
        
          closest_x = p1[0] + t * edge_x
          closest_y = p1[1] + t * edge_y
        
          dx = cx - closest_x
          dy = cy - closest_y
          distance = (dx**2 + dy**2) ** 0.5
          

          if distance <= self.radius and distance != 0:
              normal_x = dx / distance
              normal_y = dy / distance
    
              overlap = self.radius - distance + 0.5
              self.pos.x += normal_x * overlap
              self.pos.y += normal_y * overlap
              
              dot = self.velocity.x * normal_x + self.velocity.y * normal_y
              
              if dot < 0:
                  self.velocity.x = (self.velocity.x - 2 * dot * normal_x) * self.bounce_factor
                  self.velocity.y = (self.velocity.y - 2 * dot * normal_y) * self.bounce_factor            
                  
                  if abs(self.velocity.x) < 50: self.velocity.x = 50 * (1 if self.velocity.x >= 0 else -1)
                  if abs(self.velocity.y) < 50: self.velocity.y = 50 * (1 if self.velocity.y >= 0 else -1)    

    def ball_player_collision(self, player):
        """
        Resolves collision between the ball and a rectangular character.
        Applies impulse based on relative velocity along the collision normal.

        Args:
            player (Character): The character to check collision against.
        """
        cx = self.pos.x + self.radius
        cy = self.pos.y + self.radius
        
        closest_x = max(player.pos.x, min(cx, player.pos.x + player.width))
        closest_y = max(player.pos.y, min(cy, player.pos.y + player.height))
        
        dx = cx - closest_x
        dy = cy - closest_y
        
        distance = (dx**2 + dy**2) **0.5
        
        if distance <= self.radius and distance != 0:
            normal_x = dx / distance
            normal_y = dy / distance
  
            overlap = self.radius - distance + 1
            self.pos.x += normal_x * overlap
            self.pos.y += normal_y * overlap
            
            rel_vx = self.velocity.x - player.velocity.x
            rel_vy = self.velocity.y - player.velocity.y
            
            dot = rel_vx * normal_x + rel_vy * normal_y
            
            if dot < 0: #only if they move towards each other
                self.velocity.x = (self.velocity.x - 2 * dot * normal_x) * self.bounce_factor
                self.velocity.y = (self.velocity.y - 2 * dot * normal_y) * self.bounce_factor
            
                # Only transfer the player velocity component along the normal
                player_dot = player.velocity.x * normal_x + player.velocity.y * normal_y
                if player_dot > 0:  # player pushing toward ball
                    self.velocity.x += normal_x * player_dot * self.bounce_factor
                    self.velocity.y += normal_y * player_dot * self.bounce_factor
            
      
    def goal(self, field):
        """
        Detects if the ball has crossed either goal line and resets it to center.

        Returns:
            str: 'player' if the player scored, 'bot' if the bot scored, None otherwise.
        """
        if self.pos.x + self.radius < BW:
            self.pos.x = SCREEN_WIDTH/2 
            self.pos.y = SCREEN_HEIGHT/2
            self.velocity.x = 0
            self.velocity.y = 0
            self.goal_timer = 2000
            return "bot"
            
        if self.pos.x + self.radius > SCREEN_WIDTH - BW:
            self.pos.x = SCREEN_WIDTH/2 
            self.pos.y = SCREEN_HEIGHT/2
            self.velocity.x = 0
            self.velocity.y = 0
            self.goal_timer = 2000
            return "player"
            
    def draw_goal_inscription(self, screen, dt):
        """
        Displays a GOAL inscription at the center of the screen for 2 seconds after a goal.

        Args:
            screen: The Pygame surface to draw on.
            dt (float): Delta time in seconds since the last frame.
        """
        if self.goal_timer > 0:
            self.goal_timer -= dt * 1000
            font = pygame.font.SysFont(None, 120)
            text = font.render("GOAL!", True, (255, 255, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text, rect)
                    
        

                
        
    
       
        
        