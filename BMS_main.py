# coding: utf-8
# license: GPLv3

import BMS_surface as surf
import BMS_body as bod
import BMS_model as model
import tkinter as tk
import math
import time

#ширина и высота основного экрана
window_width = 600
window_height = 400
# физическая ширина и высота основного экрана в метрах
max_ox = 6
max_oy = 4
#цвета текстур
wood_bg = '#a26c47'
wood_fg = '#8d4312'
ice_bg = '#80a5f9'
ice_fg = '#3d62b6'
wind_bg = '#ff4703'
wind_fg = 'yellow'
#толщина участков поверхности
line_width = 30
#создание окна
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
root.title('Варианты интерфейса')
#создание основного окна
c_frame = tk.Frame(root)
c_frame.place(x = 0, y = 0, width = window_width + 4, height = window_height + 5)
main_screen = tk.Canvas(c_frame, width = window_width, height = window_height, bg = 'white')
main_screen.pack(fill = tk.BOTH, expand = 1)
image = tk.PhotoImage(file='pupa.png')
main_screen.create_image(0, 0, image = image, anchor = tk.NW)
#создание идентификаторов объектов на экране
#участки траектории
lines_id=[]
backs_id=[]
#точки траектории
points_id=[]
vecs=[]

#Массив мишеней
targets = []
targets_id = []

#глаза пупы
eyes = []
eyes_id=[]



def scale_x(x, max_x):
    '''
    функция масштабирует физическую координату х в экранную
    '''
    return int(window_width * x / max_x)

def scale_y(y, max_y):
    '''
    функция масштабирует физическую координату y в экранную
    '''
    return int(window_height - window_height * y / max_y)

def inv_scale_x(x, max_x):
    '''
    функция масштабирует экранную координату х в физическую
    '''
    return x * max_x / window_width

def inv_scale_y(y, max_y):
    '''
    функция масштабирует экранную координату y в физическую
    '''
    return (window_height - y) * max_y / window_height

def init_surface(screen, surface, max_x, max_y):
    '''
    Функция инициализирует графическое изображение поверхности на экране
    '''
    global points_id, lines_id
    for i in range(len(surface.points)):
        #перевод координат точек в экранные
        x = scale_x(surface.points[i].x, max_x) 
        y = scale_y(surface.points[i].y, max_y)
        if surface.points[i].friction > 0:
            surface.points[i].color = wood_bg
            texture = '@wood.xbm'
            f_color = wood_fg
        if surface.points[i].friction < 0:
            surface.points[i].color = wind_bg
            texture = '@wind.xbm'
            f_color = wind_fg
        if surface.points[i].friction == 0:
            surface.points[i].color = ice_bg
            texture = '@ice.xbm'
            f_color = ice_fg
        color = surface.points[i].color
        if i < len(surface.points) - 1:
        #добавление линий в список их изображений на экране 
            backs_id.append(screen.create_polygon(x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y),
                                                  scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y) + line_width, x, y + + line_width, 
                                                  fill = color, width = 1))
            
            lines_id.append(screen.create_polygon(x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y),
                                                  scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y) + + line_width, x, y + + line_width, 
                                                  fill = f_color, outline = color, stipple = texture, activefill = 'red', width = 2, tag = 'edit'))
            
        #добавление точек в список их изображений на экране точки добавляются после линий
        points_id.append(screen.create_oval(x - 3,y - 3,x + 3, y + 3, fill = color, activefill = 'red'))        

def redraw_surface(screen):
    '''
    Функция перерисовывает графическое изображение поверхности на экране при редактировании траектории (без использования физических координат)
    '''
    global points_id, lines_id
    for i in range(len(points_id)):
        if i < len(points_id) - 1:
            px1, py1, px2, py2 = screen.coords(points_id[i])
            lx1 = (px1 + px2) // 2
            ly1 = (py1 + py2) // 2
            px1, py1, px2, py2 = screen.coords(points_id[i + 1]) 
            lx2 = (px1 + px2) // 2
            ly2 = (py1 + py2) // 2
            screen.coords(backs_id[i], lx1, ly1, lx2, ly2, lx2, ly2 + line_width, lx1, ly1 + line_width)
            screen.coords(lines_id[i], lx1, ly1, lx2, ly2, lx2, ly2 + line_width, lx1, ly1 + line_width)

