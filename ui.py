import tkinter as tk
from threading import Event, Thread
from time import sleep
from tkinter import messagebox as mb
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np

from calculate import calc

# глобальні змінні, що тримають значення вхідних даних

picked_load = '-'
load_loc = '-'
picked_fixations = ['-', '-', '-']
load_value = 0
distributed_load_1_values = [0, 0]
distributed_load_2_values = [0, 0]
h1 = 0.0
h2 = 0.0
a = 0.0
b = 0.0
c = 0.0
E = 0.0
v = 0.0

# створення глобальних елементів інтерфейсу

window = tk.Tk()
fixation_variants = ['-', 'Шарнірна опора', 'Жорстке защемлення']
fixation_variants_box_1 = ttk.Combobox(window, values=fixation_variants, state="readonly")
fixation_variants_box_2 = ttk.Combobox(window, values=[fixation_variants[0], fixation_variants[1]], state="readonly")
fixation_variants_box_3 = ttk.Combobox(window, values=fixation_variants, state="readonly")

load_variants = ['-', 'Перерізуюча сила', 'Радіальний момент']
location_variants = ['a', 'b', 'c', '-']
load_variants_box = ttk.Combobox(window, values=load_variants, state="readonly")
load_loc_variants_box = ttk.Combobox(window, values=location_variants, state="readonly")
load_entry = tk.Entry(window, width=7)
q1_0_entry = tk.Entry(window, width=7)
q1_a_entry = tk.Entry(window, width=7)
q2_a_entry = tk.Entry(window, width=7)
q2_b_entry = tk.Entry(window, width=7)

h1_entry = tk.Entry(window, width=7)
h2_entry = tk.Entry(window, width=7)
a_entry = tk.Entry(window, width=7)
b_entry = tk.Entry(window, width=7)
c_entry = tk.Entry(window, width=7)
E_entry = tk.Entry(window, width=7)
v_entry = tk.Entry(window, width=7)

baseScheme1 = tk.PhotoImage(file='resources/2.png')
baseScheme2 = tk.PhotoImage(file='resources/1.png')
baseScheme3 = tk.PhotoImage(file='resources/3.png')
baseScheme4 = tk.PhotoImage(file='resources/2_1.png')
baseScheme5 = tk.PhotoImage(file='resources/1_1.png')
baseScheme6 = tk.PhotoImage(file='resources/3_1.png')
baseScheme = [baseScheme1, baseScheme2, baseScheme3, baseScheme4, baseScheme5, baseScheme6]

hinge1 = tk.PhotoImage(file='resources/hinge1.png')
hinge2 = tk.PhotoImage(file='resources/hinge2.png')
hinge3 = tk.PhotoImage(file='resources/hinge3.png')
hinge = [hinge1, hinge2, hinge3]

stiff_fixation1 = tk.PhotoImage(file='resources/stiff1.png')
stiff_fixation3 = tk.PhotoImage(file='resources/stiff3.png')
stiff_fixation = [stiff_fixation1, stiff_fixation3]

force1plus = tk.PhotoImage(file='resources/force1+.png')
force1_1plus = tk.PhotoImage(file='resources/force1_1+.png')
force1minus = tk.PhotoImage(file='resources/force1-.png')
force1_1minus = tk.PhotoImage(file='resources/force1_1-.png')
force2plus = tk.PhotoImage(file='resources/force2+.png')
force2minus = tk.PhotoImage(file='resources/force2-.png')
force3plus = tk.PhotoImage(file='resources/force3+.png')
force3minus = tk.PhotoImage(file='resources/force3-.png')
force = [force1plus, force1_1plus, force1minus, force1_1minus, force2plus, force2minus, force3plus, force3minus]

moment1plus = tk.PhotoImage(file='resources/moment1+.png')
moment1_1plus = tk.PhotoImage(file='resources/moment1_1+.png')
moment1minus = tk.PhotoImage(file='resources/moment1-.png')
moment1_1minus = tk.PhotoImage(file='resources/moment1_1-.png')
moment2plus = tk.PhotoImage(file='resources/moment2+.png')
moment2minus = tk.PhotoImage(file='resources/moment2-.png')
moment3plus = tk.PhotoImage(file='resources/moment3+.png')
moment3minus = tk.PhotoImage(file='resources/moment3-.png')
moment = [moment1plus, moment1_1plus, moment1minus, moment1_1minus, moment2plus, moment2minus, moment3plus, moment3minus]

blank = tk.PhotoImage(file='resources/blank.png')
axis = tk.PhotoImage(file='resources/axis.png')

