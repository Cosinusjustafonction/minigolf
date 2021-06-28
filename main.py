import pyglet
from minigolf.Lib.vectors import vec3d
from minigolf.Lib.physics import Displacement
window = pyglet.window.Window(resizable=True)

class Ball:
	def __init__(self,position,radius):
		self.shape = self.ball = pyglet.shapes.Circle( x=self.ball_position[0], y=self.ball_position[1],
		                                  radius=0.01 * max( window.height, window.width ), color=(255, 255, 255))
		self.displacement = Displacement(position,vec3d(0,0,0),vec3d(0,0,-10))
class GolfCourse:

	def __init__(self,hole_position,ball_position):
		self.hole_position = vec2d(hole_position)
		self.ball = Ball()
		self.batch = pyglet.shapes.Batch()
		self.course = pyglet.shapes.Rectangle(width=window.width, height=window.height,x=0,y=0,color=(13, 143, 26),batch=self.batch)
		self.hole = pyglet.shapes.Circle(x=self.hole_position[0],y=self.hole_position[1],radius=0.01*max(window.height,window.width),color=(0,0,0),batch=self.batch)

	def draw(self):
		self.batch.draw()

golf_course = GolfCourse((10,10),(200,150))
pyglet.clock.schedule_interval(lambda x: print(x),1/60)
@window.event()
def on_draw():
	window.clear()
	golf_course.draw()
pyglet.app.run()