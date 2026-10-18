import tkinter, matplotlib
from matplotlib import pyplot
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class ResultViewer(tkinter.Tk): # inheriting from tkinter window 
    """Class shows scores that are within typing test or typing game"""
    def __init__(self, column_headings,user_results, feature_control):
        tkinter.Tk.__init__(self, "User Results") 
        self.title("Result Viewer") # window title 


        self.results = user_results # array of tuples containing all userful information 
        self.next_screen = "StartMenu" # when tkinter window quit this is returned
        graph_button = tkinter.Button(text="Show graph", command=self.show_graph)
        graph_button.grid(column=0, row=0, columnspan=3)

        # styling the window for better visualisation 
        self.style = ttk.Style()
        self.style.theme_use("clam") # preset theme 
        self.style.configure("Treeview", background="white", 
                             fieldbackground="white", foreground=feature_control.colour)
        self.style.configure("Treeview.Columns", width=20)
        self.style.configure("Treeview.Heading", background="white")                             

        
        # Initializing treeview element and settings column identifiers
        self.graph = ttk.Treeview(master=self, columns=column_headings, show='headings')
        
        #linking the callback function self.item_view with selecting record
        self.graph.bind("<<TreeviewSelect>>", self.item_view)
        
        
        self.graph.grid(row=1, column=0)
        # making headings
        # Function to display record information 
        for index in range(len(column_headings)): 
            heading = column_headings[index]
            self.graph.heading(heading, text=heading) # placing heading text onto columns
            self.graph.column(f'# {index + 1}', anchor=CENTER) # centering heading on column

        # Implements vertical scrolling
        vertical_scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.graph.yview)
        self.graph.configure(yscroll=vertical_scrollbar.set) # linking scrollbar and graph
        vertical_scrollbar.grid(row=1, column=1, sticky='ns') # placing scrollbar on window 
        for result in user_results:
            self.graph.insert('', tkinter.END, values=result)
            
        self.mainloop()

    def item_view(self, event): 
        """Shows the user the record they have left clicked on"""
        for recordID in self.graph.selection(): # iterating through selection
            item = self.graph.item(recordID) # finding actual record
            print(item)
            # displaying window for selected record 
            messagebox.showinfo(title=f'Record',
                                message=f"Score : {item['values'][1]}\nDate : {item['values'][2].split(',')[0]}")
            
    def show_graph(self):
        """showing graph of results over time"""
        fig, ax = pyplot.subplots() # configuring graph 

        # adding user results 
        ax.plot([itemTwo[len(self.results[0])-1].split(',')[0] for itemTwo in self.results], [item[1] for item in self.results])
        pyplot.show()

        
