import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
from pandastable import Table
from tkinter import ttk
from tkinter.messagebox import showinfo

characters = ['All', 'Kate', 'Bob', 'Tom', 'Emma', 'Isabella']

def gui(interval):
    window = tk.Tk()
    window.title("Camelot DashBoard")
    window.geometry('1300x1100')

    #%%%%%%%% [Label] Character state %%%%%%%%#
    lbl = tk.Label(window, text="Character state")
    lbl.grid(column=1, row=0)#, columnspan=2)

    #%%%%%%%% [Combobox] Character state %%%%%%%%#
    selected_character = tk.StringVar()
    char_cb = ttk.Combobox(window, textvariable=selected_character)
    char_cb['values'] = characters[1::]
    char_cb['state'] = 'readonly'
    char_cb.current(0)
    # initial camera.txt (inital to Kate)
    file = open('csv/camera.txt','w+')
    file.write(selected_character.get())
    file.close()
    char_cb.grid(column=1, row=1, pady=(0, 15)) # , columnspan=2

    # bind the selected value changes
    def character_changed(event):
        showinfo(
            title='Result',
            message=f'You selected {selected_character.get()}!'
        )
        # Write into txt file
        file = open('csv/camera.txt','w+')
        file.write(selected_character.get())
        file.close()

    char_cb.bind('<<ComboboxSelected>>', character_changed)

    #%%%%%%%% [Chart plot] Character state %%%%%%%%#
    figure = plt.Figure(figsize=(5,4), dpi=100)
    ax1 = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, window)
    line.get_tk_widget().grid(column=0, row=2, padx=(15, 0), pady=(0, 15))

    def animate(i):
        if selected_character.get() == 'Kate':
            try:
                state = pd.read_csv('csv/kate_state.csv')
            except:
                return
                
        if selected_character.get() == 'Bob':
            try:
                state = pd.read_csv('csv/bob_state.csv')
            except:
                return

        xs = []
        ys_hunger = []
        ys_energy = []
        ys_health = []
        ys_wealth = []
        for index, row in state.iterrows():
            y_hunger = row.hunger
            y_energy = row.energy
            y_health = row.health
            y_wealth = row.wealth
            xs.append(int(index) + 1)
            ys_hunger.append(int(y_hunger))
            ys_energy.append(int(y_energy))
            ys_health.append(int(y_health))
            ys_wealth.append(int(y_wealth))
        ax1.clear()
        ax1.plot(xs, ys_hunger, label='hunger')
        ax1.plot(xs, ys_energy, label='energy')
        ax1.plot(xs, ys_health, label='health')
        ax1.plot(xs, ys_wealth, label='wealth')
        ax1.title.set_text(selected_character.get().capitalize() + ' state')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('State')
        ax1.legend()
    
    ani = animation.FuncAnimation(figure, animate, interval=interval)

    #%%%%%%%% [Table] Character state %%%%%%%%#
    frame =tk.Frame(window)
    frame.grid(column=1, row=2, padx=(15, 0), pady=(0, 15))

    state_table = Table(frame, width=380)
    state_table.show()

    def state_update():
        state_table.redraw()
        if selected_character.get() == 'Kate':
            try:
                state = pd.read_csv('csv/kate_state.csv')
                state_table.model.df = state.iloc[::-1]
                state_table.autoResizeColumns()
                window.after(interval, state_update) # run itself again after 1 seconds
            except:
                window.after(interval, state_update)
        if selected_character.get() == 'Bob':
            try:
                state_table.model.df = state.iloc[::-1]
                state_table.autoResizeColumns()
                window.after(interval, state_update) # run itself again after 1 seconds
                state = pd.read_csv('csv/bob_state.csv')
            except:
                window.after(interval, state_update)

    state_update()

    #%%%%%%%% [Bar chart] Character state %%%%%%%%#
    figure_bar = plt.Figure(figsize=(5,4), dpi=100)
    ax3 = figure_bar.add_subplot(111)
    bar = FigureCanvasTkAgg(figure_bar, window)
    bar.get_tk_widget().grid(column=2, row=2, padx=(15, 0), pady=(0, 15))

    def animate_bar(i):
        if selected_character.get() == 'Kate':
            try:
                value_counts = pd.read_csv('csv/kate_state.csv')['action'].value_counts().sort_index()
            except:
                return
        if selected_character.get() == 'Bob':
            try:
                value_counts = pd.read_csv('csv/bob_state.csv')['action'].value_counts().sort_index()
            except:
                return

        ax3.clear()
        actions = value_counts.keys()
        counts = value_counts.values
        pal = sns.color_palette("Blues_r", len(value_counts))
        rank = value_counts.argsort().argsort()
        sns.barplot(ax=ax3, x=actions, y=counts, palette=np.array(pal[::-1])[rank])
        ax3.set_xlabel('Actions')
        ax3.set_ylabel('Counts')


    ani3 = animation.FuncAnimation(figure_bar, animate_bar, interval=interval)


    #%%%%%%%% [Separator] %%%%%%%%#
    sep_1 = ttk.Separator(window,orient='horizontal')
    sep_1.grid(column=0, row=3, columnspan=4, sticky="ew", pady=(0, 15))

    #%%%%%%%% [Label] Buying price history %%%%%%%%#
    lbl_bp = tk.Label(window, text="Buying price history")
    lbl_bp.grid(column=0, row=4)

    #%%%%%%%% [Combobox] Buying price history %%%%%%%%#
    selected_character_bp = tk.StringVar()
    char_cb_bp = ttk.Combobox(window, textvariable=selected_character_bp)
    char_cb_bp['values'] = characters
    char_cb_bp['state'] = 'readonly'
    char_cb_bp.current(0)
    char_cb_bp.grid(column=0, row=5, pady=(0, 15))
    
    # bind the selected value changes
    def character_changed_bp(event):
        showinfo(
            title='Result',
            message=f'You selected {selected_character_bp.get()}!'
        )

    char_cb_bp.bind('<<ComboboxSelected>>', character_changed_bp)

    #%%%%%%%% [Table] Buying price history %%%%%%%%#
    frame_item =tk.Frame(window)
    frame_item.grid(column=0, row=6, padx=(15, 0), pady=(0, 15))
    buy_history_table = Table(frame_item, width=300)
    buy_history_table.show()

    def buy_history_update():
        buy_history_table.redraw()
        if selected_character_bp.get() == 'All':
            try:
                buy_history_table.model.df = pd.read_csv('csv/buy_history.csv').iloc[::-1]
            except:
                window.after(interval, buy_history_update)
        elif selected_character_bp.get() == 'Kate':
            try:
                df = pd.read_csv('csv/buy_history.csv').iloc[::-1]
            except:
                window.after(interval, buy_history_update)
            buy_history_table.model.df = df[df['Name']=='kate']
        elif selected_character_bp.get() == 'Bob':
            try:
                df = pd.read_csv('csv/buy_history.csv').iloc[::-1]
            except:
                window.after(interval, buy_history_update)
            buy_history_table.model.df = df[df['Name']=='bob']

        buy_history_table.autoResizeColumns()
        window.after(interval, buy_history_update)
    
    buy_history_update()

    #%%%%%%%% [Label] Selling price history %%%%%%%%#
    lbl_sp = tk.Label(window, text="Selling price history")
    lbl_sp.grid(column=1, row=4)

    #%%%%%%%% [Combobox] Selling price history %%%%%%%%#
    selected_character_sp = tk.StringVar()
    char_cb_sp = ttk.Combobox(window, textvariable=selected_character_sp)
    char_cb_sp['values'] = characters
    char_cb_sp['state'] = 'readonly'
    char_cb_sp.current(0)
    char_cb_sp.grid(column=1, row=5, pady=(0, 15))
    
    # bind the selected value changes
    def character_changed_bp(event):
        showinfo(
            title='Result',
            message=f'You selected {selected_character_sp.get()}!'
        )

    char_cb_sp.bind('<<ComboboxSelected>>', character_changed_bp)

    #%%%%%%%% [Table] Selling price history %%%%%%%%#
    frame_item =tk.Frame(window)
    frame_item.grid(column=1, row=6, padx=(15, 0), pady=(0, 15))
    sell_history_table = Table(frame_item, width=300)
    sell_history_table.show()

    def sell_history_update():
        sell_history_table.redraw()
        if selected_character_sp.get() == 'All':
            try:
                sell_history_table.model.df = pd.read_csv('csv/sell_history.csv').iloc[::-1]
            except:
                window.after(interval, sell_history_update)
        elif selected_character_sp.get() == 'Kate':
            try:
                df = pd.read_csv('csv/sell_history.csv').iloc[::-1]
            except:
                window.after(interval, sell_history_update)
            sell_history_table.model.df = df[df['Name']=='kate']
        elif selected_character_sp.get() == 'Bob':
            try:
                df = pd.read_csv('csv/sell_history.csv').iloc[::-1]
            except:
                window.after(interval, sell_history_update)
            sell_history_table.model.df = df[df['Name']=='bob']

        sell_history_table.autoResizeColumns()
        window.after(interval, sell_history_update)
    
    sell_history_update()

    #%%%%%%%% [Label] Market price history %%%%%%%%#
    lbl_sp = tk.Label(window, text="Market Price w/ inflation")
    lbl_sp.grid(column=2, row=4)

    #%%%%%%%% [Chart plot] Market Price w/ inflation %%%%%%%%#
    figure2 = plt.Figure(figsize=(5,4), dpi=100)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, window)
    line2.get_tk_widget().grid(column=2, row=6, padx=(15, 0), pady=(0, 15))

    def animate2(i):
        try:
            buying_price = pd.read_csv('csv/buy_history.csv')['Buying price']
            selling_price = pd.read_csv('csv/sell_history.csv')['Selling price']
        except:
            return

        min_val = min(len(buying_price), len(selling_price))
        price = pd.concat([buying_price[:min_val], selling_price[:min_val]], axis=1)[::-1]

        xs = []
        ys_buying = []
        ys_selling = []

        for index, row in price.iterrows():
            y_buying = row['Buying price']
            y_selling = row['Selling price']

            xs.append(int(index) + 1)
            ys_buying.append(y_buying)
            ys_selling.append(y_selling)

        ax2.clear()
        ax2.plot(xs, ys_buying, label='buying price')
        ax2.plot(xs, ys_selling, label='selling price')
        ax2.title.set_text('Market price')
        ax2.legend()

    ani2 = animation.FuncAnimation(figure2, animate2, interval=interval)

    #%%%%%%%% [Separator] %%%%%%%%#
    sep_2 = ttk.Separator(window,orient='horizontal')
    sep_2.grid(column=0, row=9, columnspan=7, sticky="ew", pady=(0, 15))

    #%%%%%%%% [Label] Items %%%%%%%%#
    lbl_item = tk.Label(window, text="Items")
    lbl_item.grid(column=0, row=10, columnspan=3)

    #%%%%%%%% [Table] Items %%%%%%%%#
    frame_item =tk.Frame(window)
    frame_item.grid(column=0, row=11, columnspan=3)

    item_table = Table(frame_item, width=680)
    item_table.show()

    def item_update():
        item_table.redraw()
        try:
            item_table.model.df = pd.read_csv('csv/items.csv')
        except:
                window.after(interval, item_update)
                
        item_table.autoResizeColumns()
        window.after(interval, item_update) # run itself again after 500 ms

    item_update()

    window.mainloop()

    # return window, ani

if __name__ == "__main__":
    gui(interval=500)