from CovidMonitor import CovidMonitor
from tkinter.constants import DOTBOX, FLAT, NONE, NSEW, END, E, S, SINGLE, UNDERLINE, W, EW, BOTH, LEFT, BOTTOM, ACTIVE
from tkinter.font import BOLD
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt


class CovidUi(CovidMonitor):
    def __init__(self, title: str):
        super().__init__()
        self.__window = tk.Tk()
        self.__window.title(title)

        self.__start_date = None
        self.__end_date = None

        win_width = 1000
        win_height = 700
        screen_width = self.__window.winfo_screenwidth()
        screen_height = self.__window.winfo_screenheight()
        x_pos = int((screen_width - win_width) / 2)
        y_pos = int((screen_height - win_height) / 2)

        self.__window.geometry(f'{win_width}x{win_height}+{x_pos}+{y_pos}')
        self.__font_family = 'Roboto Slab'
        self.__window.rowconfigure(0, minsize=400, weight=1)

        self.__set_first_column()
        self.__set_second_column()

    def __set_first_column(self):
        bg_color = '#25211c'

        # region Frame Config
        first_column = tk.Frame(self.__window, bg=bg_color)
        first_column.columnconfigure(1, minsize=first_column.winfo_reqwidth(), weight=1)
        first_column.rowconfigure(1, minsize=first_column.winfo_reqheight(), weight=1)
        # endregion

        # region Countries List
        label = tk.Label(first_column, text='Countries:', bg=bg_color, fg='white', font=(self.__font_family, 20, BOLD))

        countries_list = self.__list = tk.Listbox(first_column, selectmode=SINGLE, activestyle=DOTBOX,
                                                  font=(self.__font_family, 13))

        countries = self.countries()
        for country in countries:
            countries_list.insert(END, country)

        btn = tk.Button(first_column, text='Get Results', font=(self.__font_family, 15), command=self.__get_results)
        # endregion

        # region Graph Generation
        s_date_frame = tk.LabelFrame(first_column, text='Start Date', font=(self.__font_family, 15, BOLD), bg=bg_color, fg='white')
        self.__start_date = tk.Entry(s_date_frame)

        e_date_frame = tk.LabelFrame(first_column, text='End Date', font=(self.__font_family, 15, BOLD), bg=bg_color, fg='white')
        self.__end_date = tk.Entry(e_date_frame)

        graph_btn = tk.Button(first_column, text='Generate Graph', font=(self.__font_family, 15),
                              command=self.__generate_graph)
        # endregion

        # region Column 1 Grid Configuration
        label.grid(row=0, column=0, pady=10, padx=10, sticky=W)
        countries_list.grid(row=1, column=0, padx=10, sticky=NSEW)
        btn.grid(row=2, column=0, pady=10, padx=10, sticky=EW)

        s_date_frame.grid(row=3, column=0, pady=5, padx=10, sticky=EW)
        self.__start_date.grid(row=0, column=0, pady=10, padx=10)

        e_date_frame.grid(row=4, column=0, pady=5, padx=10, sticky=EW)
        self.__end_date.grid(row=0, column=0, pady=10, padx=10)
        graph_btn.grid(row=5, column=0, pady=10, padx=10, sticky=EW)
        # endregion

        first_column.pack(fill=BOTH, side=LEFT)

    def __set_second_column(self):
        second_column = self.__sec_column = tk.Frame(self.__window)
        second_column.columnconfigure(1, minsize=second_column.winfo_reqwidth(), weight=1)

        clear_btn = tk.Button(second_column, text='Clear', font=(self.__font_family, 15), command=self.__del_results)

        clear_btn.grid(row=0, column=1, sticky=E, pady=10, padx=10)
        second_column.pack(fill=BOTH, expand=True, side=BOTTOM)

    def __get_results(self):
        self.__del_results()
        country = self.__list.get(ACTIVE)

        try:
            results_label = tk.Label(self.__sec_column, text='Results:', font=(self.__font_family, 20, BOLD))
            results_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

            results = self.search(country)
            lbl_row = 1

            for key, value in results.items():
                key_lbl = tk.Label(self.__sec_column, text=f'{key}:', font=('Roboto Slab', 14, 'bold'))
                val_lbl = tk.Label(self.__sec_column, text=value)

                key_lbl.grid(row=lbl_row, column=0, pady=2, padx=10, sticky=W)
                val_lbl.grid(row=lbl_row, column=1, pady=2, padx=10, sticky=W)

                lbl_row += 1
        except IndexError as ie:
            messagebox.showerror('Error', f'Country not found:\n{ie}')

    def __generate_graph(self):
        valid_start: datetime
        valid_end: datetime

        try:
            valid_start = datetime.strptime(self.__start_date.get(), '%d-%m-%Y')
            valid_end = datetime.strptime(self.__end_date.get(), '%d-%m-%Y')

            country = self.__list.get(ACTIVE)

            date_diff = valid_end - valid_start
            if date_diff.days > 40:
                messagebox.showerror(None, "Difference between Start Date and End Date must be less than or equal to 30 days!")
                return

            cases_arr = []
            days = []
            month = ''
            for day in range(valid_start.day, valid_end.day + 1):
                date = datetime.strptime(f'{valid_start.year}-{valid_start.month}-{day}', '%Y-%m-%d')
                date_ftd = datetime.strftime(date, '%Y-%m-%d')
                cases_arr.append(self.get_previous_cases(country, date_ftd))
                days.append(day)
                month = datetime.strftime(date, "%B")

            active = [cases.get('Active') for cases in cases_arr]
            new = [cases.get('New Cases') for cases in cases_arr]
            deaths = [cases.get('Deaths') for cases in cases_arr]

            plt.plot(days, active, label='Active', color='green')
            plt.plot(days, new, label='New', color='orange')
            plt.plot(days, deaths, label='Deaths', color='maroon')

            for index, ac in enumerate(active):
                plt.text(x=days[index], y=ac + 10, s=ac,
                         fontdict=dict(fontfamily='PT Sans', fontsize=9.5, weight='bold', color='black'))

            for index, nc in enumerate(new):
                plt.text(x=days[index], y=nc + 10, s=nc,
                         fontdict=dict(fontfamily='PT Sans', fontsize=9.5, weight='bold', color='black'))

            for index, dc in enumerate(deaths):
                plt.text(x=days[index], y=dc + 10, s=dc,
                         fontdict=dict(fontfamily='PT Sans', fontsize=9.5, weight='bold', color='black'))

            plt.xlabel(f'Month - {month}')
            plt.ylabel('Cases')

            plt.title('COVID-19 Summary (Cases/Day)')

            plt.legend(loc='best')
            plt.grid(axis='y', linestyle=':', color='black')
            plt.show()
        except ValueError as ve:
            messagebox.showerror(None, f'Invalid Date:\n{ve}')

    def __del_results(self):
        self.__sec_column.destroy()
        self.__set_second_column()

    def show(self):
        self.__window.mainloop()
