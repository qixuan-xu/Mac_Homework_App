def add_history(file_name, data_name, new_message):
    import json, os

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # 确保是列表
    history = data.get(data_name, [])
    if not isinstance(history, list):
        history = []

    history.append(new_message)
    data[data_name] = history

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_history(file_name, data_name):
    import json, os

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        return []

    history = data.get(data_name, [])
    if not isinstance(history, list):
        return []
    return history