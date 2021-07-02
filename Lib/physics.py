from Lib.vectors import vec3d
import math 
class Displacement:
	def __init__(self,position, speed,acceleration):
		#setting some physical properties
		self.position = position
		self.speed = speed
		self.old_position = position
		self.acceleration = acceleration
		self.coefficient_of_friction = 0.985
		self.mass = 0
	def has_landed(self, callback=lambda : print("The eagle has landed")):
		if self.old_position[2]>self.position[2] and self.position[2]==0:
			callback()
	def mov(self, interval):
		self.has_landed()
		#This is the basis of physics in this whole game, and it simply updates the speed and position depending on acceleration
		#And it has some basic ground level collision to ensure that the object doesn't sink in the ground
		self.old_position = self.position
		self.speed+=self.acceleration*interval
		self.position+=self.speed*interval
		if self.position[2]<=0:
			self.speed[2]=0
			self.position[2]=0
		if self.position[2]<=0:
			self.friction()
	def strike(self,acceleration,interval):
		#adding speed to the ball after a strike
		self.speed+=acceleration*interval
	def is_collision(self, bounding_box, other):

		return intersect_two_rectangles(*bounding_box,*other)
	def friction(self):
		if abs(self.speed[0])<1:
			self.speed[0]=0
		if abs(self.speed[1])<1:
			self.speed[1]=0
		self.speed*=self.coefficient_of_friction

def get_line_equation_from_points(p1,p2):
	if p1[0]==p2[0]:
		p1 = (p1[0]+0.01,p1[1])
	return [(p1[1]-p2[1])/(p1[0]-p2[0]),p1[1]-((p1[1]-p2[1])/(p1[0]-p2[0])*p1[0])]
def get_normal_from_two_points(p1,p2):
	return 1,-1/get_line_equation_from_points(p1,p2)[0]
def intersect_two_lines_from_points(verts1,verts2):
	eq1 = get_line_equation_from_points(*verts1)
	eq2 = get_line_equation_from_points(*verts2)

	if eq1[0]==eq2[0]:
		return None
	else:
		return ((eq1[1]-eq2[1])/(eq2[0]-eq1[0]),(eq1[0]*(eq1[1]-eq2[1])/(eq2[0]-eq1[0]))+eq1[1])
def intersect_two_rectangles(x,y,width,height,x1,y1,width1,height1):
	overlap1 = intersect_two_intervals([x,x+width],[x1,x1+width1])
	overlap2 = intersect_two_intervals( [y, y + height], [y1, y1 + height1] )
	return overlap1 is not None and overlap2 is not None
def intersect_two_intervals(inter1,inter2):
	sorted_values = sorted([inter1,inter2],key=lambda x: x[0])
	if sorted_values[0][1]>sorted_values[1][0]:
		return [sorted_values[1][0],sorted_values[0][1]]
	else:
		return None
def get_verts_from_properties(height,width,x,y):
	return [(x,y),(x+width,y),(x+width,y+height),(x,y+height)]
