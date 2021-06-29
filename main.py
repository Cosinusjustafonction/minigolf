import pyglet
from minigolf.Lib.vectors import vec3d,vec2d
from minigolf.Lib.physics import Displacement
import math
from math import pi,atan2
window = pyglet.window.Window(resizable=False)

class Ball:
	def __init__(self,position,radius):
		print(position)
		self.shape = self.ball = pyglet.shapes.Circle( x=position[0], y=position[1],
		                                  radius=radius , color=(255, 255, 255))
		print(self.shape.position)
		self.displacement = Displacement(position,vec3d(0,0,0),vec3d(0,0,-100))
		self.audio = pyglet.media.load("Assets/GolfClubSound.mp3", streaming=False)
	def draw(self,interval):
		self.displacement.mov(interval)
		self.shape.position = self.displacement.position[0],self.displacement.position[1]
		self.shape.draw()
class GolfCourse:

	def __init__(self,hole_position,ball_position):
		self.hole_position = vec2d(hole_position[0],hole_position[1])
		self.ball = Ball(vec3d(ball_position[0],ball_position[1],0),5)
		self.ball.displacement.acceleration = vec3d(0,0,-100)
		self.batch = pyglet.graphics.Batch()
		self.course = pyglet.shapes.Rectangle(width=window.width, height=window.height,x=0,y=0,color=(13, 143, 26),batch=self.batch)
		self.hole = pyglet.shapes.Circle(x=self.hole_position[0],y=self.hole_position[1],radius=0.01*max(window.height,window.width),color=(0,0,0),batch=self.batch)
		self.radius = 0.01*max(window.height,window.width)
		self.isdraw = False
	def draw_rect(self, dx, dy):
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
		self.arrow = pyglet.shapes.Rectangle( width=self.toul, height=5, x=self.x, y=self.y+2.5, color=(0, 25, 77),
		                                      batch=self.batch, )
		self.arrow.rotation = (atan2( -self.y_dist, self.x_dist ) % (2 * pi)) * 180 / pi  # gets angle of the arrow


	def draw(self,interval):
		self.batch.draw()
		self.ball.draw(interval)
		print(self.ball.displacement.position)
golf_course = GolfCourse((10,10),(200,150))
pyglet.clock.schedule_interval(lambda x: x,1/60)
@window.event()
def on_draw():
	window.clear()
	golf_course.draw(1/60)
@window.event()
def on_mouse_drag(x,y,dx,dy,button, modifiers) :
	main_pos = x, y
	golf_course.draw_rect(main_pos[0],main_pos[1])
@window.event()
def on_mouse_release(x, y, button, modifiers):
	acceleration_vector = vec3d((golf_course.ball.displacement.position[0]-x)*10,(golf_course.ball.displacement.position[1]-y)*10,10)
	golf_course.ball.displacement.strike(acceleration_vector,1/10)
	golf_course.ball.audio.play()
	golf_course.arrow.delete()
	#here the mooving function
pyglet.app.run()