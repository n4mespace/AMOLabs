import numpy as np
import matplotlib
from tkinter import messagebox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import parser

matplotlib.use('TkAgg')


class Lab():
    def __init__(self, master: tk.Tk) -> None:
        # Initialize GUI vars and consts
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.a_plholder = '2'
        self.b_plholder = '5'
        self.n_plholder = '10'
        self.f_plholder = 'np.e ** -(x + np.sin(x))'

        self.lbl_a = tk.Label(self.frame, text='Enter a:')
        self.lbl_b = tk.Label(self.frame, text='Enter b:')
        self.lbl_n = tk.Label(self.frame, text='Enter n:')

        self.entry_a = tk.Entry(self.frame, width=3)
        self.entry_a.insert(0, self.a_plholder)
        self.entry_b = tk.Entry(self.frame, width=3)
        self.entry_b.insert(0, self.b_plholder)
        self.entry_n = tk.Entry(self.frame, width=3)
        self.entry_n.insert(0, self.n_plholder)

        self.btn_interpolate = tk.Button(
            self.frame, command=self.plot_interpolation, text='Interpolate')

        self.lbl_f = tk.Label(self.frame, text='Enter f:')
        self.entry_f = tk.Entry(self.frame, width=20)
        self.entry_f.insert(0, self.f_plholder)

        self.lbl_a.grid(row=0, column=0)
        self.entry_a.grid(row=0, column=1)
        self.lbl_b.grid(row=1, column=0)
        self.entry_b.grid(row=1, column=1)
        self.lbl_n.grid(row=2, column=0)
        self.entry_n.grid(row=2, column=1)
        self.lbl_f.grid(row=3, column=0, columnspan=2)
        self.entry_f.grid(row=4, column=0, columnspan=3)
        self.btn_interpolate.grid(row=5, column=0, columnspan=3)

    def _getNDDCoeffs(self, x: np.array, y: np.array) -> np.array:
        ''' Creates NDD (Newton's Divided Difference) pyramid
            and extracts coeffs '''
        n = y.shape[0]
        pyramid = np.zeros([n, n])  # Create a square matrix to hold pyramid
        pyramid[::, 0] = y  # first column is y
        for j in range(1, n):
            for i in range(n - j):
                # create pyramid by updating other columns
                pyramid[i][j] = ((pyramid[i+1][j-1] - pyramid[i][j-1]) /
                                 (x[i+j] - x[i]))
        return pyramid[0]  # return first row

    def interpolate(self, x: np.array, y: np.array, n: int) -> np.array:
        '''
        Uses Neuton's algo to interpolate given func

        x: np.array
            range of interpolation
        y: np.array
            function values on range of interpolation
        n: int
            number of control points
        return: np.array
            interpolation result
        '''
        coeffs = self._getNDDCoeffs(x, y)
        final_pol = np.polynomial.Polynomial([0.])  # our target polynomial
        for i in range(n):
            p = np.polynomial.Polynomial([1.])  # create a dummy polynomial
            for j in range(i):
                # each vector has degree of i
                # their terms are dependant on 'x' values
                p_temp = np.polynomial.Polynomial([-x[j], 1.])  # (x - x_j)
                p = np.polymul(p, p_temp)  # multiply dummy with expression
            p *= coeffs[i]  # apply coefficient
            final_pol = np.polyadd(final_pol, p)  # add to target polynomial

        p = np.flip(final_pol[0].coef, axis=0)
        y_intp = np.polyval(p, x)
        return y_intp

    def plot_interpolation(self) -> None:
        try:
            self.a = float(self.entry_a.get())
            self.b = float(self.entry_b.get())
            self.n = int(self.entry_n.get())

            if self.a >= self.b:
                messagebox.showerror('a >= b !')
                raise ValueError('a >= b !')

            x = np.linspace(self.a, self.b, self.n)

            self.expr = parser.expr(self.entry_f.get().replace(' ', ''))
            compiled = self.expr.compile()

            self.y_true = eval(compiled)
            self.y_intp = self.interpolate(x, self.y_true, self.n)
            self.err = self.compute_err(self.y_true, self.y_intp)
            self.show_plots()

        except Exception:
            self.entry_a.delete(0, tk.END)
            self.entry_b.delete(0, tk.END)
            self.entry_n.delete(0, tk.END)
            self.entry_f.delete(0, tk.END)
            self.entry_a.insert(0, self.a_plholder)
            self.entry_b.insert(0, self.b_plholder)
            self.entry_n.insert(0, self.n_plholder)
            self.entry_f.insert(0, self.f_plholder)

    def compute_err(self, y_true: np.array, y_intp: np.array) -> np.array:
        return y_true - y_intp

    def show_plots(self) -> None:
        plot_window = tk.Toplevel(self.frame)
        plot_window.title('Graphics')

        fig = Figure(figsize=(5, 4), dpi=150)
        canvas = FigureCanvasTkAgg(fig, plot_window)

        f1 = fig.add_subplot(211)
        f1.set_ylabel('f(x)')
        f1.set_title('Newton\'s interpolation')

        x = np.linspace(self.a - 1, self.b + 1, self.n * 100)

        compiled = self.expr.compile()
        y_true = eval(compiled)

        f1.plot(x, y_true, label='y(x)=' +
                self.entry_f.get().replace(' ', '').replace('np.', ''),
                linewidth=2)

        x = np.linspace(self.a, self.b, self.n)
        f1.plot(x, self.y_intp, 'o', label='interpolation',
                linewidth=4)
        f1.legend(loc=3, prop={'size': 7})

        f2 = fig.add_subplot(212)
        f2.set_xlabel('x')
        f2.set_ylabel('R(x)')
        f2.set_title('Divergence')

        f2.plot(x, self.err)
        fig.subplots_adjust(hspace=0.4)

        canvas.get_tk_widget().pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('LAB 3')
    root.geometry('200x150')
    app = Lab(root)
    root.mainloop()
