import sys
import json
import hashlib
import random
import requests

# =========== 百度翻译 APP 信息 ===========
APP_ID = "abcdefg"
APP_KEY = "abc@12345"

API_URL = "https://api.fanyi.baidu.com/api/trans/vip/translate"

TEST_INPUT= "This is a test sentence."
def translate(query: str) -> str:
    if not query:
        return "请输入要翻译的内容"

def translate(text):
    salt = str(random.randint(32768, 65536))
    sign = hashlib.md5((APP_ID + text + salt + APP_KEY).encode("utf-8")).hexdigest()

    params = {
        "q": text,
        "from": "auto",
        "to": "zh",
        "appid": APP_ID,
        "salt": salt,
        "sign": sign
    }

    r = requests.get(API_URL, params=params)
    data = r.json()

    if "error_code" in data:
        return data.get("error_msg", "翻译失败")

    return "\n".join([x["dst"] for x in data["trans_result"]])


def main():
    request = json.loads(sys.stdin.read())
    search = request["params"].get("search", None)
    request_id = request["id"]

    result_text = translate(search) if search else "请输入要翻译的内容"

    response = {
        "jsonrpc": "2.0",
        "result": {
            "items": [
                {
                    "title": result_text,
                    "subtitle": "百度翻译结果",
                    "icon": "emoji:🌐",
                    "actions": [
                        {
                            "id": "copy-to-clipboard",
                            "text": result_text
                        }
                    ]
                }
            ]
        },
        "id": request_id
    }

    print(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    main()