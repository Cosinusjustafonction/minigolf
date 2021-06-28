import pyglet#hello

class app : 
	def __init__(self, window): 
		self.window = window
p1 = app(pyglet.window.Window())

@p1.window.event 
def on_draw() :
	p1.window.clear()
	
pyglet.app.run()
