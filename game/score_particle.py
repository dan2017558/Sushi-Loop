import math
import random
import pygame
import config

score_particles = []


class ScoreParticle:
    def __init__(self, text: str, pos, velocity=(0, -1), color=(255, 255, 255), lifespan=1500):
        self.text = str(text)
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.color = color
        self.lifespan = lifespan
        self.creation_time = pygame.time.get_ticks()
        self.alpha = 255
        self.font = config.score_font

        score_particles.append(self)

    def update(self):
        # Apply velocity
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Gravity-like slowdown
        self.velocity[1] *= 0.95
        self.velocity[0] *= 0.95

        # Fade out
        time_alive = pygame.time.get_ticks() - self.creation_time
        self.alpha = max(0, 255 - int(255 * (time_alive / self.lifespan)))

    def draw(self):
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)
        config.text_surface.blit(text_surface, (self.pos[0] * config.scale, self.pos[1] * config.scale))

    def is_alive(self):
        return pygame.time.get_ticks() - self.creation_time < self.lifespan


def spawn_score_explosion(center_pos, values):
    angle_step = 360 / len(values)
    radius = 2  # How fast the particles explode outward
    score_colours = (
        (255, 255, 255),
        (254, 231, 97),
        (254, 174, 52),
        (247, 118, 34),
        (228, 59, 68),
        (255, 0, 68),
    )  # gradually more intense
    time_colour = (99, 199, 77)

    for i, val in enumerate(values):
        # determine position
        angle_deg = i * angle_step - random.choice([0, 45]) + random.uniform(-15, 15)  # Add slight randomness
        angle_rad = math.radians(angle_deg)
        vx = math.cos(angle_rad) * radius
        vy = math.sin(angle_rad) * radius

        # determine colour
        if val[1] == "s":
            colour = score_colours[min(math.floor(val[0] / 50 * (len(score_colours) - 1)), len(score_colours) - 1)]
        else:
            colour = time_colour

        ScoreParticle(f"+{val[0]}", list(center_pos), (vx, vy), colour)
