import tripy 
import itertools
def generate_triangle(coords) : 
	polygon = coords
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
	print(final_list)
	return [final_list[i * n:(i + 1) * n] for i in range((len(final_list) + n - 1) // n )]

print(create_triangle([(0,1), (-1, 0), (0, -1), (1, 0),(5,0)]))