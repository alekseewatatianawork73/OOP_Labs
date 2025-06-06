# подключаем библиотеки и модули
import random
import pygame
from button import Button

# инициализируем все модули в pygame
pygame.init()

# создание нового файла с текущим рекордом 0, если его не существовало
f_records = open('records.txt', 'a')
f_records.write('0\n')
f_records.close()

# создаём таймер для установки частоты смены кадров
clock = pygame.time.Clock()

# создаём игровое окно и загружаем фон экрана
w, h = 800, 586
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Машинки')
bg = pygame.image.load('images/road.png')

# фоновая музыка
pygame.mixer.music.load('fon_music.mp3')

# картинки для машин
CARS = ('images/car1.png', 'images/car2.png')
# список для хранения существующих машин
CARS_SURF = []
for i in range(len(CARS)):
    CARS_SURF.append(pygame.image.load(CARS[i]))


# класс машин-спрайтов
class Car(pygame.sprite.Sprite):
    def __init__(self, y, surf, group):
        super().__init__()
        self.image = surf
        # прямоугольник, в котором находится машинка
        self.rect = self.image.get_rect(center=(w-10, y))
        # добавляем в группу
        self.add(group)
        self.add(all_cars)
        # у машин будет разная скорость
        self.speed = random.randint(7, 11)

    # метод для движения машинок
    def update(self):
        if self.rect.x < w:
            # двигаемся влево
            self.rect.x -= self.speed
        else:
            # удаляем из всех групп
            self.kill()


