import datetime, hashlib, sqlite3


def get_username_password(username): 
    """Returns array of tuples that match username"""
    with sqlite3.connect("database/app_data.db") as con: # making connection to database 
        cur = con.cursor() # enables database manipulator
        database_information = cur.execute("""SELECT username, password 
                                            FROM user_information
                                            WHERE username = ?;""", (username,))  # returns sqlite3 object of records that match username 

    return database_information.fetchall() # returning the records of the sqlite3 contents 

def create_new_user(username, password, full_name): # inserts the arguments into database. 
    userhash = (hashlib.sha256(password.encode("utf-8")).hexdigest()) # creating secure hash for user password 
    with sqlite3.connect("database/app_data.db") as con: # making connection to database 
        cur = con.cursor()
        cur.execute("""INSERT INTO user_information 
                    VALUES (?, ?, ?)""", (username, userhash, full_name)) # sql statement that adds username, password and name 
        con.commit() # making changes permanent 

def upload_game_score(username, score): # adding new game scores from the game
    date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") # the current data and time for database
    with sqlite3.connect("database/app_data.db") as con: # making connection to database 
        cur = con.cursor()
        cur.execute("""
            INSERT INTO game_scores
                     VALUES (?, ?, ?)""", (username, score, date)) # inserting values into database 
        con.commit() # making changes permanent 

def upload_test_score(username, wpm, errors): # adding new test scores into database 
    date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") # current date and time to be added to database 
    with sqlite3.connect("database/app_data.db") as con: # making connection to database 
        cur = con.cursor()
        cur.execute("""INSERT INTO test_scores 
                    VALUES (?, ?, ?, ?)""", (username, wpm, errors, date)) # sql statement to add the important values to database 
        con.commit() # making changes permanent 

def get_user_game_scores(username): 
    """Returns array of tuples container username, scores, date from database."""
    with sqlite3.connect("database/app_data.db") as con: # making connection to database 
        cur = con.cursor()
        info = cur.execute("""SELECT username, score, date 
                           FROM game_scores 
                           WHERE username = ?;""", (username,)) # sql statement to select and return information   

    return info.fetchall() # returning the values that match criteria 

def get_user_test_scores(username): 
    """returns array of tuples containing username, words per minute, errors and data achieved """
    with sqlite3.connect("database/app_data.db") as con: # making connection to database 
        cur = con.cursor()
        info = cur.execute("""SELECT username, words_per_minute, errors, date 
                           FROM test_scores 
                           WHERE username = ?;""", (username,)) # sql statement to select information from database

    return info.fetchall() # returns the total contents of sql results .
    

