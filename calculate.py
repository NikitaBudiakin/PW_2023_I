import numpy as np
from sympy import *

 # створення глобальних змінних

r = symbols('r')
equations = []


def max(current_max, value, current_loc, value_loc): # функція для знаходження максимальних значень ті їх локації
    max = [current_max, current_loc]
    if abs(value) > current_max:
        max[0] = value
        max[1] = value_loc
    return max


def distributed_force(r1, q1, r2, q2): # функція для задання нормального тиску у символьній формі
    global r
    q = (r - r1)/(r2 - r1)*(q2 - q1) + q1
    return q


def Qr(w, D): # функція для задання перерізуючого зусилля
    global r
    return -D * diff(diff(w, r, 2) + 1 / r * diff(w, r), r)


def Mr(w, D, v): # функція для задання радіального моменту
    global r
    return -D * (diff(w, r, 2) + v / r * diff(w, r))


def boundary_conditions(w1, D1, w2, D2, a, b, c, v, equations, picked_fixations, picked_load, load_value, load_loc):  
    # функція для складання системи рівнянь
    equations.clear()

    equations.append((w1 - w2).subs(r, b))
    equations.append((diff(w1, r) - diff(w2, r)).subs(r, b))
    equations.append((Mr(w1, D1, v) - Mr(w2, D2, v)).subs(r, b))


    #________________________ЛІВИЙ_КРАЙ________________________#


    if a != 0:

        if picked_fixations[0] == 'Шарнірна опора':
            equations.append(w1.subs(r, a))
            equations.append(Mr(w1, D1, v).subs(r, a))

            if load_loc == 'a':
                if picked_load == 'Перерізуюча сила':
                    equations.append((Qr(w1, D1) - load_value).subs(r, a))

        elif picked_fixations[0] == 'Жорстке защемлення':
            equations.append(w1.subs(r, a))
            equations.append(diff(w1, r).subs(r, a))

            if load_loc == 'a':
                if picked_load == 'Перерізуюча сила':
                    equations.append((Qr(w1, D1) - load_value).subs(r, a))
                elif picked_load == 'Радіальний момент':
                    equations.append((Mr(w1, D1, v) - load_value).subs(r, a))

        elif picked_fixations[0] == '-':

            if load_loc == 'a':
                if picked_load == 'Перерізуюча сила':
                    equations.append((Qr(w1, D1) - load_value).subs(r, a))
                    equations.append(Mr(w1, D1, v).subs(r, a))
                elif picked_load == 'Радіальний момент':
                    equations.append((Mr(w1, D1, v) - load_value).subs(r, a))
                    equations.append(Qr(w1, D1).subs(r, a))
            else:
                equations.append(Qr(w1, D1).subs(r, a))
                equations.append(Mr(w1, D1, v).subs(r, a))

    
    #________________________СЕРЕДИНА________________________#


    if picked_fixations[1] == 'Шарнірна опора':
        equations.append(w1.subs(r, b))
    elif picked_fixations[1] == '-':

        if load_loc == 'b':
            if picked_load == 'Перерізуюча сила':
                equations.append((Qr(w2, D2) - load_value).subs(r, b))
        elif picked_fixations[0] == '-' or picked_fixations[2] == '-':
            equations.append((Qr(w1, D1) - Qr(w2, D2)).subs(r, b))


    #________________________ПРАВИЙ_КРАЙ________________________#


    if picked_fixations[2] == 'Шарнірна опора':
        equations.append(w2.subs(r, c))
        equations.append(Mr(w2, D1, v).subs(r, c))

        if load_loc == 'c':
            if picked_load == 'Перерізуюча сила':
                equations.append((Qr(w2, D2) - load_value).subs(r, c))
        
    elif picked_fixations[2] == 'Жорстке защемлення':
        equations.append(w2.subs(r, c))
        equations.append(diff(w2, r).subs(r, c))

        if load_loc == 'c':
            if picked_load == 'Перерізуюча сила':
                equations.append((Qr(w2, D2) - load_value).subs(r, c))
            elif picked_load == 'Радіальний момент':
                equations.append((Mr(w2, D2, v) - load_value).subs(r, c))
        
    elif picked_fixations[2] == '-':

        if load_loc == 'c':
            if picked_load == 'Перерізуюча сила':
                equations.append((Qr(w2, D2) - load_value).subs(r, c))
                equations.append(Mr(w2, D2, v).subs(r, c))
            elif picked_load == 'Радіальний момент':
                equations.append(Qr(w2, D1).subs(r, c))
                equations.append((Mr(w2, D2, v) - load_value).subs(r, c))
        else:
            equations.append(Qr(w2, D1).subs(r, c))
            equations.append(Mr(w2, D2, v).subs(r, c))
    

