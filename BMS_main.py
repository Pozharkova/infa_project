# coding: utf-8
# license: GPLv3

import BMS_surface as surf
import BMS_body as bod
import BMS_io as bio
import BMS_model as model
from BMS_vis import *
import tkinter as tk
import tkinter.ttk as ttk
import math
import time

# физическая ширина и высота основного экрана в метрах
max_ox = 6
max_oy = 4

# создание окна
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
root.title('Придумать название')
# создание основного окна
c_frame = tk.Frame(root)
c_frame.place(x=0, y=0, width=window_width + 4, height=window_height + 5)
main_screen = tk.Canvas(c_frame, width=window_width, height=window_height, bg='white')
main_screen.pack(fill=tk.BOTH, expand=1)
image = tk.PhotoImage(file='pupa.png')
start_image = tk.PhotoImage(file='start.png')
pause_image = tk.PhotoImage(file='pause.png')
stop_image = tk.PhotoImage(file='stop.png')
step_image = tk.PhotoImage(file='step.png')
reset_image = tk.PhotoImage(file='reset.png')

# создание идентификаторов объектов на экране
# участки траектории
lines_id = []
backs_id = []
# точки траектории
points_id = []
# Векторы на основном экране
vecs = []

# Массив мишеней
targets = []
targets_id = []

# глаза пупы
eyes = []
eyes_id = []

# имена файлов с уровнями
file_names = []
# названия уровней
level_names = []

# Тело
ball = bod.body(0.1, 20 / 100, 370 / 100, 0, 0, 10 / 100, 'blue')
# Глаза
eyes = [bod.Pupa_eye(2.35, 3.12, 0.1, 0.22), bod.Pupa_eye(3.29, 3.03, 0.1, 0.22)]
# Поверхность
main_surf = surf.surface()
# Логические переменные
# Запуск моделирования
start = False
# Пауза
pause = False
# Пошаговое моделирование
steping = False
# Режим перемещения точки поверхности
moving = False
# Индекс перемещаемой точки
pnum = 0
# Период обновления экрана
dtime = 0.02
# Количество шагов моделирования за один период обновления экрана
time_scale = 100
# Суммарное время моделирования
ctime = 0
# Время, за которое поражены все цели
tdone = 0
# Максимальная скорость тела
vmax = 0
# Пройденное телом расстояние
S = 0


def init_game(filename, ball, vecs, points_id, lines_id, backs_id, targets_id, eyes_id):
    '''
    Инициализация игры
    '''
    # очистка экарана и всех массивов
    main_screen.delete('all')
    main_surf.points.clear()
    points_id.clear()
    lines_id.clear()
    backs_id.clear()
    targets.clear()
    targets_id.clear()
    eyes_id.clear()
    vecs.clear()
    # Вывод изображения Пупы
    main_screen.create_image(0, 0, image=image, anchor=tk.NW)
    # загрузка
    bio.read_level(filename, ball, main_surf, targets)

    # Вычисление начальных сил и скоростей
    model.move_body(ball, main_surf, 9.8, 0, max_ox)

    # инициализация всех графических объектов
    init_eyes(main_screen, eyes, eyes_id, max_ox, max_oy)
    init_targets(main_screen, targets, targets_id, max_ox, max_oy)
    init_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
    init_ball(main_screen, ball, vecs, max_ox, max_oy)

    # рисование глаз Пупы
    for eye in eyes:
        eye.find_XY(ball.x, ball.y)
    redraw_eyes(main_screen, eyes, eyes_id, max_ox, max_oy)


def scale_ball_x(value):
    '''
    Перемещение тела по оси Х с использованием шкалы на панели управления
    '''
    global ball
    if not start:
        ball.x = float(value)
        for eye in eyes:
            eye.find_XY(ball.x, ball.y)
        redraw_eyes(main_screen, eyes, eyes_id, max_ox, max_oy)
        redraw_ball(main_screen, ball, vecs, max_ox, max_oy)


