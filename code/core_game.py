import math, sys, time, json, random

from PIL import Image
from player_file import Player_class
from settings import *

import menu

tile_size = [0,0]
rows = 18
columns = int(rows*1.3)

width, height = py.display.get_surface().get_size()
tile_size[0] = int(width / columns) + 1
tile_size[1] = int(height / rows) + 1


water = py.image.load("assets/img/tiles/water/water.png")
water_water_top = py.image.load("assets/img/tiles/water/water_water_top.png")
water_water_top_right = py.image.load("assets/img/tiles/water/water_water_top_right.png")
water_water_top_left = py.image.load("assets/img/tiles/water/water_water_top_left.png")
water_water_left = py.image.load("assets/img/tiles/water/water_water_left.png")
water_water_right = py.image.load("assets/img/tiles/water/water_water_right.png")
water_water_down = py.image.load("assets/img/tiles/water/water_water_down.png")
water_water_down_left = py.image.load("assets/img/tiles/water/water_water_down_left.png")
water_water_down_right = py.image.load("assets/img/tiles/water/water_water_down_right.png")
water_water_corner_down_right = py.image.load("assets/img/tiles/water/water_water_corner_down_right.png")
water_water_corner_down_left = py.image.load("assets/img/tiles/water/water_water_corner_down_left.png")
water_water_corner_top_right = py.image.load("assets/img/tiles/water/water_water_corner_top_right.png")
water_water_corner_top_left = py.image.load("assets/img/tiles/water/water_water_corner_top_left.png")

clear_water = py.image.load("assets/img/tiles/clear_water/clear_water.png")


grass = py.image.load("assets/img/tiles/grass/grass.png")
grass_dirt_top = py.image.load("assets/img/tiles/grass/grass_dirt_top.png")
grass_dirt_top_right = py.image.load("assets/img/tiles/grass/grass_dirt_top_right.png")
grass_dirt_top_left = py.image.load("assets/img/tiles/grass/grass_dirt_top_left.png")
grass_dirt_left = py.image.load("assets/img/tiles/grass/grass_dirt_left.png")
grass_dirt_right = py.image.load("assets/img/tiles/grass/grass_dirt_right.png")
grass_dirt_down = py.image.load("assets/img/tiles/grass/grass_dirt_down.png")
grass_dirt_down_left = py.image.load("assets/img/tiles/grass/grass_dirt_down_left.png")
grass_dirt_down_right = py.image.load("assets/img/tiles/grass/grass_dirt_down_right.png")
grass_dirt_corner_down_right = py.image.load("assets/img/tiles/grass/grass_dirt_corner_down_right.png")
grass_dirt_corner_down_left = py.image.load("assets/img/tiles/grass/grass_dirt_corner_down_left.png")
grass_dirt_corner_top_right = py.image.load("assets/img/tiles/grass/grass_dirt_corner_top_right.png")
grass_dirt_corner_top_left = py.image.load("assets/img/tiles/grass/grass_dirt_corner_top_left.png")
grass_tree_top_right = py.image.load("assets/img/tiles/grass/grass_tree_top_right.png")
grass_tree_top_left = py.image.load("assets/img/tiles/grass/grass_tree_top_left.png")
grass_tree_down_right = py.image.load("assets/img/tiles/grass/grass_tree_down_right.png")
grass_tree_down_left = py.image.load("assets/img/tiles/grass/grass_tree_down_left.png")
grass_mushroom1 = py.image.load("assets/img/tiles/grass/grass_mushroom1.png")
grass_mushroom2 = py.image.load("assets/img/tiles/grass/grass_mushroom2.png")
grass_bush = py.image.load("assets/img/tiles/grass/grass_bush.png")
grass_rock = py.image.load("assets/img/tiles/grass/grass_rock.png")





sand = py.image.load("assets/img/tiles/sand/sand.png")
sand_clearwater_top = py.image.load("assets/img/tiles/sand/sand_clearwater_top.png")
sand_clearwater_top_right = py.image.load("assets/img/tiles/sand/sand_clearwater_top_right.png")
sand_clearwater_top_left = py.image.load("assets/img/tiles/sand/sand_clearwater_top_left.png")
sand_clearwater_left = py.image.load("assets/img/tiles/sand/sand_clearwater_left.png")
sand_clearwater_right = py.image.load("assets/img/tiles/sand/sand_clearwater_right.png")
sand_clearwater_down = py.image.load("assets/img/tiles/sand/sand_clearwater_down.png")
sand_clearwater_down_left = py.image.load("assets/img/tiles/sand/sand_clearwater_down_left.png")
sand_clearwater_down_right = py.image.load("assets/img/tiles/sand/sand_clearwater_down_right.png")
sand_clearwater_corner_down_right = py.image.load("assets/img/tiles/sand/sand_clearwater_corner_down_right.png")
sand_clearwater_corner_down_left = py.image.load("assets/img/tiles/sand/sand_clearwater_corner_down_left.png")
sand_clearwater_corner_top_right = py.image.load("assets/img/tiles/sand/sand_clearwater_corner_top_right.png")
sand_clearwater_corner_top_left = py.image.load("assets/img/tiles/sand/sand_clearwater_corner_top_left.png")
sand_palm_top_right = py.image.load("assets/img/tiles/sand/sand_palm_top_right.png")
sand_palm_top_left = py.image.load("assets/img/tiles/sand/sand_palm_top_left.png")
sand_palm_down_right = py.image.load("assets/img/tiles/sand/sand_palm_down_right.png")
sand_palm_down_left = py.image.load("assets/img/tiles/sand/sand_palm_down_left.png")

