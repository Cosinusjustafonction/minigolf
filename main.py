import pyglet
from Lib.vectors import vec3d,vec2d
from Lib.physics import *
import math
from math import pi,atan2
import json

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
		self.WoodBounce = pyglet.media.load("Assets/GolfWoodBounce.wav",streaming=False)
		self.Player = pyglet.media.player.Player()
	def draw(self,interval,hole):
		self.is_hole( hole )
		self.boundaries_col( interval )
		self.displacement.mov(interval)
		self.shape.position = self.displacement.position[0],self.displacement.position[1]
		self.shape.radius = self.original_radius+self.displacement.position[2]*self.original_radius*0.3
		self.shape.draw()


	def is_grounded(self):
		return self.displacement.position[2]<=0

	def is_stopped(self):
		return self.displacement.speed == vec3d(0,0,0)

	def is_hole(self,hole):
		if self.displacement.is_collision([self.shape.x-self.shape.radius, self.shape.y-self.shape.radius, 2*self.shape.radius,2* self.shape.radius],[hole.x-hole.radius, hole.y-hole.radius, 2*hole.radius, 2*hole.radius] ) and self.displacement.position[2]<=0:
			self.displacement.speed = vec3d(0,0,0)
			self.displacement.position[0]=hole.x
			self.displacement.position[1]=hole.y
			self.displacement.position[2] = -10
			self.hole = True
			ScoreSound = pyglet.media.load( "Assets/GolfHoleSound.mp3", streaming=False )
			ScoreSound.play()
	#def boundaries_boundaries(self,x,y,width,height) :

	def boundaries_col(self,interval) :
		for i in golf_course.obstacles :
			if self.displacement.is_collision([self.shape.x-self.shape.radius, self.shape.y-self.shape.radius,2* self.shape.radius, 2*self.shape.radius],[i[2], i[3], i[1], i[0]] ):
				verts = get_verts_from_properties(*i[0:4])
				intersections = []
				for u in range(4):
					intersection = intersect_two_lines_from_points(((self.displacement.position[0],self.displacement.position[1]),(self.displacement.position[0]+self.displacement.speed[0],self.displacement.position[1]+self.displacement.speed[1])),(verts[u%4],verts[(u+1)%4]))
					if intersection is None:
						continue
					distance = math.sqrt(((self.displacement.position[0]-intersection[0])**2)+(self.displacement.position[1]-intersection[1])**2)
					intersections.append([u,intersection,distance])
				intersections = sorted(intersections,key=lambda x: x[2])
				u = intersections[0][0]
				intersected_edge = (verts[u%4],verts[(u+1)%4])
				center = (i[2]+i[1]/2,i[3]+i[0]/2)
				normal = vec2d((intersected_edge[0][0]+intersected_edge[1][0])/2-center[0],(intersected_edge[0][1]+intersected_edge[1][1])/2-center[1])
				self.rebound(normal,interval)
				break
	def rebound(self,normal,interval) :
		self.Player.volume = self.displacement.speed.magnitude()/60
		self.Player.queue(self.WoodBounce)
		self.Player.play()
		self.displacement.position-=self.displacement.speed*interval
		speed_2d = vec2d(self.displacement.speed[0],self.displacement.speed[1])
		speed_2d.rotate(2*speed_2d.angle(normal))
		speed_2d*=-1
		self.displacement.speed[0],self.displacement.speed[1]=0.6*speed_2d[0],0.6*speed_2d[1]
class GolfCourse:

	def __init__(self,json_path):
		f = open(json_path,)
		self.map_data = json.load(f)
		f.close()
		self.hole_position = vec2d(self.map_data["hole_position"][0],self.map_data["hole_position"][1])
		print(self.hole_position)
		self.ball = Ball(vec3d(self.map_data["ball_initial_position"][0],self.map_data["ball_initial_position"][1],0),5)
		print(self.ball.displacement.position)
		self.ball.displacement.acceleration = vec3d(0,0,-10)
		self.background = pyglet.graphics.Batch()
		self.batch = pyglet.graphics.Batch()
		self.music_player = pyglet.media.Player()
		self.music_player.loop = True
		self.music_player.queue(pyglet.media.load("Assets/BackGroundMusic.m4a"))
		self.music_player.volume = 0.2
		self.music_player.play()
		course_image = pyglet.image.load("Assets/GolfCourseTexture.png")
		self.golf_sprite = pyglet.sprite.Sprite(course_image,0,0,batch=self.background)
		self.golf_sprite.scale = max(window.width,window.height)/min(self.golf_sprite.height,self.golf_sprite.width)
		self.hole = pyglet.shapes.Circle(x=self.hole_position[0],y=self.hole_position[1],radius=10,color=(0,0,0),batch=self.batch)
		self.radius = 0.01*max(window.height,window.width)
		self.isdraw = False
		self.obstacles = []
		for obstacle in self.map_data["obstacles"]:
			self.obstacles.append([obstacle[3],obstacle[2],obstacle[0],obstacle[1],(119, 52, 0)])
		self.all_obstacles()

	def strike(self):
		if self.ball.is_grounded() and self.ball.is_stopped():
			acceleration_vector = vec3d( -(self.x_dist) * 100,
			                             -(self.y_dist) * 100, 0)
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
			self.music_player.pause()
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

golf_course = GolfCourse("Maps/map_demo.json")
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
	pass
pyglet.app.run()  
