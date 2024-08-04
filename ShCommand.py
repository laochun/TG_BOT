import subprocess
import re
import json

from public.data import ChatMessage


def Send_Specify_link(Specifyink):
    try:
        command = f'tdl forward --from {Specifyink} --to https://t.me/tghi_BOT --proxy socks5://127.0.0.1:10808'
        # 执行命令并捕获输出
        subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
def read_json_file():
    with open('2338.JSON','r',encoding='utf-8') as json_data:
        message = json.load(json_data)['messages'][-1]
        print(message['id'])
        if ChatMessage.get(self=message,message_id=message['id']):
            print(112312321)
        else:
            print(11111)

            ChatMessage.post(self=message,message=message)
# 测试方法
if __name__ == "__main__":
    # speed = Send_Specify_link('https://t.me/dksj666/142')
    # if speed is not None:
    #     print(f"Download speed: {speed:.2f} bytes/second")
    read_json_file()