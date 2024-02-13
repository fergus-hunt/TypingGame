import tkinter, json 


# reading the standard user settings json file
with open("./database/settings_options.json") as file: 
    ALL_SETTINGS= json.loads(file.read()) 

# storing array of names within json file. 
# setting as global constants so class can access them 
FONTS = [font for font in ALL_SETTINGS["Font"]]
KEYSOUND = [keysound for keysound in ALL_SETTINGS["Keysound"]]
COLOUR = [colour for colour in ALL_SETTINGS["Colour"]]
MUSIC = [music for music in ALL_SETTINGS["Music"]]


class Settings(tkinter.Tk):
    """Class that shows tkinter window for user to change settings"""
    def __init__(self): 
        # inheriting from tkinter Window
        tkinter.Tk.__init__(self)
        self.title("Settings")
        
        # colour attribute that changes with user selection
        colour_label = tkinter.Label(master=self, text="Colour: ")
        self.colour_clicked = tkinter.StringVar()
        self.colour_clicked.set("Blue")
        self.colour_options = tkinter.OptionMenu(self, self.colour_clicked, *COLOUR)
        # rendering colour label and drop down menu
        self.colour_options.grid(column=1, row=1)
        colour_label.grid(column=0, row=1)
        
        # keysound attribute that changes with user selection
        keysound_label = tkinter.Label(master=self, text="Key sound: ")
        self.keysound_clicked = tkinter.StringVar()
        self.keysound_clicked.set("Typewrite")
        self.keysound_options = tkinter.OptionMenu(self, self.keysound_clicked, *KEYSOUND)
        #rendering keysound lable and menu on window
        keysound_label.grid(column=0, row=2)
        self.keysound_options.grid(column=1, row=2)
        
        # font attribute that changes with user selection
        font_label = tkinter.Label(master=self, text="Font: ")
        self.font_clicked = tkinter.StringVar()
        self.font_clicked.set("Scary")
        self.font_options = tkinter.OptionMenu(self, self.font_clicked, *FONTS)
        # rendering font label and menu
        font_label.grid(column=0, row=3)
        self.font_options.grid(column=1, row=3)

        # music attribute that changes with user selection
        music_label = tkinter.Label(master=self, text="Music: ")
        self.music_clicked = tkinter.StringVar()
        self.music_clicked.set("Daft")
        self.music_options = tkinter.OptionMenu(self, self.music_clicked, *MUSIC)
        # rendering music label menu on window
        music_label.grid(column=0, row=4)
        self.music_options.grid(column=1, row=4)

        # button that changes settings based on user choices 
        set_button = tkinter.Button(self, text="Set Settings", command=self.set_settings)
        set_button.grid(columnspan=2, column=0, row=5, padx=100, pady=50) # rendering button
        
    
    def set_settings(self): 
        """changes userability features based on user choices"""
        values = {"Font":ALL_SETTINGS["Font"][self.font_clicked.get()],
                  "Keysound":ALL_SETTINGS["Keysound"][self.keysound_clicked.get()],
                  "Colour":ALL_SETTINGS["Colour"][self.colour_clicked.get()],
                  "Music":ALL_SETTINGS["Music"][self.music_clicked.get()]}
        json_object = json.dumps(values, indent=4)
        # writing new settings into file so can be accessed globally
        with open(".\\database\\user_settings.json", "w") as outfile: 
            outfile.write(json_object)
        
        self.quit() # removing tkinter window 

