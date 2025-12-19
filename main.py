from gpt import *
from jsonos import *
from calender import *
import sys
import re

def parse_command(text):
    text = text.strip().lower()

    # 只要包含 calendar 和一个数字，就当是 check_calendar
    m = re.search(r"calendar\((\d+)\)", text)
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
You are an assistant that controls a system.

When the user asks about calendar or schedule,
YOU MUST respond with a command.

Available commands:
- /12345calendar(n)

Rules:
- ONLY output the command.
- NO space in command
- NO explanation.
- NO extra text.
- If a command is applicable, do not respond in natural language.
""",
            "enable":True
        }
        )
        print("Default settings added to setting.json. Please review and modify as needed.")


    return 0







def main():
    pre_check()
    reply=chat("帮我查一下未来7天的日历",get_history("history.json","chat_history"),"gpt-4.1-mini")
    print("GPT raw reply:", reply)
    cmd = parse_command(reply)
    if cmd:
        name, arg = cmd

        if name == "check_calendar":

            reply=chat("[非用户，系统输入]："+str(clean_event(arg)),get_history("history.json","chat_history"),"gpt-4.1-mini")

    print("GPT says:", reply)

if __name__ == "__main__":
    main()


