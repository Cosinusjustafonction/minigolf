import math

class vec3d:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
	def magnitude(self):
		return math.sqrt((self.x**2)+(self.y**2)+(self.z**2))
	def __setitem__(self, key, value):
		if not isinstance(key,int):
			raise KeyError
		if key==0:
			self.x = value
		elif key==1:
			self.y = value
		elif key==2:
			self.z = value
	def __add__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x + other, self.y + other, self.z + other )
		return vec3d(self.x+other.x,self.y+other.y,self.z+other.z)
	def __sub__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x - other, self.y - other, self.z - other )
		return vec3d(self.x-other.x,self.y-other.y,self.z-other.z)
	def __iter__(self):
		return iter([self.x,self.y,self.z])
	def __rmul__(self, other):
		return self.__mul__(other)
	def __mul__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x * other, self.y * other, self.z * other )
		return vec3d(self.x*other.x,self.y*other.y,self.z*other.z)
	def __imul__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x * other, self.y * other, self.z * other )
		return vec3d(self.x*other.x,self.y*other.y,self.z*other.z)
	def __getitem__(self, item):
		return [self.x,self.y,self.z][item]
	def __iadd__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x + other, self.y + other, self.z + other )

		return vec3d( self.x + other.x, self.y + other.y, self.z + other.z )
	def __isub__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x - other, self.y - other, self.z - other )
		return vec3d( self.x - other.x, self.y - other.y, self.z - other.z )
	def __eq__(self, other):
		return self.x==other.x and self.y==other.y and self.z==other.z
	def __str__(self):
		return f"({self.x},{self.y},{self.z})"
	def __idiv__(self, other):
		return vec3d( self.x / other.x, self.y / other.y, self.z / other.z )
	def __ne__(self, other):
		return self.x != other.x and self.y != other.y and self.z != other.z
	def __neg__(self):
		return vec3d(-self.x,-self.y,-self.z)
	def __truediv__(self, other):
		if isinstance(other,(int,float)):
			return vec3d( self.x / other, self.y / other, self.z / other )
		return vec3d( self.x / other.x, self.y / other.y, self.z / other.z )
	def __floordiv__(self, other):
		return vec3d( self.x // other.x, self.y // other.y, self.z // other.z )
	def __ifloordiv__(self, other):
		return vec3d( self.x // other.x, self.y // other.y, self.z // other.z )

class vec2d:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def angle(self,other):
		cosine = (self.dot_product(other))/(self.magnitude()*other.magnitude())
		sine = (self.determinant(other)/(self.magnitude()*other.magnitude()))
		if (sine>0 and cosine>0) or (cosine<0 and sine>0):
			return math.acos(cosine)
		elif (sine<0 and cosine<0) or (sine<0 and cosine>0):
			return -math.acos(cosine)
	def magnitude(self):
		return math.sqrt((self.x**2)+(self.y**2))
	def dot_product(self,other):
		return (self.x*other.x)+(self.y*other.y)
	def rotate(self,angle):
		self.x,self.y = math.cos(angle)*self.x-math.sin(angle)*self.y,math.sin(angle)*self.x+math.cos(angle)*self.y
		return None
	def determinant(self,other):
		return (self.x*other.y)-(other.x*self.y)
	def __add__(self, other):
		return vec2d(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
		return vec2d(self.x-other.x,self.y-other.y)
	def __setitem__(self, key, value):
		if not isinstance(key,int):
			raise KeyError
		if key==0:
			self.x = value
		elif key==1:
			self.y = value
	def __iter__(self):
		return iter([self.x,self.y])
	def __mul__(self, other):
		return vec2d( self.x * other.x, self.y * other.y )
	def __imul__(self, other):
		if isinstance(other,(int,float)):
			return vec2d( self.x * other, self.y * other )
		return vec2d( self.x * other.x, self.y * other.y )
	def __getitem__(self, item):
		return [self.x,self.y][item]
	def __iadd__(self, other):
		return vec2d( self.x + other.x, self.y + other.y )
	def __isub__(self, other):
		return vec2d( self.x - other.x, self.y - other.y )
	def __eq__(self, other):
		return self.x==other.x and self.y==other.y
	def __str__(self):
		return f"({self.x},{self.y})"
	def __idiv__(self, other):
		return vec2d( self.x / other.x, self.y / other.y )
	def __ne__(self, other):
		return self.x != other.x and self.y != other.y
	def __neg__(self):
		return vec2d( -self.x, -self.y )
	def __truediv__(self, other):
		return vec2d( self.x / other.x, self.y / other.y )
	def __floordiv__(self, other):
		return vec2d( self.x // other.x, self.y // other.y )
	def __ifloordiv__(self, other):
		return vec2d( self.x // other.x, self.y // other.y )
