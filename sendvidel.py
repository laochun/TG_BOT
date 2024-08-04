# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from telegram import Bot, InputFile

app = Flask(__name__)

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)


@app.route('/send_video', methods=['POST'])
def send_video():
    chat_id = request.form['chat_id']
    video_file = request.files['video_file']

    try:
        bot.send_video(
            chat_id=chat_id,
            video=InputFile(video_file),
            supports_streaming=True,
            timeout=300  # 增加超时时间
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
