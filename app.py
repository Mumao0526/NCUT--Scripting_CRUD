from lib import upToDB, show, createDB, add, modify, delAll, login, search
import sys


def menu():
    print(
        """
---------- 選單 ----------
0 / Enter 離開
1 建立資料庫與資料表
2 匯入資料
3 顯示所有紀錄
4 新增記錄
5 修改記錄
6 查詢指定手機
7 刪除所有記錄
--------------------------"""
    )

    menuNumber = input("請輸入您的選擇 [0-7]:")
    if menuNumber == "":
        return menuNumber

    try:
        a = int(menuNumber)
        if 0 <= a <= 7:
            return a
    except ValueError:
        print("=>無效的選擇")
        menu()
    else:
        print("=>無效的選擇")


def main():
    account = str(input("請輸入帳號："))
    password = str(input("請輸入密碼："))
    if not login(account, password):
        print("=>帳密錯誤，程式結束")
        sys.exit()

    while True:
        menuNumber = menu()
        if menuNumber == 1:
            if createDB():
                print("=>資料庫已建立")
        elif menuNumber == 2:
            upToDB("members.txt")
        elif menuNumber == 3:
            show()
        elif menuNumber == 4:
            name = str(input("請輸入姓名:"))
            sex = str(input("請輸入性別:"))
            phone = str(input("請輸入手機:"))
            add(name, sex, phone)
        elif menuNumber == 5:
            name = str(input("請輸入想修改記錄的姓名:"))
            data = search(name=name)
            if data:
                sex = str(input("請輸入要改變的性別:"))
                phone = str(input("請輸入要改變的手機:"))

                print("原資料：")
                for item in data:
                    print(f"姓名：{item[1]}，性別：{item[2]}，手機：{item[3]}")
                if modify(name=name, sex=sex, phone=phone):
                    print("修改後的資料：")
                    print(f"姓名：{name}，性別：{sex}，手機：{phone}")
            else:
                print("=>必須指定姓名才可修改記錄")
        elif menuNumber == 6:
            phone = str(input("請輸入想查詢記錄的手機:"))
            show(command="SELECT * FROM members WHERE mphone=?", val=(phone,))
        elif menuNumber == 7:
            delAll()
        elif menuNumber == 0 or menuNumber == '':
            break
    sys.exit()


if __name__ == "__main__":
    main()
