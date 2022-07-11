import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Need a loop to keep to the program running and make necessary update

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (16, 10, 199)
RED = (199, 16, 10)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    # constants
    AU = 146.6e6 * 1000  # astronomical unit, of earth from the sun - meters from the sun
    G = 6.67428e-11  # force of attraction between objects - gravitational constant
    SCALE = 250 / AU  # scale to downsize to represent on window - 1AU = 100 pixels
    TIMESTEP = 3600*24 # Update the planet's movement for 1 day for each second

    def __init__(self, x, y, radius, color, mass):
        self.x = x  # meters away from the sun
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []  # keep track of all the points the planet has travelled along, so as to draw a circular orbit
        self.sun = False  # if the planet is the sun, if so then no orbit should be drawn
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 100)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

    def attraction(self, other):  # other-other planet
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:  # if other object is sun, update distance to sun property. no need to recalculate later
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2  # Force of attraction between 2 objects formula - F = GMm/d**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    # update position of planer- move them around
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue  # do not calculate if planet is current self planet, as it will return 0

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP  # using F = m * a and solving for acceleration
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP  # getting the distance/position
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()  # prevents the frame rate of game from going past a
                                 # certain value, else game will run at speed of computer

    # Declaring planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.36 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)  # 60 times per second
        WIN.fill((0, 0, 0))
        # pygame.display.update()

        for event in pygame.event.get():  # gets all the events that needs to keep track of, e.g keypress, mouseevent
            if event.type == pygame.QUIT:  # if window is closed
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()  # when loop is exited, close pygame


main()