schemeCanvas = tk.Canvas(window, bg="white", width=295, height=195)
axis_on_canvas = schemeCanvas.create_image(0, 0, image=axis, anchor=tk.NW)
scheme_on_canvas = schemeCanvas.create_image(0, 0, image=blank, anchor=tk.NW)
force_on_canvas = schemeCanvas.create_image(0, 0, image=blank, anchor=tk.NW)
fixation1_on_canvas = schemeCanvas.create_image(0, 0, image=blank, anchor=tk.NW)
fixation2_on_canvas = schemeCanvas.create_image(0, 0, image=blank, anchor=tk.NW)
fixation3_on_canvas = schemeCanvas.create_image(0, 0, image=blank, anchor=tk.NW)


def update_scheme(): # функція для оновлення схеми конструкції
    global picked_load, picked_fixations, load_loc, load_value, a, b, c, h1, h2, fixation1_on_canvas, fixation2_on_canvas, fixation3_on_canvas
    global schemeCanvas, baseScheme, hinge, stiff_fixation, force, moment, scheme_on_canvas, force_on_canvas, blank
    while True:
        sleep(0.5)

        if a == 0:
            if h1 > h2:
                schemeCanvas.itemconfig(scheme_on_canvas, image=baseScheme[1])
            elif h1 < h2:
                schemeCanvas.itemconfig(scheme_on_canvas, image=baseScheme[2])
            else:
                schemeCanvas.itemconfig(scheme_on_canvas, image=baseScheme[0])

            if load_loc == 'a':
                if picked_load == 'Перерізуюча сила':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[0])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[2])
                elif picked_load == 'Радіальний момент':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[2])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[0])

            schemeCanvas.itemconfig(fixation1_on_canvas, image=blank)
        else:
            if h1 > h2:
                schemeCanvas.itemconfig(scheme_on_canvas, image=baseScheme[4])
            elif h1 < h2:
                schemeCanvas.itemconfig(scheme_on_canvas, image=baseScheme[5])
            else:
                schemeCanvas.itemconfig(scheme_on_canvas, image=baseScheme[3])

            if picked_fixations[0] == 'Шарнірна опора':
                schemeCanvas.itemconfig(fixation1_on_canvas, image=hinge[0])
            elif picked_fixations[0] == 'Жорстке защемлення':
                schemeCanvas.itemconfig(fixation1_on_canvas, image=stiff_fixation[0])
            elif picked_fixations[0] == '-':
                schemeCanvas.itemconfig(fixation1_on_canvas, image=blank)

            if load_loc == 'a':
                if picked_load == 'Перерізуюча сила':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[1])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[3])
                    elif load_value == 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=blank)
                elif picked_load == 'Радіальний момент':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[1])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[3])
                    elif load_value == 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=blank)

        
        if picked_fixations[1] == 'Шарнірна опора':
            schemeCanvas.itemconfig(fixation2_on_canvas, image=hinge[1])
        elif picked_fixations[1] == '-':
            schemeCanvas.itemconfig(fixation2_on_canvas, image=blank)

        if picked_fixations[2] == 'Шарнірна опора':
            schemeCanvas.itemconfig(fixation3_on_canvas, image=hinge[2])
        elif picked_fixations[2] == 'Жорстке защемлення':
            schemeCanvas.itemconfig(fixation3_on_canvas, image=stiff_fixation[1])
        elif picked_fixations[2] == '-':
            schemeCanvas.itemconfig(fixation3_on_canvas, image=blank)

        if load_loc == 'b':
                if picked_load == 'Перерізуюча сила':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[5])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[4])
                elif picked_load == 'Радіальний момент':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[4])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[5])
                    elif load_value == 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=blank)
        elif load_loc == 'c':
                if picked_load == 'Перерізуюча сила':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[7])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=force[6])
                elif picked_load == 'Радіальний момент':
                    if load_value > 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[6])
                    elif load_value < 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=moment[7])
                    elif load_value == 0:
                        schemeCanvas.itemconfig(force_on_canvas, image=blank)

        elif picked_load == '-':
            schemeCanvas.itemconfig(force_on_canvas, image=blank)

        if load_loc == '-':
            schemeCanvas.itemconfig(force_on_canvas, image=blank)


def clear(): # функція для очистки вхідних даних
    global picked_load, picked_fixations, load_loc, load_value, distributed_load_1_values, distributed_load_2_values, h1, h2, a, b, c, E, v
    picked_load = '-'
    load_loc = '-'
    picked_fixations = ['-', '-', '-']
    load_value = 0.0
    distributed_load_1_values = [0.0, 0.0]
    distributed_load_2_values = [0.0, 0.0]
    h1 = 0.0
    h2 = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    E = 0.0
    v = 0.0

    load_page_1()
    

def assign_fixation(event): # функція для задання умов закріплення
    global fixation_variants_box_1, fixation_variants_box_2
    while True:
        picked_fixations[0] = str(fixation_variants_box_1.get())
        picked_fixations[1] = str(fixation_variants_box_2.get())
        picked_fixations[2] = str(fixation_variants_box_3.get())
        sleep(0.02)
        if event.is_set():
            break


