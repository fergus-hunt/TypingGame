import tkinter, hashlib
import re
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from database_manager import *
import tkinter.font
# generate good user passworeds

# style = Style()


class UserManager():
    def __init__(self) -> None:
        self.root = tkinter.Tk() # The tkitner window the frames will be placed ontop of 
        self.root.wm_minsize(340, 75) # So the size of window doesn't go below this resolution 
        self.main_font = tkinter.font.Font(family="Helvetica", size=30, weight="bold") # Font to use as titles 

    def log_in_user(self, **kwargs):
        """Tkinter window to allow user to log into account. """
        if kwargs.get('previous_frame'): # Determining whether frame is already on main window 
            previous_frame = kwargs.get('previous_frame') # storing the previous frame as value 
            previous_frame.destroy()# destroys the previous frame on main window 
            
        user_log_in_frame = tkinter.Frame(master=self.root, name="log_in_frame") # making frame widgets will be placed on 
        self.root.columnconfigure(0, weight=1) # First column will have a smaller width 
        self.root.columnconfigure(1, weight=2) # second column will have a larger width

        log_in_entry_title = tkinter.Label(master=user_log_in_frame, text="LOGIN",   font=self.main_font,  pady=10) # Title for tkinter frame 
        log_in_entry_title.grid(column=0, row=0, columnspan=2) # setting position for element 

        username_log_in_label = tkinter.Label(master=user_log_in_frame, text="Username: ") # Label to show username entry box 
        username_log_in_label.grid(column=0, row=1, sticky=tkinter.W, padx=25) # setting position for element 

        username_log_in_entry = tkinter.Entry(master=user_log_in_frame ) # Text box to enter username 
        username_log_in_entry.insert(string="username", index=tkinter.END) # placing text 'username' within entry box to show purpose 
        username_log_in_entry.grid(column=1, row=1, sticky=tkinter.E) # setting position for element 

        password_log_in_label = tkinter.Label(master=user_log_in_frame, text="Password: ") # Label to show password entry box 
        password_log_in_label.grid(column=0, row=2, sticky=tkinter.W, padx=25)# setting position for element 


        password_log_in_entry = tkinter.Entry(master=user_log_in_frame, show="*") # password entry box, all characters will be shown as '*'
        password_log_in_entry.insert(string="Password", index=tkinter.END) # Placing 'password' in box signifies the password box 
        password_log_in_entry.grid(column=1, row=2, pady=25, sticky=tkinter.E )# setting position for element 


        submit_log_in = tkinter.Button(user_log_in_frame, text="Submit", background="grey", command=lambda: self.authenticate_old_user(
            username_log_in_entry.get(), password_log_in_entry.get()
        )) # Button to submit entry box contents into the program. 
        submit_log_in.grid(column=1, row=3, columnspan=1, sticky=tkinter.W) # setting position for element 

        create_account_path = tkinter.Button(user_log_in_frame, text="Create account", font=("Helvetica", 10, 'bold'), fg="blue",bd=0,
                                            command=lambda: self.creating_user_frame(previous_frame=user_log_in_frame))
        # Button to switch frame to create account. 
        create_account_path.grid(column=0, row=4,  columnspan=2, pady=(10, 0)) # setting position for element 

        user_log_in_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.TOP) # placing frame on self.root

    def authenticate_old_user(self, username, password): 
        """Function to check user input matches the user stored in the database, then exits window"""
        try: # finding the username and password in database 
            user_password = get_username_password(username)[0][1] # selecting password that is located within database 
            if user_password == hashlib.sha256(password.encode("utf-8")).hexdigest(): # comparing hashed password against value in database
                tkinter.messagebox.showinfo(message='Logged in') # Password match, sharing to user. 
                self.username = username # Storing the username for later use. 
                self.root.destroy() # destroying window 
            else:
                tkinter.messagebox.showinfo(message='Password is incorrect') # Passowrd associated to username doesn't match input one 
        except IndexError: # Called when username not in database. 
            tkinter.messagebox.showinfo(message="Username not found") # shows the user what went wrong


    def creating_user_frame(self, **kwargs):
        """Tkinter window to allow user to create a new account""" 
        if kwargs.get('previous_frame'): # Determining whether frame is already on main window 
            previous_frame = kwargs.get('previous_frame') # storing the previous frame as value 
            previous_frame.destroy() # destroys the previous frame on main window 

        create_account_frame = tkinter.Frame(master=self.root, name="create_user_frame") # frame all widgets will be placed on 
        # create_account_frame.grid_columnconfigure(1, weight=2)
        # create_account_frame.grid_columnconfigure(0, weight=1)

        create_account_title = tkinter.Label(master=create_account_frame, text="CREATE", font=self.main_font) # Title showing the use for that frame
        create_account_title.grid(column=0, row=0, columnspan=2) # placing widget onto create_user_frame

        username_create_label = tkinter.Label(create_account_frame, text="username: ") # shows where user should enter username 
        username_create_label.grid(column=0, row=1, sticky=tkinter.W, padx=25) # placing widget onto create_user_frame

        username_create_entry = tkinter.Entry(create_account_frame) # Text box for user to enter their username 
        username_create_entry.insert(string="username", index=tkinter.END) # inputting text 'username' 
        username_create_entry.grid(column=1, row=1, sticky=tkinter.E) # placing widget onto create_user_frame

        password_create_label = tkinter.Label(create_account_frame, text="Password: ") # Label to show where user should enter password
        password_create_label.grid(column=0, row=2, sticky=tkinter.W, padx=25) # placing widget onto create_user_frame

        password_create_entry = tkinter.Entry(create_account_frame, show="*") # text box for user to enter password 
        password_create_entry.insert(string="Password", index=tkinter.END) # inserting password into text box to signify purpose 
        password_create_entry.grid(column=1, row=2, pady=25, sticky=tkinter.E) # placing widget onto create_user_frame

        fullname_label = tkinter.Label(create_account_frame, text="Full Name: ") # Label to show where user enter name 
        fullname_label.grid(column=0, row=3, sticky=tkinter.W, padx=25) # placing widget onto create_user_frame

        fullname_entry = tkinter.Entry(create_account_frame) # Text box for user to enter full name 
        fullname_entry.insert(string="Name", index=tkinter.END) # inserting 'name' into text box to signify purpose 
        fullname_entry.grid(column=1, row=3, sticky=tkinter.E) # placing widget onto create_user_frame

        log_in_path = tkinter.Button(master=create_account_frame, text="Log in",command=lambda: self.log_in_user(previous_frame=create_account_frame), bd=0,
                                     fg="blue", font=("helvetica", 10, "bold")) # Button that switches frame to the log in frame 
        log_in_path.grid(column=0, row=5, columnspan=2, pady=(10, 0)) # placing widget onto create_user_frame

        submit_new_account = tkinter.Button(create_account_frame, text="Submit", 
                                            command=lambda: self.new_create_user_record(
                                                username_create_entry.get(), password_create_entry.get(),
                                                fullname_entry.get(), create_account_frame
        )) # sends the information from text box into the program. 
        submit_new_account.grid(column=1, row=4, sticky=tkinter.W, pady=(25, 0)) # placing widget onto create_user_frame

        create_account_frame.pack(expand=1, fill=BOTH, side=tkinter.TOP) # placing create_user_frame onto the main window 

    def new_create_user_record(self, username, password, full_name, old_frame):
        """Inputs the new user account in the database, then returns the window that allows them to login"""
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$" # regex that tests for a secure password 
        
        
        result = re.findall(pattern, password) # returns a bool to ensure that password is valid. 
        # Stops inputting data if password doesn't meet requirements 
        if not result: 
            if len(password) < 8: # password isn't long enough 
                messagebox.showinfo(title="Account Error", message="Password needs to be at least 8 characterse") 
            # password isn't complex enough
            else: 
                messagebox.showinfo(title="Account Error", 
                                    message="Password needs to have uppercase letters, a digit and a special character") 
                
        else: 
            users_database = get_username_password(username) # database function to return records with same username 
            if len(users_database) == 0:  # Checks that there are no other username's that are the same 
                create_new_user(username, password, full_name) # Inputs user information into database
                tkinter.messagebox.showinfo(message="Account Created") # returns update on process
                old_frame.destroy() # destroyed create_user_frame
                self.log_in_user() # calls the log in page 
            else:
                tkinter.messagebox.showinfo(message='Already username') # if username already exists it stops 
            


