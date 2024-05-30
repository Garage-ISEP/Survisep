from settings import *

###########################################################
#
#                           To do list
#
#   Element's class rework
#
#
#
#
#
#
###########################################################



###########################################################
#
#                    Menu Classes (elements)
#
###########################################################

class Element:
    def __init__(self, topleft_coords:tuple[int, int], size:tuple[int,int], id:str, surface:py.surface.Surface=None, tags:list[str]=[], hide_tags=[False, False], pre_switched=False, colors:list[tuple[int,int,int],tuple[int,int,int]]=[(0,0,0)]) -> None:
        self.x, self.y                      = topleft_coords 
        self.width, self.height             = size

        self.switch                         = pre_switched

        self.surface_hide, self.text_hide   = hide_tags

        self.color                          = colors[0]
        self.colors                         = colors

        self.id                             = id
        self.tags                           = tags

        self.surface                        = surface

        self.rect = py.rect.Rect(self.x, self.y, self.width, self.height)
    
    def is_hovered(self, mouse_coords:tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_coords)

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
    def __init__(self, topleft_coords:tuple[int, int], size:tuple[int,int], id:str, surface:py.surface.Surface=None, tags:list[str]=['burger', 'show'], hide_tags=[False, False], pre_switched=False, colors:list[tuple[int,int,int],tuple[int,int,int]]=[(0,0,0)]) -> None:
        super().__init__(topleft_coords, size, id, surface, tags, hide_tags, pre_switched, colors)
    
    def is_hovered(self, mouse_coords:tuple[int, int]) -> bool:
        return super().is_hovered(mouse_coords)
    
    def print_text(self, font:py.font.Font, xy_offset:tuple[int,int]=(0,0), msg="", color=(0,0,0), align='center', scale_factor: tuple[float, float]=(1.0, 1.0)):
        return super().print_text(font, xy_offset, msg, color, align, scale_factor)

class HamburgerMenu(Element):
    def __init__(self, topleft_coords: tuple[int, int], size: tuple[int, int], id: str, surface: py.surface.Surface = None, tags: list[str] = ['burger', 'show', 'close'], hide_tags=[False, False], pre_switched=False, colors: list[tuple[int, int, int]] = [(0, 0, 0)], menu_items: list[str] = []) -> None:
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

    def render(self, window: py.surface.Surface, font: py.font.Font, scale_factor: tuple[float, float] = (1.0, 1.0)):
        if not self.surface_hide:
            py.draw.rect(window, self.color, self.rect)
        if not self.text_hide:
            text = self.print_text(font, msg=self.id, xy_offset=(0, 0), scale_factor=scale_factor)
            window.blit(text[0], text[1])
        
        if self.menu_open:
            for button in self.menu_buttons:
                if not button.surface_hide:
                    py.draw.rect(window, button.color, button.rect)
                if not button.text_hide:
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

        self.settings           = Json()
        self.data               = self.settings.getData()
        self.font               = py.font.Font(None, 24)
        self.CLOCK              = py.time.Clock()

        self.width, self.height = self.data["resolution"]
        self.original_res = self.data["resolution"] # Use of 'original' res as a reference for resizes

        self.fps                = self.data["fps"]

        self.index              = self.data['pc_res'][self.data['aspect_ratio']].index(self.data['resolution']) #Index -> switch between resolutions

        py.display.set_caption("Settings")

        position = (py.display.get_desktop_sizes()[0])                                   # Center the window each resize
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]/2 - self.width) + "," + str(position[1]/2 - self.height)

        self.window             = py.display.set_mode((self.width, self.height), py.HWSURFACE | py.SRCALPHA)

        self.ELEMENTS:list[Element] = []

        #self.ELEMENTS.append(HamburgerMenu((200, 200), (50, 50), "menu", colors=[(200, 200, 200)], menu_items=["Item 1", "Item 2", "Item 3"], tags=['burger', 'show', 'close']))
        
        self.ELEMENTS.append(Button((self.width/8, self.width/16), (self.width/8, self.width/16), "res-", colors=[(255,100,100)]))
        self.ELEMENTS.append(Button((self.width - (self.width/8 + self.width/8), self.width/16), (self.width/8, self.width/16), "res+", colors=[(100,255,100)], tags=['button', 'show']))
        self.ELEMENTS.append(Button((self.width//2 - self.width/6, self.height - self.width/5), (self.width/3, self.width/10), "apply", colors=[(100,100,255)]))
        
        self.resize_elements()  # Normalize positions and sizes of elements

        if DEBUG: 
            print(f"""
    | Window
- Actual Size: {self.width},{self.height}
- FPS: {self.fps}
""")
        
    def resize_elements(self):
        print(self.original_res)
        # Adjust the size and position of elements based on the new window size
        for x in self.ELEMENTS:
            print(x.id,x.rect)
            x.rect = py.rect.Rect(
                x.x * (self.width / self.original_res[0]), 
                x.y * (self.height / self.original_res[1]), 
                x.width * (self.width / self.original_res[0]), 
                x.height * (self.height / self.original_res[1])
            )
            print(x.id,x.rect)
            # SCALE element's SURFACE
        print("\n")

    def render(self):
        py.display.set_caption(f"Resolution: {self.data['resolution']} | Ratio: {self.data['aspect_ratio']} | Index: {self.index}")
        
        self.window.fill((0,0,0))

        scale_factor = (self.width / self.original_res[0], self.height / self.original_res[1])

        for x in self.ELEMENTS:
            if not x.surface_hide:
                if x.surface != None:
                    x.rect = py.rect.Rect(x.rect.topleft, x.surface.get_rect().size)
                    py.draw.rect(self.window, x.color, x.rect)
                    self.window.blit(x.surface, x.rect)
                else: py.draw.rect(self.window, x.color, x.rect)
            if not x.text_hide:
                text = x.print_text(self.font, msg=x.id, xy_offset=(0,0), scale_factor=scale_factor)
                self.window.blit(text[0], text[1])

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

    def main(self):
        self.running = True

        while self.running:

            self.CLOCK.tick(self.fps)

            self.render()
            self.events()

            py.display.update()

if __name__ == '__main__':
    DEBUG = True

    menu = Menu()
    menu.main()