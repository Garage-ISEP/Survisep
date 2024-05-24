from settings import *

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

    def print_text(self, font:py.font.Font, xy_offset:tuple[int,int]=(0,0), msg="", color=(0,0,0), align='center') -> tuple[py.surface.Surface, (int, int)]:
        text = font.render(msg, True, color)
        if align == 'center':
            x = self.x + self.width // 2 - text.get_width() // 2 + xy_offset[0]
            y = self.y + self.height // 2 - text.get_height() // 2 + xy_offset[1]
        elif align == 'left':
            x = self.x + xy_offset[0]
            y = self.y + self.height // 2 - text.get_height() // 2 + xy_offset[1]
        elif align == 'right':
            x = self.x + self.width - text.get_width() + xy_offset[0]
            y = self.y + self.height // 2 - text.get_height() // 2 + xy_offset[1]
        return (text,(x, y))

class Button(Element):
    def __init__(self, topleft_coords:tuple[int, int], size:tuple[int,int], id:str, surface:py.surface.Surface=None, tags:list[str]=[], hide_tags=[False, False], pre_switched=False, colors:list[tuple[int,int,int],tuple[int,int,int]]=[(0,0,0)]) -> None:
        super().__init__(topleft_coords, size, id, surface, tags, hide_tags, pre_switched, colors)
    
    def is_hovered(self, mouse_coords:tuple[int, int]) -> bool:
        if self.x < mouse_coords[0] < self.x + self.width and self.y < mouse_coords[1] < self.y + self.height:
            return True
        else: 
            return False
    
    def print_text(self, font:py.font.Font, xy_offset:tuple[int,int]=(0,0), msg="", color=(0,0,0), align='center'):
        return super().print_text(font, xy_offset, msg, color, align)

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

        self.fps                = self.data["fps"]
        self.width, self.height = self.data["resolution"]
        self.index              = self.data['pc_res'][self.data['aspect_ratio']].index(self.data['resolution']) #Index -> switch between resolutions

        self.window             = py.display.set_mode((self.width, self.height), py.HWSURFACE | py.SRCALPHA)
        self.RESIZE             = False

        self.ELEMENTS:list[list] = []
        self.BUTTONS:list[Button] = []

        self.BUTTONS.append(Button((self.width//4, self.height//4), (self.width//10, self.height//20), "res+", colors=[(100,255,100)]))
        self.BUTTONS.append(Button((self.width//2, self.height//4), (self.width//10, self.height//20), "res-", colors=[(255,100,100)]))
        self.BUTTONS.append(Button((self.width//2, self.height - self.height//8), (self.width//8, self.height//16), "apply", colors=[(100,100,255)]))
        self.ELEMENTS.append(self.BUTTONS)

        if DEBUG: 
            print(f"""
    | Window
- Actual Size: {self.width},{self.height}
- FPS: {self.fps}
""")

    def resize(self, rect:py.rect.Rect, index:int, ratio:str="4:3") -> None:
        w,h = self.window.get_size()
        ratio = ratio.split(":")
        ratio = (int(ratio[1]) / int(ratio[0]))
        print(ratio)
        index += 2

        # Scale and Translation ratios when Resizing Window
        scale_x = (160 * index)
        scale_y = (160 * index * ratio)
        move_x = rect.x / w
        move_y = rect.y / h

        rect.scale_by(scale_x,scale_y)
        rect.move(move_x,move_y)

    def render(self):
        py.display.set_caption(f"Resolution: {self.data['resolution']} | Ratio: {self.data['aspect_ratio']} | Index: {self.index}")
        
        self.window.fill((0,0,0))

        for element in self.ELEMENTS:
            for x in element:
                if self.RESIZE:
                    self.resize(x.rect, self.index)
                    self.RESIZE = False
                if not x.surface_hide:
                    py.draw.rect(self.window, x.color, x.rect)
                if not x.text_hide:
                    text = x.print_text(self.font, msg=x.id, xy_offset=(0,0))
                    self.window.blit(text[0], text[1])

    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONUP:
                mouse_pos = py.mouse.get_pos()

                for button in self.BUTTONS:
                    if button.is_hovered(mouse_pos):
                        if button.id == 'res+' and self.index < len(self.data['pc_res'][self.data['aspect_ratio']]) - 1:
                            self.index += 1
                        elif button.id == 'res-' and self.index > 0:
                            self.index -= 1
                        
                        if button.id == 'apply':
                            self.RESIZE = True

                            self.window = py.display.set_mode((self.data['resolution']))

    def main(self):
        self.running = True

        while self.running:

            self.CLOCK.tick(self.fps)

            self.render()
            self.events()

            py.display.update()

if __name__ == '__main__':
    DEBUG = True
    Menu().main()