def scale_ball_y(value):
    '''
    Перемещение тела по оси У с использованием шкалы на панели управления
    '''
    global ball
    if not start:
        ball.y = float(value)
        for eye in eyes:
            eye.find_XY(ball.x, ball.y)
        redraw_eyes(main_screen, eyes, eyes_id, max_ox, max_oy)
        redraw_ball(main_screen, ball, vecs, max_ox, max_oy)


def scale_kf(value):
    '''
    Настройка коэффициента трения участка поверхности с использованием шкалы на панели управления
    '''
    global main_surf
    if not start:
        main_surf.points[pnum].friction = float(value)
        full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)


# создание панели управления
frame_right = tk.LabelFrame(root, text='Панель управления')
frame_right.place(x=window_width + 5, y=0, width=800 - window_width - 5, height=600)

body_frame = tk.LabelFrame(frame_right, text='Настройки тела')
body_frame.pack(side='top', fill=tk.X)

# координаты
x_lbl = tk.Label(body_frame, text='Х')
x_lbl.pack(side='top')
x_sc = tk.Scale(body_frame, orient='horizontal', from_=2 * ball.r, to=max_ox - ball.r, resolution=0.1,
                command=scale_ball_x, troughcolor="blue")
x_sc.set(ball.x)
x_sc.pack(side='top', fill=tk.X)

y_lbl = tk.Label(body_frame, text='Y')
y_lbl.pack(side='top')
y_sc = tk.Scale(body_frame, orient='horizontal', from_=ball.r, to=max_oy - 2 * ball.r, resolution=0.1,
                command=scale_ball_y, troughcolor="blue")
y_sc.set(ball.y)
y_sc.pack(side='top', fill=tk.X)

line_frame = tk.LabelFrame(frame_right, text='Настройки участка поверхности')
line_frame.pack(side='top', fill=tk.X)

# Коэффициент трения
kf_lbl = tk.Label(line_frame, text='Коэффициент трения')
kf_lbl.pack(side='top')
kf_sc = tk.Scale(line_frame, orient='horizontal', state=tk.DISABLED, from_=-1, to=1, resolution=0.1, command=scale_kf,
                 troughcolor="grey")
kf_sc.set(0)
kf_sc.pack(side='top', fill=tk.X)


# кнопки управления
# старт
def start_click():
    '''
    Запуск движение тела при нажатии на кнопку Старт
    '''
    global start, pause, steping, ctime, vmax, S, tdone
    # отключение на время моделирования шкал настройки положения тела
    x_sc.config(state=tk.DISABLED, troughcolor="grey")
    y_sc.config(state=tk.DISABLED, troughcolor="grey")
    kf_sc.config(state=tk.DISABLED, troughcolor="grey")
    full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
    pause = False
    # начальные условия
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    ball.Vx = 0
    ball.Vy = 0
    vmax = 0
    tdone = 0
    S = 0
    for i in range(len(targets)):
        targets[i].active = False
    redraw_targets(main_screen, targets, targets_id, max_ox, max_oy)
    start = True
    steping = False
    ctime = 0


# пауза
def pause_click():
    '''
    Пауза процесса моделирования движения тела
    '''
    global pause
    if start:
        pause = not pause
        steping = False


# стоп
def stop_click():
    '''
    Остановка процесса моделирования движения тела
    '''
    global start, pause
    # активация шкал управления начальным положением тела
    x_sc.config(state=tk.ACTIVE, troughcolor="blue")
    y_sc.config(state=tk.ACTIVE, troughcolor="blue")

    pause = True
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    ball.xt = ball.x
    ball.yt = ball.y
    redraw_ball(main_screen, ball, vecs, max_ox, max_oy)
    ball.Vx = 0
    ball.Vy = 0
    for i in range(len(targets)):
        targets[i].active = False
    for eye in eyes:
        eye.find_XY(ball.x, ball.y)
    redraw_eyes(main_screen, eyes, eyes_id, max_ox, max_oy)
    redraw_targets(main_screen, targets, targets_id, max_ox, max_oy)
    start = False


# пошаговое движение
def step_click():
    '''
    Пошаговое моделирования движения тела
    '''
    global pause, steping, start
    # отключение на время моделирования шкал настройки положения тела
    x_sc.config(state=tk.DISABLED, troughcolor="grey")
    y_sc.config(state=tk.DISABLED, troughcolor="grey")
    kf_sc.config(state=tk.DISABLED, troughcolor="grey")
    full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
    start = True
    steping = True
    pause = False


