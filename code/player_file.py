from settings import *
import random as r

fps = 30

###########################################################
#
#                      Player Sprite Funcs
#
###########################################################

def load_player_sprite():
    sprite = []
    jsonFile = open("assets/data/player_info.json", "r+")
    data = json.load(jsonFile)
    sprite_name = data["sprite"]
    player_down_1 = py.image.load("assets/img/characters/"+sprite_name+"/down_1"+".png")
    player_down_2 = py.image.load("assets/img/characters/" + sprite_name + "/down_2"+".png")
    player_down_3 = py.image.load("assets/img/characters/" + sprite_name + "/down_3"+".png")
    player_left_1 = py.image.load("assets/img/characters/"+sprite_name+"/left_1"+".png")
    player_left_2 = py.image.load("assets/img/characters/" + sprite_name + "/left_2"+".png")
    player_left_3 = py.image.load("assets/img/characters/" + sprite_name + "/left_3"+".png")
    player_right_1 = py.image.load("assets/img/characters/"+sprite_name+"/right_1"+".png")
    player_right_2 = py.image.load("assets/img/characters/" + sprite_name + "/right_2"+".png")
    player_right_3 = py.image.load("assets/img/characters/" + sprite_name + "/right_3"+".png")
    player_up_1 = py.image.load("assets/img/characters/"+sprite_name+"/up_1"+".png")
    player_up_2 = py.image.load("assets/img/characters/" + sprite_name + "/up_2"+".png")
    player_up_3 = py.image.load("assets/img/characters/" + sprite_name + "/up_3"+".png")
    down = [player_down_1,player_down_2,player_down_3]
    left = [player_left_1, player_left_2, player_left_3]
    right = [player_right_1, player_right_2, player_right_3]
    up = [player_up_1, player_up_2, player_up_3]

    sprite.append(down)
    sprite.append(left)
    sprite.append(right)
    sprite.append(up)

    return sprite

def load_inventory_sprite():
    sprite = []
    data = None
    with open("assets/data/player_info.json", 'r') as _file:
        data = json.load(_file)
        _file.close()
    inventory = data["inventory"]
    for i in range(len(inventory)):
        sprite.append(py.image.load("assets/img/weapon/"+inventory[str(i+1)]["type"]+"/"+inventory[str(i+1)]["name"]+".png"))

    return sprite

def load_inventory_tile():
    sprite = []
    sprite.append(py.image.load("assets/img/GUI/inventory_tile_selected.png"))
    sprite.append(py.image.load("assets/img/GUI/inventory_tile.png"))
    sprite.append(py.image.load("assets/img/GUI/item_name_box.png"))

    return sprite

def load_inventory():
    data = None
    with open("assets/data/player_info.json", 'r') as _file:
        data = json.load(_file)
        _file.close()
    inventory = data["inventory"]
    return inventory



def create_resized_sprite(sprite):
    sprite_rs = []
    for i in range(len(sprite)):
        if (type(sprite[i])==list):
            sprite_rs.append([])
            for y in range(len(sprite[i])):
                sprite_rs[i].append(sprite[i][y])
        else:
            sprite_rs.append(sprite[i])
    return sprite_rs


###########################################################
#
#                      Player Class
#
###########################################################

