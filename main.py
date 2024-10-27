import pygame
import math

pygame.init()
WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

pygame.mixer.init()
pygame.mixer.music.load("Interstellar Soundtrack.mp3")
pygame.mixer.music.play(-1)

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_GREY = (200, 200, 200)
BROWN = (160, 132, 71)
GOLD = (255, 215, 0)  
FONT = pygame.font.SysFont("comicsans", 16)
NAME_FONT = pygame.font.SysFont("comicsans", 14)


class Spacecraft:
    def __init__(self, parent_planet, distance_from_planet, radius, color, orbital_speed, name):
        self.parent_planet = parent_planet
        self.distance = distance_from_planet
        self.radius = radius
        self.color = color
        self.orbital_speed = orbital_speed
        self.angle = math.pi  
        self.x = 0
        self.y = 0
        self.orbit = []
        self.name = name

    def update_position(self, time):
        
        self.angle = math.atan2(self.parent_planet.y, self.parent_planet.x) + math.pi

        self.x = self.parent_planet.x + self.distance * math.cos(self.angle)
        self.y = self.parent_planet.y + self.distance * math.sin(self.angle)
        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 50:
            self.orbit.pop(0)

    def draw(self, win):
        x = self.x * Planet.SCALE + WIDTH / 2
        y = self.y * Planet.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x_point, y_point = point
                x_point = x_point * Planet.SCALE + WIDTH / 2
                y_point = y_point * Planet.SCALE + HEIGHT / 2
                updated_points.append((x_point, y_point))
            pygame.draw.lines(win, self.color, False, updated_points, 1)

       
        points = []
        for i in range(6):
            angle = math.pi / 3 * i + math.pi / 6
            point_x = x + self.radius * math.cos(angle)
            point_y = y + self.radius * math.sin(angle)
            points.append((point_x, point_y))

        pygame.draw.polygon(win, self.color, points)
        
        pygame.draw.circle(win, WHITE, (x, y), self.radius / 3)

        
        name_text = NAME_FONT.render(self.name, 1, self.color)
        win.blit(name_text, (x - name_text.get_width() / 2, y - self.radius - 20))


class Moon:
    def __init__(self, parent_planet, distance_from_planet, radius, color, mass, orbital_speed, name):
        self.parent_planet = parent_planet
        self.distance = distance_from_planet
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbital_speed = orbital_speed
        self.angle = 0
        self.x = 0
        self.y = 0
        self.orbit = []
        self.name = name

    def update_position(self, time):
        self.angle += self.orbital_speed * time

        self.x = self.parent_planet.x + self.distance * math.cos(self.angle)
        self.y = self.parent_planet.y + self.distance * math.sin(self.angle)
        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 25:
            self.orbit.pop(0)

    def draw(self, win):
        x = self.x * Planet.SCALE + WIDTH / 2
        y = self.y * Planet.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x_point, y_point = point
                x_point = x_point * Planet.SCALE + WIDTH / 2
                y_point = y_point * Planet.SCALE + HEIGHT / 2
                updated_points.append((x_point, y_point))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        name_text = NAME_FONT.render(self.name, 1, self.color)
        win.blit(name_text, (x - name_text.get_width() / 2, y - self.radius - 20))


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        self.moons = []
        self.spacecraft = []
        self.name = name

    def add_moon(self, distance_from_planet, radius, color, mass, orbital_speed, name):
        moon = Moon(self, distance_from_planet, radius, color, mass, orbital_speed, name)
        self.moons.append(moon)
        return moon

    def add_spacecraft(self, distance_from_planet, radius, color, orbital_speed, name):
        spacecraft = Spacecraft(self, distance_from_planet, radius, color, orbital_speed, name)
        self.spacecraft.append(spacecraft)
        return spacecraft

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

        name_text = NAME_FONT.render(self.name, 1, self.color)
        win.blit(name_text, (x - name_text.get_width() / 2, y - self.radius - 20))

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y + self.radius + 10))

        for moon in self.moons:
            moon.draw(win)

        for spacecraft in self.spacecraft:
            spacecraft.draw(win)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

        for moon in self.moons:
            moon.update_position(self.TIMESTEP)

        for spacecraft in self.spacecraft:
            spacecraft.update_position(self.TIMESTEP)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24, "Earth")
    earth.y_vel = 29.783 * 1000

    # Adding Earth's moon
    earth.add_moon(Planet.AU / 40, 8, LIGHT_GREY, 7.34767309 * 10 ** 22, 0.025, "Moon")

    # Adding JWST at L2 point
    earth.add_spacecraft(Planet.AU / 30, 6, GOLD, 0, "JWST")

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23, "Mars")
    mars.y_vel = 24.077 * 1000

    mars.add_moon(Planet.AU / 50, 6, DARK_GREY, 1.06 * 10 ** 16, 0.035, "Phobos")
    mars.add_moon(Planet.AU / 45, 5, BROWN, 2.4 * 10 ** 15, 0.020, "Deimos")

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24, "Venus")
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()

