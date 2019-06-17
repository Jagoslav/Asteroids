import math
import random

import pygame

import Display

if __name__ == "__main__":
    exit()


class Object:
    """
    Base object class, holds most important information about the object
    """
    pos = None
    velocity = None
    velocity_angle = None
    vertices = []
    initial_collision_distance = 0

    def __init__(self, pos=(0, 0), velocity_angle=0.0, velocity=0):
        """
        Initialize Object
        :param pos: position of the origin point on screen
        :param velocity_angle: Angle of a slope on which the object is moving
        :param velocity: Velocity of the object's movement
        """
        self.pos = pos
        self.velocity = velocity * Display.value_modifier
        self.velocity_angle = velocity_angle
        self.vertices = []

    def draw(self):
        """
        If not overriden by anything, does nothing. Draws the object on the display surface otherwise
        :return:
        """
        pass

    def update(self, dt):
        """
        Updates the most important fields of the object
        :param dt: Delta time, defines the percentage of full update values
        :return:
        """
        shift = dt * self.velocity
        self.pos = (self.pos[0] + shift * math.sin(self.velocity_angle),
                    self.pos[1] + shift * math.cos(self.velocity_angle))
        self.vertices = [(x + shift * math.sin(self.velocity_angle),
                          y + shift * math.cos(self.velocity_angle))
                         for (x, y) in self.vertices]
        if self.pos[0] <= 0:
            self.pos = Display.width, self.pos[1]
            self.vertices = [(x + Display.width, y) for (x, y) in self.vertices]
        elif self.pos[0] >= Display.width:
            self.pos = 0, self.pos[1]
            self.vertices = [(x - Display.width, y) for (x, y) in self.vertices]
        if self.pos[1] <= 0:
            self.pos = self.pos[0], Display.height
            self.vertices = [(x, y + Display.height) for (x, y) in self.vertices]
        elif self.pos[1] >= Display.height:
            self.pos = (self.pos[0], 0)
            self.vertices = [(x, y - Display.height) for (x, y) in self.vertices]

    def get_vertices(self):
        """
        Returns the Polygon visualisation of the object
        :return: self.vertices
        """
        return self.vertices

    def get_initial_collision(self):
        """
        Returns a tuple representation of object's rectangular bounds, used to check if more detailed collision
        detection is needed
        :return: (left, up, right, down)
        """
        return (self.pos[0] - self.initial_collision_distance,
                self.pos[1] - self.initial_collision_distance,
                self.pos[0] + self.initial_collision_distance,
                self.pos[1] + self.initial_collision_distance)


class Asteroid(Object):
    """
    Class representation of the asteroid
    """
    size = None  # size of the asteroid
    rotation_speed = None
    top_speed = 8
    max_size = 8

    def __init__(self, pos=(0, 0), velocity_angle=0, velocity_percentage=1, size=4, rotation_speed=0):
        """
        Initialize Asteroid object using given parameters
        :param pos: position of the origin point on screen
        :param velocity_angle: Angle of a slope on which the asteroid is moving
        :param velocity_percentage: Percentage of the asteroid's potential top_speed
        :param size: Serves as Lives counter for the asteroids, specifying if it can break into smaller ones
        :param rotation_speed: Asteroid's rotation speed
        """
        Object.__init__(self, pos, velocity_angle, velocity_percentage)
        self.velocity = velocity_percentage * self.top_speed
        self.size = max(1, min(self.max_size, size))
        self.rotation_speed = rotation_speed
        number_of_spikes = random.randint(8, 16)
        self.vertices = [(Display.value_modifier * (size * 2 + random.randint(2, 10)),
                          (i * math.pi * 2) / number_of_spikes)
                         for i in range(number_of_spikes)]
        for v in self.vertices:
            self.initial_collision_distance = max(self.initial_collision_distance, v[0])
        self.vertices = [(pos[0] + v[0] * math.sin(v[1]), pos[1] + v[0] * math.cos(v[1])) for v in self.vertices]

    @classmethod
    def new(cls, pos=(0, 0)):
        """
        Used as a modification of the __init__ function that requires only a starting position of the object, and
        randomizes the rest of the init parameters
        :param pos: Position on screen of the asteroid's center
        :return: Class object
        """
        velocity_angle = random.random() * math.pi * 2
        velocity_modifier = 3 * random.random() / 4 + 0.25
        rotation_speed = random.random() * math.pi / 30
        size = random.randint(1, cls.max_size)
        if random.randint(0, 1) == 0:
            rotation_speed *= -1
        return cls(pos, velocity_angle, velocity_modifier, size, rotation_speed)

    @classmethod
    def copy(cls, parent):
        """
        Used as a modification of the __init__ function that requires only a parent asteroid to specify the new
        objects fields values
        :param parent: Asteroid to copy values from
        :return: Class object
        """
        pos = parent.pos
        velocity_angle = parent.velocity_angle + math.pi * random.randint(-30, 30) / 180
        velocity_percentage = max(0, min(parent.velocity / cls.top_speed + random.random()*0.3, 1))
        size = max(1, parent.size - 1)
        rotation_speed = parent.rotation_speed
        return cls(pos, velocity_angle, velocity_percentage, size, rotation_speed)

    def get_asteroid(self):
        """
        Acts as a getter function to return the Asteroid object if in need to create a new one from the exiting object
        :return: self
        """
        return self

    def draw(self):
        """
        Tries to draw object's polygon on the display surface
        :return:
        """
        try:
            color = 5 + 200 / self.size
            pygame.draw.polygon(Display.screen, (color, color, color), self.vertices)
            pygame.draw.aalines(Display.screen, (128, 128, 128), True, self.vertices)
        except pygame.error:
            pass

    def update(self, dt):
        """
        Updates the fields values of an object
        :param dt: Delta time, defines the percentage of full update values
        :return:
        """
        Object.update(self, dt)
        alpha = dt * self.rotation_speed
        self.vertices = [((x - self.pos[0]) * math.cos(alpha) - (y - self.pos[1]) * math.sin(alpha) + self.pos[0],
                          (x - self.pos[0]) * math.sin(alpha) + (y - self.pos[1]) * math.cos(alpha) + self.pos[1])
                         for x, y in self.vertices]


