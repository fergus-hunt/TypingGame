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
        self.root.wm_minsize(340, 75)
        self.SCARY_FONT = tkinter.font.Font(family="Helvetica", size=30, weight="bold")

    def log_in_user(self, **kwargs):
        """Tkinter window to allow user to log into account. """
        if kwargs.get('previous_frame'):
            previous_frame = kwargs.get('previous_frame')
            previous_frame.destroy()
        user_log_in_frame = tkinter.Frame(master=self.root, name="log_in_frame")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)


        log_in_entry_title = tkinter.Label(master=user_log_in_frame, text="LOGIN",   font=self.SCARY_FONT,  pady=10)
        log_in_entry_title.grid(column=0, row=0, columnspan=2)

        username_log_in_label = tkinter.Label(master=user_log_in_frame, text="Username: ")
        username_log_in_label.grid(column=0, row=1, sticky=tkinter.W, padx=25)

        username_log_in_entry = tkinter.Entry(master=user_log_in_frame )
        username_log_in_entry.insert(string="username", index=tkinter.END)
        username_log_in_entry.grid(column=1, row=1, sticky=tkinter.E)

        password_log_in_label = tkinter.Label(master=user_log_in_frame, text="Password: ")
        password_log_in_label.grid(column=0, row=2, sticky=tkinter.W, padx=25)


        password_log_in_entry = tkinter.Entry(master=user_log_in_frame, show="*")
        password_log_in_entry.insert(string="Password", index=tkinter.END)
        password_log_in_entry.grid(column=1, row=2, pady=25, sticky=tkinter.E )


        submit_log_in = tkinter.Button(user_log_in_frame, text="Submit", background="grey", command=lambda: self.authenticate_old_user(
            username_log_in_entry.get(), password_log_in_entry.get()
        ))

        submit_log_in.grid(column=1, row=3, columnspan=1, sticky=tkinter.W)

        create_account_path = tkinter.Button(user_log_in_frame, text="Create account", font=("Helvetica", 10, 'bold'), fg="blue",bd=0,   command=lambda: self.creating_user_frame(previous_frame=user_log_in_frame))
        create_account_path.grid(column=0, row=4,  columnspan=2, pady=(10, 0))

        user_log_in_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.TOP)

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

        create_account_frame = tkinter.Frame(master=self.root, name="create_user_frame")
        # create_account_frame.grid_columnconfigure(1, weight=2)
        # create_account_frame.grid_columnconfigure(0, weight=1)

        create_account_title = tkinter.Label(master=create_account_frame, text="CREATE", font=self.SCARY_FONT)
        create_account_title.grid(column=0, row=0, columnspan=2, )

        username_create_label = tkinter.Label(create_account_frame, text="Create Account: ")
        username_create_label.grid(column=0, row=1, sticky=tkinter.W, padx=25)

        username_create_entry = tkinter.Entry(create_account_frame)
        username_create_entry.insert(string="username", index=tkinter.END)
        username_create_entry.grid(column=1, row=1, sticky=tkinter.E)

        password_create_label = tkinter.Label(create_account_frame, text="Password: ")
        password_create_label.grid(column=0, row=2, sticky=tkinter.W, padx=25)

        password_create_entry = tkinter.Entry(create_account_frame, show="*")
        password_create_entry.insert(string="Password", index=tkinter.END)
        password_create_entry.grid(column=1, row=2, pady=25, sticky=tkinter.E)

        email_label = tkinter.Label(create_account_frame, text="Email: ")
        email_label.grid(column=0, row=3, sticky=tkinter.W, padx=25)

        email_entry = tkinter.Entry(create_account_frame)
        email_entry.insert(string="email", index=tkinter.END)
        email_entry.grid(column=1, row=3, sticky=tkinter.E)

        log_in_path = tkinter.Button(master=create_account_frame, text="Log in",command=lambda: self.log_in_user(previous_frame=create_account_frame), bd=0, fg="blue", font=("helvetica", 10, "bold"))
        log_in_path.grid(column=0, row=5, columnspan=2, pady=(10, 0))

        submit_new_account = tkinter.Button(create_account_frame, text="Submit", 
                                            command=lambda: self.new_create_user_record(
                                                username_create_entry.get(), password_create_entry.get(),
                                                email_entry.get(), create_account_frame
                                            ))
        submit_new_account.grid(column=1, row=4, sticky=tkinter.W, pady=(25, 0))
        create_account_frame.pack(expand=1, fill=BOTH, side=tkinter.TOP)

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
            

