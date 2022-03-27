import tkinter as tk
from math import cos, sin, pi
from random import randint

w = tk.Tk()
w.config(bg='black')
w.title('le cube')

size = 800

canvas = tk.Canvas(w, width=size, height=size, bg='black')
canvas.pack()

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

def main():
    vertex_buff = cube(.3 * size)
    color_buff = ['#' + ''.join(['0123456789abcdef'[randint(0, 15)] for _ in range(6)]) for _ in range(len(vertex_buff)//3)]
    
    alpha = pi/2
    a = 0
    b = 0

    update(vertex_buff, color_buff, alpha, a, b)
    w.mainloop()

def update(vertices, color_buff, alpha, a, b):
    canvas.delete('all')

    dx = 300*cos(alpha)
    dy = 300*sin(alpha)
    m = multiply_matrices(translation(dx, dy, 0), rotation_x(a), rotation_y(b))
    buff = []

    for i in range(len(vertices)):
        v = apply_matrix(m, [vertices[i][0], vertices[i][1], vertices[i][2], 1])
        z = 2 + 2*v[2]/size * .8
        v[0] /= z
        v[1] /= z
        buff.append(apply_matrix(projection(size//2, size//2, size//2), v))
    
    for i in range(0, len(vertices), 3):
        nz = z_normal(buff[i + 0], buff[i + 1], buff[i + 2])
        if nz >= 0: continue

        canvas.create_polygon(buff[i + 0][0], buff[i + 0][1],
                              buff[i + 1][0], buff[i + 1][1],
                              buff[i + 2][0], buff[i + 2][1],
                              fill=color_buff[i//3])

        #canvas.create_line(buff[i + 0][0], buff[i + 0][1], buff[i + 1][0], buff[i + 1][1], fill='white')
        #canvas.create_line(buff[i + 1][0], buff[i + 1][1], buff[i + 2][0], buff[i + 2][1], fill='white')
        #canvas.create_line(buff[i + 2][0], buff[i + 2][1], buff[i + 0][0], buff[i + 0][1], fill='white')

    alpha += pi/64
    a += pi/256
    b += pi/128
    canvas.after(20, update, vertices, color_buff, alpha, a, b)

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