def assign_load(event): # функція для задання навантажень
    global load_variants_box, load_loc_variants_box, fixation_variants
    global load_entry, load_value, picked_load, load_loc
    global q1_0_entry, q1_a_entry, q2_a_entry, q2_b_entry
    while True:
        picked_load = str(load_variants_box.get())
        load_loc = str(load_loc_variants_box.get())

        try:
            load_value = float(load_entry.get())
            load_entry.configure(fg='black')
        except ValueError:
            load_entry.configure(fg='red')

        try:
            distributed_load_1_values[0] = float(q1_0_entry.get())
            q1_0_entry.configure(fg='black')
        except ValueError:
            q1_0_entry.configure(fg='red')

        try:
            distributed_load_1_values[1] = float(q1_a_entry.get())
            q1_a_entry.configure(fg='black')
        except ValueError:
            q1_a_entry.configure(fg='red')

        try:
            distributed_load_2_values[0] = float(q2_a_entry.get())
            q2_a_entry.configure(fg='black')
        except ValueError:
            q2_a_entry.configure(fg='red')

        try:
            distributed_load_2_values[1] = float(q2_b_entry.get())
            q2_b_entry.configure(fg='black')
        except ValueError:
            q2_b_entry.configure(fg='red')

        sleep(0.02)
        if event.is_set():
            break


def assign_value(event): # функція для задання числових характеристик конструкції
    global h1_entry, h2_entry, a_entry, b_entry, c_entry, E_entry, v_entry
    global h1, h2, a, b, c, E, v
    while True:
        try:
            h1 = float(h1_entry.get())
            h1_entry.configure(fg='black')
            if h1 <= 0:
                raise ValueError
        except ValueError:
            h1_entry.configure(fg='red')

        try:
            h2 = float(h2_entry.get())
            h2_entry.configure(fg='black')
            if h2 <= 0:
                raise ValueError
        except ValueError:
            h2_entry.configure(fg='red')

        try:
            a = float(a_entry.get())
            a_entry.configure(fg='black')
            if a < 0:
                raise ValueError
        except ValueError:
            a_entry.configure(fg='red')

        try:
            b = float(b_entry.get())
            b_entry.configure(fg='black')
            if b <= 0:
                raise ValueError
            elif b <= a:
                raise ValueError
        except ValueError:
            b_entry.configure(fg='red')

        try:
            c = float(c_entry.get())
            c_entry.configure(fg='black')
            if c <= 0:
                raise ValueError
            elif c <= b:
                raise ValueError
        except ValueError:
            c_entry.configure(fg='red')

        try:
            E = float(E_entry.get())
            E_entry.configure(fg='black')
            if E <= 0:
                raise ValueError
        except ValueError:
            E_entry.configure(fg='red')

        try:
            v = float(v_entry.get())
            v_entry.configure(fg='black')
            if v <= 0:
                raise ValueError
        except ValueError:
            v_entry.configure(fg='red')

        sleep(0.02)
        if event.is_set():
            break


def check_fixations(): # функція для перевірки правильності заданих умов закріплення
    global picked_fixations
    if picked_fixations[0] == '-' and picked_fixations[1] == '-' and picked_fixations[2] == '-':
        mb.showwarning('Увага', f'Задайте хоча б одне закріплення!', icon='error')
        return False
    else:
        return True


