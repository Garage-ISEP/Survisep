import os, sys, json
import random as r
from settings import *


SCREEN = py.display.set_mode((800, 600))
CLOCK = py.time.Clock()

grass = py.image.load("assets/img/tiles/grass/grass.png")
dirt = py.image.load("assets/img/tiles/dirt/dirt.png")

grass_dirt_left = py.image.load("assets/img/tiles/grass/grass_dirt_left.png")
grass_dirt_right = py.image.load("assets/img/tiles/grass/grass_dirt_right.png")

def draw_background(background_frame,ended):
    width, height = py.display.get_surface().get_size()
    tile_size = (int(width/12),int(height/12))

    grass_rs = py.transform.scale(grass,tile_size)
    dirt_rs = py.transform.scale(dirt,tile_size)
    grass_dirt_left_rs = py.transform.scale(grass_dirt_left,tile_size)
    grass_dirt_right_rs = py.transform.scale(grass_dirt_right,tile_size)

    offset=tile_size[0]/2
    for y in range(int(height/tile_size[1])+2):
        SCREEN.blit(grass_dirt_right_rs, (width / 2 - offset-tile_size[0], y * tile_size[1]-background_frame))
        SCREEN.blit(dirt_rs,(width/2-offset,y*tile_size[1]-background_frame))
        SCREEN.blit(grass_dirt_left_rs,(width/2+offset,y*tile_size[1]-background_frame))

        for x in range(0,-int((width/2)/tile_size[0]) ,-1):
            SCREEN.blit(grass_rs, ((width/2 - offset - tile_size[0]*2) + tile_size[0]*x,y*tile_size[1]-background_frame))
        for x in range(int((width+tile_size[0])/tile_size[0]),int((width/2)/tile_size[0]),-1):
            SCREEN.blit(grass_rs, (x*tile_size[0]+offset,y*tile_size[1]-background_frame))

    if (not ended):
        if (background_frame>=tile_size[0]):
            background_frame =0
        else:
            background_frame+=tile_size[0]/60
    return background_frame


def select_player_sprite():
    sign_left = py.image.load("assets/img/GUI/sign_left.png")
    sign_right = py.image.load("assets/img/GUI/sign_right.png")
    start_button = py.image.load("assets/img/GUI/start_button.png")

    py.display.set_caption("Character selection")


    file_source = "assets/img/characters"
    all_sprite = os.listdir("assets/img/characters")
    animation = 1
    animation_frame = 0
    choice = 0
    animation_time = 15
    background_frame = 0




    running = True
    while running:

        background_frame = draw_background(background_frame,False)

        width, height = py.display.get_surface().get_size()
        CLOCK.tick(60)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            # check if a sign is clicked
            if event.type == py.MOUSEBUTTONUP:
                mouse_pos = py.mouse.get_pos()
                # sign left
                if sign_left_pos[0] <= mouse_pos[0] <= sign_left_pos[0] + sign_left.get_width() and \
                        sign_left_pos[1] <= mouse_pos[1] <= sign_left_pos[1] + sign_left.get_height():
                    if (choice == 0):
                        choice = len(all_sprite) - 1
                    else:
                        choice -= 1
                # sign right
                elif sign_right_pos[0] <= mouse_pos[0] <= sign_right_pos[0] + sign_right.get_width() and \
                        sign_right_pos[1] <= mouse_pos[1] <= sign_right_pos[1] + sign_right.get_height():
                    if (choice == len(all_sprite) - 1):
                        choice = 0
                    else:
                        choice += 1

                # start sign
                elif start_button_pos[0] <= mouse_pos[0] <= start_button_pos[0] + start_button.get_width() and \
                        start_button_pos[1] <= mouse_pos[1] <= start_button_pos[1] + start_button.get_height():
                    data = None
                    with open("assets/data/player_info.json", 'r') as _file:
                        data = json.load(_file)
                        _file.close()
                    data["sprite"] = all_sprite[choice]

                    with open("assets/data/player_info.json", 'w') as _file:
                        json.dump(data, _file, indent=2)
                        _file.close()

                    running = False

            if (event.type==py.MOUSEWHEEL):
                if(event.y>0):
                    # sign right
                    if (choice == len(all_sprite) - 1):
                        choice = 0
                    else:
                        choice += 1
                else:
                    if (choice == 0):
                        choice = len(all_sprite) - 1
                    else:
                        choice -= 1





        # update sign pos and size with screen size
        sign_left = py.transform.scale(sign_left, (height / 8, height / 8))
        sign_left_pos = (width / 6, height - height / 4 - sign_left.get_height())
        sign_right = py.transform.scale(sign_right, (height / 8, height / 8))
        sign_right_pos = (width - width / 6 - sign_right.get_width(), height - height / 4 - sign_right.get_height())
        start_button = py.transform.scale(start_button, (width / 4, height / 9))
        start_button_pos = (1.5 * (width / 4), (height / 10) * 8)

        SCREEN.blit(sign_left, (sign_left_pos))
        SCREEN.blit(sign_right, (sign_right_pos))
        SCREEN.blit(start_button, (start_button_pos))

        # draw player
        player_sprite = py.image.load(file_source + "/" + all_sprite[choice] + "/down_" + str(animation) + ".png")
        player_sprite = py.transform.scale(player_sprite, (height / 7, height / 7))
        player_pos = (width / 2 - player_sprite.get_width() / 2, height - height / 4 - player_sprite.get_height())
        SCREEN.blit(player_sprite, player_pos)
        # draw player name
        font_name = py.font.SysFont('Eight Bit Dragon', int(height / 20))
        sprite_name = font_name.render(all_sprite[choice], True, (0, 0, 0))
        name_pos = player_pos = (
        width / 2 - sprite_name.get_width() / 2, height - height / 4 - player_sprite.get_height() * 1.5)
        SCREEN.blit(sprite_name, name_pos)

        # update animation
        animation_frame += 1
        if (animation_frame < animation_time * 1):
            animation = 1
        elif (animation_frame < animation_time * 2):
            animation = 2
        elif (animation_frame < animation_time * 3):
            animation = 1
        elif (animation_frame < animation_time * 4):
            animation = 3
        else:
            animation_frame = 1
            animation = 1

        py.display.update()

    add_weapon()

    finished_animation(background_frame,choice)

def finished_animation(background_frame,choice):
    width, height = py.display.get_surface().get_size()
    file_source =  "assets/img/characters"
    all_sprite = os.listdir("assets/img/characters")
    side = ["down","left","up","right"]
    animation_side = 0
    lenght = 60*1
    rotation = 6
    elevation_speed = (9*(height/10))/lenght

    frame_to_rotate = int(lenght/(rotation*4))
    frame = 0


    for i in range(1,lenght):
        CLOCK.tick(60)
        draw_background(background_frame,True)
        # draw player
        player_sprite = py.image.load(file_source + "/" + all_sprite[choice] + "/"+ side[animation_side]  +"_"   + "1.png")
        player_sprite = py.transform.scale(player_sprite, (height / 7, height / 7))
        player_sprite.set_alpha(255 - (255/lenght)*i*1.2)
        player_pos = (width / 2 - player_sprite.get_width() / 2, height - height / 4 - player_sprite.get_height() - elevation_speed*i)
        SCREEN.blit(player_sprite, player_pos)
        py.display.update()
        if (frame == frame_to_rotate):
            frame=0
            if(animation_side==(len(side)-1)):
                animation_side=0
            else:
                animation_side+=1
        else:
            frame+=1

def add_weapon():
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
