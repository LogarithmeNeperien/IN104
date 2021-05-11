#!/usr/bin/env python3
#04/05 Seta: ajout du suivi d'objet par la caméra et du déplacement de la caméra par clic
#11/05 Seta: possibilité d'ajouter des corps àl'aide du clic du milieu, l'affichage du nombre de corps dans le monde en bas à droite

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import DummyEngine
from simulator.graphics import Screen

import pygame as pg

if __name__ == "__main__":
    b1 = Body(Vector2(100, 100),
              velocity=Vector2(0, 0),
              mass=1,
              draw_radius=10)
    b2 = Body(Vector2(5, 80),
              velocity=Vector2(0, 0),
              mass=1,
              draw_radius=10)

    b3 = Body(Vector2(50, 96),
              velocity=Vector2(0, 0),
              mass=1,
              draw_radius=10)

    world = World()
    world.add(b1)
    world.add(b2)
    world.add(b3)

    simulator = Simulator(world, DummyEngine, DummySolver)

    screen_size = Vector2(800, 600)
    screen = Screen(screen_size,
                    bg_color=(0, 0, 0),
                    caption="Simulator")
    screen.camera.scale = 10

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

        #right click : the camera centers on the clicked body; if the void is right clicked, the camera stay put
        elif screen.get_right_mouse():
            
            no_match=True
            for b in world.bodies():
                
                pos_abs_mouse=screen.camera.from_screen_coords(screen.mouse_position)

                if abs(pos_abs_mouse-b.position)<b.draw_radius/screen.camera.scale:
                    screen.camera.follows=world.get(b.id_nb)
                    no_match=False

            if no_match:
                screen.camera.follows=None

	   #left click : the camera centers on the clicked region
        elif screen.get_left_mouse():
            camera=screen.camera
            camera.position=camera.from_screen_coords(screen.mouse_position)-0.5*camera.screen_size/camera.scale #le -0.5*... sert à que la caméra centre sur le clic gauche

        #middle click : add a body on the click if there is enough room

        elif screen.get_middle_mouse():
            position_absolue=screen.camera.from_screen_coords(screen.mouse_position)
            b = Body(position_absolue,
              velocity=Vector2(0, 0),
              mass=1,
              draw_radius=10)
            world.add(b)
            simulator.solver.y0=simulator.engine.make_solver_state()


        #positioning of camera
        if screen.camera.follows is not None:
            camera=screen.camera
            camera.position=camera.follows.position-0.5*camera.screen_size/camera.scale


        # draw current state
        screen.draw(world)

        # draw additional stuff
        screen.draw_corner_text("Time: %f" % simulator.t)
        screen.draw_corner_text("Nb of Bodys: %d" % len(world),False)
        #screen.draw_corner_text("Nb of Body: %f" % len(world))


        # show new state
        screen.update()

    screen.close()
    print("Done")