def check_data(page_number): # функція для перевірки числових значень 
    global load_entry
    global q1_0_entry, q1_a_entry, q2_a_entry, q2_b_entry
    global h1_entry, h2_entry, a_entry, b_entry, E_entry, v_entry

    h1_entry.configure(bg='white')
    h2_entry.configure(bg='white')
    b_entry.configure(bg='white')
    c_entry.configure(bg='white')

    if page_number == 2:
        try:
            float(load_entry.get())
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для навантаження при x=0!', icon='error')
            return False

        try:
            float(q1_0_entry.get())
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для розподіленого навантаження q1 при x=0!', icon='error')
            return False

        try:
            float(q1_a_entry.get())
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для розподіленого навантаження q1 при x=a!', icon='error')
            return False

        try:
            float(q2_a_entry.get())
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для розподіленого навантаження q2 при x=a!', icon='error')
            return False

        try:
            float(q2_b_entry.get())
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для розподіленого навантаження q2 при x=b!', icon='error')
            return False
        else:
            return True
    elif page_number == 3:
        try:
            float(h1_entry.get())
            if float(h1_entry.get()) < 0:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для товщини першої ділянки!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для товщини першої ділянки!', icon='error')
            return False

        try:
            float(h2_entry.get())
            if float(h2_entry.get()) <= 0:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для товщини другої ділянки!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для товщини другої ділянки!', icon='error')
            return False

        try:
            float(a_entry.get())
            if float(a_entry.get()) < 0:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для радіусу отвору!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для радіусу отвору!', icon='error')
            return False

        try:
            float(b_entry.get())
            if float(b_entry.get()) <= 0:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для довжини першої ділянки!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для довжини першої ділянки!', icon='error')
            return False

        try:
            float(b_entry.get())
            if float(b_entry.get()) <= float(a_entry.get()):
                raise Warning
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для довжини першої ділянки! Довжина повинна бути більше радіусу отвору.', icon='error')
            return False

        try:
            float(b_entry.get())
            temp = float(h1_entry.get()) / float(b_entry.get())
            if temp > 0.05:
                raise Warning
        except Warning:
            mb.showwarning('Увага', f'Відношення товщини ділянки №1 до довжини не має перевищувати 0.05. Маємо: {temp}', icon='error')
            h1_entry.configure(bg='orange')
            b_entry.configure(bg='orange')
            return False

        try:
            float(c_entry.get())
            if float(c_entry.get()) <= 0:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для загальної довжини!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для загальної довжини!', icon='error')
            return False

        try:
            if float(c_entry.get()) <= float(b_entry.get()):
                raise Warning
        except Warning:
            mb.showwarning('Увага', f'Загальна довжина не може бути менше або дорівнювати довжині першої ділянки!', icon='error')
            return False

        try:
            float(c_entry.get())
            temp = float(h2_entry.get()) / (float(c_entry.get()) - float(b_entry.get()))
            if temp > 0.05:
                raise Warning
        except Warning:
            mb.showwarning('Увага', f'Відношення товщини ділянки №2 до довжини не має перевищувати 0.05. Маємо: {temp}', icon='error')
            h2_entry.configure(bg='orange')
            b_entry.configure(bg='orange')
            c_entry.configure(bg='orange')
            return False

        try:
            float(E_entry.get())
            if float(E_entry.get()) <= 0:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для модуля пружності!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для модуля пружності!', icon='error')
            return False
    
        try:
            float(v_entry.get())
            if float(v_entry.get()) <= 0 or float(v_entry.get()) >= 0.5:
                raise Warning
        except ValueError:
            mb.showwarning('Увага', f'Невірний формат значення для коефіцієнта Пуасона!', icon='error')
            return False
        except Warning:
            mb.showwarning('Увага', f'Невірне значення для коефіцієнта Пуасона!', icon='error')
            return False
        else:
            return True
        

def check_load(event): # функція для перевірки правильності заданих навантажень
    global picked_fixations, load_loc, load_variants, load_loc_variants_box, location_variants, a
    while True:
        if picked_fixations[0] == 'Шарнірна опора' and load_loc == 'a':
            load_variants_box.configure(values=[load_variants[0], load_variants[1], location_variants[3]])
        elif picked_fixations[1] == 'Шарнірна опора' and load_loc == 'b':
            load_variants_box.configure(values=[load_variants[0], load_variants[1], location_variants[3]])
        elif picked_fixations[2] == 'Шарнірна опора' and load_loc == 'c':
            load_variants_box.configure(values=[load_variants[0], load_variants[1], location_variants[3]])
        else:
            load_variants_box.configure(values=load_variants)


        if a == 0:
            if picked_fixations[1] != '-' and picked_fixations[2] == '-':
                load_loc_variants_box.configure(values=[location_variants[2], location_variants[3]])
                if load_loc != 'c':
                    load_loc = 'c'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[1] == '-' and picked_fixations[2] != '-':
                load_loc_variants_box.configure(values=[location_variants[1], location_variants[3]])
                if load_loc != 'b':
                    load_loc = 'b'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[1] != '-' and picked_fixations[2] != '-':
                load_loc_variants_box.configure(values=[location_variants[3]])
                if load_loc != '-':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            else:
                load_loc_variants_box.configure(values=[location_variants[1], location_variants[2], location_variants[3]])
        else:
            if picked_fixations[0] != '-' and picked_fixations[1] == '-' and picked_fixations[2] == '-':
                load_loc_variants_box.configure(values=[location_variants[1], location_variants[2], location_variants[3]])
                if load_loc == 'a':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[0] == '-' and picked_fixations[1] != '-' and picked_fixations[2] == '-':
                load_loc_variants_box.configure(values=[location_variants[0], location_variants[2], location_variants[3]])
                if load_loc == 'b':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[0] == '-' and picked_fixations[1] == '-' and picked_fixations[2] != '-':
                load_loc_variants_box.configure(values=[location_variants[0], location_variants[1], location_variants[3]])
                if load_loc == 'c':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[0] != '-' and picked_fixations[1] != '-' and picked_fixations[2] == '-':
                load_loc_variants_box.configure(values=[location_variants[2], location_variants[3]])
                if load_loc != 'c':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[0] != '-' and picked_fixations[1] == '-' and picked_fixations[2] != '-':
                load_loc_variants_box.configure(values=[location_variants[1], location_variants[3]])
                if load_loc != 'b':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[0] == '-' and picked_fixations[1] != '-' and picked_fixations[2] != '-':
                load_loc_variants_box.configure(values=[location_variants[0], location_variants[3]])
                if load_loc != 'a':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            elif picked_fixations[0] != '-' and picked_fixations[1] != '-' and picked_fixations[2] != '-':
                load_loc_variants_box.configure(values=[location_variants[3]])
                if load_loc != '-':
                    load_loc = '-'
                    load_loc_variants_box.set(load_loc)
            else:
                load_loc_variants_box.configure(values=location_variants)


        sleep(0.05)
        if event.is_set():
            break


