from PIL import Image
import os

def separate_32x32_player(filename,name):
    isExist = os.path.exists("../assets/image/characters/"+name)
    if not isExist:
        os.makedirs("../assets/image/characters/"+name)
    to_save="../assets/image/characters/"+name+"/"
    extension = ".png"
    filename = "../"+filename
    img = Image.open(filename)

    im1 = img.crop((0, 0, 32, 32))
    im1.save(to_save+"down_2"+extension)
    im1 = img.crop((32, 0, 64, 32))
    im1.save(to_save+"down_1"+extension)
    im1 = img.crop((64, 0, 96, 32))
    im1.save(to_save+"down_3"+extension)

    im1 = img.crop((0, 32, 32, 64))
    im1.save(to_save+"left_2"+extension)
    im1 = img.crop((32, 32, 64, 64))
    im1.save(to_save+"left_1"+extension)
    im1 = img.crop((64, 32, 96, 64))
    im1.save(to_save+"left_3"+extension)

    im1 = img.crop((0, 64, 32, 96))
    im1.save(to_save+"right_2"+extension)
    im1 = img.crop((32, 64, 64, 96))
    im1.save(to_save+"right_1"+extension)
    im1 = img.crop((64, 64, 96, 96))
    im1.save(to_save+"right_3"+extension)

    im1 = img.crop((0, 96, 32, 128))
    im1.save(to_save+"up_2"+extension)
    im1 = img.crop((32, 96, 64, 128))
    im1.save(to_save+"up_1"+extension)
    im1 = img.crop((64, 96, 96, 128))
    im1.save(to_save+"up_3"+extension)


#github


iter = 1
for i in range (1,1):
    for y in range(1,5):
        x=str(i)
        y=str(y)
        if (len(str(x))==1):
            x= "0"+x

        file = "assets/image/PIPOYA FREE RPG Character Sprites 32x32/PIPOYA FREE RPG Character Sprites 32x32/Male/Male "+x+"-"+y+".png"
        n = str(iter)
        if(len(n)==1):
            n="0"+n
        separate_32x32_player(file,"male"+n)
        iter+=1

file = "free_character_nude.png"
separate_32x32_player(file,"nude")
