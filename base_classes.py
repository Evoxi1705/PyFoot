from abc import ABC, abstractmethod
import pygame
from constants import *
from class_tools import Vector2

"""
This code implements a frame-independent game object hierarchy. 
By utilizing Delta Time (dt), physics calculations remain consistent across 
varying hardware performance and frame rates.
"""

class Entity(ABC):
    """
    Abstract base class for all objects that exist in the game world.
    
    Provides core spatial properties and boundary helper methods for 
    manual collision detection.

    Attributes:
        pos (Vector2): Current coordinates (x, y) in pixels.
        height (int): Vertical dimension of the entity in pixels.
        width (int): Horizontal dimension of the entity in pixels.
    """
    pos: Vector2 # Attribute hint: helps the editor remember what type it was
    height: int
    width: int

    # Way to access the dimensions of the character faster
    def get_top(self): return self.pos.y
    def get_bottom(self): return self.pos.y + self.height
    def get_left(self): return self.pos.x
    def get_right(self): return self.pos.x + self.width

    def __init__(self, pos: Vector2, height: int, width: int):
        self.pos = pos
        self.height = height
        self.width = width

    def collides_with(self, other: "Entity"):
        """
        Standard AABB collision check.
        Returns True if this entity overlaps with another entity.
        """
        return (self.get_left() < other.get_right() and
                self.get_right() > other.get_left() and
                self.get_top() < other.get_bottom() and
                self.get_bottom() > other.get_top())

    @abstractmethod
    def draw(self, screen):
        """
        Renders the entity onto the provided Pygame surface.
        Must be implemented by concrete subclasses.
        """
        pass

