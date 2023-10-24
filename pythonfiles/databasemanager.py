import sqlite3, json, datetime
# get uesr log in - to confirm 
# create user accoutns 
# store user typign runs (error count, wpm)
# only store and retrieve data, no calculations or anything
# app_data.db (user_information, typing_runs)


#table scores = game_scores
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

    def upload_game_score(self, username, score): 
        date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        with sqlite3.connect("database/app_data.db") as con: 
            cur = con.cursor()
            cur.execute(f"""
                INSERT INTO game_scores VALUES ('{username}', '{score}', '{date}')""")
            con.commit()

    def upload_test_score(self, username, wpm, errors): 
        date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        with sqlite3.connect("database/app_data.db") as con: 
            cur = con.cursor()
            cur.execute(f"""INSERT INTO test_scores VALUES ('{username}', '{wpm}', '{errors}', '{date}')""")
            con.commit()
        