class Ship(Object):
    """
    Class representation of the player's ship object
    """
    rotation_angle = None
    top_speed = Display.value_modifier * 10.0  # highest achievable speed
    rotation_speed = math.radians(15.0)  # rotation speed

    def __init__(self, pos=(0, 0), direction_angle=0.0):
        """
        Initialize new Ship object
        :param pos: position of the origin point on screen
        :param direction_angle: Defines the direction that object is facing.
        """
        Object.__init__(self, pos, direction_angle, 0)
        # distance (in pixels) from the center of the ship
        self.vertices = [(0.0, -11.0), (5.0, 5.0), (2.0, 4.0), (-2.0, 4.0), (-5.0, 5.0)]
        self.vertices = [(x * Display.value_modifier, y * Display.value_modifier) for x, y in self.vertices]
        self.initial_collision_distance = 11
        self.vertices = [(x + pos[0], y + pos[1]) for x, y in self.vertices]
        self.rotation_angle = direction_angle

    def draw(self):
        """
        Tries to draw Object's polygon on a display surface
        :return:
        """
        try:
            pygame.draw.polygon(Display.screen, (255, 255, 255), self.vertices)
            pygame.draw.aalines(Display.screen, (255, 255, 255), True, self.vertices)
        except pygame.error:
            pass

    def update(self, dt):
        """
        Updates the field values of an object
        :param dt: delta time, defines the percentage of full update values
        :return:
        """
        key_presses = pygame.key.get_pressed()
        Object.update(self, dt)
        if key_presses[pygame.K_w] or key_presses[pygame.K_UP]:
            self.accelerate(dt)
        if key_presses[pygame.K_a] or key_presses[pygame.K_LEFT]:
            self.turn(dt, -1)
        if key_presses[pygame.K_d] or key_presses[pygame.K_RIGHT]:
            self.turn(dt, 1)

    def accelerate(self, dt):
        """
        Changes ship movement velocity based on its current velocity and the direction it's facing
        :param dt: delta time, defines the percentage of full update values
        :return:
        """
        x, y = (self.velocity * math.sin(self.velocity_angle) + dt * math.sin(self.rotation_angle),
                self.velocity * math.cos(self.velocity_angle) + dt * math.cos(self.rotation_angle))
        self.velocity_angle = math.atan2(x, y)
        self.velocity = min(self.top_speed, (x**2 + y**2)**0.5)

    def turn(self, dt, direction):
        """
        Rotates the ship around it's origin point in a certain direction
        :param dt: delta time, defines the percentage of full update values
        :param direction: signed multiplier of the rotation value, specifies the direction of rotation
        :return:
        """
        alpha = dt * self.rotation_speed * direction
        self.vertices = [((x - self.pos[0]) * math.cos(alpha) - (y - self.pos[1]) * math.sin(alpha) + self.pos[0],
                          (x - self.pos[0]) * math.sin(alpha) + (y - self.pos[1]) * math.cos(alpha) + self.pos[1])
                         for x, y in self.vertices]
        self.rotation_angle -= alpha


