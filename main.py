import pyglet
from Lib.vectors import vec3d, vec2d
from Lib.physics import *
from Lib.golf_course import GolfCourse
import math
from math import pi, atan2
import json
from Lib.widgets import MenuWindow

pyglet.font.add_directory( "Assets" )

pyglet.clock.schedule_interval( lambda x: x, 1 / 120 )


class game( pyglet.window.Window ):
	def __init__(self, kwargs):
		super( game, self ).__init__( **kwargs )
		button_width = 200
		button_height = 50
		self.currentWindow = MenuWindow({"x":(self.width-button_width)/2,"y":(self.height-button_width)/3-button_height/2,"width":button_width,"height":button_height,"color":(30,150,20)},texts=["Start game"],callback=lambda x,y: self.start_game())
		self.alive = 1
	def start_game(self):
		self.currentWindow = GolfCourse( "Maps/map_demo.json", self )
	def on_draw(self):
		self.clear()
		self.currentWindow.draw( 1 / 120 )

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		self.currentWindow.on_mouse_drag( x, y, dx, dy, button, modifiers )

	def on_mouse_release(self, x, y, button, modifiers):
		self.currentWindow.on_mouse_release( x, y, button, modifiers )

	def on_mouse_press(self, x, y, button, modifiers):
		self.currentWindow.on_mouse_press(x,y,button,modifiers)


window = game( {"width": 960, "height": 480} )
pyglet.app.run()