class DynamicObject(Entity):
    """
    Base class for objects affected by physics, gravity, and movement.

    Attributes:
        velocity (Vector2): Current speed in pixels per second.
    """
    velocity: Vector2

    def __init__(self, pos: Vector2, velocity: Vector2, height, width):
        super().__init__(pos, height, width)
        self.velocity = velocity
        self.friction = FRICTION_CARS

    def update(self, dt, field):
        """
        Updates the object's position using Euler integration.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        self._apply_gravity(dt)
        self._apply_movement(dt)
        self._handle_borders(field)
        self._apply_friction(dt, field)

    def _apply_movement(self, dt):
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    def _apply_friction(self, dt, field):
        """Deccelarates the object based on friction with the surface. """
        if self.get_bottom() >= field.get_bottom():
            if abs(self.velocity.x) > 0.1: # Moving left means negative velocity so abs() and 0.1 is a treshold to make sure we stay above it
                self.velocity.x *= (self.friction**(dt*60))
                # dt*60 is to represent the velocity remaining after 1/60 of a second
            else:
                self.velocity.x = 0

    def _apply_gravity(self, dt):
        """
        Applies downward acceleration to the vertical velocity.
        """
        self.velocity.y += GRAVITY*dt
        
    def _handle_borders(self, field): # The first _ means the method is meant to be local, not called outside the class
        """ Keeps the object inside the game world. """
        if self.get_bottom() > field.get_bottom():
            self.pos.y = field.get_bottom() - self.height 
            self.velocity.y = 0

        if self.get_top() < field.get_top():
            self.pos.y = field.get_top()
            self.velocity.y = 0

        if self.get_right() > field.get_right():
            self.pos.x = field.get_right() - self.width
            self.velocity.x = 0

        if self.get_left() < field.get_left():
            self.pos.x = field.get_left()
            self.velocity.x = 0

    def collision_player_bot(self, other:"DynamicObject"):
        """
        Resolves overlap between the player and bot using AABB separation.
        Pushes both characters apart and exchanges velocity components.

        Args:
            player (Player): The human-controlled character.
            bot (Bot): The AI-controlled character.
        """
        if self.collides_with(other):
            overlap_x = min(self.get_right(), other.get_right()) - max(self.get_left(), other.get_left())
            overlap_y = min(self.get_bottom(), other.get_bottom()) - max(self.get_top(), other.get_top())
            
            if overlap_x < overlap_y:
                push = overlap_x / 2 + 1.0
                if self.pos.x < other.pos.x:
                    self.pos.x -= push
                    other.pos.x += push
                else:
                    self.pos.x += push
                    other.pos.x -= push
                self.velocity.x, other.velocity.x = other.velocity.x * 0.5, self.velocity.x * 0.5
            else:
                push = overlap_y / 2 + 1.0
                if self.pos.y < other.pos.y:
                    self.pos.y -= push
                    other.pos.y += push
                else:
                    self.pos.y += push
                    other.pos.y -= push
                self.velocity.y, other.velocity.y = other.velocity.y * 0.5, self.velocity.y * 0.5

    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class StaticObject(Entity):
    """
    Abstract base class for all static objects in the game world.
    """
    def __init__(self, pos: Vector2, height, width):
        super().__init__(pos, height, width)
    
    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class Character(DynamicObject):
    """ 
    Base class for all characters in the game world.

    Handles horizontal acceleration, jumping, and a state-managed boost system.
    Horizontal drag is calculated using exponential decay for frame-independence.

    Attributes:
        pos (Vector2): Current coordinates (x, y) in pixels.
        velocity (Vector2): Current speed in pixels per second.
        jump_force (float): Initial upward velocity applied during a jump.
        boost_force (float): Acceleration added during the boost phase.
        boost_time (int): Duration of the boost effect in milliseconds.
        max_speed (float): Terminal horizontal velocity under normal movement.
        max_boost_speed (float): Terminal horizontal velocity while boosting.
        cooldown_time (int): Required delay between boosts in milliseconds.
        is_boosting (bool): State tracker for the boost mechanic.
    """
    def __init__(self, 
                 pos: Vector2, 
                 velocity: Vector2,
                 height, 
                 width,
                 jump_force=JUMP_FORCE, 
                 boost_force=BOOST_FORCE, 
                 boost_time=BOOST_TIME,
                 max_speed = MAX_SPEED, 
                 max_boost_speed=MAX_BOOST_SPEED,
                 cooldown_time=COOLDOWN):
        
        super().__init__(pos, velocity, height, width)
        self.jump_force = jump_force
        self.boost_force = boost_force
        self.boost_time = boost_time
        self.max_speed = max_speed
        self.max_boost_speed = max_boost_speed
        self.cooldown_time = cooldown_time

        self.speed_base = MAX_SPEED
        self.jump_base = JUMP_FORCE
        self.boost_base = BOOST_TIME
        self.faster_collected = 0
        self.highjump_collected = 0
        self.longerboost_collected = 0
        self.is_boosting = False 
        self.boost_start = 0
        self.friction = FRICTION_CARS
        
    def move_left(self, dt):
        """Accelerates the character to the left up to max_speed"""
        if self.velocity.x > -self.max_speed:
            self.velocity.x -= ACCELERATION*dt
            
     
    def move_right(self, dt):
        """Accelerates the character to the right up to max_speed"""
        if self.velocity.x < self.max_speed:
            self.velocity.x += ACCELERATION*dt

    def boost(self):
        """
        Triggers a timed speed increase with a cooldown restriction.
        
        Uses pygame.time.get_ticks() to manage the duration and cooldown 
        independently of the physics update.
        """
        now = pygame.time.get_ticks()

        if not self.is_boosting:
            if (now - (self.boost_start + self.boost_time)) > self.cooldown_time:
                self.is_boosting = True
                self.boost_start = now

        if self.is_boosting:
            if (now - self.boost_start) <= self.boost_time:
                # Checks wether we are moving to the right or to the left
                direction = 1 if self.velocity.x >= 0 else -1
                self.velocity.x = self.max_boost_speed * direction
            else:
                self.is_boosting = False

    def jump(self, field):
        """
        Initiates a jump if the character is currently grounded.
        """
        if self.get_bottom() >= field.get_bottom():
            self.velocity.y = -self.jump_force
            
    def bounce_triangle(self, triangles):
        SQRT2_INV = 1 / (2 ** 0.5) #inward normal have angle 1/(2**0.5)
        outward = {
            "bottom-left":  ( SQRT2_INV, -SQRT2_INV),
            "bottom-right": (-SQRT2_INV, -SQRT2_INV),
            "top-left":     ( SQRT2_INV,  SQRT2_INV),
            "top-right":    (-SQRT2_INV,  SQRT2_INV),
        }
        corners = [(self.pos.x, self.pos.y),
                   (self.pos.x, self.pos.y + self.height),
                   (self.pos.x + self.width, self.pos.y),
                   (self.pos.x + self.width, self.pos.y + self.height)]
    
        for triangle in triangles:
            x, y, s = triangle.pos.x, triangle.pos.y, triangle.size
            normal_x, normal_y = outward[triangle.corner] #'chosing' the right corner
    
            if triangle.corner in ("bottom-left", "top-right"):
                p1 = (x, y)
            else:
                p1 = (x + s, y)
    
            for cx, cy in corners:
                
                signed_dist = (cx - p1[0]) * normal_x + (cy - p1[1]) * normal_y
                
                if signed_dist < 6:
                    overlap = 6 - signed_dist
                    self.pos.x += normal_x * overlap
                    self.pos.y += normal_y * overlap
                    dot = self.velocity.x * normal_x + self.velocity.y * normal_y
                    if dot < 0:
                        self.velocity.x -= dot * normal_x
                        self.velocity.y -= dot * normal_y

class Player(Character):
    """
    Represents the human-controlled character.

    Handles keyboard input and translates it into character actions.

    Attributes:
        controls (dict): Mapping of actions to pygame key constants.
    """

    def __init__(self, 
                 pos, 
                 velocity, 
                 height, 
                 width,
                 controls=PLAYER1_CONTROLS,
                 **kwargs):
        
        self.controls = controls
        super().__init__(pos, velocity, height, width, **kwargs)
        self.image = pygame.image.load("redcar.png")
        self.image = pygame.transform.scale(self.image, (width, height))

    def _handle_inputs(self, dt, field):
        """
        Interprets the input from the player.
        """
        keys = pygame.key.get_pressed()

        if keys[self.controls["left"]]:
            self.move_left(dt)

        if keys[self.controls["right"]]:
            self.move_right(dt)

        if keys[self.controls["jump"]]:
            self.jump(field)

        if keys[self.controls["boost"]]:
            self.boost()

    def draw(self, screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))

class Bot(Character):
    """
    Represents the AI-controlled character.

    Makes decisions based on the game state each frame.

    Attributes:
        player (Player): Reference to the human-controlled character.
        ball (Ball): Reference to the ball object.
    """
    def __init__(self, 
                 pos: Vector2, 
                 velocity: Vector2,
                 height, 
                 width, 
                 player,
                 ball,
                 **kwargs):

        self.player = player
        self.ball: "Ball" = ball
        super().__init__(pos, velocity, height, width, **kwargs)
        self.image = pygame.image.load("blackcar.png")
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        """Renders the bot as a rectangle onto the provided Pygame surface."""
        screen.blit(self.image, (self.pos.x, self.pos.y))

    @abstractmethod
    def _handle_action(self, dt):
        """Abstract method — subclasses must implement per-frame AI decision logic."""
        pass

class EasyBot(Bot):
    """
    AI-controlled character with slow reactions and predictable behavior.

    Decisions are delayed by DELAY_EASYBOT to simulate slow reaction time.
    Uses a finite state machine to switch between Attack and Defend states.

    Attributes:
        current_action (str): The current movement direction ('left' or 'right').
        last_action (int): Timestamp in milliseconds of the last decision made.
        FSM (FSM): The finite state machine managing state transitions.
    """
    def __init__(self, 
                 pos, 
                 velocity, 
                 height, 
                 width, 
                 player, 
                 ball,
                 **kwargs):
        
        super().__init__(pos, velocity, height, width, player, ball, **kwargs)
        self.current_action = ""
        self.last_action = 0
        self.FSM = FSM()
        self.FSM.states["Attack"] = Attack(self)
        self.FSM.states["Defend"] = Defend(self)
        self.FSM.set_state("Attack")  # start in attack

    def _handle_action(self, dt, field, starting_time, active_powerups=None):
        """Evaluates the game state and delegates to the FSM each frame."""
        if self.ball.pos.x < self.pos.x:
            self.FSM.change_state(self.FSM.states["Attack"])
            self.FSM.execute(dt, field, active_powerups)
        else:
            self.FSM.change_state(self.FSM.states["Defend"])
            self.FSM.execute(dt, field, active_powerups)

class MediumBot(Bot):
    """
    AI-controlled character with no reaction delay and smarter positioning.

    Reacts instantly to the ball's position each frame.
    Uses a finite state machine with improved attack and defend states.

    Attributes:
        current_action (str): The current movement direction ('left' or 'right').
        last_action (int): Timestamp in milliseconds of the last decision made.
        FSM (FSM): The finite state machine managing state transitions.
    """

    def __init__(self, 
                 pos, 
                 velocity, 
                 height, 
                 width, 
                 player, 
                 ball, 
                 **kwargs):
        super().__init__(pos, velocity, height, width, player, ball, **kwargs)
        self.current_action = ""
        self.last_action = 0
        self.FSM = FSM()
        self.FSM.states["Attack"] = MediumAttack(self)
        self.FSM.states["Defend"] = MediumDefend(self)

    def _handle_action(self, dt, field, starting_time, active_powerups=None):
        """Evaluates the game state and delegates to the FSM each frame."""
        if active_powerups:
            nearest = active_powerups[0]
            if nearest.pos.x < self.pos.x:
                self.move_left(dt)
            else:
                self.move_right(dt)
            if nearest.pos.y < self.get_top():
                self.jump(field)
        elif self.ball.pos.x < self.pos.x:
            self.FSM.change_state(self.FSM.states["Attack"])
            self.FSM.execute(dt, field, active_powerups)
        else:
            self.FSM.change_state(self.FSM.states["Defend"])
            self.FSM.execute(dt, field, active_powerups)

class HardBot(Bot):
    """
    AI-controlled character that becomes progressively faster over the match.

    Speed scales linearly with match progress from start to end.
    Uses a finite state machine with the most aggressive states.

    Attributes:
        starting_time (int): Match start time in milliseconds used to compute speed scaling.
        FSM (FSM): The finite state machine managing state transitions.
    """
    def __init__(self, 
                 pos, 
                 velocity, 
                 height, 
                 width, 
                 player, 
                 ball,
                 starting_time, 
                 **kwargs):
        
        super().__init__(pos, velocity, height, width, player, ball, **kwargs)
        self.starting_time = starting_time
        self.FSM = FSM()
        self.FSM.states["Attack"] = HardAttack(self)
        self.FSM.states["Defend"] = HardDefend(self)
        
    def _handle_action(self, dt, field, starting_time, active_powerups=None):
        """Evaluates the game state and delegates to the FSM each frame."""
        # Making the bot faster and faster
        progress = (pygame.time.get_ticks() - starting_time)/GAME_DURATION
        self.max_speed = MAX_SPEED*(1 + progress)

        # Go for powerup only when ball is not on the bot's side
        if active_powerups and self.ball.pos.x > self.pos.x:
            nearest = active_powerups[0]
            if nearest.pos.x < self.pos.x:
                self.move_left(dt)
            else:
                self.move_right(dt)
            if nearest.pos.y < self.get_top():
                self.jump(field)
        elif self.ball.pos.x < self.pos.x:
            self.FSM.change_state(self.FSM.states["Attack"])
            self.FSM.execute(dt, field, active_powerups)
        else:
            self.FSM.change_state(self.FSM.states["Defend"])
            self.FSM.execute(dt, field, active_powerups)

class State:
    """
    Base class for all FSM states.

    Attributes:
        bot (Bot): Reference to the bot this state controls.
    """
    def __init__(self, bot):
        self.bot = bot

    def execute(self, dt, field, active_powerups=None):
        pass

class Attack(State):
    """
    FSM state that moves the bot toward the ball to attempt a shot.

    Decisions are gated by _should_act() to allow subclasses to control reaction timing.
    The bot also boosts when the ball is in the opponent's half.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def _should_act(self):
        """Returns True if enough time has passed since the last action (EasyBot delay)."""
        now = pygame.time.get_ticks()
        return now - self.bot.last_action > DELAY_EASYBOT

    def run(self, dt, field, active_powerups=None):
        """Executes attack logic: moves toward the ball and jumps if needed."""
        # Decision making
        if self._should_act():
            self.bot.last_action = pygame.time.get_ticks()
            if self.bot.pos.x < self.bot.ball.get_right():
                self.bot.current_action = "right"
            elif self.bot.pos.x > self.bot.ball.pos.x:
                self.bot.current_action = "left"

            if self.bot.ball.get_bottom() < self.bot.get_top():
                self.bot.jump(field)

        # Boost execution
        if self.bot.ball.pos.x > SCREEN_WIDTH/2:
            self.bot.boost()

        if self.bot.current_action == "right":
            self.bot.move_right(dt)
        elif self.bot.current_action == "left":
            self.bot.move_left(dt)

