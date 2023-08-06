""" File with implementations of various mixins for easier creation of
    objects and following the DRY principle  """

from random import randint
from math import inf, ceil

import pygame

from .boost import render
from .collection import SceneButtonsGroup
from .hitbox import Ellipse


class SceneButtonMixin(pygame.sprite.Sprite):
    """Mixin for scene buttons, which can change current scene. The buttons
    can change position (Y axis only) when the scene changes. Mixin can be
    initialized anywhere in your `__init__` function

    Args:
        base_dir (str): An absolute path to directory where file with the main
            entrypoint is located
        config (spaceway.config.ConfigManager): The configuration object
        scene (str): The scene that the button belongs to
        sub_scene (str): The subscene that the button belongs to
        change_scene_to (str): The scene to switch to after pressing the button
        change_sub_scene_to (str): The subscene to switch to after pressing the button
        speed (Optional[float]): The speed of changing the position of the button (px/frame).
            If the parameter is positive, on button entering, it will move down, if it is
            negative, it will move up. On leaving button will move in the opposite
            direction from the entering. Defaults to 0 (button doesn't move)
        top (Optional[float]): The top limit of the button position. At the end of the
            movement, button will be adjacent to it
        bottom (Optional[float]): The bottom limit of the button position. At the end of
            the movement, button will be adjacent to it
        action (Optional[Literal["enter", "leave", "stop"]]): The action of button during
            initialization - one of *enter*, *leave* or *stop*, defaults to *stop*
    """

    def __init__(self, base_dir, config, scene, sub_scene, change_scene_to,
                 change_sub_scene_to, speed=0, top=-inf, bottom=inf,
                 action='stop'):
        """Constructor method
        """
        pygame.sprite.Sprite.__init__(self)

        # Set variables for next use
        self.config = config
        self.action = action
        self.top = top
        self.bottom = bottom
        self.speed = speed

        # Set events callbacks
        self.post_enter = lambda: None
        self.post_leave = lambda: None

        # Set scene during which button is displayed
        self.scene = scene
        self.sub_scene = sub_scene

        # Scenes on which will be changed when button will be pressed
        self.change_scene_to = change_scene_to
        self.change_sub_scene_to = change_sub_scene_to

    def update(self) -> None:
        """Update button position
        """
        # If button must move
        if self.action != 'stop':
            # Check, if move can be continued
            inc = (self.speed if self.action == 'leave' else -self.speed) * self.config['ns'].dt
            if self.speed and self.top < self.rect.y + inc < self.bottom:
                # If can be, move button
                self.rect.y += inc
            else:
                # Else, stop button, align it and call action callback
                self.rect.y = min(max(self.rect.y + inc, self.top), self.bottom)
                if self.action == 'enter':
                    self.post_enter()
                else:
                    self.post_leave()
                self.action = 'stop'

    def blit(self) -> None:
        """Blit button
        """
        self.screen.blit(self.img, self.rect)

    def enter(self, post_enter=lambda: None) -> None:
        """Start *enter* action

        Args:
            post_enter (Optional[callable]): The callback that will be called after
                the *enter* action is completed, defaults to `lambda: None`
        """
        self.action = 'enter'
        self.post_enter = post_enter

    def leave(self, post_leave=lambda: None) -> None:
        """Start *leave* action

        Args:
            post_enter (Optional[callable]): The callback that will be called after
                the *leave* action is completed, defaults to `lambda: None`
        """
        self.action = 'leave'
        self.post_leave = post_leave

    def change_scene(self) -> None:
        """Change scene to another one that was defined during initialization
        """
        self.config['scene'] = self.change_scene_to
        self.config['sub_scene'] = self.change_sub_scene_to

    def press(self) -> None:
        """Сallback of button that is performed when it is pressed. Starts
        *leave* action for buttons of the current scene and *enter* action for
        buttons of the future scene
        """
        # Find group :class:`spaceway.mixins.SceneButtonsGroup` button belongs to
        for group in self.groups():
            if isinstance(group, SceneButtonsGroup):
                # Leave buttons of the current scene, and enter of the next
                group.leave_buttons()
                group.enter_buttons(self.change_scene_to, self.change_sub_scene_to)
                break

        self.leave(self.change_scene)


