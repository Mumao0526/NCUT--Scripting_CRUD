import sqlite3

def DB_execute(command: str):
    conn = sqlite3.connect('wanghong.db')

    # 建立 cursor 物件後再 execute
    cursor = conn.cursor()
    cursor.execute({command})
    conn.commit()

    cursor.close()
    conn.close()

def createDB():
    comm = '''CREATE TABLE IF NOT EXISTS "members"
            (
                "iid"	INTEGER,
                "mname"	TEXT NOT NULL,
                "msex"	TEXT NOT NULL,
                "mphone"	TEXT NOT NULL,
                PRIMARY KEY("iid" AUTOINCREMENT)
            )
            '''
    DB_execute(comm)

def upToDB():


def show():

def add(name: str, sex: str, phone: str):
    """Add data to members table in the wanghong.db

    Args:
        name (str): _description_
        sex (str): _description_
        phone (str): _description_
    """
    conn = sqlite3.connect('wanghong.db')

    # 建立 cursor 物件後再 execute
    cursor = conn.cursor()
    # 安全的佔位符號寫法
    data = (name, sex, phone)
    cursor.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", data)
    conn.commit()

    cursor.close()
    conn.close()

def modify(name: str, sex: str, phone: str):
    """Modify data to members table in the wanghong.db

    Args:
        name (str): _description_
        sex (str): _description_
        phone (str): _description_
    """
    conn = sqlite3.connect('wanghong.db')

    # 建立 cursor 物件後再 execute
    cursor = conn.cursor()
    # 安全的佔位符號寫法
    data = (name, sex, phone, name)
    cursor.execute('UPDATE members SET mname = ? msex = ? mphone = ? WHERE name = ?', data)
    conn.commit()

    cursor.close()
    conn.close()

def sreachByPhoneNumber():

def delAll():

def exit():
