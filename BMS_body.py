# coding: utf-8
# license: GPLv3

class Body:
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
        # проекции скоростей объекта на оси У и Х 
        self.Vx = Vx
        self.Vy = Vy
        # проекции сил, действующих на объект, на оси У и Х
        self.Fx = 0 
        self.Fy = 0
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