'''
Application Factory Style
'''

from main import create_app

print("It is app.py starting")
app = create_app()

'''
Application Factory 방식에서는 create_app(예약어)을 실행하면 아래는 작동하지 않는다.

if __name__ == '__main__':
    print("It is main")

'''
