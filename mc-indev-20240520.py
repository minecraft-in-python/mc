# Install Ursina before using this "pip install ursina"
# Tutorial https://www.youtube.com/watch?v=DHSRaVeQxIk
# What are you doing here?!

from random import randint
from turtle import position, pu
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import easygui
from perlin_noise import PerlinNoise

app = Ursina()

# Variables
grass_texture = load_texture("./files/Grass_Block.png")
sand_texture = load_texture("./files/Sand_Block.png")
stone_texture = load_texture("./files/Stone_Block.png")
brick_texture = load_texture("./files/Brick_Block.png")
dirt_texture = load_texture("./files/Dirt_Block.png")
wood_texture = load_texture("./files/Wood_Block.png")
water_texture = load_texture("./files/Water_Liquid.png")
leaves_texture = load_texture("./files/Leaves_Block.png")
snowy_grass_texture = load_texture("./files/Snowy_Grass_Block.png")
bedrock_texture = load_texture("./files/Bedrock_Block.png")
sky_texture = load_texture("./files/Skybox.png")
arm_texture = load_texture("./files/Arm_Texture.png")

hotbar_texture = load_texture("./files/Grass_Block_Hotbar.png")

stone = Audio("./files/Stone.wav", loop = False, autoplay = False)
dirt = Audio("./files/Dirt.wav", loop = False, autoplay = False)
water = Audio("./files/Water.mp3", loop = False, autoplay = False)

blocks = []

player = FirstPersonController(gravity=1)
player.scale_x = 0.8
player.scale_y = 0.8
player.scale_z = 0.8

noise = PerlinNoise(octaves=4,seed=randint(-10000000,10000000))
window.exit_button.visible = False
block_pick = 1
randint=random.randint
player.speed = 5


# Updates every frame
def update():

    
    
    if player.y < -10:
        player.y = 40
        player.x = 0
        player.z = 0
    
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

    if held_keys["left shift"]:
        if player.speed == 5:
            player.speed = 8
            camera.animate("fov", camera.fov+30, delay=0)
        else:
            player.speed = 5
            camera.animate("fov", camera.fov-30, delay=0)

# Voxel (block) properties
class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_texture):
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
            xyz1 = str(self.position).split("(")
            xyz = (xyz1[1].replace(")","")).split(",")
            if key == "right mouse down":
                blocks.append(str(int(xyz[1]) + 1).replace(" ","") + "," + str(xyz[0]) + "," + str(xyz[2]).replace(" ","") + ";")
                blocks.append(str(block_pick) + "$")
                
                save = open("save.pymcs", "a")

                save.write(str(blocks[len(blocks) - 2]) + str(blocks[len(blocks) - 1]))

                save.close()
                
                if block_pick==1 or block_pick==4: dirt.play()
                elif block_pick==6: water.play()
                else: stone.play()

                #Placement
                if block_pick == 1:
                    if biome == "Snowy Plains":
                        voxel = Voxel(position = self.position + mouse.normal, texture = snowy_grass_texture)
                    else:
                        voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = wood_texture)
                if block_pick == 6: voxel = Voxel(position = self.position + mouse.normal, texture = water_texture)
                if block_pick == 7: voxel = Voxel(position = self.position + mouse.normal, texture = leaves_texture)
                if block_pick == 8: voxel = Voxel(position = self.position + mouse.normal, texture = sand_texture)
                if block_pick == 9: voxel = Voxel(position = self.position + mouse.normal, texture = bedrock_texture)


            if key == "left mouse down":
                if (str(int(xyz[1]) + 1).replace(" ","") + "," + str(xyz[0]) + "," + str(xyz[2]).replace(" ","") + ";") in blocks:
                    blocks.pop(blocks.index(str(int(xyz[1]) + 1).replace(" ","") + "," + str(xyz[0]) + "," + str(xyz[2]).replace(" ","") + ";") + 1)
                    blocks.remove(str(int(xyz[1]) + 1).replace(" ","") + "," + str(xyz[0]) + "," + str(xyz[2]).replace(" ","") + ";")
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

col = easygui.choicebox(msg="Create or load?", title="Create or load", choices=["Create", "Load"])

if col == "Create":
    warning = easygui.msgbox(msg="If having performance issues, read readme.md", title="Tip", ok_button="Okay")
    performance = easygui.choicebox(msg="Performance mode:", title="Performance mode", choices=["On", "Off"])
    width = int(easygui.enterbox(msg="Width: ", title="Width"))
    widthm = width - 2*width
    depth = int(easygui.enterbox(msg="Depth: ", title="Depth"))
    depthm = depth - 2*depth
    gentype = easygui.choicebox(msg="Generation type:", title="Generation type", choices=["Normal", "Flat"])
    biome = easygui.choicebox(msg="Choose a biome for generation:", title="Biome", choices=["Random", "Forest", "Jungle", "Plains", "Snowy Plains", "Beach"])
    if biome == "Random":
        o = randint(1,5)
        if o == 1:
            biome = "Forest"
        elif o == 2:
            biome = "Plains"
        elif o == 3:
            biome = "Jungle"
        elif o == 4:
            biome = "Beach"
        else:
            biome = "Snowy Plains"
    seedc = easygui.enterbox(msg="Seed(type random for random seed): ", title="Seed")
    if seedc != "random":
        noise = PerlinNoise(octaves=4,seed=int(seedc))

    save = open("save.pymcs", "w")
    
    save.write(str(width) + " " + str(widthm) + " " + str(depth) + " " + str(depthm) + "," + biome + "!")

    save.close()

    x = ""

    if performance == "On":
        x += "1 "
    else:
        x += "0 "

    x += str(width) + " "
    x += str(widthm) + " "
    x += str(depth) + " "
    x += str(depthm) + " "

    if gentype == "Normal":
        x += "0 "
    else:
        x += "1 "

    if biome == "Forest":
        x += "0 "
    elif biome == "Jungle":
        x += "1 "
    elif biome == "Plains":
        x += "2 "
    elif biome == "Snowy Plains":
        x += "3 "
    elif biome == "Beach":
        x += "4 "
    else:
        x += "5 "

    x += seedc

    print("Your save code:", x)

