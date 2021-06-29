import pyglet
import numpy as np 
import math 
window = pyglet.window.Window(resizable=True)

class GolfCourse:

	def __init__(self,hole_position,ball_position):
		self.hole_position = hole_position
		self.ball_position = ball_position
		self.batch = pyglet.shapes.Batch()
		self.course = pyglet.shapes.Rectangle(width=window.width, height=window.height,x=0,y=0,color=(13, 143, 26),batch=self.batch)
		self.hole = pyglet.shapes.Circle(x=self.hole_position[0],y=self.hole_position[1],radius=0.01*max(window.height,window.width),color=(0,0,0),batch=self.batch)
		self.ball = pyglet.shapes.Circle( x=self.ball_position[0], y=self.ball_position[1],
		                                  radius=0.01 * max( window.height, window.width ), color=(255, 255, 255),
		                                  batch=self.batch )
		self.radius = 0.01*max(window.height,window.width)
		self.isdraw = False 
	def draw_rect(self,dx,dy) : 
		self.x = self.ball_position[0]
		self.y = self.ball_position[1]
		self.dx = dx
		self.dy = dy
		self.toul = math.sqrt((self.dx-200)**2+(self.dy-150)**2)
		if self.toul > 100 :
			self.toul = 100
		elif self.toul < -100 : 
			self.toul = -100
		self.arrow= pyglet.shapes.Rectangle(width=self.toul, height=5,x=self.x,y=self.y,color=(0, 25, 77),batch=self.batch,)
		self.arrow.rotation = (180 / math.pi) * math.atan2(self.dy, self.dx)#gets angle of the arrow 
		self.batch.draw()
	def draw(self):
		self.batch.draw()

golf_course = GolfCourse((10,10),(200,150))

@window.event()
def on_draw():
	window.clear()
	golf_course.draw()
	
@window.event() 
def on_mouse_drag(x,y,dx,dy,button, modifiers) : 
	main_pos = x, y
	golf_course.draw_rect(main_pos[0],main_pos[1])
	print(main_pos)
@window.event()
def on_mouse_release(x, y, button, modifiers):
	golf_course.arrow.delete()
	#here the mooving function
pyglet.app.run()
