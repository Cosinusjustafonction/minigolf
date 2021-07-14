import pyglet
class MenuWindow:
	def __init__(self,kwargs,callback,text_style={"font_name":'Arial', "font_size" : 10, "color" :(255, 255, 255, 255)},texts=["hello world"]):
		super().__init__()
		self.batch = pyglet.graphics.Batch()
		self.background = pyglet.graphics.Batch()
		self.foreground = pyglet.graphics.Batch()
		kwargs["batch"]=self.batch
		self.button = Button(kwargs,text=texts[0],text_style=text_style,callback=callback,foreground=self.foreground)
		self.alive = 1
		self.is_pressed=False
		self.pressed_keys = {}
		background_image = pyglet.image.load( "Assets/background.png" )
		self.golf_sprite = pyglet.sprite.Sprite(background_image,0,0,batch=self.background)
	def draw(self,interval):
		self.render()
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.pressed_keys[buttons]=(x,y)
	def on_mouse_release(self, x, y, button, modifiers):
		del self.pressed_keys[button]
		self.button.on_release(x,y)
		self.is_pressed=False
	def on_mouse_press(self, x, y, button, modifiers):
		print(button)
		self.pressed_keys[button]=(x,y)
		self.is_pressed=True
	def render(self):
		if 1 in self.pressed_keys:
			if self.button.x <= self.pressed_keys[1][0] <= self.button.x + self.button.width and self.button.y <= self.pressed_keys[1][1] <= self.button.y + self.button.height and self.is_pressed:
				self.button.on_hold( self.pressed_keys[1][0], self.pressed_keys[1][1] )
		self.background.draw()
		self.batch.draw()
		self.foreground.draw()

class Container(pyglet.shapes.Rectangle):
	def __init__(self,kwargs,children=[]):
		super().__init__(self,**kwargs)
		self.children = children

class Button(pyglet.shapes.Rectangle):
	def __init__(self,kwargs,text="Hello world",text_style={"font_name":'Arial', "font_size" : 10, "color" :(255, 255, 255, 255)},callback=lambda x,y: (x,y),foreground=None):
		super().__init__(**kwargs)
		self.callback = callback
		batch = kwargs.get("batch")
		self.document = pyglet.text.document.FormattedDocument(text)
		self.document.set_style(0,len(self.document.text),text_style)
		self.text_layout = pyglet.text.layout.TextLayout(document=self.document,wrap_lines=True,width=self.width*0.95,height=self.height*0.9,multiline=True,batch=foreground)
		self.text_layout.x = self.x+self.width*0.3
		self.text_layout.content_valign = "center"
		self.text_layout.content_halign = "center"
		self.text_layout.y = self.y
		self.is_held = False

	def on_hold(self,x,y):
		if not self.is_held:
			self.color = (self.color[0]*1/2,self.color[1]*1/2,self.color[2]*1/2)
		self.is_held = True
	def on_release(self,x,y):
		self.is_held=False
		if not (self.x<x<self.x+self.width and self.y<y<self.y+self.height):
			return
		self.color = (self.color[0]*2,self.color[1]*2,self.color[2]*2)
		print("you clicked me")
		self.callback(x,y)