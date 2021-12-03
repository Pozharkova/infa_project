# coding: utf-8
# license: GPLv3

#ширина и высота основного экрана
window_width = 600
window_height = 400

#цвета текстур
wood_bg = '#a26c47'
wood_fg = '#8d4312'
ice_bg = '#80a5f9'
ice_fg = '#3d62b6'
wind_bg = '#ff4703'
wind_fg = 'yellow'
#толщина участков поверхности
line_width = 30

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

def init_surface(screen, surface, points_id, lines_id, backs_id, max_x, max_y):
    '''
    Функция инициализирует графическое изображение поверхности на экране
    '''
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
            backs_id.append(screen.create_polygon(x, y, scale_x(surface.points[i + 1].x, max_x), 
                                                  scale_y(surface.points[i + 1].y, max_y),
                                                  scale_x(surface.points[i + 1].x, max_x), 
                                                  scale_y(surface.points[i + 1].y, max_y) + line_width, 
                                                  x, y + line_width, fill = color, width = 1))
            
            lines_id.append(screen.create_polygon(x, y, scale_x(surface.points[i + 1].x, max_x), 
                                                  scale_y(surface.points[i + 1].y, max_y),
                                                  scale_x(surface.points[i + 1].x, max_x), 
                                                  scale_y(surface.points[i + 1].y, max_y) + line_width, 
                                                  x, y + line_width, fill = f_color, outline = color, stipple = texture, activefill = 'red', width = 2, tag = 'edit'))
            
        #добавление точек в список их изображений на экране точки добавляются после линий
        points_id.append(screen.create_oval(x - 3,y - 3,x + 3, y + 3, fill = color, activefill = 'red'))        

def redraw_surface(screen, points_id, lines_id, backs_id):
    '''
    Функция перерисовывает графическое изображение поверхности на экране при редактировании траектории (без использования физических координат)
    '''
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

def full_redraw_surface(screen, surface, points_id, lines_id, backs_id, max_x, max_y):
    '''
    Функция перерисовывает графическое изображение поверхности на экране c использованием физических координат
    '''
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
            screen.coords(backs_id[i], x, y, scale_x(surface.points[i + 1].x, max_x), 
                          scale_y(surface.points[i + 1].y, max_y),
                          scale_x(surface.points[i + 1].x, max_x), 
                          scale_y(surface.points[i + 1].y, max_y) + line_width, x, y + line_width)            
            screen.coords(lines_id[i], x, y, scale_x(surface.points[i + 1].x, max_x), 
                          scale_y(surface.points[i + 1].y, max_y), 
                          scale_x(surface.points[i + 1].x, max_x), 
                          scale_y(surface.points[i + 1].y, max_y) + line_width, x, y + line_width)
        #на экране точки добавляются после линий
        screen.itemconfig(points_id[i], fill = color)
        screen.coords(points_id[i], x - 3,y - 3,x + 3, y + 3)


def init_vec(screen, x0, y0, Mx, My, color, vecs, max_x, max_y):
    '''
    Функция инициализирует вектор, как графический объект на заданном экране
    '''
    xc = scale_x(x0, max_x)
    yc = scale_y(y0, max_y)

    x = scale_x(x0 + Mx, max_x)
    y = scale_y(y0 + My, max_y)
    vecs.append(screen.create_line(xc, yc, x, y, fill = color, arrow = 'last'))

    
def init_force_vecs(screen, ball, vecs, max_x, max_y):
    '''
    Функция инициализирует векторы сил, как графический объект на заданном экране
    '''
    init_vec(screen, ball.x, ball.y, ball.Fx, ball.Fy, 'black', vecs, max_x, max_y)
    init_vec(screen, ball.x, ball.y, 0, ball.mg, 'black', vecs, max_x, max_y)
    init_vec(screen, ball.x, ball.y, ball.Nx, ball.Ny, 'blue', vecs, max_x, max_y)
    init_vec(screen, ball.x, ball.y, ball.Ftp_x, ball.Ftp_y, 'red', vecs, max_x, max_y)
   


def init_ball(screen, ball, vecs, max_x, max_y):
    '''
    Функция инициализирует тело, как графический объект на заданном экране
    '''
    xc = x = scale_x(ball.x, max_x)
    yc = y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    color = ball.color
    ball.id = screen.create_oval(x - r, y - r, x + r, y + r, fill = color)

    init_force_vecs(screen, ball, vecs, max_x, max_y)

def redraw_vec(screen, x0, y0, Mx, My, vec, max_x, max_y):
    '''
    Функция перерисовывает вектор
    '''
    xc = scale_x(x0, max_x)
    yc = scale_y(y0, max_y)

    x = scale_x(x0 + Mx, max_x)
    y = scale_y(y0 + My, max_y)
    screen.coords(vec, xc, yc, x, y)

    
def redraw_force_vecs(screen, ball, vecs, max_x, max_y):
    '''
    Функция перерисовывает векторы сил
    '''
    redraw_vec(screen, ball.x, ball.y, ball.Fx, ball.Fy, vecs[0], max_x, max_y)
    redraw_vec(screen, ball.x, ball.y, 0, ball.mg, vecs[1], max_x, max_y)
    redraw_vec(screen, ball.x, ball.y, ball.Nx, ball.Ny, vecs[2], max_x, max_y)
    redraw_vec(screen, ball.x, ball.y, ball.Ftp_x, ball.Ftp_y, vecs[3], max_x, max_y)
    

def redraw_ball(screen, ball, vecs, max_x, max_y):
    '''
    Функция перерисовывает тело в новом месте
    '''
    xc = x = scale_x(ball.x, max_x)
    yc = y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    screen.coords(ball.id, x - r, y - r, x + r, y + r)

    redraw_force_vecs(screen, ball, vecs, max_x, max_y)

def init_eyes(screen, eyes, eyes_id, max_x, max_y):
    '''
    Функция инициализирует глаз, как графический объект на заданном экране
    '''
    for eye in eyes: 
        x = scale_x(eye.X, max_x)
        y = scale_y(eye.Y, max_y)
        r = scale_x(eye.r, max_x)
       
        eyes_id.append(screen.create_oval(x - r, y - r, x + r, y + r, fill = 'black'))
 


    
def redraw_eyes(screen, eyes, eyes_id, max_x, max_y):
    '''
    Функция перерисовывает тело в новом месте
    '''
    for eye in eyes: 
        x = scale_x(eye.X, max_x)
        y = scale_y(eye.Y, max_y)
        r = scale_x(eye.r, max_x)
       
        screen.coords(eyes_id[eyes.index(eye)], x - r, y - r, x + r, y + r) 

def init_targets(screen, targets, targets_id, max_x, max_y):
    '''
    Функция инициализирует мишени как графические объекты на экране
    '''
    for i in range(len(targets)):
        x = scale_x(targets[i].x, max_x)
        y = scale_y(targets[i].y, max_y)
        r = scale_x(targets[i].r, max_x)
        color = targets[i].color
        targets_id.append(screen.create_oval(x - r, y - r, x + r, y + r, fill=color, activefill=color))


def redraw_targets(screen, targets, targets_id, max_x, max_y):
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