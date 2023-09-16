# Install Ursina before using this "pip install ursina"
# Tutorial https://www.youtube.com/watch?v=DHSRaVeQxIk
# What are you doing here?!

from random import randint
from turtle import position, pu
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Variables
grass_texture = load_texture("Assets/Textures/Grass_Block.png")
stone_texture = load_texture("Assets/Textures/Stone_Block.png")
brick_texture = load_texture("Assets/Textures/Brick_Block.png")
dirt_texture = load_texture("Assets/Textures/Dirt_Block.png")
wood_texture = load_texture("Assets/Textures/Wood_Block.png")
water_texture = load_texture("Assets/Textures/Water_Liquid.png")
sky_texture = load_texture("Assets/Textures/Skybox.png")
arm_texture = load_texture("Assets/Textures/Arm_Texture.png")
punch_sound = Audio("Assets/SFX/Punch_Sound.wav", loop = False, autoplay = False)
window.exit_button.visible = True
block_pick = 1

# Updates every frame
def update():
    global block_pick

    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()

    if held_keys["1"]: block_pick = 1
    if held_keys["2"]: block_pick = 2
    if held_keys["3"]: block_pick = 3
    if held_keys["4"]: block_pick = 4
    if held_keys["5"]: block_pick = 5
    if held_keys["6"]: block_pick = 6
    

# Voxel (block) properties
class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = "Assets/Models/Block",
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color = color.light_gray,
            scale = 0.5
        )
    
    # What happens to blocks on inputs
    def input(self,key):
        if self.hovered:
            if key == "right mouse down":
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = wood_texture)
                if block_pick == 6: voxel = Voxel(position = self.position + mouse.normal, texture = water_texture)

            
            if key == "left mouse down":
                punch_sound.play()
                destroy(self)

# Skybox
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "Sphere",
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

# Arm
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "Assets/Models/Arm",
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Increase the numbers for more cubes. For exapmle: for z in range(20)
for z in range(32):
    for x in range(32):
        for y in range(2):
            voxel = Voxel(position = (x, y, z))
        a=random.randint(1,150)
        if a<10:
            b=random.randint(1,3)
            if b==1:
                voxel = Voxel(position = (x, 2, z))
                voxel = Voxel(position = (x+1, 2, z))
                voxel = Voxel(position = (x, 2, z+1))
            if b==2:
                voxel = Voxel(position = (x, 2, z))
                voxel = Voxel(position = (x+1, 2, z))
                voxel = Voxel(position = (x, 2, z+1))
                voxel = Voxel(position = (x-1, 2, z))
            if b==3:
                voxel = Voxel(position = (x, 2, z))
                voxel = Voxel(position = (x+1, 2, z))
                voxel = Voxel(position = (x, 2, z+1))
                voxel = Voxel(position = (x, 2, z-1))
                voxel = Voxel(position = (x-1, 2, z))
                voxel = Voxel(position = (x-1, 2, z+1))
            

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