class CaptionMixin:
    """Mixin for creating headers. Automatically selects color of the border
    defined by the user. Must be initialized at the bottom of your `__init__`
    function

    Args:
        base_dir (str): An absolute path to directory where file with the main
            entrypoint is located
        config (spaceway.config.ConfigManager): The configuration object
        caption (str): Plain or format (for dynamic captions) string - text of caption
    """

    def __init__(self, base_dir, config, caption):
        """Contructor method
        """
        # Setting variables for the further use
        self.config = config
        self.caption = caption

        # Setting color for text
        self.fg_color = (255, 255, 255)

        # Setting font for later generating image of text
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 72)

        # Available caption colors
        self.colors = [
            (0, 153, 255),
            (252, 15, 192),
            (0, 255, 0)
        ]

        # Caching caption settings
        self._prev_caption = (None, None)

        # Calling `update` function for generating all images
        self.update()

    def update(self, *args, **kwargs) -> None:
        """Update text of caption and its border. Three kinds of color of border
        correspond to #0099FF, #FC0FC0 and #00FF00

        Args:
            *args (any): Pass arguments if you are using caption text as format string
            **kwargs (any): Pass keyword arguments if you are using caption text as format string

        Note:
            Don't forget to call this function if you are redefining it (it must be called
            inside your function anywhere)

        Important:
            This function will recreate :class:`pygame.Rect` for this caption and previous
            position will be deleted (overwritten). Define `locate` function to change *rect*
            position after update
        """

        # Check if caption wasn't modified
        caption = self.caption.format(*args, **kwargs)
        color = self.config['user']['color']

        if (caption, color) == self._prev_caption:
            return

        # Synchronize image with the user's choice
        self.img = render(self.font, caption, self.fg_color, 2, self.colors[color])
        self.rect = self.img.get_rect()

        # Locate rect of text
        self.locate()

        # Cache caption
        self._prev_caption = (caption, color)

    def blit(self) -> None:
        """Blit of caption
        """
        self.screen.blit(self.img, self.rect)

    def locate(self) -> None:
        """Change *rect* position. If you don't override this function,
        caption will be located in the upper corner
        """
        pass


class SettingsButtonMixin(pygame.sprite.Sprite):
    """Mixin for creating settings buttons. Automatically changes the state
    and image of the button. Must be initialized at the bottom of your `__init__`
    function

    Args:
        screen (pygame.Surface): Screen (surface) obtained via pygame
        base_dir (str): An absolute path to directory where file with the main
            entrypoint is located
        config (spaceway.config.ConfigManager): The configuration object
        config_index (str): Key of the configuration (name of the state)

    Important:
        You should define an *imgs* dictionary with images for all states, e.g.:
        .. code:: python

            self.imgs = {state1: pygame.Surface, state2: pygame.Surface ...}
    """

    def __init__(self, screen, base_dir, config, config_index):
        """Constructor method
        """
        pygame.sprite.Sprite.__init__(self)

        # Setting variables for the further use
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config
        self.config_index = config_index

        # Getting state from configuration by *config_index*
        self.state = self.config['user'][self.config_index]

        # Setting image by current state and getting its hitbox
        self.img = self.imgs[self.state]
        self.rect = Ellipse(self.img.get_rect())

        # Configuring the generating hint images
        self.fg_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.border = 5
        self.border_radius = 3

        # Generating all hint images
        self.__gen_hints(base_dir)
        self.img_hint = self.imgs_hint[self.state]

        # Setting variables to work with the hover
        self.is_hover = False
        self.tick_hover = 0

    def __gen_hints(self, base_dir):
        """Generates hint images with description of the all button actions

        Args:
            base_dir (str): An absolute path to directory where file with the main
                entrypoint is located
        """
        # Get font object for the further text rendering
        font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 20)

        # Dictionary with images of hint messages, the structure is similar to `self.imgs`
        self.imgs_hint = {}

        for state, hint_text in self.hints.items():
            # Generating the text itself
            img_text = font.render(hint_text, True, self.fg_color)
            rect_text = img_text.get_rect()

            # Generating hint background (size a little more than text)
            rect_hint = rect_text.copy()
            rect_hint.w += self.border * 2
            rect_hint.h += self.border * 2

            img_hint = pygame.Surface(rect_hint.size, flags=pygame.SRCALPHA)
            pygame.draw.rect(img_hint, self.bg_color, rect_hint, 0, self.border_radius)

            # Blitting text to background
            rect_text.center = rect_hint.center
            img_hint.blit(img_text, rect_text)

            # Exporting hint image to dictionary
            self.imgs_hint[state] = img_hint

    def change_state(self) -> None:
        """Changes state of button. By default it has on-off behaviour. Override
        method for another behaviour
        """
        self.state = not self.state

    def update(self) -> None:
        """Update button: synchronize image and configuration with button state
        """
        # Synchronizing image and configuration
        self.img = self.imgs[self.state]
        self.img_hint = self.imgs_hint[self.state]
        self.config['user'][self.config_index] = self.state

        point = pygame.mouse.get_pos()

        if self.rect.collidepoint(point):
            # If mouse hovered on button, continue countdown
            self.tick_hover += self.config['ns'].dt / 30
        else:
            # Otherwise, reset the tick to stop the countdown
            self.tick_hover = 0
            self.is_hover = False

        # If enough time has passed, show a hint
        if self.tick_hover > 0.7:
            self.is_hover = True

    def blit(self) -> None:
        """Blit button
        """
        self.screen.blit(self.img, self.rect)

    def blit_hint(self) -> None:
        """Blit hint
        """
        if self.is_hover:
            rect = self.img_hint.get_rect()
            rect.bottomleft = pygame.mouse.get_pos()
            self.screen.blit(self.img_hint, rect)

    def press(self) -> None:
        """Press callback of button. Changes self state and updates itself
        """
        self.change_state()
        self.update()

        # Hide hint after button pressing
        self.is_hover = False
        self.tick_hover = 0


