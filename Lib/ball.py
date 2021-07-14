from Lib.vectors import *
from Lib.physics import *
import math
import pyglet
from math import pi, atan2
import json
import tripy

class Ball:
	def __init__(self, position, radius, golf_course):
		self.golf_course = golf_course
		self.shape = self.ball = pyglet.shapes.Circle( x=position[0], y=position[1],
		                                               radius=radius, color=(255, 255, 255) )

		self.displacement = Displacement( position, vec3d( 0, 0, 0 ), vec3d( 0, 0, -10 ) )
		self.speed_line = pyglet.shapes.Line(self.displacement.position[0],self.displacement.position[1],
		                                     self.displacement.position[0]+self.displacement.speed[0],
		                                      self.displacement.position[1]+self.displacement.speed[1],width=5)
		self.audio = pyglet.media.load( "Assets/GolfClubSound.mp3", streaming=False )
		self.original_radius = radius
		self.hole = False
		self.WoodBounce = pyglet.media.load( "Assets/GolfWoodBounce.wav", streaming=False )
		self.Player = pyglet.media.player.Player()

	def draw(self, interval, hole):
		self.is_hole( hole )
		self.boundaries_col( interval )
		self.speed_line = pyglet.shapes.Line( self.displacement.position[0], self.displacement.position[1],
		                                      self.displacement.position[0] + self.displacement.speed[0],
		                                      self.displacement.position[1] + self.displacement.speed[1], width=2 )
		self.speed_line.opacity= 100
		self.displacement.mov( interval )
		self.shape.position = self.displacement.position[0], self.displacement.position[1]
		self.shape.radius = self.original_radius + self.displacement.position[2] * self.original_radius * 0.3
		self.speed_line.draw()
		self.shape.draw()


	def is_grounded(self):
		return self.displacement.position[2] <= 0

	def is_stopped(self):
		return self.displacement.speed == vec3d( 0, 0, 0 )

	def is_hole(self, hole):
		if self.displacement.is_collision(
				[[self.shape.x,self.shape.y],
				 [self.shape.x+2*self.shape.radius,self.shape.y],
				 [self.shape.x+2*self.shape.radius,self.shape.y+2*self.shape.radius],
				 [self.shape.x,self.shape.y+2*self.shape.radius]],[[hole.x,hole.y],
				 [hole.x+2*hole.radius,hole.y],
				 [hole.x+2*hole.radius,hole.y+2*hole.radius],
				 [hole.x,hole.y+2*hole.radius]]):

			self.displacement.speed = vec3d( 0, 0, 0 )
			self.displacement.position[0] = hole.x
			self.displacement.position[1] = hole.y
			self.displacement.position[2] = -10
			self.hole = True
			ScoreSound = pyglet.media.load( "Assets/GolfHoleSound.mp3", streaming=False )
			ScoreSound.play()

	# def boundaries_boundaries(self,x,y,width,height) :

	def boundaries_col(self, interval):
		for i in self.golf_course.obstacles:
			if self.displacement.is_collision(
					[[self.shape.x,self.shape.y],[self.shape.x+2*self.shape.radius,self.shape.y],[self.shape.x+2*self.shape.radius,self.shape.y+2*self.shape.radius],[self.shape.x,self.shape.y+2*self.shape.radius]], i[0] ):
				verts = i[0]
				intersections = []
				for u in range( len(verts) ):
					intersection = intersect_two_lines_from_points( ((self.displacement.position[0],
					                                                  self.displacement.position[1]), (
					                                                 self.displacement.position[0] +
					                                                 self.displacement.speed[0],
					                                                 self.displacement.position[1] +
					                                                 self.displacement.speed[1])),
					                                                (verts[u % len(verts)], verts[(u + 1) % len(verts)]) )
					if intersection is None:
						continue
					distance = math.sqrt( ((self.displacement.position[0] - intersection[0]) ** 2) + (
								self.displacement.position[1] - intersection[1]) ** 2 )
					intersections.append( [u, intersection, distance] )
				if len(intersections)<=0:
					continue
				intersections = sorted( intersections, key=lambda x: x[2] )
				u = intersections[0][0]
				intersected_edge = (verts[u % len(verts)], verts[(u + 1) % len(verts)])
				verts_triangulation = tripy.earclip(verts)
				triangle = []
				for tri in verts_triangulation:
					if tuple(intersected_edge[0]) in tri and tuple(intersected_edge[0]) in tri:
						triangle = tri
				median1 = [[(triangle[0][0]+triangle[1][0])/2,(triangle[0][1]+triangle[1][1])/2],
				           [(triangle[0][0]+triangle[1][0])/2-(triangle[0][1]-triangle[1][1]),(triangle[0][1]+triangle[1][1])/2+(triangle[0][0]-triangle[1][0])]]
				median2 = [[(triangle[2][0] + triangle[1][0]) / 2, (triangle[2][1] + triangle[1][1]) / 2],
				           [(triangle[2][0] + triangle[1][0]) / 2 - (triangle[2][1] - triangle[1][1]),
				            (triangle[2][1] + triangle[1][1]) / 2 + (triangle[2][0] - triangle[1][0])]]
				center = intersect_two_lines_from_points(median1,median2)
				normal = vec2d( (intersected_edge[0][0] + intersected_edge[1][0]) / 2 - center[0],
				                (intersected_edge[0][1] + intersected_edge[1][1]) / 2 - center[1] )
				self.rebound( normal, interval )
				break

	def rebound(self, normal, interval):
		self.Player.volume = self.displacement.speed.magnitude() / 60
		self.Player.queue( self.WoodBounce )
		self.Player.play()
		self.displacement.position -= self.displacement.speed * interval
		speed_2d = vec2d( self.displacement.speed[0], self.displacement.speed[1] )
		speed_2d.rotate( 2 * speed_2d.angle( normal ) )
		speed_2d *= -1
		self.displacement.speed[0], self.displacement.speed[1] = 0.6 * speed_2d[0], 0.6 * speed_2d[1]