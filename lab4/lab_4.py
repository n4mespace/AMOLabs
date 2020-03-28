import numpy as np
import sympy as sp
import matplotlib
from tkinter import messagebox
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from typing import Tuple, List, Optional
from functools import partial

matplotlib.use('TkAgg')


class Lab4():
    def __init__(self, master: tk.Tk) -> None:
        '''Initialize GUI
        
        Arguments:
            master {tk.Tk} -- top level window
        '''
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.lbl_equation = tk.Label(self.frame, text='Enter f:')
        self.lbl_precision = tk.Label(self.frame, text='Enter presion:')

        self.equation_plholder = 'x**3 - x - 3 = 0'
        self.precision_plholder = '0.0001'

        self.entry_equation = tk.Entry(self.frame, width=20)
        self.entry_equation.insert(0, self.equation_plholder)

        self.entry_precision = tk.Entry(self.frame, width=10)
        self.entry_precision.insert(0, self.precision_plholder)

        self.btn_solve = tk.Button(
            self.frame, command=self.results_window, text='Solve!')

        self.lbl_equation.grid(row=0, column=0, columnspan=3)
        self.entry_equation.grid(row=1, column=0, columnspan=3)
        self.lbl_precision.grid(row=2, column=0, columnspan=3)
        self.entry_precision.grid(row=3, column=0, columnspan=3)
        self.btn_solve.grid(row=4, column=0, columnspan=3)

    def equation_parser(self) -> sp.Expr:
        '''Parse entry to sympy Expr type
        
        Returns:
            sp.Expr -- sympy base expression
        '''
        equ_str = (self.entry_equation
                        .get()
                        .replace(' ', '')
                        .replace('=0', '')) 
        equ = sp.simplify(equ_str)
        return equ

    def neuton_method(self, a: float, b: float, eps: float) -> Optional[float]:
        '''
        Neuton's method (tangent method) for solving nonlinear equations
        
        ''' 
        sign_a = self.equation.subs(self.x, a) * self.dy_dx_2.subs(self.x, a)
        prev_x = a if sign_a >= 0 else b

        for _ in range(1000):
            x = (prev_x -
                 float(self.equation.subs(self.x, prev_x)) /
                 float(self.dy_dx_1.subs(self.x, prev_x)))

            if x + 3 < a or x - 3 > b:
                break

            if abs(x - prev_x) <= eps:
                return x

            prev_x = x

        return None

    def get_results(self,
                    intervals: Optional[List[Tuple[float, float]]]) -> List[float]:
        '''
        Apply Neuton's method on specified intervals

        Arguments:
           intervals {Optional[List[Tuple[float, float]]]} -- search area
        
        Returns:
            {List[float]} -- result of Neuton's method
        '''
        if not intervals:
            return []

        results: List[Optional[float]] = [
            self.neuton_method(a, b, eps=self.precision)
            for a, b
            in intervals
        ]

        cleaned_result: List[float] = [result for result in results if result]
        return cleaned_result

    def find_solution_intervals(self,
                                num_epoch: int=1000,
                                step: float=1.) -> List[Tuple[float, float]]:
        '''Tries to find solution itervals 
        
        Right intervals not guararteed
        
        Keyword Arguments:
            num_epoch {int} -- epochs for searching (default: {1000})
            step {float} -- increment
        
        Returns:
            List[Tuple[float, float]] -- intervals
        '''
        intervals: List[Tuple[float, float]] = []
        a, b = -1000., 1000.
        n_points_for_search = int((b - a) / step)

        b = a + step

        for _ in range(n_points_for_search):
            if self.equation.subs(self.x, a) * self.equation.subs(self.x, b) < 0:
                intervals.append((a, b))

            a = b
            b += step

        return intervals

    def results_window(self) -> None:
        '''
        Init plot window and draw solution

        '''
        self.plot_window = tk.Toplevel(self.frame)
        self.plot_window.resizable(False, False)
        self.plot_window.title('Results')

        self.fig = Figure(figsize=(5, 4), dpi=150)
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_window)

        self.ax = self.fig.add_axes([0.15, 0.1, 0.8, 0.8])
        self.ax.grid()
        self.ax.axhline(y=0, linewidth=1, color='r')
        self.ax.axvline(x=0, linewidth=1, color='r')
        self.ax.set_ylim((-30, 30))
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('x')

        self.canvas.get_tk_widget().pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.toolbar.pack(side=tk.TOP, fill=tk.Y, expand=False)
        self.toolbar.update()

        self.lbl_enter_interval = tk.Label(
            self.plot_window, font=('monospace', 17), text='Try your own a,b:')
        self.entry_a = tk.Entry(self.plot_window, width=4)
        self.entry_b = tk.Entry(self.plot_window, width=4)

        self.btn_try_your_interval = tk.Button(
            self.plot_window, text='Search in new interval', bg='gray',
            command=self.update_plot)

        self.solve_equ()

    def solve_equ(self):
        '''Solves equation from entry
        
        Keyword Arguments:
            from_entry {bool} -- where to get intervals (default: {False})
        '''
        self.precision = float(self.entry_precision.get())
        self.equation = self.equation_parser()

        self.x = sp.Symbol('x')
        self.dy_dx_1 = self.equation.diff()
        self.dy_dx_2 = self.dy_dx_1.diff()

        intervals = self.find_solution_intervals()
        self.results = self.get_results(intervals)

        self.show_results(self.results, intervals)

    def update_plot(self) -> None:
        '''Update plots with new values
        
        Raises:
            ValueError -- if a >= b in interval
        '''
        try:
            interval = [
                (float(self.entry_a.get()), float(self.entry_b.get()))
            ]

            if interval[0][0] >= interval[0][1]:
                messagebox.showerror('Error', 'a >= b!',
                                     parent=self.plot_window)
                raise ValueError

            result = self.get_results(interval)

            if result:
                if (round(result[0], 3) not in list(
                                    map(partial(round, ndigits=3), self.results))):
                    self.ax.plot(
                        result, 0, 'o',
                        label=f'roots from [{interval[0][0]}, {interval[0][1]}]',
                        color='orange', linewidth=4)

                    (tk.Label(self.plot_window, height=5,
                              text=f'x_new = {result[0]:.3f}\n in interval ' +
                                   f'[{interval[0][0]:.3f}, {interval[0][1]:.3f}]')
                       .pack(side=tk.TOP, fill=tk.BOTH))

                    self.ax.legend(loc=3, prop={'size': 7})
                    self.canvas.draw()

                else:
                    messagebox.showinfo('Info', f'x = {result[0]:.3f} has been already found!',
                                        parent=self.plot_window)

                self.results.append(result[0])

            else:
                messagebox.showerror(
                    'Error', f'Can\'t find any solutions\non [{interval[0][0]}, {interval[0][1]}]',
                    parent=self.plot_window)

        except Exception:
            self.entry_a.delete(0, tk.END)
            self.entry_b.delete(0, tk.END)
            messagebox.showerror('Error', 'Use correct values',
                                 parent=self.plot_window)

    def show_results(self,
                     results: Optional[List[float]],
                     intervals: Optional[List[Tuple[float, float]]]) -> None:
        '''Plot results of algorythms
        
        Arguments:
            results {Optional[List[float]]} -- equation solution
            intervals {Optional[List[Tuple[float, float]]]} -- solution's intervals
        '''
        if intervals:
            extended_interval = np.linspace(intervals[0][0] - 10,
                                            intervals[-1][1] + 10,
                                            1000)
        else:
            extended_interval = np.linspace(-50, 50, 1000)

        f_values = [self.equation.subs(self.x, x_i)
                    for x_i
                    in extended_interval]

        self.ax.plot(extended_interval, f_values, color='green',
                 label=str(self.equation) + ' = 0', linewidth=2)

        if results:
            self.ax.plot(results, [0 for _ in range(len(results))],
                         'o', label='roots', linewidth=4)
            self.ax.legend(loc=3, prop={'size': 7})

        self.canvas.draw()

        lbl_results = tk.Label(
            self.plot_window, text='Solutions:', font=('monospace', 20))
        lbl_results.pack(side=tk.TOP, fill=tk.BOTH)

        if intervals and results:
            for i, (solution, interval) in enumerate(zip(results, intervals)):
                (tk.Label(self.plot_window, height=5,
                          text=f'x_{i + 1} = {solution:.3f}\n in interval ' +
                               f'[{interval[0]:.3f}, {interval[1]:.3f}]')
                   .pack(side=tk.TOP, fill=tk.BOTH))
        else:
            messagebox.showinfo(
                'Info', 'Can\'t find solution intervals.', parent=self.plot_window)

        self.lbl_enter_interval.pack(side=tk.TOP, fill=tk.BOTH)
        self.entry_a.pack(side=tk.TOP, fill=tk.BOTH)
        self.entry_b.pack(side=tk.TOP, fill=tk.BOTH)
        self.btn_try_your_interval.pack(side=tk.TOP, fill=tk.BOTH)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title('LAB 4')
    root.geometry('200x120')

    app = Lab4(root)
    root.mainloop()
