import pyglet



window = pyglet.window.Window(resizable=False,height=480,width=960)
pyglet.font.add_directory("Assets")

main_list = []
class GolfCourseEditor:

	def __init__(self,hole_position,ball_position):
		self.background = pyglet.graphics.Batch()
		self.batch = pyglet.graphics.Batch()
		course_image = pyglet.image.load("Assets/GolfCourseTexture.png")
		self.golf_sprite = pyglet.sprite.Sprite(course_image,0,0,batch=self.background)
		self.golf_sprite.scale = max(window.width,window.height)/min(self.golf_sprite.height,self.golf_sprite.width)
		self.radius = 0.01*max(window.height,window.width)
		self.obstacles = []
		self.selected_obstacle = pyglet.shapes.Rectangle(0,0,0,0,color=(200,30,20))
		self.selected_obstacle.opacity = 150

	def draw(self,interval):

		x = 0 
		y=0
		self.background.draw()
		for i in self.obstacles : 
			self.init_obstacles(i[1],i[0],i[2][0],i[2][1],(119, 52, 0)).draw()
		for i in range(window.width//10) : 
			pyglet.shapes.Rectangle(width=1,height=window.height,x=x,y=0, color=(119, 52, 0),
                                              batch=self.batch ).draw()
			x+=10
		for j in range(window.height//10) :
			pyglet.shapes.Rectangle(width=window.width,height=1,x=0,y=y, color=(119, 52, 0),
                                              batch=self.batch ).draw()
			y += 10
		self.selected_obstacle.draw()
		self.batch.draw()
	def CancelPreview(self):
		self.selected_obstacle = pyglet.shapes.Rectangle( 0, 0, 0, 0, color=(200, 30, 20) )
		self.selected_obstacle.opacity = 150
	def init_obstacles(self,width,height,x,y,color) : 
		
		return pyglet.shapes.Rectangle(width=width,height=height,x=x,y=y, color=color,
                                              batch=self.batch )
golf_course = GolfCourseEditor((50,60),(200,150))
pyglet.clock.schedule_interval(lambda x: x,1/60)
@window.event()
def on_draw():
	window.clear()
	golf_course.draw(1/60)
@window.event()
def on_mouse_press(x,y,button, modifiers) : 
	if button == pyglet.window.mouse.RIGHT :
		golf_course.obstacles.pop(-1)
	main_list.append((x,y))
@window.event()
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
	global main_list
	if buttons==pyglet.window.mouse.LEFT:
		if len(main_list)==0:
			return
		golf_course.selected_obstacle.x = main_list[0][0]
		golf_course.selected_obstacle.y = main_list[0][1]
		golf_course.selected_obstacle.width = x-main_list[0][0]
		golf_course.selected_obstacle.height = y-main_list[0][1]
@window.event()
def on_mouse_release(x,y,button, modifiers) :
	golf_course.CancelPreview()
	global main_list
	main_list.append((x, y))
	golf_course.obstacles.append(get_rect_shit(main_list))
	main_list = []
def get_rect_shit(list_) : 
	start = list_[0]
	finish = list_[-1]
	height = abs(start[0]-finish[0])
	width = abs(start[1]-finish[1])
	pos = (start[0] ,finish[1])
	return width , height , pos 


pyglet.app.run()