def init(): # функція для ініціалізації інтерфейсу
    global canvas
    window.geometry("780x420")
    window.resizable(False, False)
    window.wm_title("ОСЕСИМЕТРИЧНИЙ ЗГИН КРУГЛИХ ТА КІЛЬЦЕВИХ ПЛАСТИН")
    icon = tk.PhotoImage(file='resources\icon.png')
    window.iconphoto(False, icon)

    scheme_label = tk.Label(text="СХЕМА", font=("Cambria", 15))
    scheme_label.place(x=20, y=20)
    schemeCanvas.place(x=20, y=77)

    scheme_thread = Thread(target=update_scheme, args=(), daemon=True)
    scheme_thread.start()

    load_page_1()

    window.mainloop()
    

def load_page_1(): # функція для завантаження першої сторінки інтерфейсу
    global fixation_variants_box_1, fixation_variants_box_2, fixation_variants_box_3

    boundary_conditions_label = tk.Label(text="УМОВИ ЗАКРІПЛЕННЯ", font=("Cambria", 15))
    boundary_conditions_label.place(x=400, y=20)

    edge_label = tk.Label(text="x=a:\n\nx=b:\n\nx=c:", font=("Cambria", 12))
    edge_label.place(x=400, y=77)

    fixation_variants_box_1.set(picked_fixations[0])
    fixation_variants_box_1.place(x=450, y=80)
    fixation_variants_box_2.set(picked_fixations[1])
    fixation_variants_box_2.place(x=450, y=119)
    fixation_variants_box_3.set(picked_fixations[2])
    fixation_variants_box_3.place(x=450, y=158)

    event = Event()
    assign_fixation_thread = Thread(target=assign_fixation, args=(event,), daemon=True)
    assign_fixation_thread.start()

    proceed_button_1 = tk.Button(command=lambda:(event.set(), boundary_conditions_label.destroy(), edge_label.destroy(), fixation_variants_box_1.place_forget(), 
                                                fixation_variants_box_2.place_forget(), fixation_variants_box_3.place_forget(), load_page_2(), clear_button.destroy(),
                                                proceed_button_1.destroy()) if check_fixations() else (), height=1, width=10, text="Далі >", font=("Cambria", 12))
    proceed_button_1.place(x=615, y=370)

    clear_button = tk.Button(command=lambda:(boundary_conditions_label.destroy(), edge_label.destroy(), fixation_variants_box_1.place_forget(), 
                                                fixation_variants_box_2.place_forget(), fixation_variants_box_3.place_forget(), proceed_button_1.destroy(),
                                                clear_button.destroy(), clear()), height=1, width=20, text="Очистити вхідні дані", font=("Cambria", 12))
    clear_button.place(x=30, y=370)


