import json


def load_data():
    with open('data/alpaca_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def convert_to_jsonl(original_data):
    _len = int(len(original_data) * 0.7)
    i = 0
    with open('data/train.jsonl', 'w', encoding='utf-8') as train_file, \
            open('data/dev.jsonl', 'w', encoding='utf-8') as dev_file:
        for item in original_data:
            messages = {"messages": [
                {
                    "role": "user",
                    "content": item["instruction"]
                },
                {
                    "role": "assistant",
                    "content": item["output"]
                }
            ]}
            i += 1
            if i < _len:
                train_file.write(json.dumps(
                    messages, ensure_ascii=False) + '\n')
            else:
                dev_file.write(json.dumps(messages, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    original_data = load_data()
    convert_to_jsonl(original_data)
