import datetime, hashlib, sqlite3


def get_username_password(username):
    with sqlite3.connect("database/app_data.db") as con:
        cur = con.cursor()
        database_information = cur.execute(f"""SELECT username, password 
                                    FROM user_information WHERE username='{username}';""")

    print(database_information)
    return database_information.fetchall()

def create_new_user( username, password, email):
    userhash = (hashlib.sha256(password.encode("utf-8")).hexdigest())
    with sqlite3.connect("database/app_data.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO user_information VALUES ('{username}', '{userhash}', '{email}')")
        con.commit()

def upload_game_score( username, score):
    date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    with sqlite3.connect("database/app_data.db") as con:
        cur = con.cursor()
        cur.execute(f"""
            INSERT INTO game_scores VALUES ('{username}', '{score}', '{date}')""")
        con.commit()

def upload_test_score( username, wpm, errors):
    date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    with sqlite3.connect("database/app_data.db") as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO test_scores VALUES ('{username}', '{wpm}', '{errors}', '{date}')""")
        con.commit()

def get_user_game_scores( username):
    with sqlite3.connect("database/app_data.db") as con:
        cur = con.cursor()
        info = cur.execute(f"""SELECT username, score, date FROM game_scores WHERE username='{username}';""")

    return info.fetchall()

def get_user_test_scores( username):
    with sqlite3.connect("database/app_data.db") as con:
        cur = con.cursor()
        info = cur.execute(f"""SELECT username, words_per_minute, errors, date FROM test_scores WHERE username='{username}';""")

    return info.fetchall()
    