class Defend(State):
    """
    FSM state that moves the bot back toward its own goal.

    The bot repositions to the right side of the field and jumps if the ball is above it.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def run(self, dt, field, active_powerups=None):
        """Executes defend logic: moves to goal position and jumps if needed."""
        if self.bot.pos.x < (SCREEN_WIDTH - BW):
            self.bot.move_right(dt)
        if self.bot.ball.get_bottom() < self.bot.get_top():
            self.bot.jump(field)

class MediumAttack(Attack):
    """Attack state with no reaction delay — acts every frame."""
    def __init__(self, bot):
        super().__init__(bot)

    def _should_act(self):
        """Always returns True, removing the EasyBot reaction delay."""
        return True

class MediumDefend(Defend):
    """Defend state for MediumBot — same behavior as base Defend."""
    def __init__(self, bot):
        super().__init__(bot)

class HardAttack(Attack):
    """Attack state for HardBot — no reaction delay, same as MediumAttack."""
    def __init__(self, bot):
        super().__init__(bot)

    def _should_act(self):
        """Always returns True."""
        return True

    def run(self, dt, field, active_powerups=None):
            distance = abs(self.bot.ball.pos.x - self.bot.pos.x)
            t = distance / self.bot.max_speed if self.bot.max_speed > 0 else 0
            predicted_x = self.bot.ball.pos.x + self.bot.ball.velocity.x * t

            if self.bot.pos.x < predicted_x:
                self.bot.current_action = "right"
            else:
                self.bot.current_action = "left"

            if self.bot.ball.get_bottom() < self.bot.get_top():
                self.bot.jump(field)

            if self.bot.ball.pos.x > SCREEN_WIDTH / 2:
                self.bot.boost()

            if self.bot.current_action == "right":
                self.bot.move_right(dt)
            elif self.bot.current_action == "left":
                self.bot.move_left(dt)    

class HardDefend(Defend):
    """Defend state for HardBot — same behavior as base Defend."""
    def __init__(self, bot):
        super().__init__(bot)

class FSM:
    """
    Finite State Machine that manages bot behavior states.

    Attributes:
        current_state (State): The currently active state.
        states (dict): Dictionary mapping state names to State instances.
    """
    def __init__(self):
        self.current_state = None
        self.states = {}

    def set_state(self, stateName):
        """Sets the active state by name."""
        self.current_state = self.states[stateName]

    def change_state(self, new_state):
        """Directly sets the active state to a State instance."""
        self.current_state = new_state

    def execute(self, dt, field, active_powerups=None):
        """Runs the current state's logic for this frame."""
        self.current_state.run(dt, field, active_powerups)