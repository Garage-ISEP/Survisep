import pygame as py
import os, sys, json

py.font.init()
py.display.init()

default_settings = {
                "resolution_default": (640, 480),
                "resolution": (640, 480),
                "pc_res": {
                    "16:9": [(320,180),(480,270),(640,360),(800,450),(960,540),(1120,630)],
                    "16:10": [(320,200),(480,300),(640,400),(640,400),(640,400),(1120,700)],
                    "4:3": [(320,240),(480,360),(640,480),(800,600),(960,720),(1120,840)]
                },
                "aspect_ratio_default": '4:3',
                "aspect_ratio": '4:3',
                "fps": 30
        }

def path_to(path:str) -> str:
    path = path.split('/')
    path = f"{os.sep}".join(path)
    return path

class Json:
    def __init__(self, file:str="settings") -> None:
        self.file = file
        self.init_data()
    
    def init_data(self) -> None:
        try:
            with open(path_to(f'assets/data/{self.file}.json'), 'r') as file:
                #0/0                        # <--- Cause an error; force except
                pass
        except: # Default data for settings file
            with open(path_to(f'assets/data/{self.file}.json'), "w") as file:
                json.dump(default_settings, file)

    def getData(self) -> dict[list[int], list[int], dict, str, str, int]:
        jsonFile = open(path_to(f'assets/data/{self.file}.json'), "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        return data
        
    def updateData(self, key:str, value):
        data = self.getData()
        
        data[key] = value
        
        ## Save our changes to JSON file
        jsonFile = open(path_to(f'assets/data/{self.file}.json'), "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()