def calc(h1, h2, a, b, c, E, v, distributed_load_1_values, distributed_load_2_values, picked_fixations, picked_load, load_value, load_loc):  
    # основна функція для обчислення
    global equations, r

    E = E * 100000000000    # модуль Юнга

    D1 = E * (h1 ** 3) / (12 * (1 - v ** 2))    # жорсткість згину пластини на ділянці I
    D2 = E * (h2 ** 3) / (12 * (1 - v ** 2))    # жорсткість згину пластини на ділянці II

    C1, C2, C3, C4, C5, C6, C7, C8 = symbols('C1,C2,C3,C4,C5,C6,C7,C8')    # символьні змінні для констант інтегрування

    # знаходження загальних рішень для переміщень на
        # ділянці І

    w1 = distributed_force(a, distributed_load_1_values[0], b, distributed_load_1_values[1]) * r / D1
    w1 = (integrate(w1, r) + C1) / r
    w1 = (integrate(w1, r) + C2) * r
    w1 = (integrate(w1, r) + C3) / r
    w1 = integrate(w1, r) + C4

        # ділянці ІІ

    w2 = distributed_force(b, distributed_load_2_values[0], c, distributed_load_2_values[1]) * r / D2
    w2 = (integrate(w2, r) + C5) / r
    w2 = (integrate(w2, r) + C6) * r
    w2 = (integrate(w2, r) + C7) / r
    w2 = integrate(w2, r) + C8

    # позбуваємось доданків з логарифмами, у випадку пластини без отвору

    if a == 0:
        w1 = w1.subs([(C1, 0), (C3, 0)])

    # складаємо систему рівнянь відносно констант інтегрування

    boundary_conditions(w1, D1, w2, D2, a, b, c, v, equations, picked_fixations, picked_load, load_value, load_loc)

    try:
        # вирішуємо систему рівнянь
        if a == 0:
            solution = solve([equations[0], equations[1], equations[2], equations[3], equations[4], equations[5]], [C2, C4, C5, C6, C7, C8])
            w1 = w1.subs([(C2, solution[C2]), (C4, solution[C4])])
            w2 = w2.subs([(C5, solution[C5]), (C6, solution[C6]), (C7, solution[C7]), (C8, solution[C8])])
        else:
            solution = solve([equations[0], equations[1], equations[2], equations[3], equations[4], equations[5], equations[6], equations[7]], [C1, C2, C3, C4, C5, C6, C7, C8])
            w1 = w1.subs([(C1, solution[C1]), (C2, solution[C2]), (C3, solution[C3]), (C4, solution[C4])])
            w2 = w2.subs([(C5, solution[C5]), (C6, solution[C6]), (C7, solution[C7]), (C8, solution[C8])])


        l1 = np.linspace(a, b, int((b - a) * 100))
        l2 = np.linspace(b, c, int((c - b) * 100))

        Qr1 = np.zeros(len(l1))
        Qr2 = np.zeros(len(l2))

        W1 = np.zeros(len(l1))
        W2 = np.zeros(len(l2))

        Mr1 = np.zeros(len(l1))
        Mr2 = np.zeros(len(l2))

        M_theta1 = np.zeros(len(l1))
        M_theta2 = np.zeros(len(l2))

        max_W = 0
        max_Qr = 0
        max_Mr = 0
        max_M_theta = 0
        max_W_loc = 0
        max_Qr_loc = 0
        max_Mr_loc = 0
        max_M_theta_loc = 0

        # знаходимо значення переміщень, перерізуючого зусилля, радіального моменту, окружного моменту та відповідних екстремумів

        for i in range(0, len(l1)):
                W1[i] = w1.subs(r, l1[i])

                if abs(W1[i]) > abs(max_W):
                    max_W = W1[i]
                    max_W_loc = l1[i]

                Qr1[i] = (-D1 * diff((diff(diff(w1, r), r) + diff(w1, r) / r), r)).subs(r, l1[i])

                if abs(Qr1[i]) > abs(max_Qr):
                    max_Qr = Qr1[i]
                    max_Qr_loc = l1[i]

                Mr1[i] = (-D1 * (diff(diff(w1, r), r) + v / r * diff(w1, r))).subs(r, l1[i])

                if abs(Mr1[i]) > abs(max_Mr):
                    max_Mr = Mr1[i]
                    max_Mr_loc = l1[i]

                M_theta1[i] = (-D1 * (v * diff(diff(w1, r), r) + 1 / r * diff(w1, r))).subs(r, l1[i])

                if abs(M_theta1[i]) > abs(max_M_theta):
                    max_M_theta = M_theta1[i]
                    max_M_theta_loc = l1[i]


        for i in range(0, len(l2)):
                W2[i] = w2.subs(r, l2[i])

                if abs(W2[i]) > abs(max_W):
                    max_W = W2[i]
                    max_W_loc = l2[i]

                Qr2[i] = (-D2 * diff((diff(diff(w2, r), r) + diff(w2, r) / r), r)).subs(r, l2[i])

                if abs(Qr2[i]) > abs(max_Qr):
                    max_Qr = Qr2[i]
                    max_Qr_loc = l2[i] 

                Mr2[i] = (-D2 * (diff(diff(w2, r), r) + v / r * diff(w2, r))).subs(r, l2[i])

                if abs(Mr2[i]) > abs(max_Mr):
                    max_Mr = Mr2[i]
                    max_Mr_loc = l2[i] 

                M_theta2[i] = (-D2 * (v * diff(diff(w2, r), r) + 1 / r * diff(w2, r))).subs(r, l2[i])

                if abs(M_theta2[i]) > abs(max_M_theta):
                    max_M_theta = M_theta2[i]
                    max_M_theta_loc = l2[i] 

        extr = [max_W, max_Qr, max_Mr, max_M_theta, max_W_loc, max_Qr_loc, max_Mr_loc, max_M_theta_loc, l1, l2, W1, W2, Qr1, Qr2, Mr1, Mr2, M_theta1, M_theta2]

    except:
        return [0, 0, 0, 0, 0, 0, 0]

    return extr
    
