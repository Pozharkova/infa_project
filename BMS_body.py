# coding: utf-8
# license: GPLv3

class body:
    '''
    Класс, описывающий тело
    Содержит массу, координаты, проекции скоростей и сил, цвет и радиус
    '''
    def __init__(self, m = 1, x = 0, y = 0, Vx = 0, Vy = 0, r = 10, color = 'red'):
        '''
        Инициализация тела
        '''
        # масса объекта
        self.m = m
        # координаты объекта
        self.x = x
        self.y = y 
        # координаты точки касания
        self.xt = x
        self.yt = y
     
        # проекции скоростей объекта на оси У и Х 
        self.Vx = Vx
        self.Vy = Vy
        # Силы, действующих на объект, на оси У и Х
        self.mg = 0 
        self.Nx = 0
        self.Ny = 0
        self.Fx = 0
        self.Fy = 0
        self.Ftp_x = 0
        self.Ftp_y = 0
        # радиус объекта
        self.r = r
        # Цвет объекта
        self.color = color
        self.id = 0


class Target:

    """Класс, описывающий мишень"""
    def __init__(self, x=0, y=0, r=5, color = 'green' ):
        '''
        Инициализация мишени
        '''
        #координаты мишени
        self.x = x
        self.y = y

        #радиус мишени
        self.r = r

        #цвет мишени
        self.color = color
        self.active_color = 'yellow'

        #параметр активации мишени
        self.active = False

class Pupa_eye:

    """Класс, описывающий глаз Пупы"""
    def __init__(self, x=0, y=0, r=0.05, R = 1, color = 'black' ):
        '''
        Инициализация мишени
        '''
        #координаты центра глаза и зрачка
        self.X = self.x = x
        self.Y = self.y = y
        

        #радиус зрачка
        self.r = r
        # радиус глаза
        self.R = R

        #цвет мишени
        self.color = color
    
    def find_XY(self, viewX, viewY):
        '''
        Вычисление координат зрачка в зависимости от направления взгляда
        '''
        k = self.R/((viewX - self.x) ** 2 + (viewY - self.y) ** 2) ** 0.5
        self.X = self.x + (viewX - self.x) * k
        self.Y = self.y + (viewY - self.y) * k
