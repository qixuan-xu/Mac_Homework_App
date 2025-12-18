from openai import OpenAI               #加载OpenAI
import os                               #加载os
from dotenv import load_dotenv          #加载env api


load_dotenv("api_key.env")              #加载api到环境变量
print(os.getenv("OPENAI_API_KEY"))      #测试用 输出api

def chat(user_input,history,gptmodel):

#   Example:
#   ("牛顿三定律是什么？",
#   [{"role": "system", "content": "You are a helpful assistant."},
#   {"role": "user", "content": "你好，你是谁？"},
#   {"role": "assistant", "content": "我是一个可以帮助你学习和解决问题的助手。"}],
#   "gpt-4.1-mini"
#]


    # 创建客户端（会自动从环境变量读 OPENAI_API_KEY）
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except:
        return "api_connect_fail"       #返回报错 api链接

                                        #创建回答
    response = client.chat.completions.create(
        model=gptmodel,           #模型
        messages=[
            history,
            {"role": "user", "content": user_input}
        ]
    )
    try:
        reply = response.choices[0].message.content
    except:
        return "chat_reply_fail"
    return reply