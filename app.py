from lib import upToDB,show,createDB,add,modify,delAll,login
import sys

def menu():
    print('''
---------- 選單 ----------
0 / Enter 離開
1 建立資料庫與資料表
2 匯入資料
3 顯示所有紀錄
4 新增記錄
5 修改記錄
6 查詢指定手機
7 刪除所有記錄
--------------------------''')

    menuNumber = input("請輸入您的選擇 [0-7]:")
    if menuNumber == '':
        return menuNumber

    try:
        a = int(menuNumber)
        if 0 <= a <= 7:
            return a
    except ValueError:
        print("=>無效的選擇")
        menu()


def main():
    account = str(input('請輸入帳號：'))
    password = str(input('請輸入密碼：'))
    if not login(account, password):
        print("=>帳密錯誤，程式結束")
        sys.exit()

    while True:
        menuNumber = menu()
        if menuNumber == 1:
            createDB()
        elif menuNumber == 2:
            upToDB('members.txt')
        elif menuNumber == 3:
            show()
        elif menuNumber == 4:
            add()
        elif menuNumber == 5:
            modify()
        elif menuNumber == 6:
            phone = str(input('請輸入想查詢記錄的手機:'))
            show(command='SELECT * FROM members WHERE mphone=?', val=(phone,))
        elif menuNumber == 7:
            delAll()
        elif menuNumber == 0 or menuNumber == '':
            break
    sys.exit()


if __name__ == "__main__":
    main()

