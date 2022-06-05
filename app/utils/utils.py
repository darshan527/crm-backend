from sqlite3 import Cursor


def check_user(db: Cursor, email: str):
    # cur = db.cursor()
    res = db.execute("""SELECT * FROM Users WHERE email = ?""", email)
    if not res:
        return False
    else:
        return True