lvl_frame = tk.LabelFrame(frame_right, text='Управление уровнями')
lvl_frame.pack(side='top', fill=tk.X)

# Управление уровнями
lvl_lbl = tk.Label(lvl_frame, text='Выбор уровня')
lvl_lbl.pack(side='top')
# загрузка названий уровней
bio.find_levels(file_names, level_names)
lvl_combo = ttk.Combobox(lvl_frame, values=level_names)
lvl_combo.pack(side='top')
lvl_combo.current(0)


# сброс
def esc_click():
    '''
    Сброс игры к начальному состоянию
    '''
    global vecs, points_id, lines_id, backs_id, targets_id, eyes_id
    if lvl_combo.current() >= 0:
        init_game(file_names[lvl_combo.current()], ball, vecs, points_id, lines_id, backs_id, targets_id, eyes_id)
        x_sc.set(ball.x)
        y_sc.set(ball.y)
        stop_click()


lvl_btn = tk.Button(lvl_frame, text='Загрузить уровень', command=esc_click)
lvl_btn.pack(side='top')

mod_frame = tk.LabelFrame(frame_right, text='Управление', width=150, height=50)
mod_frame.pack(side='top', fill=tk.BOTH)

# кнопки управления моделированием движения
start_btn = tk.Button(mod_frame, image=start_image, command=start_click)
start_btn.place(x=15, y=0, width=30, height=30, anchor='nw')
pause_btn = tk.Button(mod_frame, image=pause_image, command=pause_click)
pause_btn.place(x=45, y=0, width=30, height=30, anchor='nw')
stop_btn = tk.Button(mod_frame, image=stop_image, command=stop_click)
stop_btn.place(x=75, y=0, width=30, height=30, anchor='nw')
fstep_btn = tk.Button(mod_frame, image=step_image, command=step_click)
fstep_btn.place(x=105, y=0, width=30, height=30, anchor='nw')
esc_btn = tk.Button(mod_frame, image=reset_image, command=esc_click)
esc_btn.place(x=135, y=0, width=30, height=30, anchor='nw')

# создание информационной панели
frame_bottom = tk.LabelFrame(root, text='Статистика', bg='black', fg='#5de100')
frame_bottom.place(x=0, y=window_height + 5, width=window_width + 4, height=600 - window_height - 5)

time_frame = tk.LabelFrame(frame_bottom, text='Время/Цели', bg='black', fg='#5de100')
time_frame.place(x=0, y=0, width=200, height=600 - window_height - 5)

velocity_frame = tk.LabelFrame(frame_bottom, text='Расстояния/Скорости', bg='black', fg='#5de100')
velocity_frame.place(x=200, y=0, width=200, height=600 - window_height - 5)

force_frame = tk.LabelFrame(frame_bottom, text='Модули сил', bg='black', fg='#5de100')
force_frame.place(x=400, y=0, width=200, height=600 - window_height - 5)

# Время
ctime_lbl = tk.Label(time_frame, text='Текущее время: 000.00 с', justify='left', anchor='w', bg='black', fg='#5de100')
ctime_lbl.place(x=0, y=0, width=196, height=20)
btime_lbl = tk.Label(time_frame, text='Время прохождения: 000.00 с', justify='left', anchor='w', bg='black',
                     fg='#5de100')
btime_lbl.place(x=0, y=20, width=196, height=20)
cgoals_lbl = tk.Label(time_frame, text='Целей: 0 из 10', justify='left', anchor='w', bg='black', fg='#5de100')
cgoals_lbl.place(x=0, y=40, width=196, height=20)