def full_redraw_surface(screen, surface, max_x, max_y):
    '''
    Функция перерисовывает графическое изображение поверхности на экране c использованием физических координат
    '''
    global points_id, lines_id
    for i in range(len(surface.points)):
        #перевод координат точек в экранные
        x = scale_x(surface.points[i].x, max_x) 
        y = scale_y(surface.points[i].y, max_y)
        if surface.points[i].friction > 0:
            surface.points[i].color = wood_bg
            texture = '@wood.xbm'
            f_color = wood_fg
        if surface.points[i].friction < 0:
            surface.points[i].color = wind_bg
            texture = '@wind.xbm'
            f_color = wind_fg
        if surface.points[i].friction == 0:
            surface.points[i].color = ice_bg
            texture = '@ice.xbm'
            f_color = ice_fg
        color = surface.points[i].color
        if i < len(surface.points) - 1:
        #рисование линий на экране
            screen.itemconfig(backs_id[i], fill = color)
            screen.itemconfig(lines_id[i], fill = f_color, stipple = texture, outline = color)
            screen.coords(backs_id[i], x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y),
                          scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y) + line_width, x, y + line_width)            
            screen.coords(lines_id[i], x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y),
                          scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y) + line_width, x, y + line_width)
        #на экране точки добавляются после линий
        screen.itemconfig(points_id[i], fill = color)
        screen.coords(points_id[i], x - 3,y - 3,x + 3, y + 3)



def init_ball(screen, ball, max_x, max_y, surface):
    '''
    Функция инициализирует тело, как графический объект на основном экране
    '''
    global ball_id
    xc = x = scale_x(ball.x, max_x)
    yc = y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    color = ball.color
    ball_id = screen.create_oval(x - r, y - r, x + r, y + r, fill = color)
    '''# визуализация точки касания
    x0 = ball.x
    y0 = ball.y
    r = ball.r
    xt = ball.xt
    yt = ball.yt
    

    x = scale_x(xt, max_x)
    y = scale_y(yt, max_y)
    ball.id = screen.create_oval(x - 3, y - 3, x + 3, y + 3, fill = 'red')'''

    x = scale_x(ball.Fx + ball.x, max_x)
    y = scale_y(ball.Fy + ball.y, max_y)
    vecs.append(screen.create_line(xc, yc, x, y, fill = 'black', arrow = tk.LAST))

    x = xc
    y = scale_y(ball.mg + ball.y, max_y)
    vecs.append(screen.create_line(xc, yc, x, y, fill = 'black', arrow = tk.LAST))

    
    x = scale_x(ball.Nx + ball.x, max_x)
    y = scale_y(ball.Ny + ball.y, max_y)
    vecs.append(screen.create_line(xc, yc, x, y, fill = 'blue', arrow = tk.LAST))
    
    x = scale_x(ball.Ftp_x + ball.x, max_x)
    y = scale_y(ball.Ftp_y + ball.y, max_y)
    vecs.append(screen.create_line(xc, yc, x, y, fill = 'red', arrow = tk.LAST))   


    
def redraw_ball(screen, ball, max_x, max_y, surface):
    '''
    Функция перерисовывает тело в новом месте
    '''
    xc = x = scale_x(ball.x, max_x)
    yc = y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    screen.coords(ball_id, x - r, y - r, x + r, y + r)
    '''# визуализация точки касания
    x0 = ball.x
    y0 = ball.y
    r = ball.r
    xt = ball.xt
    yt = ball.yt
    x = scale_x(xt, max_x)
    y = scale_y(yt, max_y)   
    screen.coords(ball.id, x - 3, y - 3, x + 3, y + 3)'''

    x = scale_x(ball.Fx + ball.x, max_x)
    y = scale_y(ball.Fy + ball.y, max_y)
    screen.coords(vecs[0], xc, yc,  x, y)

    
    x = xc
    y = scale_y(ball.mg + ball.y, max_y)
    screen.coords(vecs[1], xc, yc,  x, y)
    
    x = scale_x(ball.Nx + ball.x, max_x)
    y = scale_y(ball.Ny + ball.y, max_y)
    screen.coords(vecs[2], xc, yc,  x, y)

        
    x = scale_x(ball.Ftp_x + ball.x, max_x)
    y = scale_y(ball.Ftp_y + ball.y, max_y)
    screen.coords(vecs[3], xc, yc, x, y)

