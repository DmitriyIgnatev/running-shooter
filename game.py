import pygame
import pygame.locals
import time
import os
import sys
import random
import pygame.constants


''' Окно '''
window = pygame.display.set_mode((400, 430))
pygame.display.set_caption("Hello, pygame!!!")
''' Холст '''
screen = pygame.Surface((400, 400))
''' Строка состояния '''
info_string = pygame.Surface((400, 30))
width, height = 1000, 700


class Menu:
    def __init__(self, punkts):
        self.punkts = punkts

    def render(self, poverhnost, font, num):
        for i in self.punkts:
            if num == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        flag = True
        font_menu = pygame.font.Font('fonts/Pun.otf', 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while flag:
            info_string.fill((0, 100, 200))
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] > i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        flag = False
                    elif punkt == 1:
                        sys.exit()
            window.blit(info_string, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()


zombies = random.randint(4, 10)
count_of_zom = zombies


def change(zombies):
    f1 = open('data/map.txt', mode='w', encoding='utf-8')
    zombies_coords = [(random.randint(5, 14), random.randint(5, 20)) for i in range(zombies)]
    houses = [(random.randint(3, 11), random.randint(5, 15)) for i in range(1)]
    stones = [(random.randint(5, 14), random.randint(5, 20)) for i in range(random.randint(6, 15))]
    maps = []
    for i in range(14):
        a = ''
        for j in range(20):
            g = random.choice(['#', '.'])
            a += g
        maps.append(a + '\n')
    for i in zombies_coords:
        try:
            a = list(maps[i[0]])
            if a[i[1]] == '@':
                continue
            else:
                a[i[1]] = 'z'
                maps[i[0]] = a
        except:
            continue
    hos = []
    for i in houses:
        try:
            a = list(maps[i[0]])
            if a[i[1]] == '@':
                continue
            else:
                a[i[1]] = random.choice(['h', 'c'])
                maps[i[0]] = a
                hos.append(a)
        except:
            continue
    for i in stones:
        try:
            a = list(maps[i[0]])
            if a[i[1]] == '@':
                continue
            if a[i[1]] != '@' and a[i[1]] != 'h' and a[i[1]] != 'c' and a[i[1]] != 'z':
                a[i[1]] = 's'
                maps[i[0]] = a
        except:
            continue
    maps += '$$$\n'
    maps += '$@$\n'
    maps += '$$$\n'
    for i in maps:
        f1.write(''.join(i))


change(zombies)

group = pygame.sprite.Group()
lake_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate_level(level):
    player, x, y, zombie = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('grow', x, y, 0)
            elif level[y][x] == '.':
                Tile('grow', x, y, 1)
            elif level[y][x] == '@':
                Tile('st', x, y, random.randint(0, 1))
                player = Player(y, x)
                all_sprites.add(player)
            elif level[y][x] == 'z':
                Tile('grow', x, y, 1)
                mon.add(Monsters(y, x, count_of_zom))
            elif level[y][x] == 'h':
                Tile('grow', x, y, 1)
                house = Block('house', x, y, 200)
                block_group.add(house)
            elif level[y][x] == 'c':
                Tile('grow', x, y, 1)
                house = Block('cfhfq', x, y, 300)
                block_group.add(house)
            elif level[y][x] == 's':
                Tile('grow', x, y, 1)
                st = Ston('stone_figure', x, y, 100, random.randint(0, 1))
                stones.add(st)
            elif level[y][x] == '$':
                Tile('st', x, y, random.randint(0, 1))
    return player, x, y, house


tile_images = {'grow': [load_image('brick1.jpg'), load_image('brick2.jpg')], 'house': load_image('house.png'),
               'cfhfq': load_image('cfhfq.png'),
               'stone_figure': [load_image('stom.png'), load_image('stone_figure.png')],
               'st': [load_image('stone1.jpg'), load_image('stone2.jpg')]}

all_sprites = pygame.sprite.Group()
SIZE = 100
size_monster = 70
tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()
bullet = pygame.sprite.Group()
mon = pygame.sprite.Group()
block_group = pygame.sprite.Group()
stones = pygame.sprite.Group()
health = pygame.sprite.Group()

health1 = pygame.sprite.Sprite()
health1.image = pygame.transform.scale(load_image('hear.png'), (50, 50))
health1.rect = health1.image.get_rect()
health1.rect.x = 0

health2 = pygame.sprite.Sprite()
health2.image = pygame.transform.scale(load_image('hear.png'), (50, 50))
health2.rect = health2.image.get_rect()
health2.rect.x = 50

health3 = pygame.sprite.Sprite()
health3.image = pygame.transform.scale(load_image('hear.png'), (50, 50))
health3.rect = health3.image.get_rect()
health3.rect.x = 100


class Block(pygame.sprite.Sprite):
    def __init__(self, name, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(tile_images[name], (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * 45
        self.rect.y = y * 45


class Ston(pygame.sprite.Sprite):
    def __init__(self, name, x, y, size, a):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(tile_images[name][a], (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * 45
        self.rect.y = y * 45

    def update(self):
        if pygame.sprite.spritecollideany(self, block_group):
            self.kill()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, a):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type][a]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(bullet)
        if pos[2] == 0 or pos[2] == 2:
            self.image = pygame.Surface((25, 5))
        else:
            self.image = pygame.Surface((5, 25))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        if pos[2] == 0 or pos[2] == 2:
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] + 49
        else:
            self.rect.x = pos[0] + 40
            self.rect.y = pos[1] + 49
        self.pos = pos

    def x(self):
        if self.pos[2] == 0:
            self.rect = self.rect.move(20, 0)
        if self.pos[2] == 1:
            self.rect = self.rect.move(0, 20)
        if self.pos[2] == 2:
            self.rect = self.rect.move(-20, 0)
        if self.pos[2] == 3:
            self.rect = self.rect.move(0, -20)

    def dellete(self):
        if self.rect.x >= 700 or self.rect.x <= 0 or self.rect.y >= 700 or self.rect.y <= 0:
            return True


monsters_dead = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x):
        super().__init__(all_sprites)
        self.anim_right = [pygame.transform.scale(pygame.image.load(f'data/r{i}.png'), (SIZE, SIZE)) for i in
                           range(1, 5)]
        self.image = pygame.transform.scale(pygame.image.load(f'data/r1.png'), (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x * 49
        self.rect.y = y * 49
        self.dx = 0
        self.dy = 0
        self.speed_x = 0.1
        self.speed_y = 1
        self.index_animation = 1
        self.direction = 0
        self.number_1 = True
        self.number_2 = True
        self.number_3 = True
        self.a = 0
        self.dead = [
            pygame.transform.scale(pygame.image.load(f'data/{i}.png'), (size_monster, size_monster)) for i in
            range(1, 5)]
        self.life = True

    def get(self):
        return self.rect.x, self.rect.y, self.direction

    def xy(self):
        return self.rect.x, self.rect.y

    def mon_heal(self):
        if pygame.sprite.spritecollideany(self, mon):
            self.heal()
            return 160
        return 0

    def update(self, house):
        if not self.life:
            self.kill()
            return 0
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.kill()
            return 0

        if pygame.sprite.collide_mask(self, house) and self.direction == 0:
            self.rect = self.rect.move(-2, 0)
        elif pygame.sprite.collide_mask(self, house) and self.direction == 1:
            self.rect = self.rect.move(0, -2)
        elif pygame.sprite.collide_mask(self, house) and self.direction == 2:
            self.rect = self.rect.move(2, 0)
        elif pygame.sprite.collide_mask(self, house) and self.direction == 3:
            self.rect = self.rect.move(0, 2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.dx = 2
            self.direction = 0
        elif keys[pygame.K_LEFT]:
            self.dx = -2
            self.direction = 2
        elif keys[pygame.K_UP]:
            self.dy = -2
            self.direction = 3
        elif keys[pygame.K_DOWN]:
            self.dy = 2
            self.direction = 1
        else:
            self.dx = 0
            self.dy = 0

        self.animation(self.dx, self.dy)
        self.rect.x += self.dx
        # self.collider_x()
        self.rect.y += self.dy
        # self.collider_y()
        # self.golds_up()

    def animation(self, dx, dy):
        try:
            if dx == 2:
                self.image = self.anim_right[int(self.index_animation)]
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
            elif dx == -2:
                self.image = pygame.transform.flip(self.anim_right[int(self.index_animation)], True, False)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
            elif dy == 2:
                self.image = pygame.transform.rotate(self.anim_right[int(self.index_animation)], -90)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
            elif dy == -2:
                self.image = pygame.transform.rotate(self.anim_right[int(self.index_animation)], 90)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
        except:
            self.index_animation = 1

    def heal(self):
        if self.number_1 == True and self.number_2 == True and self.number_3 == True:
            self.number_1 = False
            health3.kill()
        elif self.number_1 == False and self.number_2 == True and self.number_3 == True:
            self.number_2 = False
            health2.kill()
        elif self.number_1 == False and self.number_2 == False and self.number_3 == True:
            self.number_3 = False
            health1.kill()
            self.kill()

    def kill(self):
        try:
            health1.kill()
            health2.kill()
            health3.kill()
            self.life = False
            self.image = self.dead[int(self.a)]
            if int(self.a) >= 3:
                pass
            else:
                self.a += 0.05
        except:
            pass

    def finish(self):
        if not self.life:
            return True


class Monsters(pygame.sprite.Sprite):
    def __init__(self, y, x, count_of_zom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f'data/zom1.png'), (size_monster, size_monster))
        self.rect = self.image.get_rect()
        self.rect.x = x * 50
        self.rect.y = y * 50
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 3
        self.index_animation = 1
        self.flag = False
        self.anim_right = [
            pygame.transform.scale(pygame.image.load(f'data/zom{i}.png'), (size_monster, size_monster)) for i in
            range(1, 5)]
        self.dead = [
            pygame.transform.scale(pygame.image.load(f'data/zombie_dead{i}.png'), (size_monster, size_monster)) for i in
            range(1, 5)]
        self.dx = 0
        self.dy = 0
        self.speed_x = 0.1
        self.speed_y = 0.1
        self.index_animation = 1
        self.direction = 0
        self.count_of_zom = count_of_zom
        self.alive = True
        self.a = 0

    def plus(self):
        s = int(open('data/result.txt', mode='r', encoding='utf-8').readlines()[0].replace('\n', ''))
        s += 10
        wr = open('data/result.txt', mode='w', encoding='utf-8')
        wr.write(str(s))

    def get(self):
        return self.rect.x, self.rect.y, self.direction

    def update(self, obj, house, bul):
        if pygame.sprite.collide_mask(self, house) and self.direction == 2:
            self.rect = self.rect.move(0, 2)
        if pygame.sprite.collide_mask(self, house) and self.direction == 0:
            self.rect = self.rect.move(0, 2)
        if pygame.sprite.collide_mask(self, house) and self.direction == 1:
            self.rect = self.rect.move(2, 0)
        if pygame.sprite.collide_mask(self, house) and self.direction == 3:
            self.rect = self.rect.move(-2, 0)
        px, py = obj.xy()
        if self.rect.x != px:
            if self.rect.x >= px:
                self.dx = -1
                self.direction = 2
            else:
                self.dx = 1
                self.direction = 0
        if self.rect.y != py:
            if self.rect.y + 1 >= py and self.rect.y - 1 <= py and self.dx == 1:
                self.direction = 0
                self.dy = 0
            elif self.rect.y + 1 >= py and self.rect.y - 1 <= py and self.dx == -1:
                self.direction = 2
                self.dy = 0
            elif self.rect.y <= py:
                self.dy = 1
                self.direction = 1
            else:
                self.dy = -1
                self.direction = 3
        if (self.rect.y == py and self.rect.x == px) or self.alive == False:
            self.dx = 0
            self.dy = 0

        self.animation(self.direction)
        if self.dy == 0:
            self.direction = 0
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        if self.flag == True:
            self.kill()
        elif pygame.sprite.spritecollideany(self, bullet):
            self.health -= 1
            if self.health == 0:
                self.plus()
                self.flag = True
                bul.kill()
            else:
                self.plus()
                bul.kill()

    def animation(self, direction):
        try:
            if direction == 0:
                self.image = self.anim_right[int(self.index_animation)]
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.05
            elif direction == 2:
                self.image = pygame.transform.flip(self.anim_right[int(self.index_animation)], True, False)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.05
            elif direction == 1:
                self.image = pygame.transform.rotate(self.anim_right[int(self.index_animation)], -90)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.05
            elif direction == 3:
                self.image = pygame.transform.rotate(self.anim_right[int(self.index_animation)], 90)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.05
        except:
            self.index_animation = 1

    def kill(self):
        try:
            self.alive = False
            self.image = self.dead[int(self.a)]
            if int(self.a) >= 3:
                pass
            else:
                self.a += 0.05
        except:
            pass


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def finish_window(text):
    ''' Окно '''
    window = pygame.display.set_mode((400, 430))
    pygame.display.set_caption("Hello, pygame!!!")
    ''' Холст '''
    screen = pygame.Surface((400, 400))
    ''' Строка состояния '''
    info_string = pygame.Surface((400, 30))
    """ Создание финишного окна"""
    punkts = [(90, 140, u'Return', (250, 250, 30), (250, 30, 250), 0),
              (120, 210, u'Quit', (250, 250, 30), (250, 30, 250), 1)]
    punkt = [(10, 90, f'Результат:', (250, 250, 30), (250, 30, 250), 0),
             (40, 140, f'{int(text)-10} очков', (250, 250, 30), (250, 30, 250), 0),
             (40, 190, 'ОК', (250, 250, 30), (250, 30, 250), 0)]
    res = Menu(punkt)
    game = Menu(punkts)
    game.menu()
    res.menu()


def continue_window():
    ''' Окно '''
    window = pygame.display.set_mode((400, 430))
    pygame.display.set_caption("Hello, pygame!!!")
    ''' Холст '''
    screen = pygame.Surface((400, 400))
    ''' Строка состояния '''
    info_string = pygame.Surface((400, 30))
    """ Создание финишного окна"""
    punkts = [(30, 140, u'Next Stage', (250, 250, 30), (250, 30, 250), 0),
              (120, 210, u'Quit', (250, 250, 30), (250, 30, 250), 1)]
    game = Menu(punkts)
    game.menu()


def play_game():
    health.add(health1)
    health.add(health2)
    health.add(health3)
    size = 700, 700
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill((93, 62, 29))
    pygame.display.flip()
    fps = 80
    fps_heal = 0
    camera = Camera()
    clock = pygame.time.Clock()
    player, level_x, level_y, house = generate_level(load_level('map.txt'))
    tiles_group.draw(screen)
    space_group = pygame.sprite.Group()
    a = pygame.sprite.Sprite()
    a.image = load_image('space.jpg')
    a.rect = a.image.get_rect()
    space_group.add(a)
    space_group.draw(screen)
    stones.update()
    bul = Bullet(player.get())
    while running:
        space_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(bullet.sprites()) == 0:
                        bul = Bullet(player.get())
                        pygame.mixer.init()
                        pygame.mixer.music.load("data/shoot.mp3")
                        pygame.mixer.music.play()
        if len(mon.sprites()) == 0:
            zombies = random.randint(4, 10)
            change(zombies)
        try:
            bul.x()
        except:
            pass
        try:
            if bul.dellete():
                bul.kill()
        except:
            pass
        mon.update(player, house, bul)

        if fps_heal != 0:
            fps_heal -= 1
        if fps_heal == 0:
            fps_heal = player.mon_heal()
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        mon.draw(screen)
        group.draw(screen)
        bullet.draw(screen)
        stones.draw(screen)
        block_group.draw(screen)
        health.draw(screen)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in tiles_group:
            camera.apply(sprite)
        for sprite in block_group:
            camera.apply(sprite)
        for sprite in bullet:
            camera.apply(sprite)
        for sprite in mon:
            camera.apply(sprite)
        for sprite in stones:
            camera.apply(sprite)

        if fps_heal <= 160 and fps_heal >= 150:
            screen.fill('red')
        pygame.display.flip()
        player.update(house)
        clock.tick(fps)
        res = int(open('data/result.txt', mode='r', encoding='utf-8').readlines()[0].replace('\n', ''))
        if player.finish():
            running = False
            s = int(open('data/itog.txt', mode='r', encoding='utf-8').readlines()[0].replace('\n', ''))
            res = int(open('data/result.txt', mode='r', encoding='utf-8').readlines()[0].replace('\n', ''))
            wr = open('data/result.txt', mode='w', encoding='utf-8')
            wr.write(str(10))
            wr = open('data/itog.txt', mode='w', encoding='utf-8')
            wr.write(str(10))
            if s == 10:
                return 1, res
        elif int(count_of_zom) + 1 == res // 10:
            running = False
            s = int(open('data/itog.txt', mode='r', encoding='utf-8').readlines()[0].replace('\n', ''))
            res = int(open('data/result.txt', mode='r', encoding='utf-8').readlines()[0].replace('\n', ''))
            wr = open('data/result.txt', mode='w', encoding='utf-8')
            wr.write(str(10))
            wr = open('data/result.txt', mode='w', encoding='utf-8')
            wr.write(str(s + res))
            return 2, True


if __name__ == '__main__':
    pygame.init()
    """ Создание меню """
    punkts = [(120, 140, u'Play', (250, 250, 30), (250, 30, 250), 0),
              (120, 210, u'Quit', (250, 250, 30), (250, 30, 250), 1)]
    game = Menu(punkts)
    game.menu()
    while True:
        """ Подготовка к запуску игры """
        f = play_game()
        if f[0] == 1:
            """Финишное окно"""
            finish_window(str(f[1]))
            pygame.mixer.music.load("data/shoot.mp3")
            pygame.mixer.music.play()
        elif f[0] == 2:
            """Окно продолжения"""
            continue_window()
