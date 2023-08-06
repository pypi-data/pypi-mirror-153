from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.editor_camera import EditorCamera

def Ground(model,scale,collider,texture,texture_scale):
    ground = Entity(model=model, scale=(scale), collider=collider, texture=texture, texture_scale=texture_scale)

def ThirdPersonController(model,scale,collider,texture):
    player = FirstPersonController(model=model, scale=scale, collider=collider, texture=texture)
    camera.z = -5
    
def Obstacle(model,scale,collider,texture,x,y,rotation_y,rotation_x):
    obstacle = Entity(model=model, scale=scale, x=x, y=y, rotation_y=rotation_y, rotation_x=rotation_x, collider=collider, texture=texture)
    
def Block(model,scale,collider,texture,position):
    block = Button(model=model,scale=scale,collider=collider,texture=texture,position=position)
        
app=Ursina()
ground = Ground(model='plane',scale=(100,1,100),collider='box',texture='grass',texture_scale=(100,100))
player = ThirdPersonController(model='cube', scale=0.5, collider='mesh', texture='white_cube')
obstacle = Obstacle(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45,rotation_x=0, collider='box', texture='white_cube')
app.run()