def init_eyes(screen, eyes, max_x, max_y):
    '''
    Функция инициализирует глаз, как графический объект на основном экране
    '''
    for eye in eyes: 
        x = scale_x(eye.X, max_x)
        y = scale_y(eye.Y, max_y)
        r = scale_x(eye.r, max_x)
       
        eyes_id.append(screen.create_oval(x - r, y - r, x + r, y + r, fill = 'black'))
 


    
def redraw_eyes(screen, eyes, max_x, max_y):
    '''
    Функция перерисовывает тело в новом месте
    '''
    for eye in eyes: 
        x = scale_x(eye.X, max_x)
        y = scale_y(eye.Y, max_y)
        r = scale_x(eye.r, max_x)
       
        screen.coords(eyes_id[eyes.index(eye)], x - r, y - r, x + r, y + r) 

def init_targets(screen, targets, max_x, max_y):
    '''
    Функция инициализирует мишени как графические объекты на экране
    '''
    global targets_id
    for i in range(len(targets)):
        x = scale_x(targets[i].x, max_x)
        y = scale_y(targets[i].y, max_y)
        r = scale_x(targets[i].r, max_x)
        color = targets[i].color
        targets_id.append(screen.create_oval(x - r, y - r, x + r, y + r, fill=color, activefill=color))


def redraw_targets(screen, targets, max_x, max_y):
    '''
    Функция перерисовывет мишень
    '''
    for i in range(len(targets)):
        x = scale_x(targets[i].x, max_x)
        y = scale_y(targets[i].y, max_y)
        r = scale_x(targets[i].r, max_x)
        if targets[i].active:
            color = targets[i].active_color
        else:
            color = targets[i].color
        screen.itemconfig(targets_id[i], fill = color)
        screen.coords(targets_id[i], x - r, y - r, x + r, y + r)
 

ball = bod.body(0.1, 20/100, 370/100, 0, 0, 10/100, 'blue')
eyes = [bod.Pupa_eye(2.35, 3.12, 0.1, 0.22), bod.Pupa_eye(3.29, 3.03, 0.1, 0.22)]
main_surf = surf.surface()
start = False
pause = False
moving = False
steping = False
pnum = 0
dtime = 0.02



def scale_ball_x(value):
    '''
    Перемещение тела по оси Х с использованием шкалы на панели управления
    '''
    global ball
    if not start:
        ball.x = float(value)
        for eye in eyes:
            eye.find_XY(ball.x, ball.y)
        redraw_eyes(main_screen, eyes, max_ox, max_oy)        
        redraw_ball(main_screen, ball, max_ox, max_oy, main_surf)

def scale_ball_y(value):
    '''
    Перемещение тела по оси У с использованием шкалы на панели управления
    '''    
    global ball
    if not start:
        ball.y = float(value)
        for eye in eyes:
            eye.find_XY(ball.x, ball.y)
        redraw_eyes(main_screen, eyes, max_ox, max_oy)        
        redraw_ball(main_screen, ball, max_ox, max_oy, main_surf)
        

def scale_kf(value):
    '''
    Настройка коэффициента трения участка поверхности с использованием шкалы на панели управления
    ''' 
    global main_surf
    if not start:
        main_surf.points[pnum].friction = float(value)
        full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
           



#создание панели управления
frame_right = tk.LabelFrame(root, text = 'Панель управления')
frame_right.place(x = window_width + 5, y = 0, width = 800 - window_width - 5, height = 600)


