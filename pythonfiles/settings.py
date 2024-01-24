import tkinter, json 


# reading the standard user settings 
with open("./database/settings_options.json") as file: 
    ALL_SETTINGS= json.loads(file.read()) 

# storing stander using settings in global constants 
FONTS = [font for font in ALL_SETTINGS["Font"]]
KEYSOUND = [keysound for keysound in ALL_SETTINGS["Keysound"]]
COLOUR = [colour for colour in ALL_SETTINGS["Colour"]]
MUSIC = [music for music in ALL_SETTINGS["Music"]]



class Settings(tkinter.Tk):  # inhereting from tkinter window 
    def __init__(self): 
        tkinter.Tk.__init__(self)
        self.geometry("600x200")

        # storing useability features as attributes 
        self.colour_clicked = tkinter.StringVar()
        self.colour_clicked.set("Blue")
        self.colour_options = tkinter.OptionMenu(self, self.colour_clicked, *COLOUR)
        self.colour_options.pack()
        self.keysound_clicked = tkinter.StringVar()
        self.keysound_clicked.set("Typewrite")
        self.keysound_options = tkinter.OptionMenu(self, self.keysound_clicked, *KEYSOUND)
        self.keysound_options.pack()
        self.font_clicked = tkinter.StringVar()
        self.font_clicked.set("Scary")
        self.font_options = tkinter.OptionMenu(self, self.font_clicked, *FONTS)
        self.font_options.pack()
        self.music_clicked = tkinter.StringVar()
        self.music_clicked.set("Daft")
        self.music_options = tkinter.OptionMenu(self, self.music_clicked, *MUSIC)
        self.music_options.pack()

        # button that changes settings based on user choices 
        set_button = tkinter.Button(self, text="Set Settings", command=self.set_settings)
        set_button.pack()
        
    
    def set_settings(self): 
        """changes userability features based on user choices"""
        values = {"Font":ALL_SETTINGS["Font"][self.font_clicked.get()], "Keysound":ALL_SETTINGS["Keysound"][self.keysound_clicked.get()],
                  "Colour":ALL_SETTINGS["Colour"][self.colour_clicked.get()], "Music":ALL_SETTINGS["Music"][self.music_clicked.get()]}
        json_object = json.dumps(values, indent=4)
        # writing new settings into file 
        with open(".\\database\\user_settings.json", "w") as outfile: 
            outfile.write(json_object)
        
        self.quit()

