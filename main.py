import pyglet


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
	def draw(self):
		self.batch.draw()

golf_course = GolfCourse((10,10),(200,150))

@window.event()
def on_draw():
	window.clear()
	golf_course.draw()
pyglet.app.run()