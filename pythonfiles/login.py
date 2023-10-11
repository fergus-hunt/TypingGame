import tkinter, json, sqlite3, datetime
from tkinter import messagebox
from databasemanager import DatabaseManager
# generate good user passworeds

class AuthenticateUser():
    def __init__(self, database_manager) -> None:
        self.database_manager = database_manager()
        self.root = tkinter.Tk()



    def log_in_user(self, **kwargs):  # frame to get user information
        if kwargs.get('previous_frame'):
            previous_frame = kwargs.get('previous_frame')
            previous_frame.destroy()
        user_log_in_frame = tkinter.Frame(self.root, name="log_in_frame")
        
        username_log_in_entry = tkinter.Entry(user_log_in_frame)
        username_log_in_entry.insert(string="username", index=tkinter.END)
        username_log_in_entry.grid(column=0, row=1)

        password_log_in_entry = tkinter.Entry(user_log_in_frame)
        password_log_in_entry.insert(string="password", index=tkinter.END)
        password_log_in_entry.grid(column=0, row=2)

        create_account_path = tkinter.Button(user_log_in_frame, text="Create account", command=lambda: self.creating_user_frame(previous_frame=user_log_in_frame))
        create_account_path.grid(column=0, row=0)

        submit_log_in = tkinter.Button(user_log_in_frame, text="Submit", command=lambda: self.authenticate_old_user(
            username_log_in_entry.get(), password_log_in_entry.get()
        ))
        submit_log_in.grid(column=1, row=1, rowspan=2)
        user_log_in_frame.grid(column=0, row=1)

    def authenticate_old_user(self, username, password): # compares user password to users in database
        users = self.database_manager.get_username_password()
        not_found = True
        count = -1

        # could implement other sorting algorithm 
        while not_found and count < len(users)-1:
            count += 1
            user = users[count]
            if username == user[0]:
                if user[1] == password:
                    messagebox.showinfo(message='working')
                    self.root.destroy()
                    not_found = False
        if not_found:
            messagebox.showinfo(message='verification failed')
        else: 
            self.username =  username
    

    def creating_user_frame(self, **kwargs): # allows user to create account
        if kwargs.get('previous_frame'):
            previous_frame = kwargs.get('previous_frame')
            previous_frame.destroy()
        create_account_frame = tkinter.Frame(self.root, name="create_user_frame")

        log_in_path = tkinter.Button(create_account_frame, text="Log in", command=lambda: self.log_in_user(previous_frame=create_account_frame))
        log_in_path.grid(column=0, row=0)

        username_create_entry = tkinter.Entry(create_account_frame)
        username_create_entry.insert(string="username", index=tkinter.END)
        username_create_entry.grid(column=0, row=1)
        
        full_name_create_entry = tkinter.Entry(create_account_frame)
        full_name_create_entry.insert(string="Full Name", index=tkinter.END)
        full_name_create_entry.grid(column=0, row=2)

        password_create_entry = tkinter.Entry(create_account_frame)
        password_create_entry.insert(string="Password", index=tkinter.END)
        password_create_entry.grid(column=0, row=3)

        submit_new_account = tkinter.Button(create_account_frame, text="Submit", command=lambda: self.new_create_user_record(
            username_create_entry.get(), password_create_entry.get(), full_name_create_entry.get(), create_account_frame
        ))
        submit_new_account.grid(column=1, row=1, rowspan=2)
        create_account_frame.grid(column=0, row=1)

    def new_create_user_record(self, username, password,email,  old_frame): # inputs new user information into database
        users_database = self.database_manager.get_username_password()
        usernames = [username for username, password in users_database]

        if username in usernames:
            messagebox.showinfo(message='Already username')
        else: 
            self.database_manager.create_new_user(username, password, email)
            messagebox.showinfo("Account Created")
            old_frame.destroy()
            self.log_in_user()