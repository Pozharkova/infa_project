import BMS_surface as surf
import BMS_body as bod
import BMS_model as model
import tkinter as tk
import math
import time

#������ � ������ ��������� ������
window_width = 600
window_height = 400
# ���������� ������ � ������ ��������� ������ � ������
max_ox = 6
max_oy = 4
#�������� ����
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
root.title('"��������" � ������� "����������" � ������ ���� ���. ������� ������� - ����������')
#�������� ��������� ����
c_frame = tk.Frame(root)
c_frame.place(x = 0, y = 0, width = window_width + 4, height = window_height + 5)
main_screen = tk.Canvas(c_frame, width = window_width, height = window_height, bg = 'white')
main_screen.pack(fill = tk.BOTH, expand = 1)

#�������� ��������������� �������� �� ������
#������� ����������
lines_id=[]
#����� ����������
points_id=[]

def scale_x(x, max_x):
    '''
    ������� ������������ ���������� ���������� � � ��������
    '''
    return int(window_width * x / max_x)

def scale_y(y, max_y):
    '''
    ������� ������������ ���������� ���������� y � ��������
    '''
    return int(window_height - window_height * y / max_y)

def inv_scale_x(x, max_x):
    '''
    ������� ������������ �������� ���������� � � ����������
    '''
    return x * max_x / window_width

def inv_scale_y(y, max_y):
    '''
    ������� ������������ �������� ���������� y � ����������
    '''
    return (window_height - y) * max_y / window_height

def init_surface(screen, surface, max_x, max_y):
    '''
    ������� �������������� ����������� ����������� ����������� �� ������
    '''
    global points_id, lines_id
    for i in range(len(surface.points)):
        #������� ��������� ����� � ��������
        x = scale_x(surface.points[i].x, max_x) 
        y = scale_y(surface.points[i].y, max_y)
        color = surface.points[i].color
        if i < len(surface.points) - 1:
        #���������� ����� � ������ �� ����������� �� ������ 
            lines_id.append(screen.create_line(x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y), fill = color, activefill = 'red', width = 2))
        #���������� ����� � ������ �� ����������� �� ������ ����� ����������� ����� �����
        points_id.append(screen.create_oval(x - 3,y - 3,x + 3, y + 3, fill = color, activefill = 'red'))        

