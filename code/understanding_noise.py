from perlin_noise import PerlinNoise
from PIL import Image
import time
import numpy
import pygame
from pygame.locals import *

#good values
SEED = 676
noise = PerlinNoise(octaves=800, seed=SEED) #1000 is good value
world_size = 100000 #100 000 is good value
chunk_size = 16
compteur = 0


def generate_chunk(chunk_num):

    startx = chunk_num[0]*chunk_size
    endx = (chunk_num[0]+1)*(chunk_size)

    starty = chunk_num[1] * chunk_size
    endy = (chunk_num[1] + 1) * (chunk_size)

    chunk = [[noise([ i/world_size, j/world_size])
           for j in range(starty,endy)]
            for i in range(startx,endx)]

    chunk = numpy.array([numpy.array(xi) for xi in chunk])
    return chunk


def chunkImage(chunk):
    chunk = chunk.copy()

    height = len(chunk)
    width = len(chunk[0])
    pic = [[0 for i in range(height)] for j in range(width)]

    image = Image.new("RGB", (height, width))

    for x in range(height):
        for y in range(width):
            pic[x][y] *= 255
            if (pic[x][y] < -120):
                pic[x][y] = (20, 20, 20)
            elif (pic[x][y] < -60):
                pic[x][y] = (128, 132, 135)
            elif (pic[x][y] < -20):
                pic[x][y] = (155, 118, 83)
            elif (pic[x][y] < 75):
                pic[x][y] = (126, 200, 80)
            elif (pic[x][y] < 83):
                pic[x][y] = (242, 209, 107)
            elif (pic[x][y] < 95):
                pic[x][y] = (115, 182, 254)
            else:
                pic[x][y] = (2, 75, 134)

            image.putpixel((x, y), pic[x][y])

    image.save("chunks/chunk"+str(compteur)+".png")

def testChunk():
    """chargement 2500 chunks"""
    a = time.perf_counter()
    L = []
    for j in range(50):
        for i in range(50):
            L.append(generate_chunk([i,j]))
    b = time.perf_counter()
    print(b-a)
    print("Time per chunk : ",((b-a)/2500)*1000," ms")

def loadChunk(chunk,surface : pygame.Surface):
    chunk = chunk.transpose()
    for x in range(chunk_size):
        for y in range(chunk_size):
            coord = [x*32,y*32]
            rect = pygame.Rect(coord[0],coord[1],32,32)
            chunk[y][x] *= 255
            if (chunk[y][x] < -120):
                pygame.draw.rect(surface,(20,20,20),rect)
            elif (chunk[y][x] < -60):
                pygame.draw.rect(surface,(128, 132, 135), rect)
            elif (chunk[y][x] < -20):
                pygame.draw.rect(surface,(155, 118, 83), rect)
            elif (chunk[y][x] < 60):
                pygame.draw.rect(surface, (126, 200, 80), rect)
            elif (chunk[y][x] < 83):
                pygame.draw.rect(surface, (242, 209, 107), rect)
            elif (chunk[y][x] < 95):
                pygame.draw.rect(surface, (115, 182, 254), rect)
            else:
                pygame.draw.rect(surface, (2, 75, 134), rect)

def loadSpawn():
    chunks = [[(pygame.Surface((chunk_size*32,chunk_size*32))) for j in range(3)] for i in range(3)]

    for x in range(-1,2):
        for y in range(-1,2):
            loadChunk(generate_chunk([x,y]),chunks[y+1][x+1])

    return chunks

def loadTop(chunks,coord,reso):
    #shift
    chunks[2][0],chunks[2][1],chunks[2][2] = \
        chunks[1][0].copy(),chunks[1][1].copy(),chunks[1][2].copy()

    chunks[1][0],chunks[1][1],chunks[1][2] = \
        chunks[0][0].copy(),chunks[0][1].copy(),chunks[0][2].copy()


    player_chunk_coordX = getPlayerChunkCoord(coord)[0]
    player_chunk_coordY = getPlayerChunkCoord(coord)[1]

    top_coord = [player_chunk_coordX,player_chunk_coordY-1]
    top_left_coord = [player_chunk_coordX-1, player_chunk_coordY - 1]
    top_right_coord = [player_chunk_coordX+1, player_chunk_coordY - 1]

    loadChunk(generate_chunk(top_left_coord),chunks[0][0])
    loadChunk(generate_chunk(top_coord),chunks[0][1])
    loadChunk(generate_chunk(top_right_coord),chunks[0][2])

