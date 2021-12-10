# coding: utf-8
# license: GPLv3

import matplotlib.pyplot as plt
# отключение панели инструментов в окне с графиками
plt.rcParams['toolbar'] = 'None'
import BMS_surface as surf
import BMS_body as bod
import BMS_io as bio
import BMS_model as model
from BMS_vis import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog as inputbox
import math
import time




class Game:
    def __init__(self):
        # физическая ширина и высота основного экрана в метрах
        self.max_ox = 6
        self.max_oy = 4  
        # имя игрока
        self.player_name = 'Pupa'
        self.best_name = ''
        
        #создание окна
        self.root = tk.Tk()
        self.fr = tk.Frame(self.root)
        self.root.geometry('800x600')
        self.root.title("The Pupa's Game")
        #создание основного окна
        self.c_frame = tk.Frame(self.root)
        self.c_frame.place(x = 0, y = 0, width = window_width + 4, height = window_height + 5)
        self.main_screen = tk.Canvas(self.c_frame, width = window_width, height = window_height, bg = 'white')
        self.main_screen.pack(fill = tk.BOTH, expand = 1)
        self.image = tk.PhotoImage(file='pupa.png')
        
        self.start_image = tk.PhotoImage(file='start.png')
        self.pause_image = tk.PhotoImage(file='pause.png')
        self.stop_image = tk.PhotoImage(file='stop.png')
        self.step_image = tk.PhotoImage(file='step.png')
        self.reset_image = tk.PhotoImage(file='reset.png')
        
        #создание идентификаторов объектов на экране
        #участки траектории
        self.lines_id=[]
        self.backs_id=[]
        #точки траектории
        self.points_id=[]
        #Векторы на основном экране
        self.vecs=[]
        
        #Массив мишеней
        self.targets = []
        self.targets_id = []
        
        #глаза пупы
        self.eyes = []
        self.eyes_id = []
        
        #имена файлов с уровнями
        self.file_names = [] 
        #названия уровней
        self.level_names = []
        
        #Тело
        self.ball = bod.body(0.1, 20/100, 370/100, 0, 0, 10/100, 'blue')
        #Глаза
        self.eyes = [bod.Pupa_eye(2.35, 3.12, 0.1, 0.22), bod.Pupa_eye(3.29, 3.03, 0.1, 0.22)]
        #Поверхность
        self.main_surf = surf.surface()
        #Логические переменные
        #Запуск моделирования
        self.start = False
        #Пауза
        self.pause = False
        #Пошаговое моделирование
        self.steping = False
        #Режим перемещения точки поверхности
        self.moving = False
        #Индекс перемещаемой точки
        self.pnum = 0
        #Период обновления экрана
        self.dtime = 0.02
        #Количество шагов моделирования за один период обновления экрана
        self.time_scale = 100
        #Суммарное время моделирования
        self.ctime = 0
        #Время, за которое поражены все цели
        self.tdone = 0
        #Максимальная скорость тела
        self.vmax = 0
        #Пройденное телом расстояние
        self.S = 0
        #Лучшее время уровня
        self.besttime = -1
        #Траектория с лучшим временем
        self.best_surf = surf.surface()
        #тело для "лучшего времени"
        self.best_ball = bod.body(0.1, 20/100, 370/100, 0, 0, 10/100, 'blue') 
        
        #скорость/время
        self.curr_v = []
        self.best_v = []
        self.curr_t = []
        self.best_t = []
        
        #создание панели управления
        self.frame_right = tk.LabelFrame(self.root, text = 'Панель управления')
        self.frame_right.place(x = window_width + 5, y = 0, width = 800 - window_width - 5, height = 600)
        
        self.body_frame = tk.LabelFrame(self.frame_right, text = 'Настройки тела')
        self.body_frame.pack(side = 'top', fill = tk.X)
        
        #координаты
        self.x_label = tk.Label(self.body_frame, text = 'Х') 
        self.x_label.pack(side = 'top')
        self.x_scale = tk.Scale(self.body_frame, orient='horizontal', from_ = 2 * self.ball.r, to = self.max_ox - self.ball.r, 
                             resolution = 0.1, command = self.scale_ball_x, troughcolor = "blue")
        self.x_scale.set(self.ball.x)
        self.x_scale.pack(side = 'top', fill = tk.X)
        
        self.y_label = tk.Label(self.body_frame, text = 'Y') 
        self.y_label.pack(side = 'top')
        self.y_scale = tk.Scale(self.body_frame, orient='horizontal', from_ = self.ball.r, to = self.max_oy - 2 * self.ball.r, 
                             resolution = 0.1, command = self.scale_ball_y, troughcolor = "blue")
        self.y_scale.set(self.ball.y)
        self.y_scale.pack(side = 'top', fill = tk.X)
        
        self.line_frame = tk.LabelFrame(self.frame_right, text = 'Настройки участка поверхности')
        self.line_frame.pack(side = 'top', fill = tk.X)
        
        #Коэффициент трения
        self.kf_label = tk.Label(self.line_frame, text = 'Коэффициент трения') 
        self.kf_label.pack(side = 'top')
        self.kf_scale = tk.Scale(self.line_frame, orient='horizontal', state = tk.DISABLED, from_ = -1, to = 1, 
                              resolution = 0.1, command = self.scale_kf, troughcolor = "grey")
        self.kf_scale.set(0)
        self.kf_scale.pack(side = 'top', fill = tk.X)   
        
        self.level_frame = tk.LabelFrame(self.frame_right, text = 'Управление уровнями')
        self.level_frame.pack(side = 'top', fill = tk.X)
        
        #Управление уровнями
        self.level_label = tk.Label(self.level_frame, text = 'Выбор уровня') 
        self.level_label.pack(side = 'top')
      
        #загрузка названий уровней
        bio.find_levels(self.file_names, self.level_names)
        self.level_combo = ttk.Combobox(self.level_frame, values = self.level_names)
        self.level_combo.pack(side = 'top')
        self.level_combo.current(0)        

        self.level_button = tk.Button(self.level_frame, text = 'Загрузить уровень', command = self.esc_click)
        self.level_button.pack(side = 'top')
        
        
        
        
        self.mod_frame = tk.LabelFrame(self.frame_right, text = 'Управление', width = 150, height = 50)
        self.mod_frame.pack(side = 'top', fill = tk.BOTH)
        
        
        # кнопки управления моделированием движения
        self.start_button = tk.Button(self.mod_frame, image = self.start_image, command = self.start_click)
        self.start_button.place(x = 15, y = 0, width = 30, height = 30, anchor = 'nw')
        self.pause_button = tk.Button(self.mod_frame, image = self.pause_image, command = self.pause_click)
        self.pause_button.place(x = 45, y = 0, width = 30, height = 30, anchor = 'nw')
        self.stop_button = tk.Button(self.mod_frame, image = self.stop_image, command = self.stop_click)
        self.stop_button.place(x = 75, y = 0, width = 30, height = 30, anchor = 'nw')
        self.step_button = tk.Button(self.mod_frame, image = self.step_image, command = self.step_click)
        self.step_button.place(x = 105, y = 0, width = 30, height = 30, anchor = 'nw')
        self.esc_button = tk.Button(self.mod_frame, image = self.reset_image, command = self.esc_click)
        self.esc_button.place(x = 135, y = 0, width = 30, height = 30, anchor = 'nw')
        
        #панель лучшего времени
        self.besttime_frame = tk.LabelFrame(self.frame_right, text = 'Лучшее время уровня', width = 150, height = 50)
        self.besttime_frame.pack(side = 'top', fill = tk.BOTH)
        self.besttime_label = tk.Label(self.besttime_frame, text = ' ') 
        self.besttime_label.pack(side = 'top')
        self.loadbest_button = tk.Button(self.besttime_frame, text = 'Загрузить лучшую траекторию', command = self.load_best)
        self.loadbest_button.pack(side = 'top')
        self.veloplot_button = tk.Button(self.besttime_frame, text = 'Графики скоростей', command = self.velo_plot)
        self.veloplot_button.pack(side = 'top')           
        
        
        #создание информационной панели
        self.frame_bottom = tk.LabelFrame(self.root, text = 'Статистика', bg = 'black', fg = '#5de100')
        self.frame_bottom.place(x = 0, y = window_height + 5, width = window_width + 4, height = 600 - window_height - 5)
        
        self.time_frame = tk.LabelFrame(self.frame_bottom, text = 'Время/Цели', bg = 'black', fg = '#5de100')
        self.time_frame.place(x = 0, y = 0, width = 200, height =  600 - window_height - 5)
        
        self.velocity_frame = tk.LabelFrame(self.frame_bottom, text = 'Расстояния/Скорости', bg = 'black', fg = '#5de100')
        self.velocity_frame.place(x = 200, y = 0, width = 200, height =  600 - window_height - 5)
        
        self.force_frame = tk.LabelFrame(self.frame_bottom, text = 'Модули сил', bg = 'black', fg = '#5de100')
        self.force_frame.place(x = 400, y = 0, width = 200, height =  600 - window_height - 5)
        
        
        #Время
        self.ctime_label = tk.Label(self.time_frame, text = 'Текущее время: 000.00 с', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.ctime_label.place(x = 0, y = 0, width = 196, height = 20)
        self.btime_label = tk.Label(self.time_frame, text = 'Время прохождения: 000.00 с', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.btime_label.place(x = 0, y = 20, width = 196, height = 20)
        self.cgoals_label = tk.Label(self.time_frame, text = 'Целей: 0 из 10', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.cgoals_label.place(x = 0, y = 40, width = 196, height = 20)
        
        
        #Модули скоростей, координаты
        self.cx_label = tk.Label(self.velocity_frame, text = 'X: 0.00 м', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.cx_label.place(x = 0, y = 0, width = 180, height = 20)
        self.cy_label = tk.Label(self.velocity_frame, text = 'Y: 0.00 м', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.cy_label.place(x = 0, y = 20, width = 180, height = 20)
        self.cs_label = tk.Label(self.velocity_frame, text = 'S: 00.00 м', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.cs_label.place(x = 0, y = 40, width = 180, height = 20)
        self.cv_label = tk.Label(self.velocity_frame, text = 'V: 000.00 м/с', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.cv_label.place(x = 0, y = 60, width = 180, height = 20)
        self.maxv_label = tk.Label(self.velocity_frame, text = 'Vmax: 000.00 м/с', justify = 'left', anchor = 'w', bg = 'black', fg = '#5de100') 
        self.maxv_label.place(x = 0, y = 80, width = 180, height = 20)
        
        #Модули сил
        self.cmg_label = tk.Label(self.force_frame, text = 'mg: 00.00 Н', bg = 'black', justify = 'left', anchor = 'w', fg = '#5de100') 
        self.cmg_label.place(x = 0, y = 0, width = 195, height = 20)
        self.cN_label = tk.Label(self.force_frame, text = 'N: 00.00 Н', bg = 'blue', justify = 'left', anchor = 'w', fg = '#5de100') 
        self.cN_label.place(x = 0, y = 20, width = 195, height = 20)
        self.cFtp_label = tk.Label(self.force_frame, text = 'Fтр: 00.00 Н', bg = 'red', justify = 'left', anchor = 'w', fg = '#5de100') 
        self.cFtp_label.place(x = 0, y = 40, width = 195, height = 20)
        self.cF_label = tk.Label(self.force_frame, text = 'R: 00.00 Н', bg = 'black', justify = 'left', anchor = 'w', fg = '#5de100') 
        self.cF_label.place(x = 0, y = 60, width = 195, height = 20)
        


    def init_game(self):
        '''
        Инициализация игры
        '''
        # очистка экрана и всех массивов
        self.main_screen.delete('all')
        self.main_surf.points.clear()
        self.best_surf.points.clear()
        self.points_id.clear()
        self.lines_id.clear()
        self.backs_id.clear()
        self.targets.clear()
        self.targets_id.clear()
        self.eyes_id.clear()
        self.vecs.clear()
        self.curr_v.clear()
        self.curr_t.clear()
        #Вывод изображения Пупы
        self.main_screen.create_image(0, 0, image = self.image, anchor = tk.NW)
        #загрузка
       
        self.best_name, self.besttime = bio.read_besttime(self.file_names[self.level_combo.current()], self.best_surf, self.best_ball, self.best_v, self.best_t)
        bio.read_level(self.file_names[self.level_combo.current()], self.ball, self.main_surf, self.targets)
        
        if self.besttime > -1:
            self.besttime_label.config(text = self.best_name + ': ' +str(round(self.besttime, 2)) + ' c')
        else:
            self.besttime_label.config(text = ' ')
        #Вычисление начальных сил и скоростей
        model.move_body(self.ball, self.main_surf, 9.8, 0, self.max_ox)

        #инициализация всех графических объектов
        init_eyes(self.main_screen, self.eyes, self.eyes_id, self.max_ox, self.max_oy)
        init_targets(self.main_screen, self.targets, self.targets_id, self.max_ox, self.max_oy)
        init_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
        init_ball(self.main_screen, self.ball, self.vecs, self.max_ox, self.max_oy) 
        
        #рисование глаз Пупы
        for eye in self.eyes:
            eye.find_XY(self.ball.x, self.ball.y)
        redraw_eyes(self.main_screen, self.eyes, self.eyes_id, self.max_ox, self.max_oy)     
        
        self.main_screen.bind('<Button-1>', self.takepoint)
        self.main_screen.bind('<ButtonRelease-1>', self.droppoint)
        self.main_screen.bind('<Motion>', self.movepoint)            


    def scale_ball_x(self, value):
        '''
        Перемещение тела по оси Х с использованием шкалы на панели управления
        '''
        if not self.start:
            self.ball.x = float(value)
            for eye in self.eyes:
                eye.find_XY(self.ball.x, self.ball.y)
            redraw_eyes(self.main_screen, self.eyes, self.eyes_id, self.max_ox, self.max_oy)        
            redraw_ball(self.main_screen, self.ball, self.vecs, self.max_ox, self.max_oy)

    def scale_ball_y(self, value):
        '''
        Перемещение тела по оси У с использованием шкалы на панели управления
        '''    
        if not self.start:
            self.ball.y = float(value)
            for eye in self.eyes:
                eye.find_XY(self.ball.x, self.ball.y)
            redraw_eyes(self.main_screen, self.eyes, self.eyes_id, self.max_ox, self.max_oy)        
            redraw_ball(self.main_screen, self.ball, self.vecs, self.max_ox, self.max_oy)
    

    def scale_kf(self, value):
        '''
        Настройка коэффициента трения участка поверхности с использованием шкалы на панели управления
        ''' 
        if not self.start:
            self.main_surf.points[self.pnum].friction = float(value)
            full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)

    # кнопки управления
    # старт
    def start_click(self):
        '''
        Запуск движение тела при нажатии на кнопку Старт
        '''
        # отключение на время моделирования шкал настройки положения тела
        self.x_scale.config(state = tk.DISABLED, troughcolor = "grey")
        self.y_scale.config(state = tk.DISABLED, troughcolor = "grey")
        self.kf_scale.config(state = tk.DISABLED, troughcolor = "grey")
        full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
        self.pause = False
        # начальные условия
        self.ball.x = self.x_scale.get()
        self.ball.y = self.y_scale.get()
        self.ball.Vx = 0
        self.ball.Vy = 0
        self.vmax = 0
        self.tdone = 0
        self.S = 0
        for i in range(len(self.targets)):
            self.targets[i].active = False
        redraw_targets(self.main_screen, self.targets, self.targets_id, self.max_ox, self.max_oy)    
        self.start = True
        self.steping = False
        self.ctime = 0
        self.curr_t.clear()
        self.curr_v.clear()
        self.curr_t.append(0)
        self.curr_v.append(0)
        
    
    # пауза
    def pause_click(self):
        '''
        Пауза процесса моделирования движения тела
        '''
        
        if self.start:
            self.pause = not self.pause
            self.steping = False
    
    
    # стоп
    def stop_click(self):
        '''
        Остановка процесса моделирования движения тела
        '''
        
        # активация шкал управления начальным положением тела
        self.x_scale.config(state = tk.ACTIVE, troughcolor = "blue")
        self.y_scale.config(state = tk.ACTIVE, troughcolor = "blue")
    
        self.pause = True
        self.ball.x = self.x_scale.get()
        self.ball.y = self.y_scale.get()
        self.ball.xt = self.ball.x
        self.ball.yt = self.ball.y
        redraw_ball(self.main_screen, self.ball, self.vecs, self.max_ox, self.max_oy)
        self.ball.Vx = 0
        self.ball.Vy = 0
        for i in range(len(self.targets)):
            self.targets[i].active = False
        for eye in self.eyes:
            eye.find_XY(self.ball.x, self.ball.y)
        redraw_eyes(self.main_screen, self.eyes, self.eyes_id, self.max_ox, self.max_oy)      
        redraw_targets(self.main_screen, self.targets, self.targets_id, self.max_ox, self.max_oy) 
        self.start = False
    
    # пошаговое движение
    def step_click(self):
        '''
        Пошаговое моделирования движения тела
        '''
        
        # отключение на время моделирования шкал настройки положения тела
        self.x_scale.config(state = tk.DISABLED, troughcolor = "grey")
        self.y_scale.config(state = tk.DISABLED, troughcolor = "grey")
        self.kf_scale.config(state = tk.DISABLED, troughcolor = "grey")
        full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
        self.start = True
        self.steping = True
        self.pause = False
        
    
    
    
    # сброс
    def esc_click(self):
        '''
        Сброс игры к начальному состоянию
        '''
        
        if self.level_combo.current() >= 0:
            self.init_game()
            self.x_scale.config(state = tk.ACTIVE, troughcolor = "blue")
            self.y_scale.config(state = tk.ACTIVE, troughcolor = "blue")            
            self.x_scale.set(self.ball.x)
            self.y_scale.set(self.ball.y)
            self.stop_click()

    
    def load_best(self):
        '''
        Загрузка лучшей траектории уровня и положения тела
        '''
        
        if self.besttime > -1:
            self.x_scale.config(state = tk.ACTIVE, troughcolor = "blue")
            self.y_scale.config(state = tk.ACTIVE, troughcolor = "blue")             
            for i in range(len(self.main_surf.points)):
                self.main_surf.points[i].x = self.best_surf.points[i].x
                self.main_surf.points[i].y = self.best_surf.points[i].y
                self.main_surf.points[i].friction = self.best_surf.points[i].friction
            
            full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
            
            self.ball.x = self.best_ball.x
            self.ball.y = self.best_ball.y
            self.x_scale.set(self.ball.x)
            self.y_scale.set(self.ball.y)
            self.stop_click()            

    def velo_plot(self):
        '''
        Вызов окна с построением графиков
        '''
        if len(self.best_t) > 0 or len(self.curr_t) > 0:
            fig, ax = plt.subplots(num=None, figsize=(6, 4))
            fig.canvas.set_window_title('Графики модулей полных скоростей тела')  
            if len(self.curr_t) > 0:
                ax.plot(self.curr_t, self.curr_v, color='blue', label='Текущий запуск')
            if len(self.best_t) > 0:
                ax.plot(self.best_t, self.best_v, color='red', label='Лучшее время')  
            ax.legend(loc='upper left', frameon=False) 
            ax.set_ylabel('Модуль скорости, м/с')
            ax.set_xlabel('Время, с')
            plt.show()

    def write_best(self):
        '''
        Запись лучшей траектории уровня
        '''
        self.best_surf.points.clear()
        for i in range(len(self.main_surf.points)):
            self.best_surf.points.append(self.main_surf.points[i])
        self.best_ball.x = self.x_scale.get()
        self.best_ball.y = self.y_scale.get()
        bio.write_besttime(self.file_names[self.level_combo.current()], self.best_name, self.besttime, self.best_surf, self.best_ball, self.best_v, self.best_t)
 

    def show_stats(self):
        '''
        Вывод основной статистики по игре
        '''
        
        self.tcount = 0 
        #подсчет количества пораженных целей
        for targ in self.targets:
            if targ.active:
                self.tcount += 1
        if self.tcount == len(self.targets) and self.tdone == 0:
            self.tdone = self.ctime
        # Расчет максимальной скорости
        if self.vmax < (self.ball.Vx ** 2 + self.ball.Vy ** 2) ** 0.5:
            self.vmax = (self.ball.Vx ** 2 + self.ball.Vy ** 2) ** 0.5
        
        # Рассчет пройденного расстояния
        self.S += self.dtime * (self.ball.Vx ** 2 + self.ball.Vy ** 2) ** 0.5
        
        self.ctime_label.config(text = 'Текущее время: ' + str(round(self.ctime, 2)) + ' с')
        self.curr_t.append(self.ctime)
        self.curr_v.append((self.ball.Vx ** 2 + self.ball.Vy ** 2) ** 0.5)
        
        if self.tdone == 0:
            self.btime_label.config(text = 'Время прохождения: ' + str(round(self.ctime, 2)) + ' с', bg = 'black')
        else:
            self.btime_label.config(text = 'Время прохождения: ' + str(round(self.tdone, 2)) + ' с', bg = 'red')
            if (self.besttime > -1 and self.ctime < self.besttime) or self.besttime == -1:
                player_name = inputbox.askstring("Лучшее время!", "Введите имя игрока:", parent = self.root)
                if len(player_name) > 0:
                    self.player_name = player_name
                else:
                    self.player_name = 'Pupa'
                self.besttime = self.ctime
                self.best_name = self.player_name
                self.best_v.clear()
                self.best_t.clear()
                for i in range(len(self.curr_t)):
                    self.best_v.append(self.curr_v[i])
                    self.best_t.append(self.curr_t[i])
                
                self.write_best()
                self.besttime_label.config(text = self.best_name + ': ' + str(round(self.besttime, 2)) + ' c')
            self.pause_click()
            
        self.cgoals_label.config(text = 'Целей: ' + str(self.tcount) + ' из ' + str(len(self.targets)))
        self.cv_label.config(text = 'V: ' + str(round((self.ball.Vx ** 2 + self.ball.Vy ** 2) ** 0.5, 2))+ ' м/с')
        self.maxv_label.config(text = 'Vmax: ' + str(round(self.vmax, 2))+ ' м/с')
        self.cx_label.config(text = 'X: ' + str(round(self.ball.x, 2))+ ' м') 
        self.cy_label.config(text = 'Y: ' + str(round(self.ball.y, 2))+ ' м') 
        self.cs_label.config(text = 'S: ' + str(round(self.S, 2))+ ' м') 
        self.cmg_label.config(text = 'mg: ' + str(round(abs(self.ball.mg), 2))+ ' H') 
        self.cN_label.config(text = 'N: ' + str(round((self.ball.Nx ** 2 + self.ball.Ny ** 2) ** 0.5, 2))+ ' H') 
        self.cFtp_label.config(text = 'Fтр: ' + str(round((self.ball.Ftp_x ** 2 + self.ball.Ftp_y ** 2) ** 0.5, 2))+ ' H') 
        self.cF_label.config(text = 'R: ' + str(round((self.ball.Fx ** 2 + self.ball.Fy ** 2) ** 0.5, 2))+ ' H')     
    
    # Редактирование вершин поверхности и линейных участков
    
    def takepoint(self, event):
        '''
        Выбор вершины или линии поверхности при нажатии левой клавиши мыши
        '''

        # выбор возможен только вне моделирования
        if not self.start:
            #проверка выбора объекта на экране
            obj = self.main_screen.find_withtag(tk.CURRENT)
            #если объект выбран, определяется его тип
            if obj:
                obj = obj[0]
                #если объект линия, запускается редактирование линии
                if obj in self.lines_id:
                    self.pnum = self.lines_id.index(obj)
                    full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
                    self.main_screen.itemconfig(obj, fill = 'red')
                    self.kf_scale.config(state = tk.ACTIVE, troughcolor = "blue")
                    self.kf_scale.set(self.main_surf.points[self.pnum].friction)
                #если объект вершина, то запускается перемещение вершины
                elif obj in self.points_id:
                    # определение вершины
                    full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
                    self.kf_scale.config(state = tk.DISABLED, troughcolor = "grey")                
                    self.pnum = self.points_id.index(obj)
                    #разрешение на перемещение
                    self.moving = True
                #обновление траектории
                else:
                    full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
                    self.kf_scale.config(state = tk.DISABLED, troughcolor = "grey")            
            else:
                full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
                self.kf_scale.config(state = tk.DISABLED, troughcolor = "grey") 
            
    
    def movepoint(self, event):
        '''
        Перемещение вершины поверхности при движении указателя мыши
        '''
        # Если разрешено перемещение, то вершина перемещается за указателем мыши. 
        if self.moving:
            self.main_screen.coords(self.points_id[self.pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
            # Перерисовка поверхности (без изменения физических координат)
            redraw_surface(self.main_screen, self.points_id, self.lines_id, self.backs_id)
            
    def droppoint(self, event):
        '''
        Окончание перемещения вершины поверхности при отпускании левой клавиши мыши
        '''

        if self.moving:
            self.main_screen.coords(self.points_id[self.pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
            # определение физических координат вершины
            nx = inv_scale_x(event.x, self.max_ox)
            ny = inv_scale_y(event.y, self.max_oy)
            # проверка нарушения неубывания координат следующих друг за другом вершин по оси Х
            # также расстояние по оси Х между двумя вершин не может быть менее диаметра тела
            if self.pnum > 0 and self.pnum < len(self.points_id) - 1:
                if nx < self.main_surf.points[self.pnum - 1].x + 2 * self.ball.r:
                    nx = self.main_surf.points[self.pnum - 1].x + 2 * self.ball.r
                if nx > self.main_surf.points[self.pnum + 1].x - 2 * self.ball.r:
                    nx = self.main_surf.points[self.pnum + 1].x - 2 * self.ball.r
                
            if nx < 0:
                nx = 0
            if nx > self.max_ox:
                nx = self.max_ox
            if ny < 0:
                ny = 0
            if ny > self.max_oy:
                ny = self.max_oy
           #обновление физических координат 
            self.main_surf.points[self.pnum].x = nx 
            self.main_surf.points[self.pnum].y = ny
            #полная перерисовка поверхности с учетом физических координат
            full_redraw_surface(self.main_screen, self.main_surf, self.points_id, self.lines_id, self.backs_id, self.max_ox, self.max_oy)
            self.moving = False
    

    
    
    
    def new_sim(self, event=''):
        '''
        Основной игровой процесс: редактирование параметров тела и поверхности, моделирование
        '''
        
        while self.main_surf:
            if (self.start and not self.pause) or self.steping:
                # моделирование движения с временным шагом в time_scale меньшим, чем период обновления экрана
                for j in range(self.time_scale):
                    model.move_body(self.ball, self.main_surf, 9.8, self.dtime/self.time_scale, self.max_ox)
                    for i in range(len(self.targets)):
                        model.check_hit(self.ball, self.targets[i])
                for eye in self.eyes:
                    eye.find_XY(self.ball.x, self.ball.y)
                redraw_eyes(self.main_screen, self.eyes, self.eyes_id, self.max_ox, self.max_oy)
                redraw_targets(self.main_screen, self.targets, self.targets_id, self.max_ox, self.max_oy)    
                redraw_ball(self.main_screen, self.ball, self.vecs, self.max_ox, self.max_oy)
                self.ctime += self.dtime
                self.show_stats()
                if self.steping:
                    self.pause = True
                    self.steping = False
                    self.start = True
              
            self.main_screen.update() #обновление игрового поля
            time.sleep(abs(self.dtime)) #пауза
        



    
newgame = Game()
newgame.esc_click()
newgame.show_stats()
newgame.new_sim()
newgame.root.mainloop()
new.game.root.destroy()



