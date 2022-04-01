import tkinter as tk
from math import cos, sin, pi
from random import randint

w = tk.Tk()
w.config(bg='black')
w.title('le cube')

size = 1000

canvas = tk.Canvas(w, width=size, height=size, bg='black')
canvas.pack()

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def cube(s):
    return [
        (-s,-s, s), (-s, s, s), ( s,-s, s), # Front
        (-s, s, s), ( s, s, s), ( s,-s, s),

        ( s,-s,-s), ( s, s,-s), (-s,-s,-s), # Back
        ( s, s,-s), (-s, s,-s), (-s,-s,-s),

        (-s, s, s), (-s, s,-s), ( s, s, s), # Top
        (-s, s,-s), ( s, s,-s), ( s, s, s),

        (-s,-s,-s), (-s,-s, s), ( s,-s,-s), # Bottom
        (-s,-s, s), ( s,-s, s), ( s,-s,-s),

        ( s,-s, s), ( s, s, s), ( s,-s,-s), # Right
        ( s, s, s), ( s, s,-s), ( s,-s,-s),

        (-s,-s,-s), (-s, s,-s), (-s,-s, s), # Left
        (-s, s,-s), (-s, s, s), (-s,-s, s)
    ]

def color(n):
    return ['#' + ''.join(['0123456789abcdef'[randint(0, 15)] for _ in range(6)]) for _ in range(n)]

def update_pos(key, pos, w_size, p_size):
    if key == 'Right':  pos.x = (w_size - p_size + pos.x + p_size) % (2 *  w_size - p_size)  - w_size + p_size
    elif key == 'Left': pos.x = (w_size - p_size + pos.x - p_size) % (2 * (w_size - p_size)) - w_size + p_size
    elif key == 'Up':   pos.y = (w_size - p_size + pos.y + p_size) % (2 *  w_size - p_size)  - w_size + p_size
    elif key == 'Down': pos.y = (w_size - p_size + pos.y - p_size) % (2 * (w_size - p_size)) - w_size + p_size

def main():
    w_size = .3 * size
    p_size = .05 * size

    world_buff = cube(w_size)
    world_color_buff = ['#696969' for _ in range(len(world_buff)//3)]

    pos = Point(0, 0, w_size + p_size)
    player_buff = cube(p_size)
    player_color_buff = color(len(player_buff)//3)
    
    alpha = pi/2
    a = 0
    b = 0

    w.bind('<Key>', lambda key: update_pos(key.keysym, pos, w_size, p_size))

    update(pos, player_buff, player_color_buff, world_buff, world_color_buff, a, b)
    w.mainloop()

def update(pos, player_buff, player_color_buff, world_buff, world_color_buff, a, b):
    canvas.delete('all')

    m = multiply_matrices()
    player_m = multiply_matrices(m, translation(pos.x, pos.y, pos.z))
    
    draw(world_buff, world_color_buff, m)
    draw(player_buff, player_color_buff, player_m)

    #alpha += pi/64
    a += pi/256
    #b += pi/128
    canvas.after(20, update, pos, player_buff, player_color_buff, world_buff, world_color_buff, a, b)

def draw(vertex_buff, color_buff, matrix):
    buff = []
    
    for i in range(len(vertex_buff)):
        v = apply_matrix(matrix, [vertex_buff[i][0], vertex_buff[i][1], vertex_buff[i][2], 1])
        z = 2 - 2*v[2]/size * .8
        v[0] /= z
        v[1] /= z
        buff.append(apply_matrix(projection(size//2, size//2, size//2), v))

    for i in range(0, len(vertex_buff), 3):
        nz = z_normal(buff[i + 0], buff[i + 1], buff[i + 2])
        if nz <= 0: continue

        canvas.create_polygon(buff[i + 0][0], buff[i + 0][1],
                              buff[i + 1][0], buff[i + 1][1],
                              buff[i + 2][0], buff[i + 2][1],
                              fill=color_buff[i//3])

        canvas.create_line(buff[i + 0][0], buff[i + 0][1], buff[i + 1][0], buff[i + 1][1], fill='white')
        canvas.create_line(buff[i + 1][0], buff[i + 1][1], buff[i + 2][0], buff[i + 2][1], fill='white')
        canvas.create_line(buff[i + 2][0], buff[i + 2][1], buff[i + 0][0], buff[i + 0][1], fill='white')

def projection(width, height, depth):
    return [
        1, 0, 0, width,
        0, -1, 0, height,
        0, 0, 1, depth,
        0, 0, 0, 1
    ]

def translation(dx, dy, dz):
    return [
        1, 0, 0, dx,
        0, 1, 0, dy,
        0, 0, 1, dz,
        0, 0, 0, 1
    ]

def rotation_x(a):
    c = cos(a)
    s = sin(a)
    return [
        1, 0, 0, 0,
        0, c, s, 0,
        0, -s, c, 0,
        0, 0, 0, 1
    ]

def rotation_y(a):
    c = cos(a)
    s = sin(a)
    return [
        c, 0, s, 0,
        0, 1, 0, 0,
        -s, 0, c, 0,
        0, 0, 0, 1
    ]

def rotation_z(a):
    c = cos(a)
    s = sin(a)
    return [
        c, s, 0, 0,
        -s, c, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    ]

def apply_matrix(m, v):
    result = []
    for i in range(4):
        result.append(
            m[4*i + 0] * v[0] +
            m[4*i + 1] * v[1] +
            m[4*i + 2] * v[2] +
            m[4*i + 3] * v[3]
        )
    return result

def multiply_matrices(*m):
    if len(m) == 0:
        return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    result = m[0]
    for i in range(1, len(m)):
        result = _multiply_matrices(result, m[i])
    return result


def _multiply_matrices(m1, m2):
    result = [0 for _ in range(16)]
    for i in range(4):
        for j in range(4):
            result[4*j + i] =\
                m1[4*j + 0] * m2[i + 0] +\
                m1[4*j + 1] * m2[i + 4] +\
                m1[4*j + 2] * m2[i + 8] +\
                m1[4*j + 3] * m2[i + 12]
    return result

def z_normal(A, B, C):
    ABx, ABy = B[0] - A[0], B[1] - A[1]
    ACx, ACy = C[0] - A[0], C[1] - A[1]
    
    z = ABx*ACy - ABy*ACx
    return z

main()