def loadBottom(chunks,coord,reso):
    #shift
    chunks[0][0],chunks[0][1],chunks[0][2] = \
        chunks[1][0].copy(),chunks[1][1].copy(),chunks[1][2].copy()

    chunks[1][0],chunks[1][1],chunks[1][2] = \
        chunks[2][0].copy(),chunks[2][1].copy(),chunks[2][2].copy()


    player_chunk_coordX = getPlayerChunkCoord(coord)[0]
    player_chunk_coordY = getPlayerChunkCoord(coord)[1]

    bottom_coord = [player_chunk_coordX,player_chunk_coordY+1]

    bottom_left_coord = [player_chunk_coordX-1, player_chunk_coordY + 1]

    bottom_right_coord = [player_chunk_coordX+1, player_chunk_coordY + 1]

    loadChunk(generate_chunk(
        bottom_left_coord),chunks[2][0])
    loadChunk(generate_chunk(bottom_coord),chunks[2][1])
    loadChunk(generate_chunk(
        bottom_right_coord),chunks[2][2])

def loadRight(chunks,coord,reso):
    # shift
    chunks[0][0], chunks[1][0], chunks[2][0] = \
        chunks[0][1].copy(), chunks[1][1].copy(), chunks[2][1].copy()

    chunks[0][1], chunks[1][1], chunks[2][1] = \
        chunks[0][2].copy(), chunks[1][2].copy(), chunks[2][2].copy()

    player_chunk_coordX = getPlayerChunkCoord(coord)[0]
    player_chunk_coordY = getPlayerChunkCoord(coord)[1]

    right_coord = [player_chunk_coordX+1, player_chunk_coordY]
    right_top_coord = [player_chunk_coordX + 1, player_chunk_coordY - 1]
    right_bottom_coord = [player_chunk_coordX + 1, player_chunk_coordY + 1]

    loadChunk(generate_chunk(right_top_coord), chunks[0][2])
    loadChunk(generate_chunk(right_coord), chunks[1][2])
    loadChunk(generate_chunk(right_bottom_coord), chunks[2][2])

def loadLeft(chunks,coord,reso):
    # shift
    chunks[0][2], chunks[1][2], chunks[2][2] = \
        chunks[0][1].copy(), chunks[1][1].copy(), chunks[2][1].copy()

    chunks[0][1], chunks[1][1], chunks[2][1] = \
        chunks[0][0].copy(), chunks[1][0].copy(), chunks[2][0].copy()

    player_chunk_coordX = getPlayerChunkCoord(coord)[0]
    player_chunk_coordY = getPlayerChunkCoord(coord)[1]

    right_coord = [player_chunk_coordX-1, player_chunk_coordY]
    right_top_coord = [player_chunk_coordX - 1, player_chunk_coordY - 1]
    right_bottom_coord = [player_chunk_coordX - 1, player_chunk_coordY + 1]

    loadChunk(generate_chunk(right_top_coord), chunks[0][0])
    loadChunk(generate_chunk(right_coord), chunks[1][0])
    loadChunk(generate_chunk(right_bottom_coord), chunks[2][0])

def getPlayerChunkCoord(coord):
    player_chunk_coordX = int((-coord[0] + 32*chunk_size/2 )//(chunk_size*32))
    player_chunk_coordY = int((-coord[1] + 32*chunk_size/2 )//(chunk_size*32))
    return [player_chunk_coordX,player_chunk_coordY]


def jeu():
    width = 800
    height = 600
    reso = (width,height)
    fenetre = pygame.display.set_mode(reso)
    continuer = 1

    chunks = loadSpawn()

    coord = [0,0]
    backCoord = coord.copy()
    clock = pygame.time.Clock()

    pygame.key.set_repeat(1,1)
    while(continuer):
        clock.tick(30)
        fenetre.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0


            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    coord[0] += 1
                    backCoord[0] += 1
                    if getPlayerChunkCoord(backCoord)[0] == -1:
                        loadLeft(chunks,coord,reso)
                        backCoord[0] -= 32 * chunk_size

                if event.key == K_RIGHT:
                    coord[0] -= 1
                    backCoord[0] -= 1

                    if getPlayerChunkCoord(backCoord)[0] == 1:
                        loadRight(chunks,coord,reso)
                        backCoord[0] += 32 * chunk_size

                if event.key == K_UP:
                    coord[1] += 1
                    backCoord[1] += 1
                    if getPlayerChunkCoord(backCoord)[1] == -1:
                        loadTop(chunks,coord,reso)
                        backCoord[1] -= 32 * chunk_size

                if event.key == K_DOWN:
                    coord[1] -= 1
                    backCoord[1] -= 1

                    if getPlayerChunkCoord(backCoord)[1] == 1:
                        loadBottom(chunks,coord,reso)
                        backCoord[1] += 32 * chunk_size



        for i in range(-1,2):
            for j in range(-1,2):
                x = (j*32*chunk_size+backCoord[0]+ (width-32*chunk_size)/2)
                y = (i*32*chunk_size+backCoord[1]+ (height-32*chunk_size)/2)
                fenetre.blit(chunks[i+1][j+1],(x,y))

        hero = pygame.draw.rect(fenetre,(255,0,0),(384,284,32,32))
        pygame.display.flip()

    pygame.quit()

chunkImage(generate_chunk([0,0]))
jeu()

