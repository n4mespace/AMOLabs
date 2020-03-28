import tkinter as tk
from tkinter import messagebox
from math import sqrt
from functools import reduce
from PIL import ImageTk


class MyWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.frame.pack()

        self.read_file = tk.Button(
            self.frame, command=self.read, text='Read file input.txt')
        self.from_file = False

        self.lbl_linear = tk.Label(
            self.frame, text='Linear <== a, b, c:', height=3, width=20)
        self.lbl_branch = tk.Label(
            self.frame, text='Branch <== k, d', height=3, width=20)
        self.lbl_cycle = tk.Label(
            self.frame, text='Cycle <== a[], b[]', height=3, width=20)

        self.enter_a = tk.Entry(self.frame, width=3)
        self.enter_b = tk.Entry(self.frame, width=3)
        self.enter_c = tk.Entry(self.frame, width=3)
        self.btn_linear = tk.Button(
            self.frame, command=self.linear, text='Compute')

        self.enter_k = tk.Entry(self.frame, width=3)
        self.enter_d = tk.Entry(self.frame, width=3)
        self.btn_branch = tk.Button(
            self.frame, command=self.branch, text='Compute')

        self.enter_arr_a = tk.Entry(self.frame, width=10)
        self.enter_arr_b = tk.Entry(self.frame, width=10)
        self.btn_cycle = tk.Button(
            self.frame, command=self.cycle, text='Compute')

        self.lbl_linear.grid(row=0, column=0)
        self.enter_a.grid(row=0, column=1)
        self.enter_b.grid(row=0, column=2)
        self.enter_c.grid(row=0, column=3)
        self.btn_linear.grid(row=1, column=0)

        self.lbl_branch.grid(row=2, column=0)
        self.enter_k.grid(row=2, column=1)
        self.enter_d.grid(row=2, column=2)
        self.btn_branch.grid(row=3, column=0)

        self.lbl_cycle.grid(row=4, column=0)
        self.enter_arr_a.grid(row=5, column=0)
        self.enter_arr_b.grid(row=6, column=0)
        self.btn_cycle.grid(row=5, column=1, columnspan=3)

        self.btn_show_variant = tk.Button(
            self.frame, command=self.show_variant, text='Show my variant')
        (tk.Label(self.frame, text=10 * '-', height=4)
           .grid(row=7, column=0, columnspan=4))
        self.btn_show_variant.grid(row=10, column=0, columnspan=4)
        self.read_file.grid(row=11, column=0, columnspan=4)

    def read(self):
        self.from_file = True
        try:
            with open('input.txt', 'r+') as file:
                self.file_input = file.read()
            messagebox.showinfo(
                'Success', f'Read from input.txt:\n {self.file_input}')
        except Exception:
            messagebox.showerror('Error', 'Cannot read from input.txt')

    def show_variant(self):
        window = tk.Toplevel(self.frame)
        window.title('My variant')
        canvas = tk.Canvas(window, width=746, height=102)
        canvas.imageList = []
        canvas.pack()
        variant = ImageTk.PhotoImage(
            file='/home/krok/Documents/Labs/AMO/lab1/variant.png')
        canvas.create_image(0, 0, anchor=tk.NW, image=variant)
        canvas.imageList.append(variant)

    def linear(self):
        try:
            if not self.from_file:
                a = float(self.enter_a.get())
                b = float(self.enter_b.get())
                c = float(self.enter_c.get())
            elif self.file_input.startswith('linear'):
                data = self.file_input[6:].split(',')
                a, b, c = [float(num) for num in data]
                self.from_file = False

                self.enter_a.insert(0, a)
                self.enter_b.insert(0, b)
                self.enter_c.insert(0, c)
            y = (5 + c * (b + 5 * sqrt(a))) ** (1/3)
            (tk.Label(self.frame, text=f'y1 = {y:.2f}')
                .grid(row=1, column=1, columnspan=3))
        except EnvironmentError:
            self.enter_a.delete(0, tk.END)
            self.enter_b.delete(0, tk.END)
            self.enter_c.delete(0, tk.END)
            messagebox.showerror('Error', 'Use correct values')

    def branch(self):
        try:
            if not self.from_file:
                k = float(self.enter_k.get())
                d = float(self.enter_d.get())
            elif self.file_input.startswith('branch'):
                data = self.file_input[6:].split(',')
                k, d = [float(num) for num in data]
                self.from_file = False

                self.enter_k.insert(0, k)
                self.enter_d.insert(0, d)
            y = sqrt(k * abs(d) + d * abs(k)) if k > 10 else (k + d) ** 2
        except Exception:
            self.enter_k.delete(0, tk.END)
            self.enter_d.delete(0, tk.END)
            messagebox.showerror('Error', 'Use correct values')

        (tk.Label(self.frame, text=f'y2 = {y:.2f}')
           .grid(row=3, column=1, columnspan=3))

    def cycle(self):
        try:
            if not self.from_file:
                a = [float(x) for x in self.enter_arr_a.get().split(',')]
                b = [float(x) for x in self.enter_arr_a.get().split(',')]
            elif self.file_input.startswith('cycle'):
                data = self.file_input[5:].split(';')
                a = [float(num) for num in data[0].split(',')]
                b = [float(num) for num in data[1].split(',')]
                self.from_file = False

                self.enter_arr_a.insert(0, data[0])
                self.enter_arr_b.insert(0, data[1])
            f1 = reduce(lambda x, y: x * (y[0] + y[1]), (1, *list(zip(a, b[1:]))))
            f2 = reduce(lambda x, y: x + (y[0] * y[1]), (0, *list(zip(a[1:], b))))
            F = f1 + f2
        except Exception:
            self.enter_arr_a.delete(0, tk.END)
            self.enter_arr_b.delete(0, tk.END)
            messagebox.showerror('Error', 'Use correct values')
        (tk.Label(self.frame, text=f'F = {F:.2f}')
           .grid(row=6, column=1, columnspan=3))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('260x420')
    root.title('LAB 1')
    app = MyWindow(root)
    root.mainloop()
