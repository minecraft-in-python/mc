# Install Ursina before using this "pip install ursina"
# Tutorial https://www.youtube.com/watch?v=DHSRaVeQxIk
# What are you doing here?!

from random import randint
from turtle import position, pu
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import easygui

app = Ursina()

# Variables
grass_block_texture = load_texture("./files/Grass_Block.png")
stone_texture = load_texture("./files/Stone_Block.png")
brick_texture = load_texture("./files/Brick_Block.png")
dirt_texture = load_texture("./files/Dirt_Block.png")
wood_texture = load_texture("./files/Wood_Block.png")
water_texture = load_texture("./files/Water_Liquid.png")
leaves_texture = load_texture("./files/Leaves_Block.png")
grass_texture = load_texture("./files/Grass.png")
bedrock_texture = load_texture("./files/Bedrock_Block.png")
sky_texture = load_texture("./files/Skybox.png")
arm_texture = load_texture("./files/Arm_Texture.png")


hotbar_texture = load_texture("./files/Grass_Block_Hotbar.png")
#grass_block_hotbar = load_texture("Grass_Block_Hotbar.png")
#stone_hotbar = load_texture("Stone_Hotbar.png")
#brick_hotbar = load_texture("Brick_Hotbar.png")
#dirt_hotbar = load_texture("Dirt_Hotbar.png")
#wood_hotbar = load_texture("Wood_Hotbar.png")
#water_hotbar = load_texture("Water_Hotbar.png")
#leaves_hotbar = load_texture("Leaves_Hotbar.png")
#grass_hotbar = load_texture("Grass_Hotbar.png")
#bedrock_hotbar = load_texture("Bedrock_Hotbar.png")


stone = Audio("./files/Stone.wav", loop = False, autoplay = False)
dirt = Audio("./files/Dirt.wav", loop = False, autoplay = False)
water = Audio("./files/Water.mp3", loop = False, autoplay = False)


window.exit_button.visible = False
block_pick = 1
rndint=random.randint

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
    if held_keys["7"]: block_pick = 7
    if held_keys["8"]: block_pick = 8
    if held_keys["9"]: block_pick = 9
    
    

# Voxel (block) properties
class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_block_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = "Block",
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
                if block_pick==1 or block_pick==4: dirt.play()
                elif block_pick==6: water.play()
                else: stone.play()

                #Placement
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_block_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = wood_texture)
                if block_pick == 6: voxel = Voxel(position = self.position + mouse.normal, texture = water_texture)
                if block_pick == 7: voxel = Voxel(position = self.position + mouse.normal, texture = leaves_texture)
                if block_pick == 8: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 9: voxel = Voxel(position = self.position + mouse.normal, texture = bedrock_texture)

                #Hotbar
                #if block_pick == 1: hotbar_texture = load_texture("Grass_Block_Hotbar.png")
                #if block_pick == 2: hotbar_texture = load_texture("Stone_Hotbar.png")
                #if block_pick == 3: hotbar_texture = load_texture("Brick_Hotbar.png")
                #if block_pick == 4: hotbar_texture = load_texture("Dirt_Hotbar.png")
                #if block_pick == 5: hotbar_texture = load_texture("Wood_Hotbar.png")
                #if block_pick == 6: hotbar_texture = load_texture("Water_Hotbar.png")
                #if block_pick == 7: hotbar_texture = load_texture("Leaves_Hotbar.png")
                #if block_pick == 8: hotbar_texture = load_texture("Grass_Hotbar.png")
                #if block_pick == 9: hotbar_texture = load_texture("Bedrock_Hotbar.png")
                #destroy(Hotbar())
                #Hotbar()
                
                
            if key == "left mouse down":
                stone.play()
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
            model = "Arm",
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(170, -10, 0),
            position = Vec2(0.6, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.5, -0.5)

    def passive(self):
        self.position = Vec2(0.6, -0.6)


#class Hotbar(Entity):
 #   def __init__(self):
  #      super().__init__(
   #         parent=camera.ui,
    #        model='quad',
     #       position=Vec2(0, -0.43),
      #      scale=(0.14, 0.14, 0.25),
       #     texture = hotbar_texture)


def l_shape(block, x, y, z):
    voxel = Voxel(position = (x, 2, z), texture = block)
    voxel = Voxel(position = (x+1, 2, z), texture = block)
    voxel = Voxel(position = (x, 2, z+1), texture = block)


def pwal_shape(block, x, y, z):
    voxel = Voxel(position = (x, 2, z))
    voxel = Voxel(position = (x+1, 2, z))
    voxel = Voxel(position = (x, 2, z+1))
    voxel = Voxel(position = (x-1, 2, z))


def pwac_shape(block, x, y, z):
    voxel = Voxel(position = (x, 2, z))
    voxel = Voxel(position = (x+1, 2, z))
    voxel = Voxel(position = (x, 2, z+1))
    voxel = Voxel(position = (x, 2, z-1))
    voxel = Voxel(position = (x-1, 2, z))
    voxel = Voxel(position = (x-1, 2, z+1))

warning = easygui.msgbox(msg="If having performance issues, read readme.md", title="Tip", ok_button="Okay")
width = easygui.enterbox(msg="Width: ", title="Width")
depth = easygui.enterbox(msg="Depth: ", title="Depth")
gentype = easygui.choicebox(msg="Generation type:", title="Generation type", choices=["Normal", "Flat"])

if gentype=="Normal":
    for z in range(int(width)):
        for x in range(int(depth)):
            #voxel = Voxel(position = (x, 0, z), texture = bedrock_texture)
            for y in range(2):
                voxel = Voxel(position = (x, y, z))
            a=rndint(1,150)
            if a<10:
                b=rndint(1,100)
                if b<40:
                    l_shape(grass_block_texture, x, y, z)
                if b>39 and b<70:
                    pwal_shape(grass_block_texture, x, y, z)
                if b>69:
                    pwac_shape(grass_block_texture, x, y, z)
            else:
                c=rndint(1,100)
                if c<2:
                    #Layer 1
                    voxel = Voxel(position = (x, 2, z), texture = wood_texture)
                    #Layer 2
                    voxel = Voxel(position = (x, 3, z), texture = wood_texture)
                    #Layer 3
                    voxel = Voxel(position = (x, 4, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, 4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 4, z-1), texture = leaves_texture)

                    voxel = Voxel(position = (x+1, 4, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x, 4, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 4, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 4, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x, 4, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 4, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, 4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, 4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, 4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, 4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, 4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, 4, z+1), texture = leaves_texture)
                    #Layer 4
                    voxel = Voxel(position = (x, 5, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, 5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 5, z-1), texture = leaves_texture)

                    voxel = Voxel(position = (x+1, 5, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x, 5, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 5, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 5, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x, 5, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 5, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, 5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, 5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, 5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, 5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, 5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, 5, z+1), texture = leaves_texture)
                    #Layer 5
                    voxel = Voxel(position = (x, 6, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, 6, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 6, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 6, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 6, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 6, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 6, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 6, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 6, z-1), texture = leaves_texture)
                    #Layer 6
                    voxel = Voxel(position = (x, 7, z), texture = leaves_texture)
                    voxel = Voxel(position = (x, 7, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, 7, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, 7, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, 7, z), texture = leaves_texture)

elif gentype=="Flat":
    for z in range(int(width)):
        for x in range(int(depth)):
            voxel = Voxel(position = (x, 0, z), texture = bedrock_texture)
            voxel = Voxel(position = (x, 1, z))
            voxel = Voxel(position = (x, 2, z))


player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
