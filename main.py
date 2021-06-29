import pyglet
from Lib.vectors import vec3d,vec2d
from Lib.physics import Displacement
import math
from math import pi,atan2


window = pyglet.window.Window(resizable=False)
pyglet.font.add_directory("Assets")

class Ball:
	def __init__(self,position,radius):
		print(position)
		self.shape = self.ball = pyglet.shapes.Circle( x=position[0], y=position[1],
		                                  radius=radius , color=(255, 255, 255))
		print(self.shape.position)
		self.displacement = Displacement(position,vec3d(0,0,0),vec3d(0,0,-10))
		self.audio = pyglet.media.load("Assets/GolfClubSound.mp3", streaming=False)
		self.original_radius  = radius
		self.hole = False
	def draw(self,interval,hole):
		self.is_hole( hole )
		self.displacement.mov(interval)
		self.shape.position = self.displacement.position[0],self.displacement.position[1]
		self.shape.radius = self.original_radius+self.displacement.position[2]*self.original_radius*0.3
		self.shape.draw()
	def is_grounded(self):
		return self.displacement.position[2]<=0
	def is_stopped(self):
		return self.displacement.speed == vec3d(0,0,0)
	def is_hole(self,hole):
		if self.displacement.is_collision([self.shape.x-self.shape.radius, self.shape.y-self.shape.radius, self.shape.radius, self.shape.radius],[hole.x-hole.radius, hole.y-hole.radius, hole.radius, hole.radius] ) and self.displacement.position[2]<=0:
			self.displacement.speed = vec3d(0,0,0)
			self.displacement.position[0]=hole.x
			self.displacement.position[1]=hole.y
			self.displacement.position[2] = -10
			self.hole = True
			ScoreSound = pyglet.media.load( "Assets/GolfHoleSound.mp3", streaming=False )
			ScoreSound.play()
class GolfCourse:

	def __init__(self,hole_position,ball_position):
		self.hole_position = vec2d(hole_position[0],hole_position[1])
		self.ball = Ball(vec3d(ball_position[0],ball_position[1],0),5)
		self.ball.displacement.acceleration = vec3d(0,0,-10)
		self.batch = pyglet.graphics.Batch()
		self.course = pyglet.shapes.Rectangle(width=window.width, height=window.height,x=0,y=0,color=(13, 143, 26),batch=self.batch)
		self.hole = pyglet.shapes.Circle(x=self.hole_position[0],y=self.hole_position[1],radius=0.01*max(window.height,window.width),color=(0,0,0),batch=self.batch)
		self.radius = 0.01*max(window.height,window.width)
		self.isdraw = False

	def strike(self,x,y):
		if golf_course.ball.is_grounded() and golf_course.ball.is_stopped():
			acceleration_vector = vec3d( (golf_course.ball.displacement.position[0] - x) * 10,
			                             (golf_course.ball.displacement.position[1] - y) * 10, 100 )
			golf_course.ball.displacement.strike( acceleration_vector, 1 / 10 )
			golf_course.ball.audio.play()
			golf_course.arrow.delete()
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
		self.arrow = pyglet.shapes.Rectangle( width=self.toul, height=5, x=self.x, y=self.y+2.5, color=(0, 25, 77),
		                                      batch=self.batch, )
		self.arrow.rotation = (atan2( self.y_dist, -self.x_dist ) % (2 * pi)) * 180 / pi  # gets angle of the arrow


	def draw(self,interval):
		self.batch.draw()
		if not self.ball.hole:
			self.ball.draw(interval,self.hole)
		else:
			label = pyglet.text.Label( 'Hole !',
			                           font_name="Big Shoulders Display",
			                           font_size=50,
			                           bold=True,
			                           x=window.width // 2, y=window.height-window.height // 3,
			                           anchor_x='center', anchor_y='center',
			                           color=(217, 252, 18,255))
			label.draw()
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
	golf_course.strike(x,y)
	#here the mooving function
pyglet.app.run()