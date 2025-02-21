from flask import Flask
from chatgpt_sample import chat_with_chatgpt

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/home")
def hello_home():
    chatgpt_response = chat_with_chatgpt(
                user_message="你是誰啊？可以向我介紹你自己嗎？",
                system_prompt="你是一位後端管理員，有前端使用者會呼叫你"
    )
    return chatgpt_response



#如果要使用python執行:
# if __name__ == "__main__":
#     app.run(debug=True)