import json

account, password = "root", "135795"
# with open('pass.json', 'r', encoding='UTF-8') as f:
#     try:
#         members = json.load(f)
#         for item in members:
#             if item.get("帳號") == account and item.get("密碼") == password:
#                 print(True)
#     except Exception as e:
#         print('Oops! I got some error!')
#         print(e.__traceback__)
#     finally:
#         print(False)

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

print(login(account, password))
