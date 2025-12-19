from openai import OpenAI               #加载OpenAI
import os                               #加载os
from dotenv import load_dotenv          #加载env api

from jsonos import add_history


def get_chat_history():
    import jsonos
    return jsonos.get_history("chat_history.json","chat_history")

load_dotenv("api_key.env")              #加载api到环境变量
#print(os.getenv("OPENAI_API_KEY"))      #测试用 输出api


def chat_summary(system_input, history, gptmodel):
    from openai import OpenAI
    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": "You are a assistance.  Summarize the data for the user."
        },
        {
            "role": "user",
            "content": system_input
        }
    ]

    response = client.chat.completions.create(
        model=gptmodel,
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content


def get_system_prompt():
    from jsonos import get_history
    model_cfg = get_history("setting.json", "model")
    if model_cfg and isinstance(model_cfg, list):
        return model_cfg[0].get("system_prompt", "")
    elif isinstance(model_cfg, dict):
        return model_cfg.get("system_prompt", "")
    return ""


def api_check():
    try:
        global client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        api_check_result = os.getenv("OPENAI_API_KEY")
    except:
        return 0


    if api_check_result != 0:
        print ("API check succeed, key: "+api_check_result[0:12]+"****"+api_check_result[-4:])
        return 1
    else:
        print("API check failed, please check your api_key.env file.")
        return 0

def chat(user_input, history, gptmodel):
    from openai import OpenAI

    client = OpenAI()

    system_prompt = get_system_prompt()

    messages = []
    # ✅ 1. 注入 system（只一次）
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    messages.append(get_chat_history())
    # ✅ 2. 注入历史

    for msg in history:
        if isinstance(msg, dict):
            messages.append(msg)

    # ✅ 3. 当前用户输入
    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model=gptmodel,
        messages=messages,
        temperature=0.5  # ⭐ command 模式一定要低
    )

    add_history(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()


