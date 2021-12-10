# coding: utf-8
# license: GPLv3
import BMS_surface as surf
import BMS_body as bod
import os
import os.path


def find_levels(file_names, level_names):
    """Ищет файлы с уровнями, считывает их названия и сохраняет названия и имена файлов в списки
    """
    file_names.clear()
    level_names.clear()
    for file in os.listdir():
        if file.endswith(".txt"):
            isLevel = False
            l_name = ''
            with open(file, 'r') as input_file:
                for line in input_file:
                    if '#puppagame' in line:
                        isLevel = True
                    if line.split()[0].lower() == 'name':
                        l_name = line[5:]
            if isLevel and len(l_name) > 0:
                file_names.append(file)
                level_names.append(l_name)                
                
def read_level(input_filename, body, surface, targets):
    """Cчитывает данные об объектах из файла
    """
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == 'point':
                parse_point(line, surface)
                
            elif object_type == 'target':
                parse_target(line, targets)
                
            elif object_type == 'body':
                parse_body(line, body)            

def parse_point(line, surface):
    """Считывает данные о точке из строки.

    Входная строка должна иметь слеюущий формат:

    point <x> <y> <kf>
    
    """
    s = line.split()
    x = float(s[1])
    y = float(s[2])
    kf = float(s[3])
    surface.points.append(surf.point(x, y, kf))

def parse_target(line, targets):
    """Считывает данные о цели из строки.

    Входная строка должна иметь слеюущий формат:

    target <x> <y> <r>
    
    """
    s = line.split()
    x = float(s[1])
    y = float(s[2])
    r = float(s[3])
    targets.append(bod.Target(x, y, r))

def parse_body(line, body):
    """Считывает данные о положении тела из строки.

    Входная строка должна иметь слеюущий формат:

    body <x> <y>
    
    """
    s = line.split()
    body.x = float(s[1])
    body.y = float(s[2])

def parse_besttime(line):
    """Считывает данные о лучшем времени и игроке.

    Входная строка должна иметь слеюущий формат:

    besttime <name> <time>
    
    """
    s = line.split()
    player_name = s[1]
    besttime = float(s[2])
    return player_name, besttime

def parse_velocity(line):
    """Считывает точку графика скорости.

    Входная строка должна иметь слеюущий формат:

    velocity <time> <velocity>
    
    """
    s = line.split()
    t = float(s[1])
    v = float(s[2])
    return t, v

def read_besttime(level_filename, surface, body, best_v, best_t):
    '''
    Ищет и считывает лучшее время уровня, соответствующую траекторию и начальное положение тела
    '''
    #определение имени файла с лучшим временем по имени файла уровня
    filename = level_filename[:-4] + '_besttime.txt'
    besttime = -1
    player_name = ''
    best_v.clear()
    best_t.clear()
    if os.path.exists(filename):
        with open(filename, 'r') as input_file:
            for line in input_file:
                object_type = line.split()[0].lower()
                if object_type == 'point':
                    parse_point(line, surface)
                
                elif object_type == 'body':
                    parse_body(line, body)                    
                
                elif object_type == 'besttime':
                        player_name, besttime = parse_besttime(line)
                        
                elif object_type == 'velocity':
                        t, v = parse_velocity(line)
                        best_v.append(v)
                        best_t.append(t)
    return player_name, besttime
        

def write_besttime(level_filename, player_name, besttime, surface, body, best_v, best_t):
    '''
    Записывает лучшее время уровня, соответствующую траекторию, начальное положение тела и график модуля скорости
    '''
    #определение имени файла с лучшим временем по имени файла уровня
    filename = level_filename[:-4] + '_besttime.txt'
    with open(filename, 'w') as output_file:
        output_file.write('besttime ' + player_name + ' ' + str(besttime) + '\n')
        for point in surface.points:
            output_file.write('point ' + str(point.x) + ' ' + str(point.y) + ' ' + str(point.friction) + '\n') 
        output_file.write('body ' + ' ' + str(body.x) + ' ' +  str(body.y) + ' ' +  str(body.r) + '\n')
        for i in range(len(best_t)):
            output_file.write('velocity ' + str(best_t[i]) + ' ' + str(best_v[i]) + '\n')         