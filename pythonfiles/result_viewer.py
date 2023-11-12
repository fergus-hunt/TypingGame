import tkinter
from tkinter import messagebox
from tkinter import ttk


class ResultViewer(tkinter.Tk):
    def __init__(self, userResults):
        tkinter.Tk.__init__(self, "User Results")
        self.geometry("620x200")
        self.graph = ttk.Treeview(master=self, columns=('result', 'time'), show='headings')
        self.graph.heading('result', text='Result')
        self.graph.heading('time', text="Date")

        self.graph.bind("<<TreeviewSelect>>", self.item_view)
        self.graph.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.graph.yview)
        self.graph.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky='ns')
        for result in userResults:
            self.graph.insert('', tkinter.END, values=result)

        self.mainloop()

    def item_view(self, event):
        for thing in self.graph.selection():
            item = self.graph.item(thing)
            messagebox.showinfo(title='Result',
                                message=f"First Item : {item['values'][0]}Second Item : {item['values'][1]}")
