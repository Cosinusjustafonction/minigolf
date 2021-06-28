class Displacement:
	def __init__(self,position, speed,acceleration):
		self.position = position
		self.speed = speed
		self.acceleration = acceleration
	def mov(self, interval):
		self.speed+=acceleration*interval
		self.position+=self.speed*interval