def redraw_surface(screen):
    '''
    ������� �������������� ����������� ����������� ����������� �� ������ ��� �������������� ���������� (��� ������������� ���������� ���������)
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
            screen.coords(lines_id[i], lx1, ly1, lx2, ly2)

def full_redraw_surface(screen, surface, max_x, max_y):
    '''
    ������� �������������� ����������� ����������� ����������� �� ������ c �������������� ���������� ���������
    '''
    global points_id, lines_id
    for i in range(len(surface.points)):
        #������� ��������� ����� � ��������
        x = scale_x(surface.points[i].x, max_x) 
        y = scale_y(surface.points[i].y, max_y)
        color = surface.points[i].color
        if i < len(surface.points) - 1:
        #��������� ����� �� ������ 
            screen.coords(lines_id[i], x, y, scale_x(surface.points[i + 1].x, max_x), scale_y(surface.points[i + 1].y, max_y))
        #�� ������ ����� ����������� ����� �����
        screen.coords(points_id[i], x - 3,y - 3,x + 3, y + 3)

def init_ball(screen, ball, max_x, max_y):
    '''
    ������� �������������� ����, ��� ����������� ������ �� �������� ������
    '''
    global ball_id
    x = scale_x(ball.x, max_x)
    y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    color = ball.color
    ball_id = screen.create_oval(x - r, y - r, x + r, y + r, fill = color, activefill = 'red')
    
def redraw_ball(screen, ball, max_x, max_y):
    '''
    ������� �������������� ���� � ����� �����
    '''
    x = scale_x(ball.x, max_x)
    y = scale_y(ball.y, max_y)
    r = scale_x(ball.r, max_x)
    screen.coords(ball_id, x - r, y - r, x + r, y + r)


   

ball = bod.body(1, 20/100, 370/100, 0, 0, 10/100, 'blue')
main_surf = surf.surface()
start = False
pause = False
moving = False
pnum = 0



def scale_ball_x(value):
    '''
    ����������� ���� �� ��� � � �������������� ����� �� ������ ����������
    '''
    global ball
    if not start:
        ball.x = float(value)
        redraw_ball(main_screen, ball, max_ox, max_oy)

def scale_ball_y(value):
    '''
    ����������� ���� �� ��� � � �������������� ����� �� ������ ����������
    '''    
    global ball
    if not start:
        ball.y = float(value)
        redraw_ball(main_screen, ball, max_ox, max_oy)

#�������� ������ ����������
frame_right = tk.LabelFrame(root, text = '������ ����������')
frame_right.place(x = window_width + 5, y = 0, width = 800 - window_width - 5, height = 600)


body_frame = tk.LabelFrame(frame_right, text = '��������� ����')
body_frame.pack(side = 'top', fill = tk.X)

#����������
x_lbl = tk.Label(body_frame, text = '�') 
x_lbl.pack(side = 'top')
x_sc = tk.Scale(body_frame, orient='horizontal', from_ = 2 * ball.r, to = max_ox - ball.r, resolution = 0.1, command = scale_ball_x, troughcolor = "blue")
x_sc.set(ball.x)
x_sc.pack(side = 'top', fill = tk.X)

y_lbl = tk.Label(body_frame, text = 'Y') 
y_lbl.pack(side = 'top')
y_sc = tk.Scale(body_frame, orient='horizontal', from_ = ball.r, to = max_oy - 2 * ball.r, resolution = 0.1, command = scale_ball_y, troughcolor = "blue")
y_sc.set(ball.y)
y_sc.pack(side = 'top', fill = tk.X)




mod_frame = tk.LabelFrame(frame_right, text = '����������')
mod_frame.pack(side = 'bottom')

# ������ ����������
# �����
def start_click():
    '''
    ������ �������� ���� ��� ������� �� ������ �����
    '''
    global start, pause
    # ���������� �� ����� ������������� ���� ��������� ��������� ����
    x_sc.config(state = tk.DISABLED, troughcolor = "grey")
    y_sc.config(state = tk.DISABLED, troughcolor = "grey")
    pause = False
    # ��������� �������
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    ball.Vx = 0
    ball.Vy = 0
    start = True



# �����
def pause_click():
    '''
    ����� �������� ������������� �������� ����
    '''
    global pause
    if start:
        pause = not pause



# ����
def stop_click():
    '''
    ��������� �������� ������������� �������� ����
    '''
    global start, pause
    # ��������� ���� ���������� ��������� ���������� ����
    x_sc.config(state = tk.ACTIVE, troughcolor = "blue")
    y_sc.config(state = tk.ACTIVE, troughcolor = "blue")    
    pause = True
    ball.x = x_sc.get()
    ball.y = y_sc.get()
    redraw_ball(main_screen, ball, max_ox, max_oy)
    ball.Vx = 0
    ball.Vy = 0
    start = False

# ������ ���������� �������������� ��������
start_btn = tk.Button(mod_frame, text = "�����", command = start_click)
start_btn.pack(side = 'left')
pause_btn = tk.Button(mod_frame, text = "�����", command = pause_click)
pause_btn.pack(side = 'left')
stop_btn = tk.Button(mod_frame, text = "����", command = stop_click)
stop_btn.pack(side = 'left')

# �������������� ������ ����������� � �������� ��������
def takepoint(event):
    '''
    ����� ������� ����������� ��� ������� ����� ������� ����
    '''
    global pnum, moving
    # ����� �������� ������ ��� �������������
    if not start:
        # ����������� �������
        for p in points_id:
            px1, py1, px2, py2 = main_screen.coords(p) 
            if px1 <= event.x and px2 >= event.x and py1 <= event.y and py2>= event.y:
                pnum = points_id.index(p)
                #���������� �� �����������
                moving = True

def movepoint(event):
    '''
    ����������� ������� ����������� ��� �������� ��������� ����
    '''
    # ���� ��������� �����������, �� ������� ������������ �� ���������� ����. 
    if moving:
        main_screen.coords(points_id[pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
        # ����������� ����������� (��� ��������� ���������� ���������)
        redraw_surface(main_screen)
        
def droppoint(event):
    '''
    ��������� ����������� ������� ����������� ��� ���������� ����� ������� ����
    '''
    global pnum, moving, main_surf
    if moving:
        main_screen.coords(points_id[pnum], event.x - 3, event.y - 3, event.x + 3, event.y + 3)
        # ����������� ���������� ��������� �������
        nx = inv_scale_x(event.x, max_ox)
        ny = inv_scale_y(event.y, max_oy)
        # �������� ��������� ���������� ��������� ��������� ���� �� ������ ������ �� ��� �
        if pnum > 0 and pnum < len(points_id) - 1:
            if nx < main_surf.points[pnum - 1].x:
                nx = main_surf.points[pnum - 1].x
            if nx > main_surf.points[pnum + 1].x:
                nx = main_surf.points[pnum + 1].x            
       #���������� ���������� ��������� 
        main_surf.points[pnum].x = nx 
        main_surf.points[pnum].y = ny
        #������ ����������� ����������� � ������ ���������� ���������
        full_redraw_surface(main_screen, main_surf, max_ox, max_oy)
        moving = False
    

main_screen.bind('<Button-1>', takepoint)
main_screen.bind('<ButtonRelease-1>', droppoint)
main_screen.bind('<Motion>', movepoint)   


def new_sim(event=''):
    # �������� ����������
    main_surf.addpoint(surf.point(5/100, 350/100, 0.2, 'black'))
    main_surf.addpoint(surf.point(100/100, 250/100, -1, 'green')) #������� � ������������� ������� - �������� ����
    main_surf.addpoint(surf.point(150/100, 250/100, 0.1, 'blue'))
    main_surf.addpoint(surf.point(200/100, 280/100, 0.1, 'blue'))
    main_surf.addpoint(surf.point(350/100, 300/100, 0.1, 'gray'))
    main_surf.addpoint(surf.point(400/100, 150/100, 0.1, 'gray'))
    main_surf.addpoint(surf.point(480/100, 120/100, 0.1, 'gray'))
    main_surf.addpoint(surf.point(550/100, 3/100, 0.1, 'green'))
 

    
    main_screen.create_rectangle(0, 0, window_width, window_height)
    init_surface(main_screen, main_surf, max_ox, max_oy)
    init_ball(main_screen, ball, max_ox, max_oy)
    while main_surf:
        if start and not pause:
            model.move_body(ball, main_surf, 9.8, 0.02, max_ox)
            redraw_ball(main_screen, ball, max_ox, max_oy)
          
        main_screen.update() #���������� �������� ����
        time.sleep(0.02) #�����

new_sim()
root.mainloop()



