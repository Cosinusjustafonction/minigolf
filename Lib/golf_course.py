from Lib.vectors import *
from Lib.physics import *
import math
import pyglet
from math import pi, atan2
import json
from Lib.ball import Ball

class GolfCourse:

	def __init__(self, json_path, window):
		f = open( json_path, )
		self.map_data = json.load( f )
		f.close()
		self.hole_position = vec2d( self.map_data["hole_position"][0], self.map_data["hole_position"][1] )
		print( self.hole_position )
		self.ball = Ball(
			vec3d( self.map_data["ball_initial_position"][0], self.map_data["ball_initial_position"][1], 0 ), 5, self )
		print( self.ball.displacement.position )
		self.ball.displacement.acceleration = vec3d( 0, 0, -10 )
		self.background = pyglet.graphics.Batch()
		self.batch = pyglet.graphics.Batch()
		self.music_player = pyglet.media.Player()
		self.music_player.loop = True
		self.music_player.queue( pyglet.media.load( "Assets/BackGroundMusic.m4a" ) )
		self.music_player.volume = 0.2
		self.music_player.play()
		course_image = pyglet.image.load( "Assets/GolfCourseTexture.png" )
		self.golf_sprite = pyglet.sprite.Sprite( course_image, 0, 0, batch=self.background )
		self.golf_sprite.scale = max( window.width, window.height ) / min( self.golf_sprite.height,
		                                                                   self.golf_sprite.width )
		self.hole = pyglet.shapes.Circle( x=self.hole_position[0], y=self.hole_position[1], radius=10, color=(0, 0, 0),
		                                  batch=self.batch )
		self.radius = 0.01 * max( window.height, window.width )
		self.isdraw = False
		self.obstacles = []
		for obstacle in self.map_data["obstacles"]:
			self.obstacles.append( [obstacle[3], obstacle[2], obstacle[0], obstacle[1], (119, 52, 0)] )
		self.all_obstacles()

	def strike(self):
		if self.ball.is_grounded() and self.ball.is_stopped():
			acceleration_vector = vec3d( -(self.x_dist) * 100,
			                             -(self.y_dist) * 100, 0 )
			self.ball.displacement.strike( acceleration_vector, 1 / 10 )
			self.ball.audio.play()
			self.arrow.delete()

	def draw_rect(self, dx, dy):
		if not self.ball.is_grounded() or not self.ball.is_stopped():
			return
		self.x = self.ball.displacement.position[0]
		self.y = self.ball.displacement.position[1]
		self.dx = dx
		self.dy = dy
		self.toul = math.sqrt( (self.dx - 200) ** 2 + (self.dy - 150) ** 2 )
		if self.toul > 100:
			self.toul = 100
		elif self.toul < -100:
			self.toul = -100
		self.x_dist = self.dx - self.x
		self.y_dist = self.dy - self.y
		if self.x_dist ** 2 + self.y_dist ** 2 > 100 ** 2:
			factor = 100 / math.sqrt( self.x_dist ** 2 + self.y_dist ** 2 )
			self.x_dist *= factor
			self.y_dist *= factor
		self.arrow = pyglet.shapes.Line( x=self.ball.displacement.position[0], y=self.ball.displacement.position[1],
		                                 x2=self.ball.displacement.position[0] - self.x_dist,
		                                 y2=self.ball.displacement.position[1] - self.y_dist, width=4,
		                                 color=(0, 25, 77),
		                                 batch=self.batch )
		self.arrow.opacity = 150
		self.arrow.rotation = (atan2( self.y_dist, -self.x_dist ) % (2 * pi)) * 180 / pi  # gets angle of the arrow

	def draw(self, interval):
		self.background.draw()
		for i in self.obstacles:
			self.init_obstacles( i[1], i[0], i[2], i[3], i[4] ).draw()
		self.batch.draw()
		if not self.ball.hole:
			self.ball.draw( interval, self.hole )
		else:
			label = pyglet.text.Label( 'Hole !',
			                           font_name="Big Shoulders Display",
			                           font_size=50,
			                           bold=True,
			                           x=window.width // 2, y=window.height - window.height // 3,
			                           anchor_x='center', anchor_y='center',
			                           color=(217, 252, 18, 255) )
			label.draw()
			self.music_player.pause()

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		main_pos = x, y
		self.draw_rect( main_pos[0], main_pos[1] )

	def all_obstacles(self):
		self.get_bareer( 480, 10, 0, 0, (119, 52, 0) )
		self.get_bareer( 10, 960, 0, 470, (119, 52, 0) )
		self.get_bareer( 480, 10, 950, 0, (119, 52, 0) )
		self.get_bareer( 10, 960, 0, 0, (119, 52, 0) )

	def get_bareer(self, height, width, x, y, color):
		self.obstacles.append( (height, width, x, y, color) )

	def init_obstacles(self, width, height, x, y, color):

		return pyglet.shapes.Rectangle( width=width, height=height, x=x, y=y, color=color,
		                                batch=self.batch )

	def on_mouse_release(self, x, y, button, modifiers):
		self.strike()