if col == "Load":
    lc = easygui.enterbox(msg="Enter load code: ", title="Load")

    spl = lc.split()

    if spl[0] == 1:
        performance = "On"
    else:
        performance = "Off"
    performance = spl[0]

    width = int(spl[1])

    widthm = int(spl[2])

    depth = int(spl[3])

    depthm = int(spl[4])

    if spl[5] == "0":
        gentype = "Normal"
    else:
        gentype = "Flat"

    if spl[6] == "0":
        biome = "Forest"
    elif spl[6] == "1":
        biome = "Jungle"
    elif spl[6] == "2":
        biome = "Plains"
    elif spl[6] == "3":
        biome = "Snowy Plains"
    elif spl[6] == "4":
        biome = "Beach"
    else:
        o = randint(1,5)
        if o == 1:
            biome = "Forest"
        elif o == 2:
            biome = "Plains"
        elif o == 3:
            biome = "Jungle"
        elif o == 4:
            biome = "Beach"
        else:
            biome = "Snowy Plains"

    seedc = spl[7]
    with open("save.pymcs", "r") as save:
        saveload = save.read().replace("\n", "")
    saveload1 = saveload.split("!")
    wdb = saveload1[0].split(",")
    wd = wdb[0].split(" ")

    width = int(wd[0])
    widthm = int(wd[1])
    depth = int(wd[2])
    depthm = int(wd[3])

    biome = wdb[1]

    blocksload = saveload1[1].split("$")

    for x in range(widthm, width):
        for z in range(depthm, depth):
            for y in range(-4, 15):
                for t in range(1,9):
                    if (str(y) + "," + str(x) + "," + str(z) + ";" + str(t)) in blocksload:
                        if t == 1 and biome == "Snowy Plains": loadt = snowy_grass_texture
                        else: loadt = grass_texture
                        if t == 2: loadt = stone_texture
                        if t == 3: loadt = brick_texture
                        if t == 4: loadt = dirt_texture
                        if t == 5: loadt = wood_texture
                        if t == 6: loadt = water_texture
                        if t == 7: loadt = leaves_texture
                        if t == 8: loadt = sand_texture
                        if t == 9: loadt = bedrock_texture
                        voxel = Voxel(position=(x,y,z), texture = loadt)

    

if gentype=="Normal":
    for z in range(depthm,depth):
        for x in range(widthm,width):
            y = noise([x * .02,z * .02])
            y = math.floor(y * 7.5)
            s=y
            if biome == "Forest" or biome == "Plains" or biome == "Jungle":
                voxel = Voxel(position=(x,y,z), texture = grass_texture)
            elif biome == "Beach":
                if y > -1:
                    voxel = Voxel(position=(x,y,z), texture = sand_texture)
                else:
                    voxel = Voxel(position=(x,y,z), texture = snowy_grass_texture)
            if biome == "Forest" or biome == "Jungle":
                if biome == "Forest":
                    r = randint(0,60)
                else:
                    r = randint(0,30)
                if r == 0:
                    #Layer 1
                    voxel = Voxel(position = (x, y+1, z), texture = wood_texture)
                    #Layer 2
                    voxel = Voxel(position = (x, y+2, z), texture = wood_texture)
                    #Layer 3
                    voxel = Voxel(position = (x, y+3, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, y+3, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+3, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+3, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+3, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+3, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+3, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+3, z-1), texture = leaves_texture)

                    voxel = Voxel(position = (x+1, y+3, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+3, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+3, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+3, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+3, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+3, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, y+3, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, y+3, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, y+3, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, y+3, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, y+3, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, y+3, z+1), texture = leaves_texture)
                    #Layer 4
                    voxel = Voxel(position = (x, y+4, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, y+4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+4, z-1), texture = leaves_texture)

                    voxel = Voxel(position = (x+1, y+4, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+4, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+4, z-2), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+4, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+4, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+4, z+2), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, y+4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, y+4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+2, y+4, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, y+4, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, y+4, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-2, y+4, z+1), texture = leaves_texture)
                    #Layer 5
                    voxel = Voxel(position = (x, y+5, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, y+5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+5, z-1), texture = leaves_texture)
                    #Layer 6
                    voxel = Voxel(position = (x, y+6, z), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+6, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+6, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+6, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+6, z), texture = leaves_texture)

            if biome == "Beach" and y < 0:
                voxel = Voxel(position=(x,-1,z), texture=water_texture)
                voxel = Voxel(position=(x,-2,z), texture=water_texture) 
                voxel = Voxel(position=(x,-3,z), texture=water_texture)
            if performance == "off":
                while s>-3:
                    s-=1
                    voxel = Voxel(position=(x,s,z))


elif gentype=="Flat":
    for z in range(int(width)):
        for x in range(int(depth)):
            voxel = Voxel(position = (x, 0, z), texture = bedrock_texture)
            if biome == "Forest" or biome == "Plains":
                voxel = Voxel(position=(x,1,z), texture = grass_texture)
            else:
                voxel = Voxel(position=(x,1,z), texture = snowy_grass_texture)

sky = Sky()
hand = Hand()

app.run()
