import tkinter, hashlib

from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from database_manager import *
import tkinter.font
# generate good user passworeds

# style = Style()


class UserManager():
    def __init__(self) -> None:
        self.root = tkinter.Tk()
        # self.root.geometry("400x200")
        self.root.wm_minsize(600, 400)
        self.SCARY_FONT = tkinter.font.Font(family="ravie", size=30, weight="bold")

    def log_in_user(self, **kwargs):
        """Tkinter window to allow user to log into account. """
        if kwargs.get('previous_frame'):
            previous_frame = kwargs.get('previous_frame')
            previous_frame.destroy()
        user_log_in_frame = tkinter.Frame(master=self.root, name="log_in_frame", background="blue")
        user_log_in_frame.grid_columnconfigure(0, weight=2)
        user_log_in_frame.grid_columnconfigure(1, weight=1)


        log_in_entry_title = tkinter.Label(master=user_log_in_frame, text="LOGIN", font=self.SCARY_FONT, bg="blue", pady=10)
        log_in_entry_title.grid(column=0, row=0)

        username_log_in_entry = tkinter.Entry(master=user_log_in_frame, bg="yellow", bd=2)
        username_log_in_entry.insert(string="username", index=tkinter.END)
        username_log_in_entry.grid(column=0, row=1)

        password_log_in_entry = tkinter.Entry(master=user_log_in_frame, show="*")
        password_log_in_entry.insert(string="Password", index=tkinter.END)
        password_log_in_entry.grid(column=0, row=2)

        create_account_label = tkinter.Label(master=user_log_in_frame, text="Click to create an account: ")
        create_account_label.grid(column=1, row=1, pady=(0, 30))

        create_account_path = tkinter.Button(user_log_in_frame, text="Create account", command=lambda: self.creating_user_frame(previous_frame=user_log_in_frame))
        create_account_path.grid(column=1, row=2)


        submit_log_in = tkinter.Button(user_log_in_frame, text="Submit", command=lambda: self.authenticate_old_user(
            username_log_in_entry.get(), password_log_in_entry.get()
        ))

        submit_log_in.grid(column=0, row=3)
        user_log_in_frame.pack(expand=1, fill=BOTH)

    def authenticate_old_user(self, username, password):
        """Function to check user input matches the user stored in the database, then exits window"""
        user_data = get_username_password(username)
        try:
            user_password = get_username_password(username)[0][1]
            if user_password == hashlib.sha256(password.encode("utf-8")).hexdigest(): 
                tkinter.messagebox.showinfo(message='working')
                self.username = username
                self.root.destroy()
            else:
                tkinter.messagebox.showinfo(message='Password is incorrect')
        except IndexError: 
            tkinter.messagebox.showinfo(message="Username not found")


    def creating_user_frame(self, **kwargs):
        """Tkinter window to allow user to create a new account"""
        if kwargs.get('previous_frame'):
            previous_frame = kwargs.get('previous_frame')
            previous_frame.destroy()
        create_account_frame = tkinter.Frame(master=self.root, name="create_user_frame", bg="blue")
        create_account_frame.grid_columnconfigure(0, weight=2)
        create_account_frame.grid_columnconfigure(1, weight=1)

        create_account_title = tkinter.Label(master=create_account_frame, text="CREATE\nACCOUNT", font=("ravie",15,"bold"), bg="blue", pady=10)
        create_account_title.grid(column=0, row=0)

        username_create_entry = tkinter.Entry(create_account_frame)
        username_create_entry.insert(string="username", index=tkinter.END)
        username_create_entry.grid(column=0, row=1)

        password_create_entry = tkinter.Entry(create_account_frame, show="*")
        password_create_entry.insert(string="Password", index=tkinter.END)
        password_create_entry.grid(column=0, row=2)

        email_entry = tkinter.Entry(create_account_frame)
        email_entry.insert(string="email", index=tkinter.END)
        email_entry.grid(column=0, row=3)

        log_in_label = tkinter.Label(master=create_account_frame, text="Click to log in: ")
        log_in_label.grid(column=1, row=1, pady=(10))

        log_in_path = tkinter.Button(master=create_account_frame, text="Log in",command=lambda: self.log_in_user(previous_frame=create_account_frame))
        log_in_path.grid(column=1, row=2)

        submit_new_account = tkinter.Button(create_account_frame, text="Submit", 
                                            command=lambda: self.new_create_user_record(
                                                username_create_entry.get(), password_create_entry.get(),
                                                email_entry.get(), create_account_frame
                                            ))
        submit_new_account.grid(column=0, row=4)
        create_account_frame.pack(expand=1, fill=BOTH)

    def new_create_user_record(self, username, password, email, old_frame):
        """Inputs the new user account in the database, then returns the window that allows them to login"""
        users_database = get_username_password(username)
        if len(users_database) == 0: 
            create_new_user(username, password, email)
            tkinter.messagebox.showinfo("Account Created")
            old_frame.destroy()
            self.log_in_user()

        else:
            tkinter.messagebox.showinfo(message='Already username')
            


