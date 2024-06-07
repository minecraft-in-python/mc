from random import randint
from turtle import position, pu
try:
    from ursina import *
    from ursina.prefabs.first_person_controller import FirstPersonController
    import easygui
    from perlin_noise import PerlinNoise
except:
    print("None/Not all modules installed! Please install them by running 'pip install -r ./requirements.txt' in Command Prompt while in 'mc-main' directory.")
    quit()

app = Ursina()

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

stone = Audio("./files/Stone.wav", loop = False, autoplay = False)
dirt = Audio("./files/Dirt.wav", loop = False, autoplay = False)
water = Audio("./files/Water.mp3", loop = False, autoplay = False)

dryhands = Audio("./files/dryhands.mp3", loop = True, autoplay = False)
haggstrom = Audio("./files/haggstrom.mp3", loop = True, autoplay = False)
hauntmuskie = Audio("./files/hauntmuskie.mp3", loop = True, autoplay = False)
livingmice = Audio("./files/livingmice.mp3", loop = True, autoplay = False)
miceonvenus = Audio("./files/miceonvenus.mp3", loop = True, autoplay = False)
minecraft = Audio("./files/minecraft.mp3", loop = True, autoplay = False)
subwoofer = Audio("./files/subwoofer.mp3", loop = True, autoplay = False)

blocks = []

player = FirstPersonController(gravity=0.8)

noise = PerlinNoise(octaves=4,seed=randint(-10000000,10000000))
window.exit_button.visible = False
block_pick = 1
randint=random.randint
player.speed = 5
camera.fov = 100

health = 2
playmusic = 1

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


col = easygui.choicebox(msg="Create or load?", title="Create or load", choices=["Create", "Load"])
savename = easygui.enterbox(msg="Save file name: ", title="Save file name")
fov = int(easygui.enterbox(msg="Field of view/FOV(default is 100): ", title="Field of view/FOV"))
fsn = savename + ".pymcs"
camera.fov = fov

class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = "Block",
            origin_y = 0.5,
            texture = texture,
            color = color.hsv(0, 0, random.uniform(0.9, 1)),
            highlight_color = color.light_gray,
            scale = 0.5
        )

    def input(self,key):
        if self.hovered:
            xyz1 = str(self.position).split("(")
            xyz = (xyz1[1].replace(")","")).split(",")
            if key == "escape":
                quit()
            if key == "left shift":
                if player.speed == 5:
                    player.speed = 8
                    camera.animate("fov", camera.fov+20, delay=0)
                else:
                    player.speed = 5
                    camera.animate("fov", camera.fov-20, delay=0)
            if key == "right mouse down":
                blocks.append(str(int(xyz[1]) + 1).replace(" ","") + "," + str(xyz[0]) + "," + str(xyz[2]).replace(" ","") + ";")
                blocks.append(str(block_pick) + "$")

                global fsn
                save = open(fsn, "a")

                save.write(str(blocks[len(blocks) - 2]) + str(blocks[len(blocks) - 1]))

                save.close()
                
                if block_pick==1 or block_pick==4: dirt.play()
                elif block_pick==6: water.play()
                else: stone.play()

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

pmrandint = randint(1,7)
if pmrandint == 1:
    dryhands.play()
elif pmrandint == 2:
    haggstrom.play()
elif pmrandint == 2:
    hauntmuskie.play()
elif pmrandint == 2:
    livingmice.play()
elif pmrandint == 2:
    miceonvenus.play()
elif pmrandint == 2:
    minecraft.play()
else:
    subwoofer.play()

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "Sphere",
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

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

if col == "Create":
    warning = easygui.msgbox(msg="If having performance issues, read readme.md", title="Tip", ok_button="Okay")
    performance = easygui.choicebox(msg="Performance mode:", title="Performance mode", choices=["On", "Off"])
    width = int(easygui.enterbox(msg="Width: ", title="Width"))
    widthm = width - 2*width
    depth = int(easygui.enterbox(msg="Depth: ", title="Depth"))
    depthm = depth - 2*depth
    gentype = easygui.choicebox(msg="Generation type:", title="Generation type", choices=["Normal", "Flat"])
    biome = easygui.choicebox(msg="Choose a biome for generation:", title="Biome", choices=["Random", "Desert", "Forest", "Jungle", "Plains", "Snowy Plains", "Beach"])
    if biome == "Random":
        o = randint(1,6)
        if o == 1:
            biome = "Forest"
        elif o == 2:
            biome = "Plains"
        elif o == 3:
            biome = "Jungle"
        elif o == 4:
            biome = "Beach"
        elif o == 5:
            biome = "Desert"
        else:
            biome = "Snowy Plains"
    seedc = easygui.enterbox(msg="Seed(type random for random seed): ", title="Seed")
    if seedc != "random":
        noise = PerlinNoise(octaves=4,seed=int(seedc))
    else:
        noise = PerlinNoise(octaves=4,seed=randint(-10000000,10000000))
    
    save = open(fsn, "w")
    
    save.write(str(width) + " " + str(widthm) + " " + str(depth) + " " + str(depthm) + "?" + biome + "," + performance + "," + gentype + "," + str(seedc) + "!")

    save.close()

if col == "Load":
    with open(fsn, "r") as save:
        saveload = save.read().replace("\n", "")
    saveload1 = saveload.split("!")
    wdb = saveload1[0].split("?")
    wd = wdb[0].split(" ")

    width = int(wd[0])
    widthm = int(wd[1])
    depth = int(wd[2])
    depthm = int(wd[3])

    bpgs = wdb[1].split(",")

    biome = bpgs[0]
    performance = bpgs[1]
    gentype = bpgs[2]
    seedc = int(bpgs[3])
    noise = PerlinNoise(octaves=4,seed=int(seedc))

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
            elif biome == "Beach" or biome == "Desert":
                if biome == "Beach":
                    if y > -1:
                        voxel = Voxel(position=(x,y,z), texture = sand_texture)
                else:
                    voxel = Voxel(position=(x,y,z), texture = sand_texture)
            else:
                voxel = Voxel(position=(x,y,z), texture = snowy_grass_texture)
            if biome == "Forest" or biome == "Jungle":
                if biome == "Forest":
                    r = randint(0,60)
                else:
                    r = randint(0,30)
                if r == 0:

                    voxel = Voxel(position = (x, y+1, z), texture = wood_texture)
                    
                    voxel = Voxel(position = (x, y+2, z), texture = wood_texture)
                    
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
                    
                    voxel = Voxel(position = (x, y+5, z), texture = wood_texture)
                    voxel = Voxel(position = (x+1, y+5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+5, z), texture = leaves_texture)
                    voxel = Voxel(position = (x+1, y+5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x-1, y+5, z-1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+5, z+1), texture = leaves_texture)
                    voxel = Voxel(position = (x, y+5, z-1), texture = leaves_texture)
                    
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
