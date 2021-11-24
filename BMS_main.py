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
#создание окна
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
root.title('"Болванка" с физикой "скатывания" с учетом всех сил. Зеленый участок - ускоряющий')
#создание основного окна
c_frame = tk.Frame(root)
c_frame.place(x = 0, y = 0, width = window_width + 4, height = window_height + 5)
main_screen = tk.Canvas(c_frame, width = window_width, height = window_height, bg = 'white')
main_screen.pack(fill = tk.BOTH, expand = 1)

#создание идентификаторов объектов на экране
#участки траектории
lines_id=[]
#точки траектории
points_id=[]

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
    return int(x * max_x / window_width)

def inv_scale_y(y, max_y):
    '''
    функция масштабирует экранную координату y в физическую
    '''
    return int(window_height - y) * max_y / window_height

def init_surface(screen, surface, max_x, max_y):
    '''
    Функция инициализирует графическое изображение поверхности на экране
    '''
    global points_id, lines_id
    for i in range(len(surface.points)):
        #перевод координат точек в экранные
        x = scale_x(surface.points[i].x, max_x) 
        y = scale_y(surface.points[i].y, max_y)
        color = surface.points[i].color
        if i < len(surface.points) - 1:
        #добавление линий в список их изображений на экране 
            lines_id.append(screen.create_line(x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y), fill = color, activefill = 'red', width = 2))
        #добавление точек в список их изображений на экране точки добавляются после линий, чтобы 
        points_id.append(screen.create_oval(x - 3,y - 3,x + 3, y + 3, fill = color, activefill = 'red'))        

def init_ball(screen, ball, max_x, max_y):
    '''
    Функция инициализирует тело, как графический объект на основном экране
    '''
    global ball_id
    x = scale_x(ball.x, max_x)
    y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    color = ball.color
    ball_id = screen.create_oval(x - r, y - r, x + r, y + r, fill = color, activefill = 'red')
    
def redraw_ball(screen, ball, max_x, max_y):
    '''
    Функция перерисовывает тело в новом месте
    '''
    x = scale_x(ball.x, max_x)
    y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    screen.coords(ball_id, x - r, y - r, x + r, y + r)


   

ball = bod.body(1, 340/100, 370/100, 0, 0, 10/100, 'blue')
main_surf = surf.surface()
start = False
pause = False



def scale_ball_x(value):
    global ball
    if not start:
        ball.x = float(value)
        redraw_ball(main_screen, ball, max_ox, max_oy)
def scale_ball_y(value):
    global ball
    if not start:
        ball.y = float(value)
        redraw_ball(main_screen, ball, max_ox, max_oy)

#создание панели управления
frame_right = tk.LabelFrame(root, text = 'Панель управления')
frame_right.place(x = window_width + 5, y = 0, width = 800 - window_width - 5, height = 600)


body_frame = tk.LabelFrame(frame_right, text = 'Настройки тела')
body_frame.pack(side = 'top', fill = tk.X)
#масса
#m_lbl = tk.Label(body_frame, text = 'Масса') 
#m_lbl.pack(side = 'top')
#m_ent = tk.Entry(body_frame)
#m_ent.pack(side = 'top')
#m_ent.insert(0, str(ball.m))
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

mod_frame = tk.LabelFrame(frame_right, text = 'Управление')
mod_frame.pack(side = 'bottom')

# кнопки управления
# старт
def start_click():
    global start, pause
    x_sc.config(state = tk.DISABLED, troughcolor = "grey")
    y_sc.config(state = tk.DISABLED, troughcolor = "grey")
    pause = False
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    ball.Vx = 0
    ball.Vy = 0
    start = True

start_btn = tk.Button(mod_frame, text = "Старт", command = start_click)
start_btn.pack(side = 'left')

# пауза
def pause_click():
    global pause
    if start:
        pause = not pause

pause_btn = tk.Button(mod_frame, text = "Пауза", command = pause_click)
pause_btn.pack(side = 'left')

# стоп
def stop_click():
    global start, pause
    x_sc.config(state = tk.ACTIVE, troughcolor = "blue")
    y_sc.config(state = tk.ACTIVE, troughcolor = "blue")    
    pause = True
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    redraw_ball(main_screen, ball, max_ox, max_oy)
    ball.Vx = 0
    ball.Vy = 0
    start = False

stop_btn = tk.Button(mod_frame, text = "Стоп", command = stop_click)
stop_btn.pack(side = 'left')


def new_sim(event=''):
    # создание траектории
    main_surf.addpoint(surf.point(5/100, 350/100, 0.2, 'black'))
    main_surf.addpoint(surf.point(100/100, 250/100, -1, 'green')) #участок с отрицательным трением - ускоряет тело
    main_surf.addpoint(surf.point(150/100, 250/100, 0.1, 'blue'))
    main_surf.addpoint(surf.point(200/100, 280/100, 0.1, 'blue'))
    main_surf.addpoint(surf.point(350/100, 300/100, 0.1, 'gray'))
    main_surf.addpoint(surf.point(400/100, 150/100, 0.1, 'gray'))
    main_surf.addpoint(surf.point(480/100, 120/100, 0.1, 'gray'))
    main_surf.addpoint(surf.point(580/100, 3/100, 0.1, 'green'))

    
    main_screen.create_rectangle(0, 0, window_width, window_height)
    init_surface(main_screen, main_surf, max_ox, max_oy)
    init_ball(main_screen, ball, max_ox, max_oy)
    while main_surf:
        if start and not pause:
            model.move_body(ball, main_surf, 9.8, 0.02, max_ox)
            redraw_ball(main_screen, ball, max_ox, max_oy)
        
        main_screen.update() #обновление игрового поля
        time.sleep(0.02) #пауза
        


new_sim()
root.mainloop()



