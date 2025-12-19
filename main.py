from gpt import *
from jsonos import *
import sys

def pre_check():
    if api_check() == 0:
        sys.exit(1)
    if get_history("setting.json", "model") == []:
        add_history(
        "setting.json",
        "model",
        {
            "gpt_model": "gpt-4.1-turbo",
            "temperature": 0.7,
            "max_tokens": 1500,
            "system_prompt": "You are a helpful assistant.",
            "enable":True
        }
        )
        print("Default settings added to setting.json. Please review and modify as needed.")
    if get_history("history.json", "chat_history") == []:
        add_history(
            "history.json",
            "chat_history",

            {
                    "role": "system",
                    "content": "You are a helpful assistant."
                }

        )

        print("Chat history initialized in history.json.")
    return 0







def main():
    pre_check()



if __name__ == "__main__":
    main()
