import pyglet
import random
from pyglet.gl import * 
from Lib.triangulation import *
import itertools
import tripy
window = pyglet.window.Window(resizable=False,height=480,width=960)
pyglet.font.add_directory("Assets")
white = [255]*3
main_list = []
i = 0 
main_coordiantes = []
polygon_list = []
final_polygons = []
polycoords = []
final_quads = []
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
		self.is_polygone = False
		self.saved = False
		#self.batch.add(3, pyglet.gl.GL_, None, ('v2i',[509, 324, 588, 94, 790, 309]), ('c3B',white*3))
		#self.batch.add(3, pyglet.gl.GL_POLYGON, None, ('v2i',[114, 247, 222, 400, 333, 257]), ('c3B',white*3))
	def draw(self,interval):
		x = 0 
		y=0
		self.polygon_obstacle()
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
	def polygon_obstacle(self) :
		global polygon_list 
		main_list = polygon_list 
		cock = 0 
		for i in polygon_list : 
			cock = create_triangle(main_list)
		if cock != 0:
			for i in cock:
				self.batch.add(3, pyglet.gl.GL_TRIANGLES, None, ('v2i',i), ('c3B',white*3))
		print(cock)
		polygon_list = []
golf_course = GolfCourseEditor((50,60),(200,150))
pyglet.clock.schedule_interval(lambda x: x,1/60)
@window.event()
def on_draw():
	window.clear()
	golf_course.draw(1/60)
@window.event()
def on_mouse_press(x,y,button, modifiers) : 
	print(x, y)
	global main_list
	global main_coordiantes
	if button == pyglet.window.mouse.RIGHT :
		golf_course.obstacles.pop(-1)
	if golf_course.is_polygone == True :
		main_coordiantes.append((x, y))  

		
	else :
		main_list.append((x,y))
@window.event()
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
	global main_list
	global main_coordiantes
	i = 0  
	if golf_course.is_polygone == False:
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
	if golf_course.is_polygone == False:
		main_list.append((x, y))
		golf_course.obstacles.append(get_rect_shit(main_list))
		main_list = []
def get_rect_shit(list_) : 
	start = list_[0]
	finish = list_[-1]
	height = finish[0]-start[0]
	width = finish[1]-start[1]
	pos = (start[0] ,start[1])
	return width , height , pos 
@window.event()
def on_key_press(symbol, modifiers):
	global main_coordiantes
	global i 
	if symbol == 114:
		golf_course.obstacles = []
	if symbol == 112 : 
		if i % 2 == 0 : 
			golf_course.is_polygone = True
			i+=1 
		else : 
			golf_course.is_polygone = False
			i+=1			
	if symbol == 115 : 
		golf_course.is_polygone = False 
		polygon_list.append(main_coordiantes)
		polycoords.append(main_coordiantes)
		main_coordiantes = []	 
def generate_triangle(coords) : 
	polygon = coords[0]
	triangles = tripy.earclip(polygon)
	final = []
	for i in triangles: 
		final.append(list(i))
	return final 

def create_triangle(Lis_) : 
	main_list = generate_triangle(Lis_)
	n  = 6
	final_list = []
	for i in main_list : 
		for t in i:
			for x in t:
				final_list.append(x)
	kiki = [final_list[i * n:(i + 1) * n] for i in range((len(final_list) + n - 1) // n )]
	final_polygons.append(kiki)
	return kiki




pyglet.app.run()