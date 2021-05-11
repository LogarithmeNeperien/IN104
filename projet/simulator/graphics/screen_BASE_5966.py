import pygame as pg

from ..utils.pygame_utils import draw_text
from ..utils.vector import Vector2
from .camera import Camera


class Screen:
    def __init__(self, screen_size, bg_color=(0, 0, 0), caption=None):
        self.screen_size = screen_size
        self._bg_color = bg_color

        self.camera = Camera(screen_size)

        # this is incremented at each frame
        self.frame = 0

        # this will store the last recorded mouse position
        self.mouse_position = Vector2(0, 0)

        # this will store which buttons have been pressed in the current frame
        # [LeftMouse, MiddleMouse, RightMouse, ScrollWheelUp, SrollWheelDown]
        self._buttons = [False, False, False, False, False]

        # this will be true when the user presses the exit button of the window
        self.should_quit = False

        # this is used to limit the
        # number of frames computed evey second
        self.clock = pg.time.Clock()

        pg.init()
        self._screen = pg.display.set_mode(
            (self.screen_size.get_x(), self.screen_size.get_y()))
        self._font = pg.font.SysFont('Arial', 12)

        if caption is not None:
            pg.display.set_caption(caption)

    def get_events(self):
        self.mouse_position = Vector2(*pg.mouse.get_pos())

        for i in range(0, len(self._buttons)):
            self._buttons[i] = False

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.should_quit = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button <= len(self._buttons):
                    self._buttons[event.button - 1] = True

        self.frame += 1

    def draw(self, world):
        self._screen.fill(self._bg_color)

        s = pg.Surface(self.screen_size, pg.SRCALPHA)
        self.__draw_world(s, world)
        self._screen.blit(s, s.get_rect())

        draw_text(self._screen, self._font, "Frame: %s" % self.frame,
                  Vector2(0, 0), (255, 255, 255))
        draw_text(self._screen, self._font, "Mouse position: %s" % self.mouse_position,
                  Vector2(0, 12), (255, 255, 255))
        draw_text(self._screen, self._font, "Buttons: %s" % self._buttons,
                  Vector2(0, 24), (255, 255, 255))
        draw_text(self._screen, self._font, "Should quit: %s" % self.should_quit,
                  Vector2(0, 36), (255, 255, 255))

    def tick(self, fps):
        self.clock.tick(fps)
        return self.clock.get_time()

    def update(self):
        pg.display.update()

    def close(self):
        pg.display.quit()

    def __draw_world(self, s, world):
        for body in world.bodies():
            screen_pos = self.camera.to_screen_coords(body.position)
            pg.draw.circle(s, body.color,
                           (int(screen_pos.get_x()), int(screen_pos.get_y())),
                           int(body.draw_radius), 0)

    def draw_corner_text(self, s):
        draw_text(self._screen, self._font, s,
                  Vector2(0, self.screen_size.get_y() - 12), (255, 255, 255))

    def get_left_mouse(self): return self._buttons[0]
    def get_middle_mouse(self): return self._buttons[1]
    def get_right_mouse(self): return self._buttons[2]
    def get_wheel_up(self): return self._buttons[3]
    def get_wheel_down(self): return self._buttons[4]
