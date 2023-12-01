import sqlite3


command = "SELECT * FROM members WHERE mname=?"
val = '我他媽',

conn = sqlite3.connect("wanghong.db")
cursor = conn.cursor()
cursor.execute(command, val)

result = cursor.fetchall()
if result:
    print(type(result))
    print(result)
    for row in result:
        print(f"{row[1]:<7}\t{row[2]:<5}{row[3]}")
conn.commit()
cursor.close()
conn.close()
