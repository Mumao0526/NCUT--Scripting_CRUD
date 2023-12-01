import sqlite3
import csv
import json

DB_PATH = "wanghong.db"


def DB_execute(command: str, data: tuple = None) -> bool:
    """
    Execute a command in the wanghong.db and return the success status.

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
        if cursor.rowcount > 0:
            print(f"=>異動 {cursor.rowcount} 筆記錄")
    except sqlite3.Error as error:
        print(f"執行 SQL 操作時發生錯誤：{error}")

    cursor.close()
    conn.close()
    return success


def createDB() -> bool:
    """
    Create database and members table.
    """
    comm = """CREATE TABLE IF NOT EXISTS "members"
            (
                "iid"	INTEGER,
                "mname"	TEXT NOT NULL,
                "msex"	TEXT NOT NULL,
                "mphone"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("iid" AUTOINCREMENT)
            )
            """
    return DB_execute(comm)


def upToDB(
    path: str, dbTableName: str = "members", title: list = ["mname", "msex", "mphone"]
) -> bool:
    """
    Bulk insert data from a CSV file into a database table.

    Args:
        path (str): Path to the CSV file.
        dbTableName (str, optional): Name of the database table.
        title (list, optional): List of column names.

    Returns:
        bool: True if operation was successful, False otherwise.
    """
    # 構建 SQL 插入命令，使用 INSERT OR IGNORE 來避免重複插入
    titleStr = ",".join(title)
    placeholders = ",".join("?" * len(title))  # 創建 '?' 佔位符
    command = (
        f"INSERT OR IGNORE INTO {dbTableName} ({titleStr}) VALUES ({placeholders})"
    )
    inserted_count = 0  # 計數器，計算插入了多少筆紀錄

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 以 CSV 格式打開文件並讀取所有行到一個列表中
        with open(path, "r", encoding="UTF-8") as file:
            reader = csv.reader(file)
            for row in reader:
                cursor.execute(command, tuple(row))
                # 更新計數器
                inserted_count += cursor.rowcount

        conn.commit()
        if inserted_count:
            print(f"=>異動 {inserted_count} 筆記錄")
        else:
            print("=>沒有新紀錄被添加。")
        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def show(table: str = "members", command: str = None, val: tuple = ()):
    """
    Displays records from a database table or using a custom SQL command.

    Args:
        table: Table name to display records from. Defaults to "members".
        command: Custom SQL command to execute. Defaults to None.
        val: Values for SQL command placeholders.

    Returns:
        None
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if command is None:
        cursor.execute(f"SELECT * FROM {table}")
    else:
        cursor.execute(command, val)

    result = cursor.fetchall()
    if result:
        print()
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
    """
    Adds a new record to the 'members' table in the database.

    Args:
        name: Name of the member.
        sex: Sex of the member.
        phone: Phone number of the member, used as a unique identifier.

    Returns:
        True if the addition is successful, False otherwise.
    """
    # 安全的佔位符號寫法
    data = (name, sex, phone)

    return DB_execute(
        "INSERT OR IGNORE INTO members (mname, msex, mphone) VALUES (?, ?, ?)", data
    )


def search(name: str = None, sex: str = None, phone: str = None) -> list:
    """
    Search data by name, sex, and/or phone.

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
    """
    Modify data in the members table in the wanghong.db by name.

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
    """
    Deletes all records from the 'members' table in the database.

    Returns:
        True if the deletion is successful, False otherwise.
    """
    return DB_execute("DELETE FROM members")


def login(account: str, password: str) -> bool:
    """
    Validates user login credentials against stored credentials in 'pass.json'.

    Args:
        account: User's account name.
        password: User's password.

    Returns:
        True if credentials are valid, False otherwise.
    """
    with open("pass.json", "r", encoding="UTF-8") as f:
        try:
            members = json.load(f)
            for item in members:
                if item.get("帳號") == account and item.get("密碼") == password:
                    return True
        except Exception as e:
            print(e.__traceback__)
        return False