def load_page_2(): # функція для завантаження другої сторінки інтерфейсу
    global load_variants_box, load_loc_variants_box, q1_0_entry, q1_a_entry, q2_a_entry, q2_b_entry, load_value, picked_load

    boundary_loads_label = tk.Label(text="РОЗПОДІЛЕНЕ ПО КОЛУ\nНАВАНТАЖЕННЯ", font=("Cambria", 15), justify=tk.LEFT)
    boundary_loads_label.place(x=400, y=20)

    edge_label = tk.Label(text="Тип:\n\nУ вузлі:", font=("Cambria", 10), justify=tk.RIGHT)
    edge_label.place(x=390, y=78)

    equal_label = tk.Label(text="=", font=("Cambria", 10))
    equal_label.place(x=600, y=78)

    load_entry.delete(0, tk.END)
    load_entry.insert(0, str(load_value))
    load_entry.place(x=620, y=80)

    load_variants_box.set(picked_load)
    load_variants_box.place(x=450, y=80)
    load_loc_variants_box.set(load_loc)
    load_loc_variants_box.place(x=450, y=110)
    load_loc_variants_box.configure(width=5)

    event = Event()
    load_check_thread = Thread(target=check_load, args=(event,), daemon=True)
    load_check_thread.start()

    distributed_loads_label = tk.Label(text="НОРМАЛЬНИЙ ТИСК", font=("Cambria", 15))
    distributed_loads_label.place(x=400, y=200)

    element_DL_label = tk.Label(text="a<x<b:\t                 b<x<c:", font=("Cambria", 12))
    element_DL_label.place(x=415, y=240)

    q1_label = tk.Label(text="q1(a)=\n\nq1(b)=", font=("Cambria", 10), justify=tk.LEFT)
    q1_label.place(x=415, y=270)
    q2_label = tk.Label(text="Па\tq2(b)=\n\nПа\tq2(c)=", font=("Cambria", 10), justify=tk.LEFT)
    q2_label.place(x=500, y=270)

    unit_label = tk.Label(text="Па\n\nПа", font=("Cambria", 10), justify=tk.LEFT)
    unit_label.place(x=647, y=270)

    q1_0_entry.delete(0, tk.END)
    q1_0_entry.insert(0, str(distributed_load_1_values[0]))
    q1_0_entry.place(x=460, y=273)
    q1_a_entry.delete(0, tk.END)
    q1_a_entry.insert(0, str(distributed_load_1_values[1]))
    q1_a_entry.place(x=460, y=303)

    q2_a_entry.delete(0, tk.END)
    q2_a_entry.insert(0, str(distributed_load_2_values[0]))
    q2_a_entry.place(x=600, y=273)
    q2_b_entry.delete(0, tk.END)
    q2_b_entry.insert(0, str(distributed_load_2_values[1]))
    q2_b_entry.place(x=600, y=303)

    assign_load_thread = Thread(target=assign_load, args=(event,), daemon=True)
    assign_load_thread.start()

    proceed_button_2 = tk.Button(command=lambda:(event.set(), proceed_button_2.destroy(), back_button_1.destroy(), boundary_loads_label.destroy(), 
                                                edge_label.destroy(), load_variants_box.place_forget(), load_loc_variants_box.place_forget(), 
                                                load_entry.place_forget(), equal_label.destroy(), load_page_3(), 
                                                distributed_loads_label.destroy(), element_DL_label.destroy(), unit_label.destroy(), 
                                                q1_label.destroy(), q2_label.destroy(), q1_0_entry.place_forget(), q1_a_entry.place_forget(), 
                                                q2_a_entry.place_forget(), q2_b_entry.place_forget()) if check_data(2) else (), height=1, width=10, 
                                                text="Далі >", font=("Cambria", 12))
    proceed_button_2.place(x=615, y=370)

    back_button_1 = tk.Button(command=lambda:(event.set(), back_button_1.destroy(), proceed_button_2.destroy(), boundary_loads_label.destroy(), 
                                                edge_label.destroy(), load_variants_box.place_forget(), load_loc_variants_box.place_forget(), 
                                                load_entry.place_forget(), equal_label.destroy(), load_page_1(), 
                                                distributed_loads_label.destroy(), element_DL_label.destroy(), unit_label.destroy(),  
                                                q1_label.destroy(), q2_label.destroy(), q1_0_entry.place_forget(), q1_a_entry.place_forget(), 
                                                q2_a_entry.place_forget(), q2_b_entry.place_forget()) if check_data(2) else (), height=1, width=10, 
                                                text="< Назад", font=("Cambria", 12))
    back_button_1.place(x=510, y=370)

    clear_button = tk.Button(command=lambda:(event.set(), back_button_1.destroy(), proceed_button_2.destroy(), boundary_loads_label.destroy(), 
                                                edge_label.destroy(), load_variants_box.place_forget(), load_loc_variants_box.place_forget(), 
                                                load_entry.place_forget(), equal_label.destroy(), distributed_loads_label.destroy(), element_DL_label.destroy(), 
                                                unit_label.destroy(), q1_label.destroy(), q2_label.destroy(), q1_0_entry.place_forget(), q1_a_entry.place_forget(), 
                                                q2_a_entry.place_forget(), q2_b_entry.place_forget(), clear_button.destroy(), clear()), 
                                                height=1, width=20, text="Очистити вхідні дані", font=("Cambria", 12))
    clear_button.place(x=30, y=370)


