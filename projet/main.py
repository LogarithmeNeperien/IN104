#!/usr/bin/env python3
#04/05 Seta: ajout du suivi d'objet par la caméra et du déplacement de la caméra par clic

#11/05 Theophane: ajout de la possibilité d'afficher ou non les traçantes des objets par pression de la molette de la souris

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import DummyEngine
from simulator.graphics import Screen

import pygame as pg

if __name__ == "__main__":
    b1 = Body(Vector2(10, 10),
              velocity=Vector2(0.002, 0),
              mass=10,
              draw_radius=50,
              real_radius=5)
    b2 = Body(Vector2(1, 1),
              velocity=Vector2(0, 0),
              mass=1,
              draw_radius=5,
              real_radius=1)

    world = World()
    world.add(b1)
    world.add(b2)

    simulator = Simulator(world, DummyEngine, DummySolver)

    screen_size = Vector2(800, 600)
    screen = Screen(screen_size,
                    bg_color=(0, 0, 0),
                    caption="Simulator")
    screen.camera.scale = 50

    should_erase_background = True

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
            screen.camera.scale *= 1.1
        elif screen.get_wheel_down():
            screen.camera.scale *= 0.9

        #right click : the camera centers on the body clicked; if the void is right clicked, the camera stay put
        elif screen.get_right_mouse():

            no_match=True
            for b in world.bodies():

                pos_abs_mouse=screen.camera.from_screen_coords(screen.mouse_position)

                if abs(pos_abs_mouse-b.position)<b.draw_radius/screen.camera.scale:
                    screen.camera.follows=world.get(b.id_nb)
                    no_match=False

            if no_match:
                screen.camera.follows=None


        elif screen.get_left_mouse():
            camera=screen.camera
            camera.position=camera.from_screen_coords(screen.mouse_position)-0.5*camera.screen_size/camera.scale #le -0.5*... sert à que la caméra centre sur le clic gauche


        #positioning of camera
        if screen.camera.follows is not None:
            camera=screen.camera
            camera.position=camera.follows.position-0.5*camera.screen_size/camera.scale

        # enable or disable body visual tracking
        if screen.get_middle_mouse():
            should_erase_background = not(should_erase_background)

        # draw current state
        screen.draw(world,should_erase_background)

        # draw additional stuff
        screen.draw_corner_text("Time: %f" % simulator.t)

        # show new state
        screen.update()

    screen.close()
    print("Done")