class BoostMixin(pygame.sprite.Sprite):
    """Mixin for creating boosts. Must be initialized at the bottom of your
    `__init__` function

    Args:
        screen (pygame.Surface): Screen (surface) obtained via pygame
        base_dir (str): An absolute path to directory where file with the main
            entrypoint is located
        config (spaceway.config.ConfigManager): The configuration object
        name (str): Name of boost (defines a type of button)
        life (float): Lifetime of boost (in seconds)

    Important:
        You must previously define :img_idle:`pygame.Surface` (moving image
        that is displayed before activation) and :img_small:`pygame.Surface`
        (displayed in the upper-left corner after activation)
    """

    COLOR_LONG = (255, 255, 255)   # Color of lifetime if there are a lot of
    COLOR_SHORT = (255, 0, 0)      # Color of lifetime if there are a few of

    def __init__(self, screen, base_dir, config, name, life):
        """Constructor method
        """
        pygame.sprite.Sprite.__init__(self)

        # Setting variables for the further use
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 28)

        self.name = name
        self.life = life
        self.is_active = False

        # Generating a hitbox of :img_idle:`pygame.Surface` and randomly positioning it
        self.rect_idle = Ellipse(self.img_idle.get_rect())
        self.rect_idle.y = randint(self.screen_rect.top, self.screen_rect.bottom - self.rect_idle.height - 2)
        self.rect_idle.left = self.screen_rect.right
        self.rect = self.rect_idle

        # Generating a rect of :img_small:`pygame.Surface` and positioning it at the upper-left corner
        self.rect_small = self.img_small.get_rect()
        self.rect_small.left = self.screen_rect.left + 2

    def update(self) -> None:
        """Updates boost
        """
        # If boost was activated
        if self.is_active:
            # Count life time
            self.life -= self.config['ns'].dt / 30

            if self.life <= 0:
                # Deactivate and kill the boost if there is no time left
                self.deactivate()
                self.kill()
                return

            # Vertical positioning of boost, taking into account the number in the boost queue
            self.rect_small.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)

            # Generating text with the remaining lifetime
            if ceil(self.life) <= 3:
                # Rendering text using *COLOR_SHORT*, if there is little time left
                self.img_life = self.font.render(f"{ceil(self.life)}S", True, self.COLOR_SHORT)
                self.rect_life = self.img_life.get_rect()
                self.rect_life.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
                self.rect_life.left = self.screen_rect.left + 24
            else:
                # Rendering text using *COLOR_LONG*, if there is a lot of time left
                self.img_life = self.font.render(f"{ceil(self.life)}S", True, self.COLOR_LONG)
                self.rect_life = self.img_life.get_rect()
                self.rect_life.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
                self.rect_life.left = self.screen_rect.left + 24
        else:
            # Continue movement of boost if it has not activated yet
            self.rect_idle.x -= self.config['ns'].speed * self.config['ns'].dt

        # Kill boost if it has left the screen
        if self.rect_idle.right < 0:
            self.kill()

    def blit(self) -> None:
        """Blit boost
        """
        if self.is_active:
            # If boost was activated, blit small and time left images
            self.screen.blit(self.img_life, self.rect_life)
            self.screen.blit(self.img_small, self.rect_small)
        else:
            # If boost was not activated, blit idle image
            self.screen.blit(self.img_idle, self.rect_idle)

    def activate(self) -> None:
        """Сallback that is called when the boost is activated

        Importnant:
            Do not forget to call this method if you redefine it in your boost
        """
        # Activate boost
        self.is_active = True

    def deactivate(self) -> None:
        """Callback that is called when the boost is deactivated
        """
        pass
