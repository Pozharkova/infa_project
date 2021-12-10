# coding: utf-8
# license: GPLv3
import math

def check_hit(body, target):
    """Проверяет столконовение шарика с мишенью"""
    if (body.x - target.x) ** 2 + (body.y - target.y) ** 2 <= target.r ** 2:
        target.active = True
def find_norm_x(k, b, x0, y0):
    return (k * y0 + x0 - k * b)/(1 + k ** 2)

def move_body(body, surface, g, dt, max_x):
    """Вычисляет проекции равнодействующей на тело силы, определяет ускорения скорости.
    Перемещает тело. Производит необходимые коррекции
    """

    body.Nx = body.Ny = body.Ftp_x = body.Ftp_y = body.mg = body.Fx = body.Fy = 0
    
    x0 = body.x
    y0 = body.y
    r = body.r
    body.xt = body.x
    body.yt = body.y
    #На тело всегда действует сила тяжести
    body.mg = -body.m * g
    
    #Определение точки касания телом поверхности
    num = surface.find_num(x0)
    (k, b) = surface.find_kb(num)
    fi1 = -math.atan(k)
    body.xt = x = x1 = find_norm_x(k, b, x0, y0)
    body.yt = y = y1 = surface.find_y(x)
    x2 = x1
    y2 = y1
    fi = fi2 = fi1
    if body.Vx > 0 and num < len(surface.points) - 1:

        (k, b) = surface.find_kb(num + 1)
        fi2 = -math.atan(k)
        x2 = find_norm_x(k, b, x0, y0)
        y2 = surface.find_y(x2)
        if x2 < surface.points[num + 1].x or x2 > surface.points[num+2].x:
            x2 = x1
            y2 = y1
            fi2 = fi1
    if body.Vx < 0 and num > 0:
        (k, b) = surface.find_kb(num - 1)
        fi2 = -math.atan(k)
        x2 = find_norm_x(k, b, x0, y0)
        y2 = surface.find_y(x2)
        if x2 < surface.points[num - 1].x or x2 > surface.points[num].x:
            x2 = x1
            y2 = y1
            fi2 = fi1
    if (x1 - x0) ** 2 + (y1 - y0) ** 2 <= (x2 - x0) ** 2 + (y2 - y0) ** 2:
        body.xt = x = x1
        fi = fi1
        body.yt = y = y1
    else:
        body.xt = x = x2
        fi = fi2
        body.yt = y = y2
    #Если тело касается поверхности, то определяются силы, действующие на него при движении     
    if abs(r ** 2 - ((x0 - x) ** 2 + (y0 - y) ** 2)) <= 0.002:
       
        #сила реакции поверхности
        N = abs(body.mg) * math.cos(fi)
        body.Nx = N * math.sin(fi)
        body.Ny = N * math.cos(fi)
        #сила трения
        kf = surface.find_friction(x)
        if fi != 0:
            Ftp = abs(N)
        else:
            Ftp = abs(body.m * g) 
        if body.Vx > 0:
            body.Ftp_x = -Ftp * math.cos(fi)
            body.Ftp_y = Ftp * math.sin(fi)
        elif body.Vx < 0:
            body.Ftp_x = Ftp * math.cos(fi)
            body.Ftp_y = -Ftp * math.sin(fi)
        body.Ftp_x *= kf
        body.Ftp_y *= kf
    #проекции результирующей силы
    oldx = body.x
    body.Fx = body.Nx + body.Ftp_x
    body.Fy = body.Ny + body.mg + body.Ftp_y   
    # перемещение тела
    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt
  
    oldy = body.y
    ay = body.Fy / body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt
    # проверка и коррекция при выходе тела за поверхность
    # определение точки касания
    x0 = body.x
    y0 = body.y
    r = body.r
    body.xt = body.x
    body.yt = body.y
    num = surface.find_num(x0)
    (k, b) = surface.find_kb(num)
    fi1 = -math.atan(k)
    body.xt = x = x1 = find_norm_x(k, b, x0, y0)
    body.yt = y = y1 = surface.find_y(x)
    x2 = x1
    y2 = y1
    fi = fi2 = fi1
    if body.Vx > 0 and num < len(surface.points) - 1:

        (k, b) = surface.find_kb(num + 1)
        fi2 = -math.atan(k)
        x2 = find_norm_x(k, b, x0, y0)
        y2 = surface.find_y(x2)
        if x2 < surface.points[num + 1].x or x2 > surface.points[num+2].x:
            x2 = x1
            y2 = y1
            fi2 = fi1
    if body.Vx < 0 and num > 0:
        (k, b) = surface.find_kb(num - 1)
        fi2 = -math.atan(k)
        x2 = find_norm_x(k, b, x0, y0)
        y2 = surface.find_y(x2)
        if x2 < surface.points[num - 1].x or x2 > surface.points[num].x:
            x2 = x1
            y2 = y1
            fi2 = fi1
    #выбор точки касания
    if (x1 - x0) ** 2 + (y1 - y0) ** 2 <= (x2 - x0) ** 2 + (y2 - y0) ** 2:
        body.xt = x = x1
        fi = fi1
        body.yt = y = y1
    else:
        body.xt = x = x2
        fi = fi2
        body.yt = y = y2
    #коррекция положения тела
    if (x0 - x) ** 2 + (y0 - y) ** 2 < r ** 2:
        R = ((x0 - x) ** 2 + (y0 - y) ** 2) ** 0.5
        a = math.acos((x0 - x) / R)
        body.y = body.y + math.sin(a) * (r - R) 
        body.x = body.x + math.cos(a) * (r - R) 
        V_sq = body.Vx ** 2 + body.Vy ** 2
        #коррекция скорости
        body.Vy = (body.y - oldy) / dt
        #закон сохранения энергии
        if V_sq > body.Vy ** 2:
            V = (V_sq - body.Vy ** 2) ** 0.5
        else: 
            V = 0
        if body.Vx < 0:
            V = -V
        if body.Vx == 0:
            if fi < 0:
                V = -V
            if fi == 0:
                V = 0
        body.Vx = V
            
    #обработка достижения телом края экрана
    if x0 + r > max_x:
        body.x = max_x - r
        body.Vx = 0
    if y0 - r < 0:
        body.y = r
        body.Vy = 0
    if x0 - 2 * r < 0:
        body.x = 2 * r
        body.Vx = 0