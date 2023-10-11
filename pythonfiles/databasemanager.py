import sqlite3, json 
# get uesr log in - to confirm 
# create user accoutns 
# store user typign runs (error count, wpm)
# only store and retrieve data, no calculations or anything
# app_data.db (user_information, typing_runs)

class DatabaseManager(): 
    def ___init__(self) -> None:
        self.path = "./database/app_data.db"

    def get_username_password(self): 
        with sqlite3.connect("database/app_data.db") as con: 
            cur = con.cursor()
            database_information = cur.execute("""SELECT username, password 
                                        FROM user_information""")
        return database_information.fetchall()

    def create_new_user(self, username, password, email): 
        with sqlite3.connect("database/app_data.db") as con: 
            cur = con.cursor()
            cur.execute(f"INSERT INTO user_information VALUES ('{username}', '{password}', '{email}')")
            con.commit()

