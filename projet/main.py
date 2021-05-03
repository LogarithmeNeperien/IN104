#!/usr/bin/env python3

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import DummyEngine
from simulator.graphics import Screen

import pygame as pg

if __name__ == "__main__":

    v1 = 0.3471168881
    v2 = 0.5327249454
    M = 1

    b1 = Body(Vector2(-1,0),
              velocity=Vector2(v1, v2),
              mass=M,
              color = (0,128,128),
              draw_radius=2)
    b2 = Body(Vector2(1, 0),
              velocity=Vector2(v1, v2),
              mass=M,
              color = (255,240,20),
              draw_radius=2)
    b3 = Body(Vector2(0,0),
              velocity = Vector2(-2*v1,-2*v2),
              mass = M,
              color = (255,50,50),
              draw_radius =2)
    # b4 = Body(Vector2(15, 15),
    #           velocity=Vector2(-3, 3),
    #           mass=300,
    #           color = (255,50,50),
    #           draw_radius=20)
    world = World()
    world.add(b1)
    world.add(b2)
    world.add(b3)
    #world.add(b4)

    simulator = Simulator(world, DummyEngine, DummySolver)

    screen_size = Vector2(900, 600)
    screen = Screen(screen_size,
                    bg_color=(0, 0, 0),
                    caption="Simulator")
    screen.camera.scale = 50

    # this coefficient controls the speed
    # of the simulation
    time_scale = 1000

    print("Start program")
    while not screen.should_quit:
        dt = screen.tick(60)

        # simulate physics
        delta_time = time_scale * dt / 1000
        simulator.step(delta_time)

        # read events
        screen.get_events()

        # handle events
        #   scroll wheel
        if screen.get_wheel_up():
            screen.erase()
            screen.camera.scale *= 1.1
        elif screen.get_wheel_down():
            screen.erase()
            screen.camera.scale *= 0.9

        # draw current state
        screen.draw(world)

        # draw additional stuff
        screen.draw_corner_text("Time: %f" % simulator.t)

        # show new state
        screen.update()

    screen.close()
    print("Done")