# Модули скоростей, координаты
cx_lbl = tk.Label(velocity_frame, text='X: 0.00 м', justify='left', anchor='w', bg='black', fg='#5de100')
cx_lbl.place(x=0, y=0, width=180, height=20)
cy_lbl = tk.Label(velocity_frame, text='Y: 0.00 м', justify='left', anchor='w', bg='black', fg='#5de100')
cy_lbl.place(x=0, y=20, width=180, height=20)
cs_lbl = tk.Label(velocity_frame, text='S: 00.00 м', justify='left', anchor='w', bg='black', fg='#5de100')
cs_lbl.place(x=0, y=40, width=180, height=20)
cv_lbl = tk.Label(velocity_frame, text='V: 000.00 м/с', justify='left', anchor='w', bg='black', fg='#5de100')
cv_lbl.place(x=0, y=60, width=180, height=20)
maxv_lbl = tk.Label(velocity_frame, text='Vmax: 000.00 м/с', justify='left', anchor='w', bg='black', fg='#5de100')
maxv_lbl.place(x=0, y=80, width=180, height=20)

# Модули сил
cmg_lbl = tk.Label(force_frame, text='mg: 00.00 Н', bg='black', justify='left', anchor='w', fg='#5de100')
cmg_lbl.place(x=0, y=0, width=195, height=20)
cN_lbl = tk.Label(force_frame, text='N: 00.00 Н', bg='blue', justify='left', anchor='w', fg='#5de100')
cN_lbl.place(x=0, y=20, width=195, height=20)
cFtp_lbl = tk.Label(force_frame, text='Fтр: 00.00 Н', bg='red', justify='left', anchor='w', fg='#5de100')
cFtp_lbl.place(x=0, y=40, width=195, height=20)
cF_lbl = tk.Label(force_frame, text='R: 00.00 Н', bg='black', justify='left', anchor='w', fg='#5de100')
cF_lbl.place(x=0, y=60, width=195, height=20)


def show_stats(ball):
    '''
    Вывод основной статистики по игре
    '''
    global vmax, S, tdone
    tcount = 0
    # подсчет количества пораженных целей
    for targ in targets:
        if targ.active:
            tcount += 1
    if tcount == len(targets) and tdone == 0:
        tdone = ctime
    # Расчет максимальной скорости
    if vmax < (ball.Vx ** 2 + ball.Vy ** 2) ** 0.5:
        vmax = (ball.Vx ** 2 + ball.Vy ** 2) ** 0.5

    # Рассчет пройденного расстояния
    S += dtime * (ball.Vx ** 2 + ball.Vy ** 2) ** 0.5

    ctime_lbl.config(text='Текущее время: ' + str(round(ctime, 2)) + ' с')
    if tdone == 0:
        btime_lbl.config(text='Время прохождения: ' + str(round(ctime, 2)) + ' с', bg='black')
    else:
        btime_lbl.config(text='Время прохождения: ' + str(round(tdone, 2)) + ' с', bg='red')
    cgoals_lbl.config(text='Целей: ' + str(tcount) + ' из ' + str(len(targets)))
    cv_lbl.config(text='V: ' + str(round((ball.Vx ** 2 + ball.Vy ** 2) ** 0.5, 2)) + ' м/с')
    maxv_lbl.config(text='Vmax: ' + str(round(vmax, 2)) + ' м/с')
    cx_lbl.config(text='X: ' + str(round(ball.x, 2)) + ' м')
    cy_lbl.config(text='Y: ' + str(round(ball.y, 2)) + ' м')
    cs_lbl.config(text='S: ' + str(round(S, 2)) + ' м')
    cmg_lbl.config(text='mg: ' + str(round(abs(ball.mg), 2)) + ' H')
    cN_lbl.config(text='N: ' + str(round((ball.Nx ** 2 + ball.Ny ** 2) ** 0.5, 2)) + ' H')
    cFtp_lbl.config(text='Fтр: ' + str(round((ball.Ftp_x ** 2 + ball.Ftp_y ** 2) ** 0.5, 2)) + ' H')
    cF_lbl.config(text='R: ' + str(round((ball.Fx ** 2 + ball.Fy ** 2) ** 0.5, 2)) + ' H')


# Редактирование вершин поверхности и линейных участков

