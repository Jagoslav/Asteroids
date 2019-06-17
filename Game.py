# Python 3.6, Windows 10, Pycharm 2017.2.4
import json
import random

import pygame

import Display
import Collision
import Objects


class Game:
    menu_asteroids = None
    player = None

    def menu(self):
        """
        Function representing game menu's state.
        :return:
        """
        title_font = pygame.font.SysFont("Comic Sans MS", Display.height // 8)
        title_surface = title_font.render("Asteroids", True, (228, 228, 128))
        normal_font = pygame.font.SysFont("Comic Sans MS", Display.height // 32)
        new_game_rect = self.define_rect("New Game", normal_font, (Display.center_x, Display.height // 2))
        highscores_rect = self.define_rect("Highscores", normal_font, (Display.center_x, 5 * Display.height // 8))
        exit_rect = self.define_rect("Exit", normal_font, (Display.center_x, 6 * Display.height // 8))
        self.menu_asteroids = []
        for i in range(64):
            self.menu_asteroids.extend(self.spawn())
        running = True
        while running:
            dt = Display.clock.tick() / 100
            Display.screen.fill((0, 0, 0))
            for asteroid in self.menu_asteroids:
                asteroid.update(dt)
                asteroid.draw()
            Display.screen.blit(title_surface, (Display.center_x - title_surface.get_width() / 2, Display.height // 8))
            self.write_interactive("New Game",
                                   normal_font,
                                   (Display.center_x, Display.height // 2),
                                   (228, 228, 196),
                                   (150, 150, 140))
            self.write_interactive("Highscores",
                                   normal_font,
                                   (Display.center_x, 5 * Display.height // 8),
                                   (228, 228, 196),
                                   (150, 150, 140))
            self.write_interactive("Exit",
                                   normal_font,
                                   (Display.center_x, 6 * Display.height // 8),
                                   (228, 228, 196),
                                   (150, 150, 140))
            pygame.display.flip()
            #  event checking
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    if new_game_rect.collidepoint(mouse_pos):
                        score = self.new_game()
                        if score > 0:
                            self.highscores(score)
                    if highscores_rect.collidepoint(mouse_pos):
                        self.highscores()
                    if exit_rect.collidepoint(mouse_pos):
                        running = False
        pygame.quit()
        exit()

    def highscores(self, new_score=None):
        """
        Function representing scores tab state.
        :param new_score: optional value. If provided, new score might be added to a scores list (if high enough) and
        get highlighted
        :return:
        """
        scores = []
        title_font = pygame.font.SysFont("Comic Sans MS", Display.height // 12)
        normal_font = pygame.font.SysFont("Comic Sans MS", Display.height // 32)
        highlighted_id = None
        try:
            file = open("highscores.json", "r", encoding="utf8")
            info = json.loads(file.read())
            scores.extend(info["scores"])
            scores.sort(key=lambda val: val[1], reverse=True)
            file.close()
        except IOError:
            file = open("highscores.json", "w", encoding="utf8")
            file.write(json.dumps({"scores": scores}))
            file.close()
        if new_score is not None and new_score > 0:
            temp_id = 0
            for score in scores:
                if score[1] > new_score:
                    temp_id += 1
                else:
                    break
            if temp_id <= 10:
                scores.insert(temp_id, ("player", new_score))
                highlighted_id = temp_id
                try:
                    file = open("highscores.json", "w", encoding="utf8")
                    file.write(json.dumps({"scores": scores}))
                    file.close()
                except IOError:
                    pass
        running = True
        title_surface = title_font.render("Highscores", True, (228, 228, 128))
        back_rect = self.define_rect("Back", normal_font, (Display.center_x, Display.height - 90))

        scores_y_pos = Display.height // 4
        scores_displace = Display.height // 20
        while running:
            dt = Display.clock.tick() / 100
            Display.screen.fill((0, 0, 0))
            for asteroid in self.menu_asteroids:
                asteroid.update(dt)
                asteroid.draw()
            Display.screen.blit(title_surface,
                                (Display.center_x - title_surface.get_width() / 2, 30))
            for i in range(1, 11):
                if highlighted_id == (i - 1):
                    color = (255, 128, 128)
                else:
                    color = (228, 228, 128)
                score_surface = normal_font.render(str(i)+":", True, color)
                Display.screen.blit(score_surface,
                                    ((3 * Display.center_x / 4 - score_surface.get_width() - 10),
                                     scores_y_pos + (i-1) * scores_displace))
            for i in range(0, 10):
                if i < len(scores):
                    if highlighted_id == i:
                        color = (255, 128, 128)
                    else:
                        color = (255, 255, 255)
                    score_surface = normal_font.render(scores[i][0], True, color)
                    Display.screen.blit(score_surface,
                                        ((3 * Display.center_x / 4),
                                         scores_y_pos + i * scores_displace))
                    score_surface = normal_font.render(str(scores[i][1]), True, color)
                    Display.screen.blit(score_surface,
                                        ((5 * Display.center_x / 4 - score_surface.get_width()),
                                         scores_y_pos + i * scores_displace))
                else:
                    score_surface = normal_font.render("---", True, (255, 255, 255))
                    Display.screen.blit(score_surface,
                                        ((3 * Display.center_x / 4),
                                         scores_y_pos + i * scores_displace))
                    score_surface = normal_font.render("---", True, (255, 255, 255))
                    Display.screen.blit(score_surface,
                                        ((5 * Display.center_x / 4 - score_surface.get_width()),
                                         scores_y_pos + i * scores_displace))

            self.write_interactive("Back",
                                   normal_font,
                                   (Display.center_x, Display.height - 90),
                                   (228, 228, 196),
                                   (150, 150, 140))
            pygame.display.flip()

            #  event checking
            for event in pygame.event.get():
                if event.type == pygame.QUIT or\
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                if pygame.mouse.get_pressed()[0]:
                    if back_rect.collidepoint(pygame.mouse.get_pos()):
                        running = False

    def new_game(self):
        """
        Function representing playable game mode
        :return:
        """
        asteroids = []
        player = Objects.Player()
        score = 0
        running = True
        asteroid_count_clock = pygame.time.get_ticks()
        asteroid_max_count = 3
        text_font = pygame.font.SysFont("Comic Sans MS", 11)
        while running:
            dt = Display.clock.tick() / 100
            Display.screen.fill((0, 0, 0))

            #  drawing and updating objects
            for i in range(len(asteroids)):
                asteroids[i].update(dt)
                asteroids[i].draw()
            if len(asteroids) < asteroid_max_count:
                asteroids.extend(self.spawn())
            player.update(dt)
            player.draw()

            #  drawing gui
            score_surface = text_font.render("Score: " + str(score), True, (255, 255, 255))
            lives_surface = text_font.render(("Lives left: " + str(player.lives)), True, (255, 255, 255))
            Display.screen.blit(score_surface, (0, 0))
            Display.screen.blit(lives_surface, (0, 20))
            pygame.display.flip()

            #  collision detections:
            for i in range(len(asteroids) - 1, -1, -1):
                #  asteroid with a player
                if player.ship is not None:
                    if Collision.rect_to_rect(
                            player.ship.get_initial_collision(),
                            asteroids[i].get_initial_collision()):
                        if Collision.polygon_to_polygon(
                                player.ship.get_vertices(),
                                asteroids[i].get_vertices()):
                            player.ship = None
                            player.lives -= 1
                #  asteroid with projectiles from a player
                if player.projectiles is not None:
                    for j in range(len(player.projectiles) - 1, -1, -1):
                        if Collision.rect_to_rect(
                                asteroids[i].get_initial_collision(),
                                player.projectiles[j].get_initial_collision()):
                            if Collision.point_to_polygon(
                                    asteroids[i].pos,
                                    asteroids[i].vertices,
                                    player.projectiles[j].pos):
                                score += asteroids[i].size*2
                                asteroids.extend(self.spawn(asteroids[i]))
                                asteroids.pop(i)
                                player.projectiles.pop(j)
                                break

            #  event checking
            for event in pygame.event.get():
                if event.type == pygame.QUIT or\
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            if pygame.time.get_ticks() - asteroid_count_clock > 10000:
                asteroid_max_count += 1
                asteroid_count_clock = pygame.time.get_ticks()
            if player.lives == 0:
                running = False
        #  if end, return score
        return score

    @staticmethod
    def spawn(parent=None):
        """
        spawns additional asteroid/s
        :param parent: optional parent asteroid to take values from
        :return: list of asteroids to be added
        """
        asteroids = []
        if parent is None:
            edge = random.randint(0, 1)
            shift = random.random()
            if edge == 0:
                pos = (shift * Display.width, 0)
            else:
                pos = (0, shift * Display.height)

            asteroids.append(Objects.Asteroid.new(pos))
        else:
            if parent.size > 1:
                asteroids.append(Objects.Asteroid.copy(parent))
                asteroids.append(Objects.Asteroid.copy(parent))
        return asteroids

    @staticmethod
    def write_interactive(message, font, pos, color_active, color_inactive):
        """
        Draws a message onto a screen and changes its color if mouse cursor is above it
        :param message: Message to display
        :param font: Font to use
        :param pos: Origin point
        :param color_active: color of displayed message in active state
        :param color_inactive: color of displayed message in inactive state
        :return:
        """
        surface = font.render(message, True, color_inactive)
        pos = pos[0] - surface.get_width() / 2, pos[1] - surface.get_height() / 2
        rect = surface.get_rect().move(pos)
        if rect.collidepoint(pygame.mouse.get_pos()):
            surface = font.render(message, True, color_active)
        Display.screen.blit(surface, (rect[0], rect[1]))

    @staticmethod
    def define_rect(message, font, pos):
        """
        Defines and returns rectangle of a displayed message
        :param message: Message to display
        :param font: Font to use
        :param pos: Origin point of a text to display
        :return: Rectangle around origin point
        """
        surface = font.render(message, False, (255, 255, 255))
        pos = pos[0] - surface.get_width() / 2, pos[1] - surface.get_height() / 2
        return surface.get_rect().move(pos)


if __name__ == "__main__":
    game = Game()
    game.menu()
