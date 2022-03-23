import tkinter as tk
from math import cos, sin, pi

w = tk.Tk()
w.title('qomp')

size = 800
canvas = tk.Canvas(w, width=size, height=size)
canvas.pack()

def cube(s):
    return [
        [-s,-s, s], [-s, s, s], [ s, s, s], [ s,-s, s],
        [-s,-s,-s], [-s, s,-s], [ s, s,-s], [ s,-s,-s],
        [ s,-s, s], [ s, s, s], [ s, s,-s], [ s,-s,-s],
        [-s,-s,-s], [ s,-s,-s], [ s,-s, s], [-s,-s, s],
        [-s,-s,-s], [-s,-s, s], [-s, s, s], [-s, s,-s],
        [ s, s, s], [ s, s,-s], [-s, s,-s], [-s, s, s]
    ]

def main():
    a = 0
    b = 0
    loop(a, b)
    

def loop(a, b):
    canvas.delete('all')
    
    c = cube(.3 * size)
    m = multiply_matrices(translation(.5*size, .5*size, 0), multiply_matrices(rotation_x(a), rotation_y(b)))
    
    for i in range(6*4):
        c[i] = apply_matrix(m, [c[i][0], c[i][1], c[i][2], 1])
    
    for i in range(6):
        canvas.create_line(c[4*i + 0][0], c[4*i + 0][1], c[4*i + 1][0], c[4*i + 1][1])
        canvas.create_line(c[4*i + 1][0], c[4*i + 1][1], c[4*i + 2][0], c[4*i + 2][1])
        canvas.create_line(c[4*i + 2][0], c[4*i + 2][1], c[4*i + 3][0], c[4*i + 3][1])
        canvas.create_line(c[4*i + 3][0], c[4*i + 3][1], c[4*i + 0][0], c[4*i + 0][1])

    a += pi/200
    b += pi/100
    canvas.after(10, loop, a, b)

def identity():
    return [
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
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

def multiply_matrices(m1, m2):
    result = [0 for i in range(16)]
    for i in range(4):
        for j in range(4):
            result[4*j + i] =\
                m1[4*j + 0] * m2[i + 0] +\
                m1[4*j + 1] * m2[i + 4] +\
                m1[4*j + 2] * m2[i + 8] +\
                m1[4*j + 3] * m2[i + 12]
    return result

main()