def takepoint(event):
    '''
    Выбор вершины или линии поверхности при нажатии левой клавиши мыши
    '''
    global pnum, moving
    # выбор возможен только вне моделирования
    if not start:
        # проверка выбора объекта на экране
        obj = main_screen.find_withtag(tk.CURRENT)
        # если объект выбран, определяется его тип
        if obj:
            obj = obj[0]
            # если объект линия, запускается редактирование линии
            if obj in lines_id:
                pnum = lines_id.index(obj)
                full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
                main_screen.itemconfig(obj, fill='red')
                kf_sc.config(state=tk.ACTIVE, troughcolor="blue")
                kf_sc.set(main_surf.points[pnum].friction)
            # если объект вершина, то запускается перемещение вершины
            elif obj in points_id:
                # определение вершины
                full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
                kf_sc.config(state=tk.DISABLED, troughcolor="grey")
                pnum = points_id.index(obj)
                # разрешение на перемещение
                moving = True
            # обновление траектории
            else:
                full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
                kf_sc.config(state=tk.DISABLED, troughcolor="grey")
        else:
            full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
            kf_sc.config(state=tk.DISABLED, troughcolor="grey")


def movepoint(event):
    '''
    Перемещение вершины поверхности при движении указателя мыши
    '''
    # Если разрешено перемещение, то вершина перемещается за указателем мыши.
    if moving:
        main_screen.coords(points_id[pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
        # Перерисовка поверхности (без изменения физических координат)
        redraw_surface(main_screen, points_id, lines_id, backs_id)


def droppoint(event):
    '''
    Окончание перемещения вершины поверхности при отпускании левой клавиши мыши
    '''
    global pnum, moving, main_surf
    if moving:
        main_screen.coords(points_id[pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
        # определение физических координат вершины
        nx = inv_scale_x(event.x, max_ox)
        ny = inv_scale_y(event.y, max_oy)
        # проверка нарушения неубывания координат следующих друг за другом вершин по оси Х
        # также расстояние по оси Х между двумя вершин не может быть менее диаметра тела
        if pnum > 0 and pnum < len(points_id) - 1:
            if nx < main_surf.points[pnum - 1].x + 2 * ball.r:
                nx = main_surf.points[pnum - 1].x + 2 * ball.r
            if nx > main_surf.points[pnum + 1].x - 2 * ball.r:
                nx = main_surf.points[pnum + 1].x - 2 * ball.r

        if nx < 0:
            nx = 0.1
        if nx > max_ox:
            nx = max_ox - 0.1
        if ny < 0:
            ny = 0.1
        if ny > max_oy:
            ny = max_oy - 0.1
        # обновление физических координат
        main_surf.points[pnum].x = nx
        main_surf.points[pnum].y = ny
        # полная перерисовка поверхности с учетом физических координат
        full_redraw_surface(main_screen, main_surf, points_id, lines_id, backs_id, max_ox, max_oy)
        moving = False


main_screen.bind('<Button-1>', takepoint)
main_screen.bind('<ButtonRelease-1>', droppoint)
main_screen.bind('<Motion>', movepoint)


def new_sim(event=''):
    '''
    Основной игровой процесс: редактирование параметров тела и поверхности, моделирование
    '''
    global start, pause, steping, lines_id, ctime
    while main_surf:
        if (start and not pause) or steping:
            # моделирование движения с временным шагом в time_scale меньшим, чем период обновления экрана
            for j in range(time_scale):
                model.move_body(ball, main_surf, 9.8, dtime / time_scale, max_ox)
                for i in range(len(targets)):
                    model.check_hit(ball, targets[i])
            for eye in eyes:
                eye.find_XY(ball.x, ball.y)
            redraw_eyes(main_screen, eyes, eyes_id, max_ox, max_oy)
            redraw_targets(main_screen, targets, targets_id, max_ox, max_oy)
            redraw_ball(main_screen, ball, vecs, max_ox, max_oy)
            ctime += dtime
            show_stats(ball)
            if steping:
                pause = True
                steping = False
                start = True

        main_screen.update()  # обновление игрового поля
        time.sleep(abs(dtime))  # пауза


# init_game('lvl1.txt', ball, vecs, points_id, lines_id, backs_id, targets_id, eyes_id)
esc_click()
show_stats(ball)
new_sim()
root.mainloop()



