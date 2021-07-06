import itertools
from Lib.vectors import vec2d
from math import pi
def earcut(coords) :
	triangles = []
	polygon = coords
	i=0
	while len(polygon)>3:
		i = i % len( polygon )
		v = vec2d(polygon[1+i][0]-polygon[0+i][0],polygon[1+i][1]-polygon[0+i][1])
		u = vec2d( polygon[(len(polygon)-1+i)%len(polygon)][0] - polygon[0+i][0], polygon[(len(polygon)-1+i)%len(polygon)][1] - polygon[0+i][1] )
		if v.angle(u)<=0:
			i+=1
		else:
			triangles.append([polygon[i+1],polygon[i],polygon[(len(polygon)-1+i)%len(polygon)]])
			del polygon[i]
	if len( polygon ) == 3:
		triangles.append( polygon )
		return triangles
print(earcut([(0,0),(10,0),(10,10),(0,10)]))