clear_sand = py.image.load("assets/img/tiles/clear_sand/clear_sand.png")


rock = py.image.load("assets/img/tiles/cave/rock.png")
dirt_rock_top = py.image.load("assets/img/tiles/dirt/dirt_rock_top.png")
dirt_rock_top_right = py.image.load("assets/img/tiles/dirt/dirt_rock_top_right.png")
dirt_rock_top_left = py.image.load("assets/img/tiles/dirt/dirt_rock_top_left.png")
dirt_rock_left = py.image.load("assets/img/tiles/dirt/dirt_rock_left.png")
dirt_rock_right = py.image.load("assets/img/tiles/dirt/dirt_rock_right.png")
dirt_rock_down = py.image.load("assets/img/tiles/dirt/dirt_rock_down.png")
dirt_rock_down_left = py.image.load("assets/img/tiles/dirt/dirt_rock_down_left.png")
dirt_rock_down_right = py.image.load("assets/img/tiles/dirt/dirt_rock_down_right.png")
dirt_rock_corner_down_right = py.image.load("assets/img/tiles/dirt/dirt_rock_corner_down_right.png")
dirt_rock_corner_down_left = py.image.load("assets/img/tiles/dirt/dirt_rock_corner_down_left.png")
dirt_rock_corner_top_right = py.image.load("assets/img/tiles/dirt/dirt_rock_corner_top_right.png")
dirt_rock_corner_top_left = py.image.load("assets/img/tiles/dirt/dirt_rock_corner_top_left.png")




dirt = py.image.load("assets/img/tiles/dirt/dirt.png")




snow = py.image.load("assets/img/tiles/snow/snow.png")


atlas_top_right = py.image.load("assets/img/tiles/building/atlas/atlas_top_right.png")
atlas_top_left = py.image.load("assets/img/tiles/building/atlas/atlas_top_left.png")
atlas_down_right = py.image.load("assets/img/tiles/building/atlas/atlas_down_right.png")
atlas_down_left = py.image.load("assets/img/tiles/building/atlas/atlas_down_left.png")



tower_top_right = py.image.load("assets/img/tiles/building/tower/tower_top_right.png")
tower_right = py.image.load("assets/img/tiles/building/tower/tower_right.png")
tower_down_right = py.image.load("assets/img/tiles/building/tower/tower_down_right.png")
tower_down = py.image.load("assets/img/tiles/building/tower/tower_down.png")
tower_down_left = py.image.load("assets/img/tiles/building/tower/tower_down_left.png")
tower_left = py.image.load("assets/img/tiles/building/tower/tower_left.png")
tower_top_left = py.image.load("assets/img/tiles/building/tower/tower_top_left.png")
tower_top = py.image.load("assets/img/tiles/building/tower/tower_top.png")
tower_center = py.image.load("assets/img/tiles/building/tower/tower_center.png")






void = py.image.load("assets/img/tiles/void/void.png")



all_tile_list = [
    [snow],

    [rock],

    [dirt, dirt_rock_top,dirt_rock_top_left,dirt_rock_top_right,dirt_rock_right,dirt_rock_down_right,
     dirt_rock_down,dirt_rock_down_left,dirt_rock_left,dirt_rock_corner_top_right,dirt_rock_corner_top_left,
     dirt_rock_corner_down_right,dirt_rock_corner_down_left],

    [grass,grass_tree_top_right,grass_tree_top_left,grass_tree_down_right,grass_tree_down_left,grass_mushroom1,grass_mushroom2,
     grass_bush,grass_rock, grass_dirt_top,grass_dirt_top_left,grass_dirt_top_right,grass_dirt_right,grass_dirt_down_right,
     grass_dirt_down,grass_dirt_down_left,grass_dirt_left,grass_dirt_corner_top_right,grass_dirt_corner_top_left,
     grass_dirt_corner_down_right,grass_dirt_corner_down_left],

    [sand, sand_palm_top_right,sand_palm_top_left,sand_palm_down_right,sand_palm_down_left,sand_clearwater_top,sand_clearwater_top_left,
     sand_clearwater_top_right,sand_clearwater_right,sand_clearwater_down_right,sand_clearwater_down,
     sand_clearwater_down_left,sand_clearwater_left,sand_clearwater_corner_top_right,sand_clearwater_corner_top_left,
     sand_clearwater_corner_down_right,sand_clearwater_corner_down_left],

    [clear_water],

    [water, water_water_top,water_water_top_left,water_water_top_right,water_water_right,water_water_down_right,
     water_water_down,water_water_down_left,water_water_left,
     water_water_corner_top_right,water_water_corner_top_left,water_water_corner_down_right,water_water_corner_down_left
     ],

    [atlas_top_right,atlas_top_left,atlas_down_right,atlas_down_left],

    [tower_top,tower_top_right ,tower_right,tower_down_right,tower_down,tower_down_left,tower_left,
     tower_top_left,tower_center],

    [void]
]

