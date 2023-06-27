import pygame
from sys import exit
from random import randint


# Spaceman game, by Hamza Rana

def display_score():
    current_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, 'White')
    score_rect = score_surf.get_rect(center=(450, 60))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 430:
                screen.blit(meteor_surface, obstacle_rect)
            else:
                screen.blit(satellite_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def spaceman_animation():
    global space_man_surf, space_man_frames_index
    # play in air animation
    if space_man_rect.bottom < 440:
        space_man_surf = space_man_frames[1]
    # play standing animation when on ground
    else:
        space_man_frames_index += 0
        if space_man_frames_index >= len(space_man_frames):
            space_man_frames_index = 0
        space_man_surf = space_man_frames[int(space_man_frames_index)]


pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption('Spaceman')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

pygame.mixer.init()

pygame.mixer.music.load('Music/nba youngboy outside today low quality.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

space_background = pygame.image.load('Images/tumblr_d3ef4ce9f679ade84289bc951152ca45_24ed1b88_640.png').convert_alpha()
space_background = pygame.transform.scale(space_background, (900, 600))

moon_surface = pygame.image.load('Images/58f9fd580ed2bdaf7c128327.png').convert_alpha()
moon_surface = pygame.transform.scale(moon_surface, (700, 550))
moon_rotation = pygame.transform.rotate(moon_surface, 360)

# score_surface = test_font.render('Spaceman Game', False, 'White')
# score_rect = score_surface.get_rect(center=(450, 40))

# Obstacle
meteor_surface = pygame.image.load('Images/result (3).png').convert_alpha()
meteor_surface = pygame.transform.scale(meteor_surface, (150, 50))
meteor_surface2 = pygame.image.load('Images/result (3) - Copy.png').convert_alpha()
meteor_surface2 = pygame.transform.scale(meteor_surface2, (150, 50))
meteor_frames = [meteor_surface, meteor_surface2]
meteor_frames_index = 0
meteor_default = meteor_frames[meteor_frames_index]

satellite_surf = pygame.image.load('Images/result (8).png').convert_alpha()
satellite_surf = pygame.transform.scale(satellite_surf, (110, 90)).convert_alpha()
satellite_surf2 = pygame.image.load('Images/result (8) - Copy.png').convert_alpha()
satellite_surf2 = pygame.transform.scale(satellite_surf2, (110, 90)).convert_alpha()
satellite_frames = [satellite_surf, satellite_surf2]
satellite_frames_index = 0
satellite_default = satellite_frames[satellite_frames_index]

obstacle_rect_lst = []

space_man_surf = pygame.image.load('Images/result (5) - Copy.png').convert_alpha()
space_man_surf = pygame.transform.scale(space_man_surf, (90, 135))
space_man_jumping = pygame.image.load('Images/result (5).png').convert_alpha()
space_man_jumping = pygame.transform.scale(space_man_jumping, (90, 135))

space_man_rect = space_man_surf.get_rect(midbottom=(440, 440))
space_man_gravity = 0

# Spaceman animation
space_man_frames = [space_man_surf, space_man_jumping]
space_man_frames_index = 0
space_man_surf = space_man_frames[space_man_frames_index]

# Intro screen
intro_message_surface = test_font.render('Welcome to Spaceman, by Hamza S.R.', False, 'Blue')
intro_message_rect = intro_message_surface.get_rect(center=(450, 100))
intro_message_surface2 = test_font.render('Press SPACE to play', False, 'Blue')
intro_message_rect2 = intro_message_surface2.get_rect(center=(450, 500))
spaceman_stand = pygame.image.load('Images/result (7).png').convert_alpha()
spaceman_stand = pygame.transform.scale(spaceman_stand, (400, 300))
spaceman_stand_rect = spaceman_stand.get_rect(center=(410, 300))

# Outro screen
message_surface = test_font.render('No way you lost (ToT)', False, 'Blue')
message_rect = message_surface.get_rect(center=(450, 500))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

meteor_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(meteor_animation_timer, 300)

satellite_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(satellite_animation_timer, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if space_man_rect.collidepoint(event.pos) and space_man_rect.bottom >= 300:
                    space_man_gravity = -5

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and space_man_rect.bottom >= 300:
                    space_man_gravity = -5
        else:
            if event.type == pygame.KEYDOWN and event.key == (pygame.K_UP and pygame.K_SPACE):
                game_active = True
                # meteor_rect.left = 900
                start_time = pygame.time.get_ticks() // 1000

        if game_active:
            if event.type == obstacle_timer and game_active:
                if randint(0, 2):
                    obstacle_rect_lst.append(meteor_surface.get_rect(midbottom=(randint(1100, 1600), 430)))
                else:
                    obstacle_rect_lst.append(satellite_surf.get_rect(midbottom=(randint(1100, 1600), 230)))

            if event.type == meteor_animation_timer:
                if meteor_frames_index == 0:
                    meteor_frames_index = 1
                else:
                    meteor_frames_index = 0
                meteor_surface = meteor_frames[meteor_frames_index]

            if event.type == satellite_animation_timer:
                if satellite_frames_index == 0:
                    satellite_frames_index = 1
                else:
                    satellite_frames_index = 0
                satellite_surf = satellite_frames[satellite_frames_index]

    if game_active:
        screen.blit(space_background, (0, 0))
        screen.blit(moon_surface, (100, 430))
        # pygame.draw.rect(screen, '#ed3434', score_rect, 9, 20)
        # pygame.draw.rect(screen, '#ed3434', score_rect, 0, 20)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        # meteor_rect.x -= 4
        # if meteor_rect.right <= 0:
        #     meteor_rect.left = 850
        # screen.blit(meteor_surface, meteor_rect)

        # Player
        space_man_gravity += 0.1
        space_man_rect.y += space_man_gravity
        if space_man_rect.bottom >= 440:
            space_man_rect.bottom = 440
        spaceman_animation()
        screen.blit(space_man_surf, space_man_rect)

        # Obstacle movement
        obstacle_rect_lst = obstacle_movement(obstacle_rect_lst)

        # collision
        game_active = collisions(space_man_rect, obstacle_rect_lst)

    else:
        # Intro screen
        screen.fill('Grey')
        screen.blit(spaceman_stand, spaceman_stand_rect)
        obstacle_rect_lst.clear()
        space_man_rect.midbottom = (440, 440)
        space_man_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, 'Blue')
        score_message_rect = score_message.get_rect(center=(450, 550))
        screen.blit(intro_message_surface, intro_message_rect)

        if score == 0:
            screen.blit(intro_message_surface2, intro_message_rect2)
        else:
            screen.blit(message_surface, message_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
