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
    # b1 = Body(Vector2(-1,0),
    #           velocity=Vector2(v1,v2),
    #           mass=M,
    #           color = (255,0,230),
    #           draw_radius=5)
    # b2 = Body(Vector2(1,0),
    #           velocity=Vector2(v1, v2),
    #           mass=M,
    #           color = (50,255,0),
    #           draw_radius=5)
    # b3 = Body(Vector2(0,0),
    #           velocity=Vector2(-2*v1, -2*v2),
    #           mass=M,
    #           color = (255,50,50),
    #           draw_radius=5)



    b1 = Body(Vector2(-0.5358076316429841,0.37180556472793874),
              velocity=Vector2(0.9743317053313775, -1.096362116657104),
              mass=M,
              color = (0,128,128),
              draw_radius=4)
    b2 = Body(Vector2(0.7676771558912595, -0.867823428450871),
              velocity=Vector2(0.08096334827522714, -1.0175492452692891),
              mass=M,
              color = (255,240,20),
              draw_radius=4)
    b3 = Body(Vector2(-0.031055488577342624,-1.2763443049957865 ),
              velocity = Vector2(-0.6990773093771361,0.672388539946965),
              mass = M,
              color = (255,50,50),
              draw_radius =4)
    b4 = Body(Vector2(0.1675715831569598, 0.3604411202596589),
              velocity=Vector2(0.5493639322512589 , 1.5662040016531198),
              mass=M,
              color = (50,255,0),
              draw_radius=4)
    b5 = Body(Vector2(-0.36838561882789267, 1.41192104845906),
              velocity=Vector2(-0.9055816764807272, -0.12468117967369167),
              mass=M,
              color = (255,0,230),
              draw_radius=4)
    world = World()
    world.add(b1)
    world.add(b2)
    world.add(b3)
    world.add(b4)
    world.add(b5)

    simulator = Simulator(world, DummyEngine, DummySolver)

    screen_size = Vector2(1200, 800)
    screen = Screen(screen_size,
                    bg_color=(0, 0, 0),
                    caption="Simulator")
    screen.camera.scale = 50

    # this coefficient controls the speed
    # of the simulation
    time_scale = 10

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
