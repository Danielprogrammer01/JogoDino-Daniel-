import pygame


from dino_runner.utils.constants import (
    BG,
    MENU,
    ICON,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    FPS,
    X_POS_BG,
    Y_POS_BG,
    X_POS_MENU,
    Y_POS_MENU,
    GAME_SPEED,
    DEFAULT_TYPE,
    CLOUD,
)
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.powerups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = GAME_SPEED
        self.x_pos_bg = X_POS_BG
        self.y_pos_bg = Y_POS_BG
        self.x_pos_menu = X_POS_MENU
        self.y_pos_menu = Y_POS_MENU
        self.x_pos_cloud = 0
        self.y_pos_cloud = 50
        self.death_count = 0
        self.score = 0
        self.record = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = GAME_SPEED
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            if self.score < 500:
                self.game_speed += 2
            if 500 < self.score < 1000:
                self.game_speed += 3
            if self.score >= 1000:
                self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_cloud()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_upper_time()
        self.power_up_manager.draw(self.screen)

        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_cloud(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
        if self.x_pos_cloud <= -image_width:
            self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
            self.x_pos_cloud = 1000
        self.x_pos_cloud -= self.game_speed

    def draw_power_upper_time(self):
        if self.player.has_power_up:
            time_to_show = round(
                (self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2
            )
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} ativado por {time_to_show} segundos",
                    self.screen,
                    font_size=18,
                    pos_x_center=500,
                    pos_y_center=50,
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw_score(self):
        draw_message_component(
            f"Pontuação: {self.score}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=50,
            font_size=20,
        )
        draw_message_component(
            f"Recorde: {self.record}",
            self.screen,
            pos_x_center=100,
            pos_y_center=50,
            font_size=20,
        )

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.run()
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False

    def show_menu(self):
        image_width = MENU.get_width()
        self.screen.blit(MENU, (self.x_pos_menu, self.y_pos_menu))
        self.screen.blit(MENU, (image_width + self.x_pos_menu, self.y_pos_menu))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        # self.screen.fill((225, 225, 225))

        if self.death_count == 0:
            draw_message_component(
                "BEM-VINDO AO JOGO DO DINO!",
                self.screen,
                pos_y_center=half_screen_height - 10,
            )
            draw_message_component(
                'Pressione a tecla "ENTER" para iniciar',
                self.screen,
                pos_y_center=half_screen_height + 50,
                font_size=30,
            )

        else:
            draw_message_component(
                'Pressione a tecla "ENTER" para jogar novamente',
                self.screen,
                pos_y_center=half_screen_height + 140,
                font_size=25,
            )
            draw_message_component(
                'Pressione a tecla "ESC" para sair',
                self.screen,
                pos_y_center=half_screen_height + 200,
                font_size=25,
            )
            draw_message_component(
                f"Sua pontuação: {self.score}",
                self.screen,
                pos_y_center=half_screen_height - 200,
                font_size=25,
            )
            if self.score > self.record:
                self.record = self.score

            draw_message_component(
                f"Recorde: {self.record}",
                self.screen,
                pos_y_center=half_screen_height - 150,
                font_size=25,
            )
            draw_message_component(
                f"Mortes: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height - 100,
                font_size=25,
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 40))

        pygame.display.update()

        self.handle_events_on_menu()