class Player_class:
    pos = [0,0]
    name = ""
    hp = 0
    hp_max = 0
    level = 0
    item_selected = 0
    inventory_size=4
    inventory = None
    sprite = []
    sprite_rs = []
    animation = 1
    direction = "down"
    speed = 0
    frame = 0
    no_walk_tile = []
    offset = [0,0]
    inventory_tile =0
    inventory_tile_rs = 0

    inventory_sprite = 0
    inventory_sprite_rs = 0




    def __init__(self):

        self.actualize()
        self.pos = [r.randint(501,1500),r.randint(500,1500)]
        self.item_selected = 0
        self.sprite = load_player_sprite()
        self.sprite_rs = create_resized_sprite(self.sprite)
        self.animation = 0
        self.frame = 0
        self.direction = "down"
        self.speed = 0.15
        self.offset=[0,0]
        self.no_walk_tile = ["3.01","3.02","3.03","3.04","3.07","3.08","4.01","4.02","4.03","4.04","6"]
        self.inventory = load_inventory()
        self.inventory_tile = load_inventory_tile()
        self.inventory_tile_rs = create_resized_sprite(self.inventory_tile)
        self.inventory_sprite = load_inventory_sprite()
        self.inventory_sprite_rs = create_resized_sprite(self.inventory_sprite)



    def draw(self,screen,tile_size):
        font_name = py.font.SysFont('Eight Bit Dragon', 200)
        width, height = py.display.get_surface().get_size()
        #draw sprite
        if (self.direction=="down"):
            sprite_id1=0
        elif (self.direction=="left"):
            sprite_id1=1
        elif (self.direction == "right"):
            sprite_id1 = 2
        elif (self.direction == "up"):
            sprite_id1 = 3
        pos = (width/2-self.sprite_rs[sprite_id1][self.animation].get_width()/2 + self.offset[0],
                    height/2-self.sprite_rs[sprite_id1][self.animation].get_height()/2 + self.offset[1])
        screen.blit(self.sprite_rs[sprite_id1][self.animation],
                    pos)

        #draw inventory
        self.draw_inventory(screen,width,height,tile_size)

        #draw player name
        player_name_sprite = font_name.render(self.name, True, (255, 255, 255))
        name_size = player_name_sprite.get_size()
        rapport = tile_size[1]*0.3 / name_size[1]
        player_name_sprite = py.transform.scale(player_name_sprite,(name_size[0]*rapport,name_size[1]*rapport))
        player_name_sprite.set_alpha(160)
        player_name_pos = (width/2-player_name_sprite.get_width()/2 , pos[1]-tile_size[1]/20-player_name_sprite.get_height())
        screen.blit(player_name_sprite,player_name_pos)

        #draw level
        level_sprite = font_name.render(str(self.level), True, (50, 255, 50))
        level_size = level_sprite.get_size()
        rapport = tile_size[1] * 0.4 / level_size[1]
        level_sprite = py.transform.scale(level_sprite,(level_size[0]*rapport,level_size[1]*rapport))
        screen.blit(level_sprite,(player_name_pos[0]+tile_size[0]/10+player_name_sprite.get_width(),pos[1]-tile_size[1]/20-level_sprite.get_height()))



        #draw health bar full
        health_bar_lenght = int(tile_size[0]*1.5)
        health_bar_width = int(tile_size[1] * 0.2)
        health_bar_pos = (pos[0]-health_bar_lenght/2 + self.sprite_rs[sprite_id1][self.animation].get_width()/2,pos[1]-tile_size[1]/1.5)
        py.draw.rect(screen,(255,0,0),(int(health_bar_pos[0]),int(health_bar_pos[1]),health_bar_lenght,health_bar_width))
        #draw health bar hp
        bar_lenght = health_bar_lenght * (self.hp/self.hp_max)
        bar_width = int(tile_size[1] * 0.2)
        bar_pos = (pos[0]-health_bar_lenght/2 + self.sprite_rs[sprite_id1][self.animation].get_width()/2,pos[1]-tile_size[1]/1.5)
        py.draw.rect(screen,(0,255,0),(int(bar_pos[0]),int(health_bar_pos[1]),bar_lenght,bar_width))


    # Draw Inventory TOP LEFT of Screen

    def draw_inventory(self,screen,width, height,tile_size):
        font_name = py.font.SysFont('Eight Bit Dragon', 200)
        for x in range(self.inventory_size):
            #normal tile
            tile_to_draw = 1
            if (x==self.item_selected):
                #tile of selected item
                tile_to_draw = 0
            #draw inventory tile
            screen.blit(self.inventory_tile_rs[tile_to_draw],(width/100 + x*self.inventory_tile_rs[tile_to_draw].get_width()*1.5,height/100))
            #draw inventory name box
            screen.blit(self.inventory_tile_rs[2],
                        (width / 100 + x * self.inventory_tile_rs[2].get_width() * 1.5, height / 100 + self.inventory_tile_rs[tile_to_draw].get_height()*1.2 ))
            #draw inventory
            inv_pos = (width/100 + x*self.inventory_tile_rs[tile_to_draw].get_width()*1.5 + self.inventory_tile_rs[tile_to_draw].get_width()/2-(tile_size[0])/2,
                       height/100 + self.inventory_tile_rs[tile_to_draw].get_height()/2-(tile_size[0])/2)
            screen.blit(self.inventory_sprite_rs[x],inv_pos)

            #draw inventory name
            sprite_name = font_name.render(self.inventory[str(x+1)]["name"], True, (255, 255, 255))
            sprite_name = py.transform.scale(sprite_name,(self.inventory_tile_rs[2].get_width()*0.8,self.inventory_tile_rs[2].get_height()*0.6))
            screen.blit(sprite_name,
                        (width / 100 + x * self.inventory_tile_rs[2].get_width() * 1.5 + self.inventory_tile_rs[2].get_width()*0.1,
                         height / 100 + self.inventory_tile_rs[tile_to_draw].get_height() * 1.2 + self.inventory_tile_rs[tile_to_draw].get_height() * 0.1))

    def resize(self,tile_size):
        for i in range(len(self.inventory_tile)):
            self.inventory_tile_rs[i] = py.transform.scale(self.inventory_tile[i], (tile_size[0]*1.2, tile_size[0]*1.2))
            if (i==2):
                self.inventory_tile_rs[i] = py.transform.scale(self.inventory_tile[i],
                                                               (tile_size[0] * 1.2, tile_size[0] * 0.5))

        for i in range(len(self.sprite)):
            for y in range(len(self.sprite[i])):
                self.sprite_rs[i][y] = py.transform.scale(self.sprite[i][y],(tile_size[0],tile_size[1]))

        for i in range(len(self.inventory_sprite)):
            self.inventory_sprite_rs[i] = py.transform.scale(self.inventory_sprite[i], (tile_size[0], tile_size[0]))



    def move(self,tableau):
        self.can_move(tableau)
        key = py.key.get_pressed()
        moving = False
        if key[py.K_d]:
            self.direction="right"
            moving =True
            if(self.can_move(tableau)):
                self.pos[0] += self.speed
        elif key[py.K_q] :
            self.direction = "left"
            moving = True
            if (self.can_move(tableau)):
               self.pos[0] -= self.speed
        elif key[py.K_s] :
            self.direction = "down"
            moving = True
            if (self.can_move(tableau)):
                self.pos[1] += self.speed
        elif key[py.K_z] :
            self.direction = "up"
            moving = True
            if (self.can_move(tableau)):
                self.pos[1] -= self.speed


        self.update_animation_frame(moving)


    def update_animation_frame(self,moving):
        if (moving):
            self.frame+=1
            animation_time = int(fps*0.25)
            if (self.frame==animation_time*4):
                self.frame=0
            if(self.frame<animation_time*1):
                self.animation=0
            elif(self.frame<animation_time*2):
                self.animation=1
            elif(self.frame<animation_time*3):
                self.animation=0
            else:
                self.animation=2

        else:
            self.animation=0

    def can_move(self,tableau):
        move = True
        if (self.get_block_infront(tableau)in self.no_walk_tile):
            move = False
        return move

    def update_selected_item(self,delta):

        if (delta> 0):
            if (self.item_selected == self.inventory_size - 1):
                self.item_selected = 0
            else:
                self.item_selected += 1
        if (delta < 0):
            if (self.item_selected == 0):
                self.item_selected = self.inventory_size - 1
            else:
                self.item_selected -= 1


    def get_block_infront(self,tableau):
        if (self.direction=="up"):
            tile = tableau[int(self.pos[0])][int(self.pos[1]-self.speed)]

        elif (self.direction=="down"):
            tile = tableau[int(self.pos[0])][int(self.pos[1]+self.speed)]

        elif (self.direction=="right"):
            tile = tableau[int(self.pos[0]+self.speed)][int(self.pos[1])]

        elif (self.direction=="left"):
            tile = tableau[int(self.pos[0]-self.speed)][int(self.pos[1])]

        return tile

    def interract(self,tableau):
        if (self.get_block_infront(tableau)=="3.07"):
            if (self.direction == "up"):
                tableau[int(self.pos[0])][int(self.pos[1] - self.speed)] = "3"

            elif (self.direction == "down"):
                tableau[int(self.pos[0])][int(self.pos[1] + self.speed)]  = "3"

            elif (self.direction == "right"):
                tableau[int(self.pos[0] + self.speed)][int(self.pos[1])]  = "3"

            elif (self.direction == "left"):
                tableau[int(self.pos[0] - self.speed)][int(self.pos[1])] = "3"


        return tableau

    def add_weapon(self):
        all_hammer = os.listdir("assets/img/weapon/hammer")
        all_hammer = [hammer.replace(".png","") for hammer in all_hammer]

        all_knife = os.listdir("assets/img/weapon/knife")
        all_knife = [knife.replace(".png", "") for knife in all_knife]

        all_sword = os.listdir("assets/img/weapon/sword")
        all_sword = [sword.replace(".png", "") for sword in all_sword]
        all_weapon = []
        for hammer in all_hammer:
            all_weapon.append(["hammer",hammer])
        for knife in all_knife:
            all_weapon.append(["knife",knife])
        for sword in all_sword:
            all_weapon.append(["sword",sword])

        data = None
        with open("assets/data/player_info.json", 'r') as _file:
            data = json.load(_file)
            _file.close()

        for i in range(1,5):
            weapon = all_weapon[r.randint(0,len(all_weapon)-1)]
            data["inventory"][str(i)]["type"] = weapon[0]
            data["inventory"][str(i)]["name"] = weapon[1]


        with open("assets/data/player_info.json", 'w') as _file:
            json.dump(data, _file, indent=2)
            _file.close()

        self.inventory_sprite=load_inventory_sprite()
        self.inventory = load_inventory()

    def actualize(self):
        data = None
        with open("assets/data/player_info.json", 'r') as _file:
            data = json.load(_file)
            _file.close()
        self.name = data["name"]
        self.hp = data["hp"]
        self.hp_max = data["hp_max"]
        self.level = data["level"]