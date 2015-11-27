'''
' Filename		planetgamelayout.py
' Author		gandie
' License		
' Description	Handling Touch-Events for the Buttons and the Slider
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


class PlanetGameLayout(BoxLayout):
    def on_touch_down(self, touch):
        if self.children[0].collide_point(touch.x,touch.y):
            self.children[0].on_touch_down(touch)
            #print 'Button1'
        elif self.children[1].collide_point(touch.x,touch.y):
            self.children[1].on_touch_down(touch)
            #print 'Button2'
        elif self.children[3].collide_point(touch.x,touch.y):
            self.children[3].on_touch_down(touch)
            #print 'Slider'
        else:
            self.children[2].on_touch_down(touch)
            #print 'Game'

    def on_touch_up(self, touch):
        if self.children[0].collide_point(touch.x,touch.y):
            self.children[0].on_touch_up(touch)
            #print 'Button1'
        elif self.children[1].collide_point(touch.x,touch.y):
            self.children[1].on_touch_up(touch)
            #print 'Button2'
        elif self.children[3].collide_point(touch.x,touch.y):
            self.children[3].on_touch_up(touch)
            #print 'Slider'
        else:
            pass
            #self.children[2].on_touch_up(touch)
            #print 'Game'


    def clear_planets(self,instance):
        self.children[2].clear_planets()

    def reset_game(self):
        self.children[2].reset_game()