class Projectile(Object):
    """
    Class representation of the projectiles
    """
    expiration_time = None

    def __init__(self, pos=(0, 0), velocity_angle=0.0, velocity=0):
        """
        Initialize new Projectile object
        :param pos: Position of the origin point on screen
        :param velocity_angle: Angle of a slope on which the asteroid is moving
        :param velocity: Velocity of the object's movement
        """
        Object.__init__(self, pos, velocity_angle, velocity)
        self.vertices = (-1, 0), (0, -1), (1, 0), (0, 1)
        self.vertices = [(x + pos[0], y + pos[1]) for x, y in self.vertices]
        self.expiration_time = pygame.time.get_ticks() + 2500 // Display.value_modifier
        for v in self.vertices:
            x, y = math.fabs(self.pos[0] - v[0]), math.fabs(self.pos[1] - v[1])
            self.initial_collision_distance = max(self.initial_collision_distance, x, y)

    def draw(self):
        """
        Tries to draw object's polygon on the display surface
        :return:
        """
        try:
            pygame.draw.polygon(Display.screen, (255, 255, 255), self.vertices)
            pygame.draw.aalines(Display.screen, (255, 255, 255), True, self.vertices)
        except pygame.error:
            pass

    def update(self, dt):
        """
        Updates the fields values of an object
        :param dt: Delta time, defines the percentage of full update values
        :return:
        """
        Object.update(self, dt)


class Player:
    """
    Player's class, allows a player to interact with the ship in a game.
    """
    ship = None
    ammo_loaded = False
    reload_time = None
    respawn_delay = None
    respawn_time = None
    respawn_font = pygame.font.SysFont("Comic Sans MS", 11)
    lives = None
    projectiles = []

    def __init__(self, pos=(Display.center_x, Display.center_y), lives=3):
        """
        Initialize Player object
        :param pos: Origin point of player's ships
        :param lives: Ammount of lives a player have left
        """
        self.ammo_loaded = False
        self.reload_time = 500
        self.respawn_delay = 3000
        self.respawn_time = None
        self.reload = 0
        self.lives = lives
        self.spawn_pos = pos
        self.ship = Ship(pos, math.pi)

    def draw(self):
        """
        Tries to draw a content of player's ship and the projectiles he shot.
        :return:
        """
        if self.ship is not None:
            self.ship.draw()
        else:
            respawn_surface = self.respawn_font.render(
                ("Respawn in: " + str((self.respawn_time - pygame.time.get_ticks()) / 1000) + "s"),
                True,
                (255, 255, 255))
            Display.screen.blit(respawn_surface, (0, 40))
        for i in range(len(self.projectiles)):
            self.projectiles[i].draw()

    def update(self, dt,):
        """
        Updates the field values of an object
        :param dt: Delta time, defines the percentage of full update values
        :return:
        """
        key_presses = pygame.key.get_pressed()
        if self.ship is not None:
            self.ship.update(dt)
            if self.ammo_loaded:
                if key_presses[pygame.K_SPACE]:
                    self.projectiles.append(
                        Projectile(self.ship.vertices[0],
                                   self.ship.rotation_angle,
                                   self.ship.top_speed*2))
                    self.ammo_loaded = False
                    self.reload = pygame.time.get_ticks() + self.reload_time
            elif self.reload < pygame.time.get_ticks():
                    self.ammo_loaded = True
        elif self.lives > 0:
            if self.respawn_time is None:
                self.respawn_time = pygame.time.get_ticks() + self.respawn_delay
            elif self.respawn_time < pygame.time.get_ticks():
                self.ship = Ship(self.spawn_pos, math.pi)
                self.respawn_time = None
        else:
            self.respawn_time = pygame.time.get_ticks() + self.respawn_delay
        for i in range(len(self.projectiles) - 1, -1, -1):
            self.projectiles[i].update(dt)
            if self.projectiles[i].expiration_time < pygame.time.get_ticks():
                self.projectiles.pop(i)
