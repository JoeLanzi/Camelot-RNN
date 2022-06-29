import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from matplotlib import animation
from pandastable import Table

def gui(self):
    window = tk.Tk()
    window.title("Camelot DashBoard")
    window.geometry('900x700')

    # Character state
    lbl = tk.Label(window, text="Character state")
    lbl.grid(column=0, row=0, columnspan=2)

    #%% Chart plot
    figure = plt.Figure(figsize=(5,4), dpi=100)
    ax1 = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, window)
    line.get_tk_widget().grid(column=0, row=1)

    def animate(i):
        data = self.state_history_kate_df

        xs = []
        ys_hunger = []
        ys_energy = []
        ys_health = []
        for index, row in data.iterrows():
            y_hunger = row.hunger
            y_energy = row.energy
            y_health = row.health
            xs.append(int(index))
            ys_hunger.append(int(y_hunger))
            ys_energy.append(int(y_energy))
            ys_health.append(int(y_health))
        ax1.clear()
        ax1.plot(xs, ys_hunger, label='hunger')
        ax1.plot(xs, ys_energy, label='energy')
        ax1.plot(xs, ys_health, label='health')
        ax1.legend()

    ani = animation.FuncAnimation(figure, animate, interval=self.interval)

    #%% Character table
    frame =tk.Frame(window)
    frame.grid(column=1, row=1)

    state_table = Table(frame, width=380)
    state_table.show()

    def state_update(self):
        state_table.redraw()
        state_table.model.df = self.state_history_kate_df.iloc[::-1]
        state_table.autoResizeColumns()
        window.after(self.interval, state_update, self) # run itself again after 1 seconds

    state_update(self)

    #%% Item table
    frame_item =tk.Frame(window)
    frame_item.grid(column=0, row=4, columnspan=2)

    item_table = Table(frame_item, width=530)
    item_table.show()

    def item_update(self):
        item_table.redraw()
        item_table.model.df = self.apple_df
        item_table.autoResizeColumns()
        window.after(self.interval, item_update, self) # run itself again after 500 ms

    item_update(self)

    return window, ani