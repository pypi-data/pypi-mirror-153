""" Root file with main entrypoint """

import os
from sys import platform

import pygame

from . import scenes, collection, updater
from .config import ConfigManager
from .music import MusicManager, SoundGroup


# Set environment variable for centering window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialization of pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


def main() -> None:
    """ Main entrypoint of Space Way. Execute this to run game """

    # Get base directory to create absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Initialization of configuration manager
    config = ConfigManager(base_dir)

    # Check software updates and view information dialog if update is available
    if config['user']['updates']:
        updater.check_software_updates(config['version'], base_dir)

    # Сreate screen with accounting for user settings
    flags = pygame.FULLSCREEN * config['user']['full_screen'] | pygame.SCALED
    screen = pygame.display.set_mode(config['mode'], flags=flags)

    # Configure screen
    pygame.display.set_caption(config['caption'])
    pygame.display.set_icon(pygame.image.load(f'{base_dir}/icon.ico'))

    # Get clock onject for the further use
    clock = pygame.time.Clock()

    # Initialize debug modules if configuration allows it
    if config['debug']:
        from . import debug

        debugger = debug.Debugger(config)
        debugger.enable_module(debug.DebugStat(screen, base_dir, clock))
        debugger.enable_module(debug.DebugHitbox(screen))

    # Define variables in namespace
    config['ns'].dt = 0     # Set delta-time for the further use
    config['ns'].tick = 1   # Set tick for calculating the past time in seconds
    config['ns'].mm = MusicManager({
        'bang': (f'{base_dir}/assets/sounds/bang.ogg', SoundGroup.EFFECT),
        'score': (f'{base_dir}/assets/sounds/score.ogg', SoundGroup.EFFECT),
        'game': (f'{base_dir}/assets/sounds/game.ogg', SoundGroup.SOUND)
    })

    # Configure sounds volume
    config['ns'].mm.set_volume(config['user']['effects'], SoundGroup.EFFECT)
    config['ns'].mm.set_volume(config['user']['music'], SoundGroup.SOUND)

    # Initialization of headpiece scene
    text, pb = scenes.headpiece.init(screen, base_dir, config)

    # Initialization of lobby scene
    play_button, table_button, settings_button, caption = scenes.lobby.init(screen, base_dir, config)

    # Initialization of table scene
    table, table_back_button = scenes.table.init(screen, base_dir, config)
    config['ns'].table = table

    # Initialization of settings scene
    effects_button, music_button, full_screen_button, updates_button, settings_back_button, nick_input = scenes.settings.init(screen, base_dir, config)

    settings_buttons = collection.CenteredButtonsGroup(config['mode'])
    settings_buttons.add(effects_button, music_button, full_screen_button, updates_button)

    # Initialization of game scene
    astrs = pygame.sprite.Group()
    boosts = collection.BoostsGroup()

    bg, plate, score, end, pause, resume_button, pause_lobby_button, again_button, end_lobby_button, pause_button = scenes.game.init(screen, base_dir, config)

    pause_buttons = collection.CenteredButtonsGroup(config['mode'])
    pause_buttons.add(pause_lobby_button, resume_button)

    end_buttons = collection.CenteredButtonsGroup(config['mode'])
    end_buttons.add(end_lobby_button, again_button)

    # Scene buttons linking
    scene_buttons = collection.SceneButtonsGroup(config)
    scene_buttons.add(play_button, table_button, settings_button,
                      settings_back_button, table_back_button, resume_button,
                      pause_lobby_button, again_button, end_lobby_button, pause_button)

    while True:
        # Showing a specific scene
        if config['scene'] == 'headpiece':
            scenes.headpiece.functions.check_events(config, base_dir)
            scenes.headpiece.functions.update(screen, config, text, pb)

        elif config['scene'] == 'lobby':
            scenes.lobby.functions.check_events(config, base_dir, scene_buttons, caption)
            scenes.lobby.functions.update(bg, scene_buttons, caption)

        elif config['scene'] == 'table':
            scenes.table.functions.check_events(config, scene_buttons)
            scenes.table.functions.update(base_dir, bg, table, scene_buttons)

        elif config['scene'] == 'settings':
            scenes.settings.functions.check_events(config, scene_buttons, settings_buttons, nick_input)
            scenes.settings.functions.update(bg, config, scene_buttons, settings_buttons, nick_input)

            # If fullscreen button was pressed, change screen to fullscreen and back again
            if full_screen_button.changed:
                flags = pygame.FULLSCREEN * config['user']['full_screen'] | pygame.SCALED
                screen = pygame.display.set_mode(config['mode'], flags=flags)
                full_screen_button.changed = False

        elif config['scene'] == 'game':
            scenes.game.functions.check_events(config, base_dir, plate, astrs, boosts, end, pause, scene_buttons)
            scenes.game.functions.update(screen, config, base_dir, bg, plate, astrs, boosts, score, end, pause, pause_buttons, end_buttons, scene_buttons)

        # Update debugger if debug mode enabled
        if config['debug']:
            debugger.update()

        # Update screen and adjust speed to FPS
        pygame.display.update()
        config['ns'].dt = clock.tick(config['FPS']) * 0.03

        # Update tick
        config['ns'].tick += 1
