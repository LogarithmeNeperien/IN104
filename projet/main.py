#!/usr/bin/env python3
# 04/05 Seta: ajout du suivi d'objet par la caméra et du déplacement de la caméra par clic
# 11/05 Seta: possibilité d'ajouter des corps àl'aide du clic du milieu, l'affichage du nombre de corps dans le monde en bas à droite
# seta: on centre sur la position moyenne la camera au début
#16/05 : Theophane : possibilité de sélectionner la configuration de départ directement en ligne de commande, les configurations disponibles sont dans le fichier trajectories.txt

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import DummyEngine
from simulator.graphics import Screen

import pygame as pg
import sys

if __name__ == "__main__":

    world = World()

    #Permet de sélectionner la trajectoire voulue
    f = open("trajectories.txt","r")

    line = f.readline()

    while line != (str(sys.argv[1])+'\n') :
        line = f.readline()
        if line == '' :
            print("Please type a valid trajectory")
            f.close()
            sys.exit()

    print("You have selected the " + str(line)+" configuration")
    nb_body = int(f.readline())

    for i in range(nb_body):
        attributes = f.readline().split()
        position = Vector2(float(attributes[0]),float(attributes[1]))
        velocity = Vector2(float(attributes[2]),float(attributes[3]))
        mass = float(attributes[4])
        color = (int(attributes[5]),int(attributes[6]),int(attributes[7]))
        real_radius = float(attributes[8])
        draw_radius = float(attributes[9])
        b = Body(position,velocity,mass,color,real_radius,draw_radius)
        world.add(b)

    f.close()

    #Permet de contrôler l'affichage des traçantes
    should_erase_background = True


    simulator = Simulator(world, DummyEngine, DummySolver)

    screen_size = Vector2(800, 600)
    screen = Screen(screen_size, bg_color=(0, 0, 0), caption="Simulator")

    # centrage de la caméra
    for b in world.bodies():
        screen.camera.position = b.position

        screen.camera.position /= len(world)

    # le bon scale (diagonale d'écran/ distance max entre body et la caméra)
    max_norm = 1
    for b in world.bodies():
        max_norm = max(max_norm, (b.position - screen.camera.position).norm())

        screen.camera.scale = screen_size.get_y() / max_norm / 2
    # this coefficient controls the speed
    # of the simulation
    time_scale = 1

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

        # right click : the camera centers on the clicked body; if the void is right clicked, the camera stay put
        elif screen.get_right_mouse():

            no_match = True
            for b in world.bodies():

                pos_abs_mouse = screen.camera.from_screen_coords(screen.mouse_position)

                if (
                    abs(pos_abs_mouse - b.position)
                    < b.draw_radius / screen.camera.scale
                ):
                    screen.camera.follows = world.get(b.id_nb)
                    no_match = False

                if no_match:
                    screen.camera.follows = None

        # left click : the camera centers on the clicked region
        elif screen.get_left_mouse():
            camera = screen.camera
            camera.position = camera.from_screen_coords(screen.mouse_position)

        # middle click : add a body on the click if there is enough room

        elif screen.get_middle_mouse():

            position_absolue = screen.camera.from_screen_coords(screen.mouse_position)
            b = Body(position_absolue, velocity=Vector2(0, 0), mass=1, draw_radius=10)

            world.add(b)

            simulator.solver.y0 = simulator.engine.make_solver_state()

        # positioning of camera
        if screen.camera.follows is not None:
            camera = screen.camera
            camera.position = camera.follows.position

        # draw current state
        screen.draw(world,should_erase_background)

        # draw additional stuff
        screen.draw_corner_text("Time: %f" % simulator.t)
        screen.draw_corner_text(
            "Scale :%.2f Nb of Bodys: %d" % (screen.camera.scale, len(world)), False
        )

        # show new state
        screen.update()

    screen.close()
    print("Done")