body_frame = tk.LabelFrame(frame_right, text = 'Настройки тела')
body_frame.pack(side = 'top', fill = tk.X)

#координаты
x_lbl = tk.Label(body_frame, text = 'Х') 
x_lbl.pack(side = 'top')
x_sc = tk.Scale(body_frame, orient='horizontal', from_ = 2 * ball.r, to = max_ox - ball.r, resolution = 0.1, command = scale_ball_x, troughcolor = "blue")
x_sc.set(ball.x)
x_sc.pack(side = 'top', fill = tk.X)

y_lbl = tk.Label(body_frame, text = 'Y') 
y_lbl.pack(side = 'top')
y_sc = tk.Scale(body_frame, orient='horizontal', from_ = ball.r, to = max_oy - 2 * ball.r, resolution = 0.1, command = scale_ball_y, troughcolor = "blue")
y_sc.set(ball.y)
y_sc.pack(side = 'top', fill = tk.X)

line_frame = tk.LabelFrame(frame_right, text = 'Настройки участка поверхности')
line_frame.pack(side = 'top', fill = tk.X)

#Коэффициент трения
kf_lbl = tk.Label(line_frame, text = 'Коэффициент трения') 
kf_lbl.pack(side = 'top')
kf_sc = tk.Scale(line_frame, orient='horizontal', state = tk.DISABLED, from_ = -1, to = 1, resolution = 0.1, command = scale_kf, troughcolor = "grey")
kf_sc.set(0)
kf_sc.pack(side = 'top', fill = tk.X)



mod_frame = tk.LabelFrame(frame_right, text = 'Управление')
mod_frame.pack(side = 'bottom')

# кнопки управления
# старт
def start_click():
    '''
    Запуск движение тела при нажатии на кнопку Старт
    '''
    global start, pause, steping
    # отключение на время моделирования шкал настройки положения тела
    x_sc.config(state = tk.DISABLED, troughcolor = "grey")
    y_sc.config(state = tk.DISABLED, troughcolor = "grey")
    kf_sc.config(state = tk.DISABLED, troughcolor = "grey")
    full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
    pause = False
    # начальные условия
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    ball.Vx = 0
    ball.Vy = 0
    for i in range(len(targets)):
        targets[i].active = False
    redraw_targets(main_screen, targets, max_ox, max_oy)    
    start = True
    steping = False



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
    x_sc.config(state = tk.ACTIVE, troughcolor = "blue")
    y_sc.config(state = tk.ACTIVE, troughcolor = "blue")

    pause = True
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    ball.xt = ball.x
    ball.yt = ball.y
    redraw_ball(main_screen, ball, max_ox, max_oy, main_surf)
    ball.Vx = 0
    ball.Vy = 0
    for i in range(len(targets)):
        targets[i].active = False
    for eye in eyes:
        eye.find_XY(ball.x, ball.y)
    redraw_eyes(main_screen, eyes, max_ox, max_oy)      
    redraw_targets(main_screen, targets, max_ox, max_oy) 
    start = False

# пошаговое движение
def step_click():
    '''
    Пошаговое моделирования движения тела
    '''
    global pause, steping, start
    # отключение на время моделирования шкал настройки положения тела
    x_sc.config(state = tk.DISABLED, troughcolor = "grey")
    y_sc.config(state = tk.DISABLED, troughcolor = "grey")
    kf_sc.config(state = tk.DISABLED, troughcolor = "grey")
    full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
    start = True
    steping = True
    pause = False

# кнопки управления моделированием движения
start_btn = tk.Button(mod_frame, text = "Старт", command = start_click)
start_btn.pack(side = 'left')
pause_btn = tk.Button(mod_frame, text = "Пауза", command = pause_click)
pause_btn.pack(side = 'left')
stop_btn = tk.Button(mod_frame, text = "Стоп", command = stop_click)
stop_btn.pack(side = 'left')
fstep_btn = tk.Button(mod_frame, text = "Шаг", command = step_click)
fstep_btn.pack(side = 'left')

