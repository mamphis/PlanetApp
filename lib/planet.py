'''
' Filename		planet.py
' Author		gandie
' License		
' Description	The Planet itself. It is Defined by differente fields, eg. mass,
'				speed, direction...
' Version		0.0.8
' Date			18:25 27.11.2015
'''

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, 
							BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
from math import sqrt, pow
from kivy.graphics import Line
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.settings import SettingsWithSidebar
from settingsjson import settings_json
from kivy.core.image import Image
from random import choice

import os
from lib.planet import Planet
from lib.planetgame import PlanetGame
from lib.planetgamelayout import PlanetGameLayout
from lib.settingsbutton import SettingsButton
from lib.utilitys import Utilitys

class Planet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    red = NumericProperty(255)
    green = NumericProperty(255)
    blue = NumericProperty(255)
    colour = ReferenceListProperty(red, green, blue)

    fixed = BooleanProperty(False)

    mass = NumericProperty(1)
    density = NumericProperty(10)

    showforcelimit = NumericProperty(5)

    def __init__(self, fixed, position, velocity, mass, density, colour,
                 **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.fixed = fixed
        self.mass = mass
        self.center = (position[0],position[1])
        self.velocity = velocity
        self.density = density
        self.colour = colour
        self.showforcelimit = float(Utilitys.get_app_config('planetapp',
                                                            'showforcelimit'))
        self.calc_size()
        self.hillbodies = []

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def calc_gravity(self, planet, gravity):
        if not self.fixed:
            dist_x = self.center_x - planet.center_x
            dist_y = self.center_y - planet.center_y
            dist = self.parent.calc_distance(self.center,planet.center)

            force = (gravity * self.mass * planet.mass) / (dist**2)
            force_x = force * (dist_x / dist)
            force_y = force * (dist_y / dist)

            self.calc_hillbodies(force, planet)

            self.velocity_x -= force_x / self.mass
            self.velocity_y -= force_y / self.mass

    def calc_hillbodies(self, force, planet):
        # typecasting problem while crosscompiling
        foo = Utilitys.get_app_config('planetapp','showforcemode')
        if foo == u'0':
            return
        if ((force / self.mass) > (self.showforcelimit * 0.0002)):
            if not planet.fixed:
                if not planet in self.hillbodies: 
                    self.hillbodies.append(planet)
        else:
            if planet in self.hillbodies:
                self.hillbodies.remove(planet)

        for dude in self.canvas.children:
            if 'InstructionGroup' in  type(dude).__name__:
                self.canvas.remove(dude)
        shit = InstructionGroup()
        for body in self.hillbodies:
            shit.add(Line(points=(self.center_x,self.center_y,
                                  body.center_x,body.center_y),
                          width=1,
                          group=str(self.uid)))
        if len(self.hillbodies) > 0:
            self.canvas.add(shit)


    def merge(self, planet):

        impulse_x = (self.velocity_x * self.mass + planet.velocity_x * planet.mass)
        impulse_y = (self.velocity_y * self.mass + planet.velocity_y * planet.mass)

        self.mass += planet.mass

        if not self.fixed:
            self.velocity_x = impulse_x / self.mass
            self.velocity_y = impulse_y / self.mass
        if (self.red > 0.1) and not self.fixed:
            self.red -= 0.1
        self.hillbodies = []

    def on_mass(self, instance, value):
        self.calc_size()

    def calc_size(self):
        diameter = 2 * sqrt(self.density * self.mass / 3.14)
        self.size = (diameter,diameter)
