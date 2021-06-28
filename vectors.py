class vec3d:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
	def __add__(self, other):
		return vec3d(self.x+other.x,self.y+other.y,self.z+other.z)
	def __sub__(self, other):
		return vec3d(self.x-other.x,self.y-other.y,self.z-other.z)
	def __iter__(self):
		return iter([self.x,self.y,self.z])
	def __mul__(self, other):
		return vec3d(self.x*other.x,self.y*other.y,self.z*other.z)
	def __imul__(self, other):
		return vec3d(self.x*other.x,self.y*other.y,self.z*other.z)
	def __getitem__(self, item):
		return [self.x,self.y,self.z][item]
	def __iadd__(self, other):
		return vec3d( self.x + other.x, self.y + other.y, self.z + other.z )
	def __isub__(self, other):
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
		return vec3d( self.x / other.x, self.y / other.y, self.z / other.z )
	def __floordiv__(self, other):
		return vec3d( self.x // other.x, self.y // other.y, self.z // other.z )
	def __ifloordiv__(self, other):
		return vec3d( self.x // other.x, self.y // other.y, self.z // other.z )

class vec2d:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __add__(self, other):
		return vec2d(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
		return vec2d(self.x-other.x,self.y-other.y)
	def __iter__(self):
		return iter([self.x,self.y])
	def __mul__(self, other):
		return vec2d( self.x * other.x, self.y * other.y )
	def __imul__(self, other):
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
