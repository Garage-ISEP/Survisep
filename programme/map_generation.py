from PIL import Image
import random as r
from perlin_noise import PerlinNoise
import pygame as py






def create_map_image():
        height,width = 2000,2000
        noise = PerlinNoise(octaves=25, seed=r.randint(1,100000))
        xpix, ypix = height,width
        pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]




        # creating a image object
        image = Image.new("RGB",(height,width))

        for x in range(height):
            for y in range(width):
                pic[x][y]*=255
                if(pic[x][y]<-120):
                    pic[x][y]= (20,20,20)
                elif (pic[x][y] < -60):
                    pic[x][y] = (128,132,135)
                elif (pic[x][y] < -20):
                    pic[x][y] = (155,118,83)
                elif (pic[x][y] < 75):
                    pic[x][y] = (126,200,80)
                elif (pic[x][y] < 83):
                    pic[x][y] = (242, 209, 107)
                elif (pic[x][y] < 95):
                    pic[x][y] = (115,182,254)
                else:
                    pic[x][y] = (2, 75, 134)

                image.putpixel((x, y), pic[x][y])


        image.save("map.png")


def creat_map_text(size):
    height, width = size,size
    noise = PerlinNoise(octaves=23, seed=r.randint(1, 100000))
    xpix, ypix = height, width
    pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]


    for x in range(height):
        for y in range(width):
            pic[x][y] *= 255
            pic[x][y] +=10
            if (pic[x][y] < -90):
                pic[x][y] = "0" #snow
            elif (pic[x][y] < -50):
                pic[x][y] = "1" #rock
            elif (pic[x][y] < -20):
                pic[x][y] = "2"  #dirt
            elif (pic[x][y] < 78):
                pic[x][y] = "3" #grass
            elif (pic[x][y] < 90):
                pic[x][y] = "4"  # sand
            elif (pic[x][y] < 100):
                pic[x][y] = "5" #clear water
            else:
                pic[x][y] = "6" #deep water

    with open('map.txt', 'w') as f:
        for x in range(len(pic)):
            f.write(",".join(pic[x]))
            f.write("\n")
        f.close()


