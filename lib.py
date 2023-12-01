import sqlite3
import json

DB_PATH = "wanghong.db"


def DB_execute(command: str, data: tuple = None) -> bool:
    """Execute a command in the wanghong.db and return the success status.

    Args:
        command (str): SQL command to be executed.
        data (tuple, optional): Data to be used with placeholders in the SQL command.

    Returns:
        bool: True if the command was executed successfully, False otherwise.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    success = False

    try:
        if data:
            cursor.execute(command, data)
        else:
            cursor.execute(command)

        conn.commit()
        success = True
        if cursor.rowcount:
            print(f"=>異動 {cursor.rowcount} 筆記錄")
    except sqlite3.Error as error:
        print(f"執行 SQL 操作時發生錯誤：{error}")

    cursor.close()
    conn.close()
    return success


def createDB() -> bool:
    comm = """CREATE TABLE IF NOT EXISTS "members"
            (
                "iid"	INTEGER,
                "mname"	TEXT NOT NULL,
                "msex"	TEXT NOT NULL,
                "mphone"	TEXT NOT NULL,
                PRIMARY KEY("iid" AUTOINCREMENT)
            )
            """
    return DB_execute(comm)


def upToDB(
    path: str, dbTableName: str = "members", title: list = ["mname", "msex", "mphone"]
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    titleStr = ",".join(title)
    val = list()
    for i in range(len(title)):
        val.append("?")
    valNum = ",".join(val)
    command = f"INSERT INTO {dbTableName} ({titleStr}) VALUES ({valNum})"

    with open(path, "r", encoding="UTF-8") as f:
        for line in f:
            item = tuple(line.strip().split(","))
            cursor.execute(command, item)
            conn.commit()
    cursor.close()
    conn.close()


def show(table: str = "members", command: str = None, val: tuple = ()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if command is None:
        cursor.execute(f"SELECT * FROM {table}")
    else:
        cursor.execute(command, val)

    result = cursor.fetchall()
    if result:
        print("姓名           性別  手機")
        print("--------------------------------")
        for row in result:
            print(f"{row[1]:<7}\t{row[2]:<5}{row[3]}")
    else:
        print("=>查無資料")

    conn.commit()
    cursor.close()
    conn.close()


def add(name: str, sex: str, phone: str) -> bool:
    """Add data to members table in the wanghong.db

    Args:
        name (str): _description_
        sex (str): _description_
        phone (str): _description_
    """
    # 安全的佔位符號寫法
    data = (name, sex, phone)
    return DB_execute(
        "INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", data
    )


def search(name: str = None, sex: str = None, phone: str = None) -> list:
    """Search data by name, sex, and/or phone.

    Args:
        name (str): Name to search for.
        sex (str): Sex to search for.
        phone (str): Phone number to search for.

    Returns:
        list: A list of search results.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 構建查詢條件和參數
    conditions = []
    params = []

    if name:
        conditions.append("mname=?")
        params.append(name)
    if sex:
        conditions.append("msex=?")
        params.append(sex)
    if phone:
        conditions.append("mphone=?")
        params.append(phone)

    # 如果沒有提供搜索條件，返回空列表
    if not conditions:
        return None

    # 創建最終的 SQL 查詢
    query = "SELECT * FROM members WHERE " + " AND ".join(conditions)
    cursor.execute(query, params)

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result if result else None


def modify(name: str, sex: str, phone: str) -> bool:
    """Modify data in the members table in the wanghong.db by name.

    Args:
        name (str): Name of the member to modify.
        sex (str): New sex value.
        phone (str): New phone number value.

    Returns:
        bool: True if the modification was successful, False otherwise.
    """
    # 安全的佔位符號寫法
    data = (sex, phone, name)

    return DB_execute(
        "UPDATE members SET msex = ?, mphone = ? WHERE mname = ?", data=data
    )


def delAll() -> bool:
    return DB_execute("DELETE FROM members")


def login(account: str, password: str) -> bool:
    with open("pass.json", "r", encoding="UTF-8") as f:
        try:
            members = json.load(f)
            for item in members:
                if item.get("帳號") == account and item.get("密碼") == password:
                    return True
        except Exception as e:
            print("Oops! I got some error!")
            print(e.__traceback__)
        return False
