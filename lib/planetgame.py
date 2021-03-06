'''
' Filename		planetgame.py
' Author		gandie
' License		
' Description	The Game-Handler for Handling events, like Touching the display
' 				anywhere but the Buttons and Slider.
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

class PlanetGame(Scatter):
    zoom = NumericProperty(1)
    gravity = NumericProperty(1)
    planetmass = NumericProperty(1)
    resetmass = NumericProperty(10)
    sunmass = NumericProperty(1000)

    def __init__(self, **kwargs):
        super(PlanetGame, self).__init__(**kwargs)
        self.textures = []
        self.files = []
        self.load_textures()

    def i_am_dead(self, deadplanet):
        for planet in self.children:
            if deadplanet in planet.hillbodies:
                planet.hillbodies.remove(deadplanet)

    def load_textures(self):
        path = ('./textures/')
        for file in os.listdir(path):
            if file.endswith('.png'):
                self.files.append(path + str(file))
        for string in self.files:
            self.textures.append(Image(string).texture)

    def add_planet(self, fixed, position, velocity, mass=1, 
                   density=5, colour=(1,1,1)):
        new_planet = Planet(fixed, position, velocity, mass, density, colour)
        if not fixed:
            new_planet.canvas.children[1].texture = choice(self.textures)
        self.add_widget(new_planet)

    def update(self,dt):
        for planet in self.children:
            if planet.fixed:
                planet.center = (self.width/2+50,self.height/2)
            planet.move()
            for planet2 in self.children:
                if planet == planet2:
                    continue
                planet.calc_gravity(planet2, self.gravity)
                if not planet.collide_widget(planet2):
                    continue
                if planet.mass < planet2.mass:
                    continue
                planet.merge(planet2)
                self.i_am_dead(planet2)
                self.remove_widget(planet2)

    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)

        ud = touch.ud
        ud['id'] = 'gametouch'
        ud['firstpos'] = touch.pos
        ud['group'] = g = str(touch.uid)

        with self.canvas:
            ud['lines'] = [
                Line(points=(touch.x,touch.y,touch.x+1,touch.y+1),width=1,
                     group=g)]
        
        touch.grab(self)
        touch.pop()

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        touch.push()
        touch.apply_transform_2d(self.to_local)
        ud = touch.ud

        velocity = ((ud['firstpos'][0] - touch.x) / -50, (ud['firstpos'][1] - touch.y) / - 50)
        planetpos = (ud['firstpos'][0], ud['firstpos'][1])

        sunpos = (self.width/2+50,self.height/2)
        trajectory = self.calc_trajectory(planetpos, velocity, self.planetmass,
                                          sunpos, self.sunmass, 1, 250)  

        # make this optional!
        #ud['lines'][0].points = (ud['firstpos'][0],ud['firstpos'][1],
        #                         touch.x,touch.y)


        ud['lines'][0].points = trajectory




        touch.pop()

    def calc_trajectory (self, coord_planet, speed_planet, weight_planet, coord_sun,
                     weight_sun, interval, count):
	gamma =  self.gravity
	L = []
	
	coords = coord_planet
	speed = speed_planet
	for i in range(count):
		r = self.calc_distance(coords, coord_sun)
		g = (-1 * gamma) * (weight_sun) / math.pow(r, 2.0) 
		gx = g * ((coords[0] - coord_sun[0]) / r)
		gy = g * ((coords[1] - coord_sun[1]) / r)
		speed = (speed[0] + (gx * interval), speed[1] + (gy * interval))
		coords = (coords[0] + (speed[0] * interval) + 
                          (0.5 * gx * math.pow(interval, 2.0)),
                          coords[1] + (speed[1] * interval) + 
                          (0.5 * gy * math.pow(interval, 2.0)))
		
		L.append(coords)
	
        R = []
        for item in L:
            R.append(item[0])
            R.append(item[1])

        return tuple(R)

    def calc_distance(self, tuple1, tuple2):
        dist =  math.sqrt(math.pow(tuple1[0] - tuple2[0], 2.0) + 
                          math.pow(tuple1[1] - tuple2[1], 2.0))
        if dist == 0: 
            dist = 0.000001
        return dist	 

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        touch.push()
        touch.apply_transform_2d(self.to_local)

        ud = touch.ud

        touchdownv = Vector(ud['firstpos'])
        touchupv = Vector(touch.pos)
        velocity = (touchupv - touchdownv) / 50
        print '#'
        print velocity

        self.add_planet(False, ud['firstpos'], (velocity.x, velocity.y), 
						self.planetmass)
        self.canvas.remove_group(ud['group'])

        touch.pop()

    def on_zoom(self,instance,value):
        self.scale = 1/value

    def clear_planets(self):
        L = []
        for planet in self.children:
            if planet.mass < self.resetmass:
                L.append(planet)
        if L:
            for planet in L:
                self.i_am_dead(planet)
            self.clear_widgets(L)

    def reset_game(self):
        L = []
        for planet in self.children:
            L.append(planet)
        if L:
            self.clear_widgets(L)
        sunmass = float(Utilitys.get_app_config('planetapp','defaultsunmass'))
        self.sunmass = sunmass
        self.gravity = float(Utilitys.get_app_config('planetapp','gravity'))
        self.planetmass = float(Utilitys.get_app_config('planetapp','planetmass'))
        self.resetmass = float(Utilitys.get_app_config('planetapp','resetmass'))
        self.add_planet(True, (100,100), (0,0), float(sunmass), 10, (1,1,1))