def load_page_3(): # функція для завантаження третьої сторінки інтерфейсу
    global h1_entry, h2_entry, a_entry, b_entry, c_entry, E_entry, v_entry
    global h1, h2, a, b, c, E, v, picked_fixations, picked_load, load_loc, load_value, distributed_load_1_values, distributed_load_2_values

    entry_coord = 597

    param_label = tk.Label(text="ПАРАМЕТРИ КОНСТРУКЦІЇ", font=("Cambria", 15))
    param_label.place(x=400, y=20)

    var_label = tk.Label(text='Товщина першої ділянки h1 =\n\nТовщина другої ділянки h2 =\n\nРадіус отвору a =\n'
                            '\nДовжина першої діляки b =\n\nЗагальна довжина c =\n\nМодуль пружності E =\n\nКоефіцієнт Пуасона v =', justify=tk.RIGHT, font=("Cambria", 10))
    var_label.place(x=entry_coord-185, y=100)

    h1_entry.place(x=entry_coord, y=102)
    h1_entry.delete(0, tk.END)
    h1_entry.insert(0, str(h1))
    h2_entry.place(x=entry_coord, y=132)
    h2_entry.delete(0, tk.END)
    h2_entry.insert(0, str(h2))
    a_entry.place(x=entry_coord, y=162)
    a_entry.delete(0, tk.END)
    a_entry.insert(0, str(a))
    b_entry.place(x=entry_coord, y=192)
    b_entry.delete(0, tk.END)
    b_entry.insert(0, str(b))
    c_entry.place(x=entry_coord, y=222)
    c_entry.delete(0, tk.END)
    c_entry.insert(0, str(c))
    E_entry.place(x=entry_coord, y=252)
    E_entry.delete(0, tk.END)
    E_entry.insert(0, str(E))
    v_entry.place(x=entry_coord, y=282)
    v_entry.delete(0, tk.END)
    v_entry.insert(0, str(v))

    unit_label = tk.Label(text='[м]\n\n[м]\n\n[м]\n\n[м]\n\n[м]\n\n*10^11 [Па]\n\n[  ]', justify=tk.LEFT, font=("Cambria", 10))
    unit_label.place(x=entry_coord+55, y=100)

    event = Event()
    assign_value_thread = Thread(target=assign_value, args=(event,), daemon=True)
    assign_value_thread.start()
    

    calculate_button = tk.Button(command=lambda:(event.set(), calculate_button.destroy(), back_button_2.destroy(), var_label.destroy(), 
                                                    param_label.destroy(), unit_label.destroy(), h1_entry.place_forget(), h2_entry.place_forget(), 
                                                    a_entry.place_forget(), b_entry.place_forget(), c_entry.place_forget(), E_entry.place_forget(), 
                                                    v_entry.place_forget(), clear_button.destroy(), show_results(calc(h1, h2, a, b, c, E, v, distributed_load_1_values, 
                                                    distributed_load_2_values, picked_fixations,  picked_load, load_value, load_loc))) if check_data(3) else (), 
                                                    height=1, width=10, text="Розрахувати", font=("Cambria", 12))
    calculate_button.place(x=615, y=370)

    back_button_2 = tk.Button(command=lambda:(event.set(), back_button_2.destroy(), calculate_button.destroy(), var_label.destroy(), param_label.destroy(), unit_label.destroy(), 
                                                h1_entry.place_forget(), h2_entry.place_forget(), a_entry.place_forget(), b_entry.place_forget(), 
                                                c_entry.place_forget(), E_entry.place_forget(), v_entry.place_forget(), clear_button.destroy(), load_page_2()) 
                                                if check_data(3) else (), height=1, width=10, text="< Назад", font=("Cambria", 12))
    back_button_2.place(x=510, y=370)

    clear_button = tk.Button(command=lambda:(event.set(), back_button_2.destroy(), calculate_button.destroy(), var_label.destroy(), param_label.destroy(), 
                                                unit_label.destroy(), h1_entry.place_forget(), h2_entry.place_forget(), a_entry.place_forget(), 
                                                b_entry.place_forget(), c_entry.place_forget(), E_entry.place_forget(), v_entry.place_forget(), clear(), 
                                                clear_button.destroy()), height=1, width=20, text="Очистити вхідні дані", font=("Cambria", 12))
    clear_button.place(x=30, y=370)


