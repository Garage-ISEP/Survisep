from typing import Any
from settings import *

###########################################################
#
#                    Menu Classes (elements)
#
###########################################################

class ImageLoader:
    def __init__(self, id:str="menu", path:str="assets/img/GUI/settings") -> None:
        self.dir = {'id':id,
                    'path':path}
        
        for file in os.listdir(path):
            if file.endswith('.png'):
                self.dir[file.removesuffix('.png')] = py.image.load(f"{path}/{file}").convert_alpha()

class Element:
    def __init__(self, topleft_coords:tuple[int, int], size:tuple[int,int], id:str, surface:py.surface.Surface=None, tags:list[str]=[], hide_tags=[False, False, False], pre_switched=False, colors:list[tuple[int,int,int],tuple[int,int,int]]=[(0,0,0)]) -> None:
        self.id                 = id
        self.switch             = pre_switched

        self.x, self.y          = topleft_coords 
        self.width, self.height = size

        self.hide_tags          = hide_tags
        self.tags               = tags


        self.color              = colors[0]
        self.colors             = colors
        
        self.surface            = surface
        self.rect = py.rect.Rect(self.x, self.y, self.width, self.height)
    
    def is_hovered(self, mouse_coords:tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_coords)
    
    def draw(self, window: py.surface.Surface, font: py.font.Font, scale_factor: tuple[float, float] = (1.0, 1.0)) -> None:
        if not self.hide_tags[0]:
            py.draw.rect(window, self.color, self.rect)
        if not self.hide_tags[1] and self.surface != None:
            self.surface = py.transform.scale(self.surface, self.rect.size)
            window.blit(self.surface, self.rect.topleft)
        if not self.hide_tags[2]:
            text = self.print_text(font, msg=self.id, xy_offset=(0, 0), scale_factor=scale_factor)
            window.blit(text[0], text[1])

    def print_text(self, font: py.font.Font, xy_offset: tuple[int,int]=(0,0), msg="", color=(0,0,0), align='center', scale_factor: tuple[float, float]=(1.0, 1.0)) -> tuple[py.surface.Surface, (int, int)]:
    #   Scale Font for resized windows
        scaled_font = py.font.Font(None, int(font.get_height() * scale_factor[1]))
        text = scaled_font.render(msg, True, color)

        scaled_x = self.x * scale_factor[0]
        scaled_y = self.y * scale_factor[1]
        scaled_width = self.width * scale_factor[0]
        scaled_height = self.height * scale_factor[1]
        offset_x = xy_offset[0] * scale_factor[0]
        offset_y = xy_offset[1] * scale_factor[1]

    #   Align text + offset for custom placement
        if align == 'center':
            x = int(scaled_x + scaled_width // 2 - text.get_width() // 2 + offset_x)
            y = int(scaled_y + scaled_height // 2 - text.get_height() // 2 + offset_y)
        elif align == 'left':
            x = int(scaled_x + offset_x)
            y = int(scaled_y + scaled_height // 2 - text.get_height() // 2 + offset_y)
        elif align == 'right':
            x = int(scaled_x + scaled_width - text.get_width() + offset_x)
            y = int(scaled_y + scaled_height // 2 - text.get_height() // 2 + offset_y)

        return (text, (x, y))

class Button(Element):
    def __init__(self, topleft_coords:tuple[int, int], size:tuple[int,int], id:str, surface:py.surface.Surface=None, tags:list[str]=['burger', 'show'], hide_tags=[False, False, False], pre_switched=False, colors:list[tuple[int,int,int],tuple[int,int,int]]=[(0,0,0)]) -> None:
        super().__init__(topleft_coords, size, id, surface, tags, hide_tags, pre_switched, colors)

class HamburgerMenu(Element):
    def __init__(self, topleft_coords: tuple[int, int], size: tuple[int, int], id: str, surface: py.surface.Surface = None, tags: list[str] = ['burger', 'show', 'close'], hide_tags=[False, False, False], pre_switched=False, colors: list[tuple[int, int, int]] = [(0, 0, 0)], menu_items: list[str] = []) -> None:
        super().__init__(topleft_coords, size, id, surface, tags, hide_tags, pre_switched, colors)
        self.menu_items = menu_items
        self.menu_buttons = self.create_menu_buttons()
        self.menu_open = False

    def create_menu_buttons(self) -> list[Button]:
        buttons = []
        item_height = self.height
        for i, item in enumerate(self.menu_items):
            button_y = self.y + (i + 1) * item_height
            button = Button((self.x, button_y), (self.width, item_height), item, colors=[(100, 100, 255)])
            buttons.append(button)
        return buttons

    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def is_hovered(self, mouse_coords: tuple[int, int]) -> bool:
        if self.rect.collidepoint(mouse_coords):
            return True
        if self.menu_open:
            for button in self.menu_buttons:
                if button.rect.collidepoint(mouse_coords):
                    return True
        return False

    def draw(self, window: py.surface.Surface, font: py.font.Font, scale_factor: tuple[float, float] = (1.0, 1.0)) -> None:
        super().draw(window, font, scale_factor)
        
        if self.menu_open:
            for button in self.menu_buttons:
                if not button.hide_tags[0]:
                    py.draw.rect(window, button.color, button.rect)
                if not self.hide_tags[1] and self.surface != None:
                    pass
                if not button.hide_tags[2]:
                    text = button.print_text(font, msg=button.id, xy_offset=(0, 0), scale_factor=scale_factor)
                    window.blit(text[0], text[1])

    def handle_click(self, mouse_coords: tuple[int, int]):
        if self.rect.collidepoint(mouse_coords):
            self.toggle_menu()
        elif self.menu_open:
            for button in self.menu_buttons:
                if button.rect.collidepoint(mouse_coords):
                    return button.id
        return None

###########################################################
#
#                 Menu (screen, render, events)
#
###########################################################

class Menu:
    def __init__(self) -> None:
        self.isActive = True

        self.settings           = Json()
        self.data               = self.settings.getData()
        self.font               = py.font.Font(None, 24)

        self.width, self.height = self.data["resolution"]
        self.original_res = self.data["resolution"] # Use of 'original' res as a reference for resizes

        self.index              = self.data['pc_res'][self.data['aspect_ratio']].index(self.data['resolution']) #Index -> switch between resolutions

        py.display.set_caption("Settings")

        position = (py.display.get_desktop_sizes()[0])                                   # Center the window each resize
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]/2 - self.width) + "," + str(position[1]/2 - self.height)

        self.window             = py.display.set_mode((self.width, self.height), py.HWSURFACE | py.SRCALPHA)

        self.ELEMENTS:list[Element] = []
        menuImages = ImageLoader().dir
        print(menuImages)

        #self.ELEMENTS.append(HamburgerMenu((200, 200), (50, 50), "menu", colors=[(200, 200, 200)], menu_items=["Item 1", "Item 2", "Item 3"], tags=['burger', 'show', 'close']))
        
        self.ELEMENTS.append(Button((self.width/8, self.width/16), (self.width/8, self.width/16), "res-", colors=[(255,100,100)], surface=menuImages['bs']))
        self.ELEMENTS.append(Button((self.width - (self.width/8 + self.width/8), self.width/16), (self.width/8, self.width/16), "res+", colors=[(100,255,100)], tags=['button', 'show'], surface=menuImages['bs']))
        self.ELEMENTS.append(Button((self.width//2 - self.width/6, self.height - self.width/5), (self.width/3, self.width/10), "apply", colors=[(100,100,255)]))
        self.ELEMENTS.append(Button((self.width - self.width/16, 0), (self.width/16, self.width/16), "X", colors=[(0,0,0)], hide_tags=[True, False, True], surface=menuImages['home']))
        
        self.resize_elements()  # Normalize positions and sizes of elements

        if DEBUG: 
            print(f"""
    | Window
- Actual Size: {self.width},{self.height}
- FPS: {FPS}
- Tick rate: {TICK}
""")

    def resize_elements(self):
        # Adjust the size and position of elements based on the new window size
        for x in self.ELEMENTS:
            x.rect = py.rect.Rect(
                x.x * (self.width / self.original_res[0]), 
                x.y * (self.height / self.original_res[1]), 
                x.width * (self.width / self.original_res[0]), 
                x.height * (self.height / self.original_res[1])
            )
            # SCALE element's SURFACE

    def render(self):
        py.display.set_caption(f"Resolution: {self.data['resolution']} | Ratio: {self.data['aspect_ratio']} | Index: {self.index}")
        
        self.window.fill((0,0,0))

        scale_factor = (self.width / self.original_res[0], self.height / self.original_res[1])

        for x in self.ELEMENTS:
            x.draw(self.window, self.font, scale_factor)

    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONUP:
                mouse_pos = py.mouse.get_pos()

                for button in self.ELEMENTS:
                    if button.is_hovered(mouse_pos):
                        if button.id == 'res+' and self.index < len(self.data['pc_res'][self.data['aspect_ratio']]) - 1:
                            self.index += 1
                            self.data['resolution'] = self.data['pc_res'][self.data['aspect_ratio']][self.index]    # Stock resolution (local)
                        elif button.id == 'res-' and self.index > 0:
                            self.index -= 1
                            self.data['resolution'] = self.data['pc_res'][self.data['aspect_ratio']][self.index]    # Stock resolution (local)
                        
                        if button.id == 'apply':
                            self.width, self.height = self.data['resolution']                                       # Retreive local resolution
                            self.settings.updateData('resolution', [self.width, self.height])                       # Stock local resolution in settings.json (global)

                            self.window = py.display.set_mode((self.width, self.height), py.SRCALPHA)
                            self.resize_elements()
                        
                        if button.id == 'X':
                            self.isActive = False
            
            if event.type == py.KEYUP:
                if event.key == py.K_ESCAPE:
                    self.running = False

    def main(self):
        #self.running = True

        while self.isActive:

            CLOCK.tick(FPS)

            self.render()
            self.events()

            py.display.update()

def run():
    menu = Menu()
    menu.main()

if __name__ == '__main__':
    run()