from settings import *

###########################################################
#
#                    Menu Classes (elements)
#
###########################################################

class Button:
    def __init__(self, pos:tuple[int, int], size:tuple[int,int], id:str, surface:py.surface.Surface=None, tags:list[str]=[], shown=True, pre_switched=False, colors:list[tuple[int,int,int],tuple[int,int,int]]=[(0,0,0)]) -> None:
        self.x, self.y = pos
        self.width, self.height = size
        self.switch = pre_switched
        self.shown = shown
        self.color = colors[0]
        self.colors = colors
        self.id = id
        self.tags = tags
        self.surface = surface
        self.rect = py.rect.Rect(self.x, self.y, self.width, self.height)
    
    def is_pressed(self, mouse_coords:tuple[int, int]) -> bool:
        if self.x < mouse_coords[0] < self.x + self.width and self.y < mouse_coords[1] < self.y + self.height:
            return True
        else: return False
    
    def print_text(self, font:py.font.Font, xy_offset:tuple[int,int]=(0,0), msg="", color=(0,0,0), align='center'):
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
        return (text,(x,y))


class Menu:
    def __init__(self) -> None:
        self.settings = Json(path='')
        self.data = self.settings.getData()
        self.font = py.font.Font(None, 24)
        self.CLOCK = py.time.Clock()

        self.fps = self.data["fps"]
        self.width, self.height = self.data["resolution"]
        self.index = self.data['pc_res'][self.data['aspect_ratio']].index(self.data['resolution'])

        self.window = py.display.set_mode((self.width, self.height))

        self.BUTTONS:list[Button] = []
        self.offset = self.width // 100

        self.BUTTONS.append(Button((self.width//4, self.height//2), (self.width//10, self.height//20), "res-", colors=[(255,100,100)]))
        self.BUTTONS.append(Button((self.width//4 + self.BUTTONS[0].width + self.offset, self.height//2), (self.width//10, self.height//20), "res+", colors=[(100,255,100)]))

    def render(self):
        py.display.set_caption(f"Resolution: {self.data['resolution']} | Ratio: {self.data['aspect_ratio']} | Index: {self.index}")
        self.window.fill((0,0,0))
        for button in self.BUTTONS:
            py.draw.rect(self.window, button.color, button.rect)
            text = button.print_text(self.font, msg=button.id)
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
                    if button.is_pressed(mouse_pos):
                        if button.id == 'res+' and self.index < len(self.data['pc_res'][self.data['aspect_ratio']]) - 1:
                            self.index += 1
                        elif button.id == 'res-' and self.index > 0:
                            self.index -= 1
                
                print(self.data['pc_res'][self.data['aspect_ratio']], self.index)

                self.settings.updateData('resolution', self.data['pc_res'][self.data['aspect_ratio']][self.index])
                self.data['resolution'] = self.data['pc_res'][self.data['aspect_ratio']][self.index]
                self.window = py.display.set_mode((self.data['resolution']))



    def main(self):
        self.running = True

        while self.running:

            self.CLOCK.tick(self.fps)

            self.render()
            self.events()

            py.display.update()

if __name__ == '__main__':
    Menu().main()