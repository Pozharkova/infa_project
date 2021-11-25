# coding: utf-8
# license: GPLv3
import math

def move_body(body, surface, g, dt, max_x):
    """Вычисляет проекции равнодействующей на тело силы, определяет ускорения скорости.
    Перемещает тело. Производит необходимые коррекции
    """

    body.Fx = body.Fy = 0
    x0 = body.x
    y0 = body.y
    r = body.r
    #Определение точки касания телом поверхности
    alpha = surface.find_alpha(x0)
    x = math.sin(alpha) * r + x0
    y = surface.find_y(x)
    #Если тело касается поверхности, то определяются силы, действующие на него при движении
    if  abs(r ** 2 - ((x0 - x) ** 2 + (y0 - y) ** 2)) <= 0.02:
        F = -body.m * g * math.sin(alpha - math.pi)
        kf = surface.find_friction(x)
        if alpha != 0:
            Ftp = kf * abs(F / math.tan(alpha - math.pi))
        else:
            Ftp = kf * body.m * g 
        if body.Vx > 0:
            F += Ftp
        elif body.Vx < 0:
            F -= Ftp
        body.Fx += F * math.cos(alpha - math.pi)
        body.Fy += F * math.sin(alpha - math.pi)
    #Если шарик не касается поверхности, то на него действует только сила тяжести
    else:
        body.Fx = 0
        body.Fy = -body.m * g
    # перемещение тела
    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt
  
    oldy = body.y
    ay = body.Fy / body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt
    # проверка и коррекция при выходе тела за поверхность
    x0 = body.x
    y0 = body.y
    r = body.r
    alpha = surface.find_alpha(x0)
    x = math.sin(alpha) * r + x0
    y = surface.find_y(x)
    if (x0 - x) ** 2 + (y0 - y) ** 2 < r ** 2:
        body.y = (r ** 2 - (x0 - x) ** 2) ** 0.5 + y
        body.Vy = (body.y - oldy) / dt
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