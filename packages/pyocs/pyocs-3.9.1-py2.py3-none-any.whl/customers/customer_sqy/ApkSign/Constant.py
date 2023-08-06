import os,sys
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    print(os.path.join(BASE_PATH, 'tmp/MailRecord.txt'))