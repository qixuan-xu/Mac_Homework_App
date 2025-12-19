from gpt import *
from jsonos import *
from calender import *
import sys
import re

def parse_command(text):
    text = text.lower()

    # 移除所有空格
    text = text.replace(" ", "")

    m = re.search(r"/?calendar\((\d+)\)", text)
    if m:
        return ("check_calendar", int(m.group(1)))

    return None




def pre_check():
    if api_check() == 0:
        sys.exit(1)
    check_icloud()
    if get_history("setting.json", "model") == []:
        add_history(
        "setting.json",
        "model",
        {
            "gpt_model": "gpt-4.1-turbo",
            "temperature": 0.7,
            "max_tokens": 1500,
            "system_prompt":
"""
You are an assistant of a person

When the user asks about calendar or schedule, YOU MUST respond with a command.

Available commands:
- /12345calendar(n)

Rules:- 
- NO space in command
- NO explanation while output command.
- NO extra text in command.
- If a command is applicable, do not respond in natural language.
""",
            "enable":True
        }
        )
        print("Default settings added to setting.json. Please review and modify as needed.")


    return 0







def main():
    pre_check()
    reply=chat("帮我查一下未来7天的日程",get_history("history.json","chat_history"),"gpt-4.1-mini")
    print("GPT raw reply:", reply)
    cmd = parse_command(reply)
    if cmd:
        name, arg = cmd

        if name == "check_calendar":
            result = clean_event(arg)
            reply = chat_summary(str(result), [], "gpt-4.1-mini")

    print("GPT says:", reply)

if __name__ == "__main__":
    main()


