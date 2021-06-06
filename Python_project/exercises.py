from tkinter import *
import pickle
import random
from tkinter import messagebox


def open_file(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


PRTF = open_file('PRTF_final.pickle')
PRTS = open_file('PRTS_final.pickle')
ADJF = open_file('ADJ_full_final.pickle')
ADJS = open_file('ADJ_short_final.pickle')
Adj_cmp = open_file('Adj_cmp_final.pickle')
Adj_sup = open_file('Adj_sup_final.pickle')

exercise_list_prtf = list(PRTF.values())
exercise_list_prts = list(PRTS.values())
exercise_list_adjf = list(ADJF.values())
exercise_list_adjs = list(ADJS.values())
exercise_list_adjs.extend(list(Adj_sup.values()))
exercise_list_adjs.extend(list(Adj_cmp.values()))

root = Tk()
root.title('Упражнения по русскому языку')


def get_sent_list(pos_list):
    pos_exercises = []
    for _ in range(10):
        exercise = random.choice(pos_list)
        pos_exercises.append(exercise)
    return pos_exercises


def normalize_answer(raw_answer):
    normalized_answer = ''.join(raw_answer.lower().strip().replace('ё', 'e').split())
    return normalized_answer


def display_exercise():
    global my_lbl
    my_lbl = Label(root, text=exercises[index][0], wraplength=790)
    my_lbl.config(font=('Roboto', 15))
    my_lbl.grid(row=2, column=0, columnspan=2, sticky=W+E, pady=10)


def further():
    global index, further_button, e, submit_button, status
    further_button.grid_forget()
    status.grid_forget()
    submit_button = Button(root, text='Ответить', command=lambda: submit(exercises[index][1]), width=15, height=2)
    submit_button.grid(row=4, column=0, sticky=E, pady=5, padx=7)
    a.grid_forget()
    my_lbl.grid_forget()
    e.delete(0, END)
    index += 1
    display_exercise()
    further_button = Button(root, text='Далее', state=DISABLED, width=17, height=2)
    further_button.grid(row=4, column=1, sticky=W, pady=5, padx=7)
    status = Label(root, text=f'{index + 1} из 10', anchor=E, fg='grey')
    status.grid(row=0, column=1, sticky=E)


def submit(answer):
    global a, restart_button, further_button, submit_button, score
    a.grid_forget()
    if len(e.get()) == 0:
        a = Label(root, text='Введите ответ', foreground='red')
        a.config(font=("Arial", 14))
        a.grid(row=5, column=0, columnspan=2)
    else:
        submit_button = Button(root, text='Ответить', state=DISABLED, width=15, height=2)
        submit_button.grid(row=4, column=0, sticky=E, pady=5, padx=7)
        further_button.grid_forget()
        user_answer = e.get()
        if normalize_answer(answer) == normalize_answer(user_answer):
            score += 1
            result = 'Это правильный ответ'
            a = Label(root, text=result, foreground='green')
        else:
            result = 'Это неправильный ответ'
            a = Label(root, text=result, foreground='red')
        a.config(font=("Arial", 14))
        a.grid(row=5, column=0, columnspan=2)
        further_button = Button(root, text='Далее', command=further, width=17, height=2)
        further_button.config(font=("Arial", 14))
        further_button.grid(row=4, column=1, sticky=W, pady=5, padx=7)
        if index == 9:
            further_button.grid_forget()
            messagebox.showinfo('result', f'Ваш результат: {score} правильных ответов из 10')
            further_button = Button(root, text='Далее', state=DISABLED, width=17, height=2)
            further_button.grid(row=4, column=1, sticky=W, pady=5, padx=7)
            restart_button = Button(
                root, text='Начать сначала', command=lambda: restart(restart_ex, restart_pos), height=2
            )
            restart_button.config(font=("Arial", 14))
            restart_button.grid(row=6, column=0, columnspan=2)


def menu_return():
    try:
        for widget in [
            my_lbl, e, a, further_button,
            first_label, submit_button, menu_button, restart_button, status
        ]:

            widget.grid_forget()
    except NameError:
        for widget in [
            my_lbl, e, a, further_button,
            first_label, submit_button, menu_button, status
        ]:
            widget.grid_forget()
    get_first_menu()


def restart(ex_list, next_pos):
    for widget in [
        my_lbl, e, a, further_button,
        first_label, submit_button, restart_button, menu_button, status
    ]:
        widget.grid_forget()
    exercise_loop(ex_list, next_pos)


def exercise_loop(exercise_list, pos):
    global first_label, my_lbl, e, a, exercises, index, restart_ex, restart_pos
    global further_button, submit_button, menu_button, status, score
    root.geometry('800x300')
    starting_widgets = [starting_lbl, prtf_button, prts_button, adjf_button, adjs_button]
    for widget in starting_widgets:
        widget.grid_forget()
    menu_button = Button(root, text='⟵ Вернуться в главное меню', command=menu_return, bg='red')
    menu_button.grid(row=0, column=0, sticky=W)
    first_label = Label(root, text=f'Образуйте нужную форму {pos} от слова в скобках'
                                   f' (если больше одного, запишите их через пробел):', anchor=W, fg='#807F81')
    first_label.config(font=("Arial", 14))
    first_label.grid(row=1, column=0, columnspan=2, sticky=W + E, pady=5)
    e = Entry(root, width=85, bg='grey')
    e.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    e.focus()
    a = Label(root, text='')
    exercises = get_sent_list(exercise_list)
    score = 0
    index = 0
    restart_ex, restart_pos = exercise_list, pos
    display_exercise()

    submit_button = Button(root, text='Ответить', command=lambda: submit(exercises[index][1]), width=15, height=2)
    submit_button.grid(row=4, column=0, sticky=E, pady=5, padx=7)
    further_button = Button(root, text='Далее', state=DISABLED, width=17, height=2)
    further_button.grid(row=4, column=1, sticky=W, pady=5, padx=7)
    status = Label(root, text=f'{index + 1} из 10', anchor=E, fg='grey')
    status.grid(row=0, column=1, sticky=E)


def get_first_menu():
    root.geometry('300x300')
    global starting_lbl, prtf_button, prts_button, adjf_button, adjs_button
    # Стартовый экран
    starting_lbl = Label(root, text='Выберите часть речи для упражнений')
    starting_lbl.config(font=("Arial", 16))
    starting_lbl.grid(row=0, column=0, pady=20, padx=5)
    prtf_button = Button(
        root,
        text='Полные причастия',
        command=lambda: exercise_loop(exercise_list_prtf, 'причастия'),
        height=2, bg='red'
    )
    prtf_button.config(font=("Arial", 16))
    prtf_button.grid(row=1, column=0, pady=2, padx=10, sticky=W + E)
    prts_button = Button(
        root,
        text='Краткие причастия',
        command=lambda: exercise_loop(exercise_list_prts, 'причастия'),
        height=2
    )
    prts_button.config(font=("Arial", 16))
    prts_button.grid(row=2, column=0, pady=2, padx=10, sticky=W + E)
    adjf_button = Button(
        root,
        text='Полные прилагательные',
        command=lambda: exercise_loop(exercise_list_adjf, 'прилагательного'),
        height=2
    )
    adjf_button.config(font=("Arial", 15))
    adjf_button.grid(row=3, column=0, pady=2, padx=10, sticky=W + E)
    adjs_button = Button(
        root,
        text='Краткие прилагательные +\nСравнительная и превосходная степени',
        command=lambda: exercise_loop(exercise_list_adjs, 'прилагательного'),
        height=3, bg='red'
    )
    adjs_button.config(font=("Arial", 13))
    adjs_button.grid(row=4, column=0, pady=2, padx=10, sticky=W + E)


get_first_menu()

mainloop()