# Редактирование вершин поверхности и линейных участков
def takepoint(event):
    '''
    Выбор вершины или линии поверхности при нажатии левой клавиши мыши
    '''
    global pnum, moving
    # выбор возможен только вне моделирования
    if not start:
        #проверка выбора объекта на экране
        obj = main_screen.find_withtag(tk.CURRENT)
        #если объект выбран, определяется его тип
        if obj:
            obj = obj[0]
            #если объект линия, запускается редактирование линии
            if obj in lines_id:
                pnum = lines_id.index(obj)
                full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
                main_screen.itemconfig(obj, fill = 'red')
                kf_sc.config(state = tk.ACTIVE, troughcolor = "blue")
                kf_sc.set(main_surf.points[pnum].friction)
            #если объект вершина, то запускается перемещение вершины
            elif obj in points_id:
                # определение вершины
                full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
                kf_sc.config(state = tk.DISABLED, troughcolor = "grey")                
                pnum = points_id.index(obj)
                #разрешение на перемещение
                moving = True
            #обновление траектории
            else:
                full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
                kf_sc.config(state = tk.DISABLED, troughcolor = "grey")            
        else:
            full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
            kf_sc.config(state = tk.DISABLED, troughcolor = "grey") 
        

def movepoint(event):
    '''
    Перемещение вершины поверхности при движении указателя мыши
    '''
    # Если разрешено перемещение, то вершина перемещается за указателем мыши. 
    if moving:
        main_screen.coords(points_id[pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
        # Перерисовка поверхности (без изменения физических координат)
        redraw_surface(main_screen)
        
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
       #обновление физических координат 
        main_surf.points[pnum].x = nx 
        main_surf.points[pnum].y = ny
        #полная перерисовка поверхности с учетом физических координат
        full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
        moving = False

     
    
    

main_screen.bind('<Button-1>', takepoint)
main_screen.bind('<ButtonRelease-1>', droppoint)
main_screen.bind('<Motion>', movepoint)



def new_sim(event=''):
    global start, pause, steping, lines_id
    # создание траектории
    main_surf.addpoint(surf.point(5/100, 300/100, 0.2, 'grey'))
    main_surf.addpoint(surf.point(100/100, 200/100, -0.4, 'green')) #участок с отрицательным трением - ускоряет тело
    main_surf.addpoint(surf.point(150/100, 200/100, 0.2, 'blue'))
    main_surf.addpoint(surf.point(200/100, 230/100, 0, 'blue'))
    main_surf.addpoint(surf.point(350/100, 250/100, 0.2, 'gray'))
    main_surf.addpoint(surf.point(400/100, 100/100, 0.2, 'gray'))
    main_surf.addpoint(surf.point(480/100, 70/100, 0.2, 'gray'))
    main_surf.addpoint(surf.point(550/100, 3/100, 0.2, 'green'))

    targets.append(bod.Target(5, 2.5, 0.1))
    targets.append(bod.Target(2, 3, 0.1))   
    #main_screen.create_rectangle(0, 0, window_width, window_height)
    init_eyes(main_screen, eyes, max_ox, max_oy)
    for eye in eyes:
        eye.find_XY(ball.x, ball.y)
    redraw_eyes(main_screen, eyes, max_ox, max_oy)
    init_targets(main_screen, targets, max_ox, max_oy)
    init_surface(main_screen, main_surf, max_ox, max_oy)
    init_ball(main_screen, ball, max_ox, max_oy, main_surf)

    
    while main_surf:
        if (start and not pause) or steping:
            model.move_body(ball, main_surf, 9.8, dtime, max_ox)
            for i in range(len(targets)):
                model.check_hit(ball, targets[i])
            for eye in eyes:
                eye.find_XY(ball.x, ball.y)
            redraw_eyes(main_screen, eyes, max_ox, max_oy)
            redraw_targets(main_screen, targets, max_ox, max_oy)    
            redraw_ball(main_screen, ball, max_ox, max_oy, main_surf)
            
            if steping:
                pause = True
                steping = False
                start = True
          
        main_screen.update() #обновление игрового поля
        time.sleep(abs(dtime)) #пауза

new_sim()
root.mainloop()



