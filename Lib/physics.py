from Lib.vectors import vec3d

class Displacement:
	def __init__(self,position, speed,acceleration):
		self.position = position
		self.speed = speed
		self.acceleration = acceleration
		self.coefficient_of_friction = 10
		self.mass = 0
	def mov(self, interval):
		self.speed+=self.acceleration*interval
		self.position+=self.speed*interval
		if self.position[2]<0:
			self.speed[2]-=self.acceleration[2]*interval
			self.position[2]-=self.speed[2]*interval
	def strike(self,acceleration,interval):
		self.speed+=acceleration*interval