def show_results(extr): # функція для побудови графіків та виведення результатів
    sigma = [0, 0, 0]

    if extr[4] <= b:
        sigma[0] = round((3 * abs(extr[1]))  / ((2 * h1) * 1000000), 4)
    else:
        sigma[0] = round((3 * abs(extr[1]))  / ((2 * h1) * 1000000), 4)

    if extr[5] <= b:
        sigma[1] = round((6 * abs(extr[2])) / ((h1 ** 2) * 1000000), 4)
    else:
        sigma[1] = round((6 * abs(extr[2])) / ((h1 ** 2) * 1000000), 4)

    if extr[6] <= b:
        sigma[2] = round((6 * abs(extr[3])) / ((h1 ** 2) * 1000000), 4)
    else:
        sigma[2] = round((6 * abs(extr[3])) / ((h1 ** 2) * 1000000), 4)

    result_label = tk.Label(window, text=f"РЕЗУЛЬТАТИ ОБЧИСЛЕНЬ", font=("Cambria", 15))
    result_label.place(x=400, y=20)
    extr_label = tk.Label(window, text=f"\n  Максимальні значення:\n\n    W = ............{round(extr[0], 6)} м    \n    Qr = ...........{round(extr[1], 4)} Н/м\n    Mrr = ..........{round(extr[2], 4)} Н\n    Mθθ = ..........{round(extr[3], 4)} Н\n\n\n  Максимальні напруження:\n\n    |σrz| = ........{sigma[0]} МПа\n    |σrr| = ........{sigma[1]} МПа\n    |σθθ| = ........{sigma[2]} МПа\n", font=("Consolas", 10), justify=tk.LEFT, bg='white')
    extr_label.place(x=420, y=77)
    back_button_3 = tk.Button(command=lambda:(result_label.destroy(), extr_label.destroy(), back_button_3.destroy(), load_page_3(), clear_button.destroy()),
                                            height=1, width=10, text="< Назад", font=("Cambria", 12))
    back_button_3.place(x=510, y=370)

    clear_button = tk.Button(command=lambda:(clear(), result_label.destroy(), extr_label.destroy(), back_button_3.destroy(), clear_button.destroy()), height=1, width=20, text="Очистити вхідні дані", font=("Cambria", 12))
    clear_button.place(x=30, y=370)

    max_W = extr[0]
    max_Qr = extr[1]
    max_Mr = extr[2]
    max_M_theta = extr[3]
    max_W_loc = extr[4]
    max_Qr_loc = extr[5]
    max_Mr_loc = extr[6]
    max_M_theta_loc = extr[7]

    l1 = extr[8]
    l2 = extr[9]
    W1 = extr[10]
    W2 = extr[11]
    Qr1 = extr[12]
    Qr2 = extr[13]
    Mr1 = extr[14]
    Mr2 = extr[15]
    M_theta1 = extr[16]
    M_theta2 = extr[17]

    try:
        plt.subplot(2, 2, 1)  # Побудова графіку прогину
        plt.plot(l1, W1, 'b-', label="Ділянка I")
        plt.plot(l2, W2, 'r-', label="Ділянка II")
        if max_W_loc < b:
            plt.plot(max_W_loc, max_W, 'b', marker='o', label='Екстремум')
        else:
            plt.plot(max_W_loc, max_W, 'r', marker='o', label='Екстремум')
        plt.title("Прогин, [м]", size=10)
        plt.grid()
        plt.ylabel('w')
        plt.legend(loc='upper center', bbox_to_anchor=(1.15, 1.3), ncol=3, fancybox=True)

        plt.subplot(2, 2, 2)  # Побудова графіку перерізуючої сили
        plt.plot(l1, Qr1, 'b-')
        plt.plot(l2, Qr2, 'r-')
        plt.plot(np.linspace(b, b + 10 ** (-20), 5), np.linspace(Qr1[len(Qr1) - 1], Qr2[0], 5), 'b-')
        if max_Qr_loc <= b:
            plt.plot(max_Qr_loc, max_Qr, 'b', marker='o')
        else:
            plt.plot(max_Qr_loc, max_Qr, 'r', marker='o')
        plt.title("Перерізуюча сила, [Н/м]", size=10)
        plt.grid()
        plt.ylabel('Qr')

        plt.subplot(2, 2, 3)  # Побудова графіку радіального згинального моменту
        plt.plot(l1, Mr1, 'b-')
        plt.plot(l2, Mr2, 'r-')
        plt.plot(np.linspace(b, b + 10 ** (-20), 5), np.linspace(Mr1[len(Mr1) - 1], Mr2[0], 5), 'b-')
        if max_Mr_loc <= b:
            plt.plot(max_Mr_loc, max_Mr, 'b', marker='o')
        else:
            plt.plot(max_Mr_loc, max_Mr, 'r', marker='o')
        plt.title("Радіальний знинальний момент, [Н]", size=10)
        plt.grid()
        plt.ylabel('Mrr')

        plt.subplot(2, 2, 4)  # Побудова графіку окружного згинального моменту
        plt.plot(l1, M_theta1, 'b-')
        plt.plot(l2, M_theta2, 'r-')
        plt.plot(np.linspace(b, b + 10 ** (-20), 5), np.linspace(M_theta1[len(M_theta1) - 1], M_theta2[0], 5), 'b-')
        if max_M_theta_loc <= b:
            plt.plot(max_M_theta_loc, max_M_theta, 'b', marker='o')
        else:
            plt.plot(max_M_theta_loc, max_M_theta, 'r', marker='o')
        plt.title("Окружний згинальний момент, [Н]", size=10)
        plt.grid()
        plt.ylabel('Mθθ')

        plt.subplots_adjust(right=0.95, wspace=0.45, hspace=0.45)
        plt.show()
    except:
        pass
    
