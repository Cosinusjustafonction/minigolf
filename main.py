import pyglet
from Lib.vectors import vec3d,vec2d
from Lib.physics import *
import math
from math import pi,atan2


window = pyglet.window.Window(resizable=False,height=480,width=960)
pyglet.font.add_directory("Assets")

class Ball:
	def __init__(self,position,radius):
		self.shape = self.ball = pyglet.shapes.Circle( x=position[0], y=position[1],
		                                  radius=radius , color=(255, 255, 255))
		self.displacement = Displacement(position,vec3d(0,0,0),vec3d(0,0,-10))
		self.audio = pyglet.media.load("Assets/GolfClubSound.mp3", streaming=False)
		self.original_radius = radius
		self.hole = False
	def draw(self,interval,hole):
		self.is_hole( hole )

		self.displacement.mov(interval)
		self.shape.position = self.displacement.position[0],self.displacement.position[1]
		self.shape.radius = self.original_radius+self.displacement.position[2]*self.original_radius*0.3
		self.shape.draw()
		self.boundaries_col()
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
	#def boundaries_boundaries(self,x,y,width,height) : 
	def boundaries_col(self) : 
		for i in golf_course.obstacles :
			print(i)
			if self.displacement.is_collision([self.shape.x-self.shape.radius, self.shape.y-self.shape.radius, self.shape.radius, self.shape.radius],[i[2], i[3], i[1], i[0]] ):
				verts = get_verts_from_properties(*i[0:4])
				for i in range(4):
					intersection = intersect_two_lines_from_points(((self.displacement.position[0],self.displacement.position[1]),(0,)))
				self.rebound()
				continue 
	def rebound(self,normal) :
		acceleration_vector = vec3d( (golf_course.x_dist)+(30) * 10,
			                          (golf_course.y_dist)+(30) * 10, 0 )
		golf_course.ball.displacement.strike( acceleration_vector, 1 / 10 )
class GolfCourse:

	def __init__(self,hole_position,ball_position):
		self.hole_position = vec2d(hole_position[0],hole_position[1])
		self.ball = Ball(vec3d(ball_position[0],ball_position[1],0),5)
		self.ball.displacement.acceleration = vec3d(0,0,-10)
		self.background = pyglet.graphics.Batch()
		self.batch = pyglet.graphics.Batch()
		course_image = pyglet.image.load("Assets/GolfCourseTexture.png")
		self.golf_sprite = pyglet.sprite.Sprite(course_image,0,0,batch=self.background)
		self.golf_sprite.scale = max(window.width,window.height)/min(self.golf_sprite.height,self.golf_sprite.width)
		self.hole = pyglet.shapes.Circle(x=self.hole_position[0],y=self.hole_position[1],radius=10,color=(0,0,0),batch=self.batch)
		self.radius = 0.01*max(window.height,window.width)
		self.isdraw = False
		self.obstacles = []
		self.all_obstacles()

	def strike(self):
		if self.ball.is_grounded() and self.ball.is_stopped():
			acceleration_vector = vec3d( -(self.x_dist) * 10,
			                             -(self.y_dist) * 10, 100 )
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
		if self.x_dist**2+self.y_dist**2>100**2:
			factor = 100/math.sqrt(self.x_dist**2+self.y_dist**2)
			self.x_dist*=factor
			self.y_dist*=factor
		self.arrow = pyglet.shapes.Line(x=self.ball.displacement.position[0],y=self.ball.displacement.position[1],x2=self.ball.displacement.position[0]-self.x_dist,y2=self.ball.displacement.position[1]-self.y_dist, width=4,  color=(0, 25, 77),
		                                      batch=self.batch )
		self.arrow.opacity = 150
		self.arrow.rotation = (atan2( self.y_dist, -self.x_dist ) % (2 * pi)) * 180 / pi  # gets angle of the arrow


	def draw(self,interval):
		self.background.draw()
		for i in self.obstacles : 
			self.init_obstacles(i[1],i[0],i[2],i[3],i[4]).draw()
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
	def all_obstacles(self) : 
		self.get_bareer(480,10,0,0,(119, 52, 0))
		self.get_bareer(10,960,0,470,(119, 52, 0))
		self.get_bareer(480,10,950,0,(119, 52, 0))
		self.get_bareer(10,960,0,0,(119, 52, 0))
	def get_bareer(self,height,width,x,y,color) :
		self.obstacles.append((height, width, x, y, color))
	def init_obstacles(self,width,height,x,y,color) : 
		
		return pyglet.shapes.Rectangle(width=width,height=height,x=x,y=y, color=color,
                                              batch=self.batch )

golf_course = GolfCourse((50,60),(200,150))
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
	golf_course.strike()
	#here the mooving function
@window.event()
def on_mouse_press(x, y, button, modifiers):
	print(x,y)
pyglet.app.run() 