def add_map_effect(filename):

    #get map in tablea
    with open('map.txt', 'r') as f:
        # Lecture de chaque ligne et stockage dans une liste
        lignes = f.readlines()

        tableau = []

        # recuperation du tablea
        for ligne in lignes:
            element = ligne.strip().split(',')
            # Ajout de la liste d'éléments dans le tableau
            tableau.append(element)

    #add transition
    left = False
    right = False
    top = False
    down = False
    for x in range(1,len(tableau)-1):
        for y in range(1,len(tableau[x])-1):
            left = False
            right = False
            top = False
            down = False
            #sand to water
            if tableau[x][y]=="4":
                if tableau[x][y-1]=="5":
                    top = True
                if tableau[x][y+1]=="5":
                    down = True
                if tableau[x-1][y]=="5":
                    left = True
                if tableau[x+1][y]=="5":
                    right = True

                if (top and not left and not right):
                    tableau[x][y]="4.1"
                elif (top and  left and not right):
                    tableau[x][y]="4.2"
                elif (top and not left and right):
                    tableau[x][y]="4.3"
                elif (down and not left and not right):
                    tableau[x][y]="4.6"
                elif (down and  left and not right):
                    tableau[x][y]="4.7"
                elif (down and not left and right):
                    tableau[x][y]="4.5"
                elif (left and not right):
                    tableau[x][y]="4.8"
                elif (not left and  right):
                    tableau[x][y]="4.4"

            left = False
            right = False
            top = False
            down = False
            #grass to dirt
            if tableau[x][y] == "3":
                if tableau[x][y - 1] == "2":
                    top = True
                if tableau[x][y + 1] == "2":
                    down = True
                if tableau[x - 1][y] == "2":
                    left = True
                if tableau[x + 1][y] == "2":
                    right = True

                if (top and not left and not right):
                    tableau[x][y] = "3.1"
                elif (top and left and not right):
                    tableau[x][y] = "3.2"
                elif (top and not left and right):
                    tableau[x][y] = "3.3"
                elif (down and not left and not right):
                    tableau[x][y] = "3.6"
                elif (down and left and not right):
                    tableau[x][y] = "3.7"
                elif (down and not left and right):
                    tableau[x][y] = "3.5"
                elif (left and not right):
                    tableau[x][y] = "3.8"
                elif (not left and right):
                    tableau[x][y] = "3.4"

            left = False
            right = False
            top = False
            down = False
            #dirt to rock
            if tableau[x][y] == "2":
                if tableau[x][y - 1] == "1":
                    top = True
                if tableau[x][y + 1] == "1":
                    down = True
                if tableau[x - 1][y] == "1":
                    left = True
                if tableau[x + 1][y] == "1":
                    right = True

                if (top and not left and not right):
                    tableau[x][y] = "2.1"
                elif (top and left and not right):
                    tableau[x][y] = "2.2"
                elif (top and not left and right):
                    tableau[x][y] = "2.3"
                elif (down and not left and not right):
                    tableau[x][y] = "2.6"
                elif (down and left and not right):
                    tableau[x][y] = "2.7"
                elif (down and not left and right):
                    tableau[x][y] = "2.5"
                elif (left and not right):
                    tableau[x][y] = "2.8"
                elif (not left and right):
                    tableau[x][y] = "2.4"

            left = False
            right = False
            top = False
            down = False
            #water to clearwater
            if tableau[x][y] == "6":
                if tableau[x][y - 1] == "5":
                    top = True
                if tableau[x][y + 1] == "5":
                    down = True
                if tableau[x - 1][y] == "5":
                    left = True
                if tableau[x + 1][y] == "5":
                    right = True

                if (top and not left and not right):
                    tableau[x][y] = "6.1"
                elif (top and left and not right):
                    tableau[x][y] = "6.2"
                elif (top and not left and right):
                    tableau[x][y] = "6.3"
                elif (down and not left and not right):
                    tableau[x][y] = "6.6"
                elif (down and left and not right):
                    tableau[x][y] = "6.7"
                elif (down and not left and right):
                    tableau[x][y] = "6.5"
                elif (left and not right):
                    tableau[x][y] = "6.8"
                elif (not left and right):
                    tableau[x][y] = "6.4"

    print("done2")

    #corner
    top_left = False
    top_right = False
    down_left = False
    down_right = False
    for x in range(1,len(tableau)-1):
        for y in range(1,len(tableau[x])-1):
            top_left = False
            top_right = False
            down_left = False
            down_right = False
            #sand to water
            if tableau[x][y]=="4":

                if tableau[x-1][y+1]=="5" :
                    down_left = True
                elif tableau[x+1][y-1]=="5" :
                    top_right = True
                elif tableau[x-1][y-1]=="5"  :
                    top_left = True
                elif tableau[x+1][y+1]=="5" :
                    down_right = True

                if (down_right):
                    tableau[x][y]="4.93"
                elif (down_left):
                    tableau[x][y] = "4.94"
                elif (top_right):
                    tableau[x][y]="4.91"
                elif (top_left):
                    tableau[x][y] = "4.92"

            top_left = False
            top_right = False
            down_left = False
            down_right = False
            #grass to dirt
            if tableau[x][y] == "3":

                if tableau[x-1][y+1]=="2" :
                    down_left = True
                elif tableau[x+1][y-1]=="2" :
                    top_right = True
                elif tableau[x-1][y-1]=="2"  :
                    top_left = True
                elif tableau[x+1][y+1]=="2" :
                    down_right = True

                if (down_right):
                    tableau[x][y]="3.93"
                elif (down_left):
                    tableau[x][y] = "3.94"
                elif (top_right):
                    tableau[x][y]="3.91"
                elif (top_left):
                    tableau[x][y] = "3.92"

            top_left = False
            top_right = False
            down_left = False
            down_right = False
            #water to clearwater
            if tableau[x][y] == "6":

                if tableau[x - 1][y + 1] == "5":
                    down_left = True
                elif tableau[x + 1][y - 1] == "5":
                    top_right = True
                elif tableau[x - 1][y - 1] == "5":
                    top_left = True
                elif tableau[x + 1][y + 1] == "5":
                    down_right = True

                if (down_right):
                    tableau[x][y] = "6.93"
                elif (down_left):
                    tableau[x][y] = "6.94"
                elif (top_right):
                    tableau[x][y] = "6.91"
                elif (top_left):
                    tableau[x][y] = "6.92"

            top_left = False
            top_right = False
            down_left = False
            down_right = False
            #dirt to rock
            if tableau[x][y]=="2":

                if tableau[x-1][y+1]=="1" :
                    down_left = True
                elif tableau[x+1][y-1]=="1" :
                    top_right = True
                elif tableau[x-1][y-1]=="1"  :
                    top_left = True
                elif tableau[x+1][y+1]=="1" :
                    down_right = True

                if (down_right):
                    tableau[x][y]="2.93"
                elif (down_left):
                    tableau[x][y] = "2.94"
                elif (top_right):
                    tableau[x][y]="2.91"
                elif (top_left):
                    tableau[x][y] = "2.92"


    print("done3")

    #other element
    for x in range(1,len(tableau)-1):
        for y in range(1,len(tableau[x])-1):
            #sand
            if tableau[x][y]=="4":
                #palm
                if (tableau[x][y-1]==tableau[x-1][y-1]==tableau[x-1][y]=="4"):
                     if (r.random()<0.03):
                        tableau[x][y]="4.03"
                        tableau[x-1][y] = "4.04"
                        tableau[x][y-1] = "4.01"
                        tableau[x-1][y-1] = "4.02"

            #grass
            if tableau[x][y] == "3":
                #mushroom
                if(r.random()<0.004):
                    if(r.random()<0.5):
                        tableau[x][y] = "3.05"
                    else:
                        tableau[x][y] = "3.06"

                #bush
                elif(r.random()<0.004):
                    tableau[x][y] = "3.07"
                #rock
                elif (r.random() < 0.001):
                    tableau[x][y] = "3.08"
                #tree
                elif (tableau[x][y-1]==tableau[x-1][y-1]==tableau[x-1][y]=="3"):
                     if (r.random()<0.003):
                        tableau[x][y]="3.03"
                        tableau[x-1][y] = "3.04"
                        tableau[x][y-1] = "3.01"
                        tableau[x-1][y-1] = "3.02"
                #atlas
                if (tableau[x][y-1]==tableau[x-1][y-1]==tableau[x-1][y]=="3"):
                     if (r.random()<0.0001):
                        tableau[x][y]="10.3"
                        tableau[x-1][y] = "10.4"
                        tableau[x][y-1] = "10.1"
                        tableau[x-1][y-1] = "10.2"

                #tower
                if (tableau[x][y]==tableau[x][y-1]==tableau[x][y-2]==
                    tableau[x-1][y] == tableau[x-1][y - 1] == tableau[x-1][y - 2]==
                    tableau[x-2][y] == tableau[x-2][y - 1] == tableau[x-2][y - 2]=="3"):

                     if (r.random()<0.00007):
                        tableau[x][y]="11.4"
                        tableau[x-1][y] = "11.5"
                        tableau[x-2][y] = "11.6"
                        tableau[x][y-1]="11.3"
                        tableau[x-1][y-1] = "11.9"
                        tableau[x-2][y-1] = "11.7"
                        tableau[x][y-2]="11.2"
                        tableau[x-1][y-2] = "11.1"
                        tableau[x-2][y-2] = "11.8"

    print("done4")
    #rewrite map
    with open('map.txt', 'w') as f:
        for x in range(len(tableau)):
            f.write(",".join(tableau[x]))
            f.write("\n")
        f.close()
    print("done5")





creat_map_text(2000)
print("done1")
add_map_effect("map.txt")
