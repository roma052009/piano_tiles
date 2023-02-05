from pygame import*
from random import*

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_width, player_height, player_image, player_x, player_y, player_speed):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.width = player_width
        self.height = player_height
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Tile(GameSprite):
    def set_route(self):
        a = randint(1, 4)
        if a == 1:
            self.rect.x = 0
        elif a == 2:
            self.rect.x = self.width
        elif a == 3:
            self.rect.x = self.width * 2
        elif a == 4:
            self.rect.x = self.width * 3
    def update(self):
        self.speed = tiles_speed
        self.rect.y += self.speed

class Arrow(GameSprite):
    def set_button(self, button):
        self.button = button

win_width = 400
win_height = 600

update_time = 1200
tiles_speed = 1

background = transform.scale(image.load("background_piano_tiles.png"), (win_width, win_height))
arrow_l = Arrow(int(win_width / 4), int(win_width / 4), "arrow_l.png", 0, win_height - int(win_width / 4), 0)
arrow_l.set_button("l")
arrow_u = Arrow(int(win_width / 4), int(win_width / 4), "arrow_u.png", int(win_width / 4), win_height - int(win_width / 4), 0)
arrow_u.set_button("u")
arrow_d = Arrow(int(win_width / 4), int(win_width / 4), "arrow_d.png", int(win_width / 4) * 2, win_height - int(win_width / 4), 0)
arrow_d.set_button("d")
arrow_r = Arrow(int(win_width / 4), int(win_width / 4), "arrow_r.png", int(win_width / 4) * 3, win_height - int(win_width / 4), 0)
arrow_r.set_button("r")

list_tiles = []

lost_tiles = 0

clock = time.Clock()
FPS = 60

window = display.set_mode((win_width, win_height))
display.set_caption("Piano_tiles")

font.init()
font1 = font.SysFont('Arial', 15)
text_lose = font1.render("Пропущено: " + str(lost_tiles), 1, (0, 0, 0))
text_speed = font1.render("Швидкість: " + str(tiles_speed), 1, (0, 0, 0))

game = True
while game:
    window.blit(background, (0, 0))
    

    window.blit(text_lose, (0, 0))

    window.blit(text_speed, (0, 15))

    if tiles_speed == 11:
        game = False
    
    if lost_tiles == 20:
        game = False

    if update_time != 0:
        update_time -= 1
    else:
        tiles_speed += 1
        text_speed = font1.render("Швидкість: " + str(tiles_speed), 1, (0, 0, 0))
        update_time = 1200


    if len(list_tiles) == 0:
        new_tile = Tile(int(win_width / 4), int(win_width / 4), "piano_tile.png", 0, 0, tiles_speed)
        new_tile.set_route()
        list_tiles.append(new_tile)
    else:
        if list_tiles[len(list_tiles) - 1].rect.y > list_tiles[len(list_tiles) - 1].height:
            new_tile = Tile(int(win_width / 4), int(win_width / 4), "piano_tile.png", 0, 0, 1)
            new_tile.set_route()
            list_tiles.append(new_tile)

    for i in list_tiles:
        if i.rect.y > win_height:
            list_tiles.remove(i)
            lost_tiles += 1
            text_lose = font1.render("Пропущено: " + str(lost_tiles), 1, (0, 0, 0))
        i.update()
        i.reset()
    
    keys = key.get_pressed()
    for i in list_tiles:
        if sprite.collide_rect(i , arrow_l) and keys[K_a]:
            list_tiles.remove(i)
        if sprite.collide_rect(i , arrow_u) and keys[K_w]:
            list_tiles.remove(i)
        if sprite.collide_rect(i , arrow_d) and keys[K_s]:
            list_tiles.remove(i)
        if sprite.collide_rect(i , arrow_r) and keys[K_d]:
            list_tiles.remove(i)

    arrow_l.reset()
    arrow_u.reset()
    arrow_d.reset()
    arrow_r.reset()


    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)