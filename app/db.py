# import required module
import sqlite3
from sqlite3 import Connection, Cursor


def check_user(db: Connection, email: str) -> bool:
    cur = db.cursor()
    query = f"""SELECT * FROM Users WHERE email = '{email}';"""
    res = cur.execute(query).fetchall()
    # print(res, email, query)
    if len(res) == 0:
        return False
    else:
        return True


def check_login(db: Connection, login_details: dict) -> bool:
    cur = db.cursor()
    query = f"""SELECT * FROM Users where email = '{login_details['email']}' AND password = '{login_details['password']}' AND secret_que = '{login_details['secret_que']}' AND secret_ans = '{login_details['secret_ans']}';"""
    res = cur.execute(query).fetchone()
    print(res)
    if not res:
        return False
    else:
        return True


if __name__ == "__main__":

    # connect to database
    con = sqlite3.connect("crm_sql.db")

    # create cursor object
    cur = con.cursor()

    # # create tables
    cur.execute(
        """CREATE TABLE IF NOT EXISTS Users(
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            password VARCHAR(255),
            role VARCHAR(255),
            secret_que VARCHAR(255) NOT NULL,
            secret_ans VARCHAR(255) NOT NULL,
            PRIMARY KEY (email));"""
    )
    print("Users table created")

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Posts(
        title VARCHAR(255),
        body TEXT, author VARCHAR(255),
        status VARCHAR(255),
        pubdate DATE);"""
    )
    print("Post table created")

    tmp = cur.execute("SELECT * FROM Users;").fetchall()

    if not tmp:
        print("Inserting Data to new Tables")
        test_users = [
            ("user1", "user1@test.com", "hasheduser1", "admin", "fav num", "1"),
            ("user2", "user2@test.com", "hasheduser2", "admin", "fav num", "2"),
            ("user3", "user3@test.com", "hasheduser3", "super_admin", "fav num", "3"),
        ]

        for user in test_users:
            cur.execute("""INSERT INTO Users VALUES (?,?,?,?,?,?)""", user)
        con.commit()

        test_posts = [
            ("tp1", "This is the body of tp1", "user1", "published", "2022-05-10"),
            ("tp2", "This is the body of tp2", "user1", "published", "2022-05-11"),
            ("tp3", "This is the body of tp3", "user2", "published", "2022-01-18"),
            ("tp4", "This is the body of tp4", "user1", "draft", "2022-04-23"),
        ]

        for post in test_posts:
            cur.execute("""INSERT INTO Posts VALUES (?,?,?,?,?)""", post)
        con.commit()

    con.close()
