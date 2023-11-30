import sqlite3
import json

import sqlite3

def DB_execute(command: str, data: tuple = None):
    """Execute a command in the wanghong.db. If data is provided, execute the command with placeholders.

    Args:
        command (str): SQL command to be executed.
        data (tuple, optional): Data to be used with placeholders in the SQL command. Defaults to None.
    """
    conn = sqlite3.connect('wanghong.db')
    cursor = conn.cursor()

    try:
        # data is provided
        if data:
            # execute the command with placeholders
            cursor.execute(command, data)
        else:
            cursor.execute(command)

        if cursor.rowcount:
            print(f"=>異動 {cursor.rowcount} 筆記錄")

        conn.commit()
    except sqlite3.Error as error:
        print(f"執行 INSERT 操作時發生錯誤：{error}")

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

def upToDB(path: str, dbTableName: str = "members", title: list = ["mname", "msex", "mphone"]):
    conn = sqlite3.connect('wanghong.db')
    cursor = conn.cursor()

    titleStr = ",".join(title)
    val = list()
    for i in range(len(title)):
        val.append('?')
    valNum = ",".join(val)
    command = f"INSERT INTO {dbTableName} ({titleStr}) VALUES ({valNum})"

    with open(path, 'r', encoding='UTF-8') as f:
        for line in f:
            item = tuple(line.split(','))
            cursor.execute(command, item)
            conn.commit()
    cursor.close()
    conn.close()

def show(table: str = "members", command: str = None, val:tuple = ()):
    conn = sqlite3.connect('wanghong.db')
    cursor = conn.cursor()

    if not command:
        cursor.execute(f'SELECT * FROM {table}')
    else:
        cursor.execute(command,val)

    result = cursor.fetchall()
    if result:
        print('姓名           性別  手機')
        print('--------------------------------')
        for row in result:
            print(f'{row[1]:<7}\t{row[2]:<5}{row[3]}')
    else:
        print('=>查無資料')

    conn.commit()
    cursor.close()
    conn.close()

def add(name: str, sex: str, phone: str):
    """Add data to members table in the wanghong.db

    Args:
        name (str): _description_
        sex (str): _description_
        phone (str): _description_
    """
    # 安全的佔位符號寫法
    data = (name, sex, phone)
    DB_execute("INSERT INTO IF EXISTS members (mname, msex, mphone) VALUES (?, ?, ?)", data)

def modify(name: str, sex: str, phone: str):
    """Modify data to members table in the wanghong.db by name

    Args:
        name (str): _description_
        sex (str): _description_
        phone (str): _description_
    """
    # 安全的佔位符號寫法
    data = (name, sex, phone, name)
    DB_execute('UPDATE members SET mname = ? msex = ? mphone = ? WHERE name = ?', data)


def delAll():
    DB_execute('DELETE FROM members')


def login(account: str, password: str) -> bool:
    with open('pass.json', 'r', encoding='UTF-8') as f:
        try:
            members = json.load(f)
            for item in members:
                if item.get("帳號") == account and item.get("密碼") == password:
                    return True
        except Exception as e:
            print('Oops! I got some error!')
            print(e.__traceback__)
        return False
