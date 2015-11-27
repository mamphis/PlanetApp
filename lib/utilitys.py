'''
' Filename		utilitys.py
' Author		mamphis
' License		
' Description	Utilitys :D
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

class Utilitys(App):
    def get_app_config(section, key):
		return App.get_running_app().config.get(section,key)