all_tile_list_rs = []
for i in range(len(all_tile_list)):
    all_tile_list_rs.append([])
    for y in range(len(all_tile_list[i])):
        all_tile_list_rs[i].append(all_tile_list[i][y])


def resize_tile():
    for i in range(len(all_tile_list)):
        for y in range(len(all_tile_list[i])):
            all_tile_list_rs[i][y] = py.transform.scale(all_tile_list[i][y],(tile_size[0], tile_size[1]))

resize_tile()

tile_dict = {}
# Opening JSON file
with open("assets/data/tile.json") as json_file:
    tile_dict = json.load(json_file)




def draw_map_txt(tableau,player):



    time_start = time.time()
    frame = 0
    while True:
        frame+=1

        if(time.time()-time_start>1):
            print(frame)
            if DEBUG:
                print(f"clock fps: {CLOCK.get_fps()} | clock time: {CLOCK.get_time()}")
            time_start=time.time()
            frame=0


        #affichage
        width, height = py.display.get_surface().get_size()
        tile_size[0] = int(width/columns)+1
        tile_size[1] = int(height / rows)+1

        CLOCK.tick(FPS)
        draw_txt(width,height,tableau,player)
        player.draw(SCREEN,tile_size)


        py.display.flip()

        #all event
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            elif (event.type == py.MOUSEWHEEL):
                player.update_selected_item(event.y)

        player.move(tableau)
        key = py.key.get_pressed()

        if key[py.K_w]:
            player.add_weapon()
            player.resize(tile_size)

        if key[py.K_a]:
            player.hp-=1
        if key[py.K_e]:
            player.hp+=1

        if (py.mouse.get_pressed()[0] == 1):
            tableau = player.interract(tableau)
        
        if key[py.K_ESCAPE]:
            menu.run()


def check_tile_id(value):

    if value in tile_dict.keys():
        return tile_dict[value]
    else:
        print(value)
        return (len(all_tile_list)-1,0)


def draw_txt(width,height,tableau,player):

    pos = player.pos


    for x in range(int(pos[0]) - int(columns/2) -2,  int(pos[0]) + int(columns/2) +2):
         for y in range( int(pos[1])- int(rows/2) -2, int(pos[1])+ int(rows/2) +2):

                tile_id = check_tile_id(tableau[x][y])

                tile_to_draw = all_tile_list_rs[tile_id[0]][tile_id[1]]

                SCREEN.blit(tile_to_draw,((x-pos[0] + columns/2 )*tile_size[0],(y-pos[1]  + rows/2 )*tile_size[1]))

def read_map(filename):
    with open("assets/data/"+filename, 'r') as f:
        # Lecture de chaque ligne et stockage dans une liste
        lignes = f.readlines()

        tableau = []

        # Boucle sur chaque ligne pour diviser les nombres et les stocker dans une liste
        for ligne in lignes:
            element = ligne.strip().split(',')
            # Ajout de la liste d'éléments dans le tableau
            tableau.append(element)
        f.close()

    return tableau

def player_apparition(tableau,player):
    width, height = py.display.get_surface().get_size()

    side = ["down","left","up","right"]
    animation_side = 0
    lenght = 60*1
    rotation = 5
    elevation_speed = (9*(height/10))/lenght

    frame_to_rotate = int(lenght/(rotation*5))
    frame = 0

    player.offset[1]=-(height/2)
    player.resize(tile_size)
    for i in range(lenght):
        CLOCK.tick(FPS)

        width, height = py.display.get_surface().get_size()
        tile_size[0] = int(width / columns) + 1
        tile_size[1] = int(height / rows) + 1
        player.resize(tile_size)
        resize_tile()

        draw_txt(width, height, tableau, player)

        player.offset[1]+=(height/2)/lenght

        player.direction=side[animation_side]


        player.draw(SCREEN,tile_size)

        py.display.update()


        if (frame == frame_to_rotate):
            frame=0
            if(animation_side==(len(side)-1)):
                animation_side=0
            else:
                animation_side+=1
        else:
            frame+=1



        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

    player.offset=[0,0]
    player.direction="down"



def launch_game():
    py.display.set_caption("Survival")
    
    tableau = read_map("map.txt")

    player = Player_class()

    player_apparition(tableau,player)
    draw_map_txt(tableau,player)


