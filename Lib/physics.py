from Lib.vectors import vec3d
import math 
class Displacement:
	def __init__(self,position, speed,acceleration):
		#setting some physical properties
		self.position = position
		self.speed = speed
		self.acceleration = acceleration
		self.coefficient_of_friction = 0.97
		self.mass = 0
	def mov(self, interval):
		#This is the basis of physics in this whole game, and it simply updates the speed and position depending on acceleration
		#And it has some basic ground level collision to ensure that the object doesn't sink in the ground
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
		if abs(self.speed[0])<0.1:
			self.speed[0]=0
		if abs(self.speed[1])<0.1:
			self.speed[1]=0
		self.speed*=self.coefficient_of_friction
	def get_list(self,height , width):
		big = []
		if height > width : 
		    for i in range(height) : 
		        big.append((i, width))
		else  :
		    for i in range(width) : 
		        big.append((i, height))
		return big 
	def get_list2(self,height , width) :	 
		big = []
		if height < width : 
			for i in  range(height) : 
				big.append((width,i ))
		else : 
			for i in range(width):
				big.append((height, i))

		return big 
	def is_col(self,height,width,x,y,radius,pos) :
		main_list = []
		if pos == "left" : 
			main_list = self.get_list(height,width)
		else : 
			main_list = self.get_list2(height,width)
		for i in main_list : 
			if ((i[0]-x)**2 +(i[1]-y)**2)<radius**2 : 
				return True



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
