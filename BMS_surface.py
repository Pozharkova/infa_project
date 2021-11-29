# coding: utf-8
# license: GPLv3
import math
'''
Содержит класс поверхностей
'''
class point:
    ''' 
    Класс, описывающий точки поверхности
    Содержит координаты точки, тип (подвижная) цвет и коэффициент трения
    '''
    def __init__(self, x = 0, y = 0, friction = 0, color = 'black'):
        '''
        Инициализация класса точки
        '''
        # координаты точки
        self.x = x
        self.y = y
        # коэффициент трения, который действует на участке поверхности, начиная с данной точки.
        self.friction = friction
        # цвет
        self.color = color

class surface:
    '''
    Класс, описывающий поверхности, по которой двигается шар
    Содержит точки, ограничивающие прямые участки поверхности
    '''
    def __init__(self):
        '''
        Инициализация класса траектории: пустой список точек
        По умолчанию черный цвет и линейная интерполяция
        '''
        # точки 
        self.points = []
        self.lines = []
       

        
    def addpoint(self, newpoint):
        '''
        Добавление точки поверхности.
        Поверхность не может иметь точки с одинаковыми координатами по оси Х, поэтому, если новая точка имеет дубль по оси Х, то она не добавляется.
        Точки поверхности всегда упорядочены по оси Х, поэтому после добавления точки производится сортировка
        '''
        #Проверка дубликатов
        find = False
        for a in self.points:
            if a.x==newpoint.x:
                find = True
        if not find:
            #Добавление точки в список
            self.points.append(newpoint)
            #Сортировка списка точек по Х
            self.points.sort(key = lambda points: points.x)
    
    def find_y(self, x):
        '''
        Определение координаты У по координате Х для любой точки поверхности на основе линейной интерполяции 
        '''
        n = len(self.points)
        # если количество точек менее 2 или Х выходит за диапазон поверхности, то функция возвращает -1
        y = -1
        if n > 2 and x >= self.points[0].x and x <= self.points[n - 1].x:
            # поиск точки с абсциссой Х или интервала, в котором лежит точка
            for i in range(0, n - 1):
                if x == self.points[i].x:
                    y = self.points[i].y
                #если найден интервал, то вычисляется координата точки на основе интерполяции
                
                elif x > self.points[i].x and x < self.points[i + 1].x:
                    k = (self.points[i + 1].y - self.points[i].y) / (self.points[i + 1].x - self.points[i].x)
                    b = self.points[i].y - self.points[i].x * k
                    y = k * x + b
            if y == -1 and x == self.points[n - 1].x:
                y = self.points[n - 1].y                        
        return y

    def find_friction(self, x):
        '''
        Определение коэффициента трения по координате Х для любой точки поверхности на основе линейной интерполяции 
        '''
        n = len(self.points)
        # если количество точек менее 2 или Х выходит за диапазон поверхности, то функция возвращает -1
        kf = 0
        if n > 2 and x >= self.points[0].x and x <= self.points[n - 1].x:
            # поиск точки с абсциссой Х или интервала, в котором лежит точка
            for i in range(0, n - 1):
                if x >= self.points[i].x and x < self.points[i + 1].x:
                    kf = self.points[i].friction
        return kf

    def find_alpha(self, x):
        '''
        Функция вычисляет угол касательной к кривой в точке с координатой Х 
        '''
        n = len(self.points)
        # если количество точек менее 2 или Х выходит за диапазон поверхности, то функция возвращает 0
        alpha = math.pi / 2
        if n > 2 and x >= self.points[0].x and x <= self.points[n - 1].x:
            if self.points[0].x == x:
                alpha = math.atan2(self.find_y(self.points[0].x + 0.01) - self.points[0].y, 0.01)
            elif self.points[n - 1].x == x:
                alpha = math.atan2(self.points[n - 1].y - self.find_y(self.points[n - 1].x - 0.01), 0.01)
            else:
                alpha = math.atan((self.find_y(x + 0.01) - self.find_y(x - 0.01))/0.02)
        return alpha
   
    def find_x(self, y, num):
        '''
        Определение координаты X по координате У для любой точки num-го участка поверхности на основе линейной интерполяции 
        '''
        n = len(self.points)
        # если количество точек менее 2
        x = -1
        if num < n - 1:
            if y >= self.points[num].y and y <= self.points[num + 1].y:
                if y == self.points[num].y:
                    x = self.points[num].x
                #если найден интервал, то вычисляется координата точки на основе интерполяции
                elif y == self.points[num - 1].y:
                    x = self.points[num - 1].x                
                else:
                    k = (self.points[num + 1].y - self.points[num].y) / (self.points[num + 1].x - self.points[num].x)
                    b = self.points[num].y - self.points[num].x * k
                    x = (y - b) / k
        return x    

    def find_kb(self, num):
        '''
        Определение параметров уравнения участка num 
        '''
        n = len(self.points)
        # если количество точек менее 2, то функция возвращает -1
        if num < n - 1:
            k = (self.points[num + 1].y - self.points[num].y) / (self.points[num + 1].x - self.points[num].x)
            b = self.points[num].y - self.points[num].x * k
        return (k, b)  
   
    def find_num(self, x):
        '''
        Определение номера участка по координате Х для любой точки поверхности на основе линейной интерполяции 
        '''
        n = len(self.points)
        # если количество точек менее 2 или Х выходит за диапазон поверхности, то функция возвращает -1
        num = -1
        if n > 2 and x >= self.points[0].x and x <= self.points[n - 1].x:
            # поиск точки с абсциссой Х или интервала, в котором лежит точка
            for i in range(0, n - 2):
                if x == self.points[i].x:
                    num = i
                elif x > self.points[i].x and x < self.points[i + 1].x:
                    num = i
            if num == -1 and x == self.points[n - 1].x:
                num = n - 1                        
        return num 