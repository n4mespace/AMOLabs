import tkinter as tk
import time
import matplotlib
from numpy import random
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as anim


matplotlib.use("TkAgg")
random.seed(42)


class MyWindow:
    def __init__(self, master):
        self.master = master
        self.range = tk.Scale(from_=10, to=200, bg='white', width=15,
                              resolution=10, troughcolor='gray',
                              orient=tk.HORIZONTAL, command=self.show_plot,
                              sliderlength=20, showvalue=100, length=300)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.ax = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)

        self.range.pack(side=tk.BOTTOM)
        self.canvas.get_tk_widget().pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.Y)

    def add_exec_time(f):
        def timed(*args, **kw):
            ts = time.time()
            result = f(*args, **kw)
            te = time.time()
            exec_time = (te - ts) * 1000
            return exec_time, result
        return timed

    @add_exec_time
    def shake_sort(self, arr: list) -> list:
        up = range(len(arr) - 1)
        while True:
            for indices in (up, reversed(up)):
                swapped = False
                for i in indices:
                    if arr[i] > arr[i+1]:
                        arr[i], arr[i+1] = arr[i+1], arr[i]
                        swapped = True
                if not swapped:
                    return arr

    def show_plot(self, n_samples):
        n_samples = int(n_samples)

        # Creating unsorted arrays with different sizes
        test_samples = [random.randint(low=1, high=20, size=size)
                        for size in range(n_samples)]

        # Get times of algorythm execution
        times = [self.shake_sort(sample)[0] for sample in test_samples]
        lens = [len(sample) for sample in test_samples]

        teor_times = [(len(sample)**2 - len(sample)) / 4 / 1000
                      for sample in test_samples]

        # Plot results of teoretical and testing times
        self.ax.clear()
        line, = self.ax.plot(
            0, 0, color='blue', linewidth=3, label='test')
        self.ax.plot(lens, teor_times, linestyle='-.',
                     color='green', linewidth=3, label='teoretical')

        self.ax.set_xlim(0, lens[-1])
        self.ax.set_ylim(0, times[-1])
        self.ax.set(title='Testing Shaker sorting algorythm',
                    xlabel='length of array', ylabel='sorting time ms')
        self.ax.legend()

        def animate(i):
            line.set_data(lens[:i], times[:i])
            return line,

        self.anim = anim.FuncAnimation(
            self.fig, animate, lens, interval=70, blit=False)

        self.canvas.draw()
        self.toolbar.update()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background='white')
    root.geometry('420x500')
    root.title('LAB 2')
    app = MyWindow(root)
    root.mainloop()
