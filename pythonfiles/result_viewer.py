

import tkinter, matplotlib
from matplotlib import pyplot
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyperclip 



    # car !!!

class ResultViewer(tkinter.Tk):
    def __init__(self, column_headings,user_results):
        tkinter.Tk.__init__(self, "User Results")

        self.results = user_results
        self.next_screen = "StartMenu"
        graph_button = tkinter.Button(text="Show graph", command=self.show_graph)
        graph_button.grid(column=0, row=0, columnspan=3)

     

        self.style = ttk.Style()
        self.style.theme_use("clam") 
        self.style.configure("Treeview", background="black", 
                             fieldbackground="black", foreground="blue")
        self.style.configure("Treeview.Columns", width=20)
        self.style.configure("Treeview.Heading", background="white")                             

        self.geometry("620x200")
        self.graph = ttk.Treeview(master=self, columns=column_headings, show='headings')
        for index in range(len(column_headings)): 
            heading = column_headings[index]
            self.graph.heading(heading, text=heading)
            self.graph.column(f'# {index + 1}', anchor=CENTER)
        # self.graph.heading("username", text="User")
        # self.graph.heading('result', text='Result')
        # self.graph.heading('time', text="Date")
        # self.graph.column("# 1", anchor=CENTER)
        # self.graph.column("# 2", anchor=CENTER)
        # self.graph.column("# 3", anchor=CENTER)
        self.graph.bind("<<TreeviewSelect>>", self.item_view)
        self.graph.grid(row=1, column=0)

        scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.graph.yview)
        self.graph.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=1, column=1, sticky='ns')
        for result in user_results:
            self.graph.insert('', tkinter.END, values=result)
            
        self.mainloop()

    def item_view(self, event):
        for thing in self.graph.selection():
            item = self.graph.item(thing)
            messagebox.showinfo(title='Result',
                                message=f"First Item : {item['values'][0]}Second Item : {item['values'][1]}")
            
    def show_graph(self):
        fig, ax = pyplot.subplots()
        # x_plot = []
        # y_plot = []
        # for index in range(len(self.results)-1, -1, -1):
        #     x_plot.append(self.results[index][len(self.results[0])-1].split(',')[0])
        #     y_plot.append(self.results[index][1])
        # ax.plot(x_plot, y_plot)

        ax.plot([itemTwo[len(self.results[0])-1].split(',')[0] for itemTwo in self.results], [item[1] for item in self.results])
        pyplot.show()

        

# test = ResultViewer(("Username", "Result", "Date"), self.user_results)