# класс для основного игрока-машины
class MyCar(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.image = surf
        # прямоугольник, в котором находится машинка
        self.rect = self.image.get_rect(center=(w / 2 - 50, h / 2))
        self.add(all_cars)

    # метод для движения машинки
    def update(self):
        p = pygame.key.get_pressed()
        if p[pygame.K_UP]:
            self.rect.y -= 5
        if p[pygame.K_DOWN]:
            self.rect.y += 5


# группы для машин-спрайтов
cars = pygame.sprite.Group()
all_cars = pygame.sprite.Group()

# создание основного игрока-машины и загрузка картинок для него
pl = pygame.image.load('images/my_car.png')
pl2 = pygame.image.load('images/my_car_2.png')
pl2 = pygame.transform.flip(pl2, True, False)
player = MyCar(pl)

# установка пользовательских событий и задание частоты их появления в миллисекундах
DISTANCE = pygame.USEREVENT + 1  # для увеличения дистанции
NEW_CAR = pygame.USEREVENT + 2  # для появления машинок, едущих навстречу
pygame.time.set_timer(NEW_CAR, 300)
pygame.time.set_timer(DISTANCE, 500)

my_font = pygame.font.SysFont(name='Arial', size=50, bold=True, italic=True)
f_end = pygame.font.SysFont(name='Arial', size=30, bold=True, italic=True)
# создание надписи game over
game_over = f_end.render('GAME OVER', True, (0, 0, 0))

# начальные данные
cls = 0  # количество столкновений
meters = 0  # дистанция в метрах

bg_x = 0  # координата для анимации фона
run = True  # для основного игрового цикла
close = False  # для обработки проигрыша
menu = False  # для постановки игры на паузу
win = True  # для проверки на достижение рекорда
rst = False  # для обнуления рекорда
start = True
while run:
    # начало игры
    while start:
        screen.blit(bg, (0, 0))
        # перекрываем основной экран белым полупрозрачным фоном
        area = pygame.Surface((w, h))
        area.fill((255, 255, 255))
        area.set_alpha(100)

        pause = my_font.render('Game «Mini-Cars»', True, (0, 0, 0))
        r1 = pause.get_rect(center=(w / 2, h / 2 - 200))
        screen.blit(area, (0, 0))
        screen.blit(pause, r1)

        button_start = Button((w / 2, h / 2 + 100), 300, 150, 'images/button.png', 'START')
        button_start.draw(screen)
        pygame.display.update()
        button_start.press_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                start = False
            # обработка нажатий на кнопки
            if event.type == pygame.USEREVENT:
                if event.button == button_start:
                    start = False
                    pygame.mixer.music.play(-1)

    # анимация фона (имитация движения)
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (w + bg_x, 0))
    bg_x -= 3
    if bg_x < -w:
        bg_x = 0

    # надписи о количестве столкновений и преодолённой дистанции
    clls = f_end.render(f'Collisions: {cls}/5', True, (0, 0, 0))
    mtr = f_end.render(f'Distance: {meters} m', True, (0, 0, 0))
    cl = clls.get_rect(topleft=(w - 250, 0))
    screen.blit(clls, cl)
    mt = mtr.get_rect(topleft=(10, 0))
    screen.blit(mtr, mt)

    # меню, всплывающее во время приостановки игры
    while menu:
        pygame.mixer.music.stop()
        screen.blit(bg, (0, 0))
        # перекрываем основной экран чёрным полупрозрачным фоном
        area = pygame.Surface((w, h))
        area.fill((0, 0, 0))
        area.set_alpha(100)
        # отображаем надпись ПАУЗА
        pause = my_font.render('PAUSE', True, (0, 0, 0))
        r1 = pause.get_rect(center=(w / 2, h / 2 - 200))
        screen.blit(area, (0, 0))
        screen.blit(pause, r1)

        # кнопка для продолжения игры
        button_continue = Button((w / 2, h / 2), 300, 125, 'images/button.png', 'CONTINUE')
        button_continue.draw(screen)

        # кнопка для замены автомобиля
        button_change = Button((w / 2, h / 2 + 100), 300, 125, 'images/button.png', 'CHANGE CAR')
        button_change.draw(screen)

        # кнопка для того, чтобы начать игру заново
        button_restart = Button((w / 2, h / 2 + 200), 300, 125, 'images/button.png', 'RESTART')
        button_restart.draw(screen)

        pygame.display.update()
        button_continue.press_button()
        button_restart.press_button()
        button_change.press_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu = False
            # обработка нажатий на кнопки
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.play(-1)
                if event.button == button_continue:
                    menu = False
                if event.button == button_change:
                    menu = False
                    player.kill()
                    pl, pl2 = pl2, pl
                    player = MyCar(pl)
                if event.button == button_restart:
                    menu = False
                    cls = 0
                    meters = 0
                    player.rect.y = h // 2
                    for car in cars:
                        car.kill()

    # обработка завершения игры при проигрыше
    while close:
        pygame.mixer.music.stop()
        # если текущий рекорд был сброшен, выводим сообщение об этом
        if rst:
            reset = f_end.render(f'The record has been reset', True, (0, 0, 0))
            r = reset.get_rect(center=(w / 2, h / 2 + 250))
            screen.blit(reset, r)
        # выводим сообщение о проигрыше и результат (количество метров)
        r1 = game_over.get_rect(center=(w / 2, h / 2 - 200))
        r2 = res.get_rect(center=(w/2, h / 2 - 100))
        screen.blit(game_over, r1)
        screen.blit(res, r2)
        # если установлен новый рекорд, выводим сообщение об этом
        if win:
            r3 = wn.get_rect(center=(w / 2, h / 2))
            screen.blit(wn, r3)

        # кнопка для того, чтобы начать игру заново
        button_restart = Button((w / 2, h / 2 + 100), 300, 125, 'images/button.png', 'RESTART')
        button_restart.draw(screen)

        # кнопка для того, чтобы обнулить рекорд
        button_reset = Button((w / 2, h / 2 + 200), 320, 125, 'images/button.png', 'RESET THE RECORD')
        button_reset.draw(screen)

        pygame.display.update()
        button_restart.press_button()
        button_reset.press_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = False
                run = False
            # обработка нажатия на кнопки
            if event.type == pygame.USEREVENT:
                if event.button == button_restart:
                    pygame.mixer.music.play(-1)
                    close = False
                    cls = 0
                    meters = 0
                if event.button == button_reset:
                    # сброс текущего рекорда
                    rst = True
                    # создаём новый файл с нулевым рекордом
                    f_records = open('records.txt', 'w+')
                    f_records.write('0\n')
                    f_records.close()

    if not run:
        break

    # игра завершается при пяти столкновениях
    if cls == 5:
        res = f_end.render(f'YOUR RESULT: {meters} M', True, (0, 0, 0))
        wn = f_end.render(f"This is a new record!", True, (0, 0, 0))
        close = True

        # проверка на рекорд, заполнение файла
        f_records = open('records.txt', 'r+')
        records = f_records.readlines()
        record = max(map(int, records))
        win = record < meters
        f_records.write(str(meters) + '\n')
        f_records.close()

    # цикл для обработки событий в игре
    for event in pygame.event.get():

        # обработка закрытия игрового окна
        if event.type == pygame.QUIT:
            run = False

        # при нажатии на пробел игра приостанавливается, появляется меню
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            menu = True

        # каждые 300 миллисекунд появляется новая машинка
        if event.type == NEW_CAR:
            Car(random.randint(10, h), CARS_SURF[random.randint(0, 1)], cars)

        # каждые полсекунды мы проезжаем 10 метров, то есть увеличиваем нашу дистанцию
        if event.type == DISTANCE:
            meters += 10

    # отображаем все машинки из группы cars
    all_cars.draw(screen)

    # обновляем экран и задаём FPS (частота смены кадров)
    pygame.display.update()
    clock.tick(60)

    # обработка столкновения с игрока с другими машинами
    if pygame.sprite.spritecollide(player, cars, True):
        cls += 1

    # применяем метод для перемещения всех спрайтов-машин
    all_cars.update()

# закрываем основное игровое окно
pygame.quit()
