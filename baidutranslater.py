#!/usr/bin/env python3
# {
#   "Id": "90e0b0f7-9d8c-4f42-b3f7-8e9b0b24d9b1",
#   "Name": "百度翻译",
#   "Author": "qianlifeng",
#   "Version": "0.2.0",
#   "MinWoxVersion": "2.0.0",
#   "Description": "在 Wox 中使用百度翻译 API 翻译文本",
#   "Website": "https://api.fanyi.baidu.com/",
#   "Icon": "emoji:🌐",
#   "TriggerKeywords": ["fy", "translate"],
#   "SupportedOS": ["windows", "linux", "darwin"],
#   "SettingDefinitions": [
#     {
#       "Type": "textbox",
#       "Value": {
#         "Key": "app_id",
#         "Label": "Baidu APP ID",
#         "Tooltip": "请输入百度翻译开放平台的 APP ID",
#         "Style": {
#           "Width": 420
#         }
#       }
#     },
#     {
#       "Type": "textbox",
#       "Value": {
#         "Key": "app_key",
#         "Label": "Baidu APP KEY",
#         "Tooltip": "请输入百度翻译开放平台的 APP KEY",
#         "Style": {
#           "Width": 420
#         }
#       }
#     },
#     {
#       "Type": "textbox",
#       "Value": {
#         "Key": "target_language",
#         "Label": "Target Language",
#         "Tooltip": "目标语言代码，默认 zh。示例：zh、en、jp、kor",
#         "DefaultValue": "zh",
#         "Style": {
#           "Width": 240
#         }
#       }
#     }
#   ]
# }
from __future__ import annotations

import datetime
import hashlib
import json
import os
import random
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Tuple, TypedDict


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


APP_ID = os.getenv("BAIDU_TRANSLATE_APP_ID", "abcdefg")
APP_KEY = os.getenv("BAIDU_TRANSLATE_APP_KEY", "abc@12345")
API_URL = "https://api.fanyi.baidu.com/api/trans/vip/translate"
ICON = "emoji:🌐"
DEFAULT_TARGET_LANGUAGE = "zh"


class WoxPluginBase:
    """Base class for Wox script plugins."""

    class ActionItem(TypedDict, total=False):
        id: str
        name: str
        text: str
        url: str
        path: str
        message: str
        data: Any

    class QueryResult(TypedDict, total=False):
        title: str
        subtitle: str
        icon: str
        score: int
        actions: List["WoxPluginBase.ActionItem"]

    def __init__(self) -> None:
        self.log_file_path = __file__ + ".log"
        self._current_params: Dict[str, Any] = {}

    def is_invoke_from_wox(self) -> bool:
        return "WOX_PLUGIN_ID" in os.environ

    def log(self, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        if self.is_invoke_from_wox():
            with open(self.log_file_path, "a", encoding="utf-8") as file:
                file.write(f"{line}\n")
        else:
            print(f"LOG: {line}", file=sys.stderr)

    def _build_response(self, result: Any, request_id: Any) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "result": result, "id": request_id}

    def _build_error_response(
        self, code: int, message: str, data: Any = None, request_id: Any = None
    ) -> Dict[str, Any]:
        error: Dict[str, Any] = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return {"jsonrpc": "2.0", "error": error, "id": request_id}

    def query(
        self, raw_query: str, trigger_keyword: str, command: str, search: str
    ) -> List["WoxPluginBase.QueryResult"]:
        return []

    def action(self, action_id: str, data: Any) -> None:
        return None

    def handle_query(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        self._current_params = params
        search = params.get("search") or params.get("query", "")
        trigger_keyword = params.get("trigger_keyword", "")
        command = params.get("command", "")
        raw_query = params.get("raw_query", search)
        results = self.query(raw_query, trigger_keyword, command, search)
        return self._build_response({"items": results}, request_id)

    def handle_action(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        action_id = params.get("id", "")
        action_data = params.get("data", "")
        self.action(action_id, action_data)
        return self._build_response({}, request_id)

    def run(self) -> int:
        if self.is_invoke_from_wox():
            try:
                stdin_text = sys.stdin.read()
            except Exception as exc:
                self.log(f"Read stdin failed: {exc}")
                return 1
        else:
            print("Manual mode - please enter text to translate:")
            query_input = input().strip()
            stdin_text = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "query",
                    "params": {
                        "raw_query": query_input,
                        "search": query_input,
                        "trigger_keyword": "fy",
                        "command": "",
                    },
                    "id": 1,
                },
                ensure_ascii=False,
            )

        try:
            request = json.loads(stdin_text)
        except json.JSONDecodeError as exc:
            response = self._build_error_response(-32700, "Parse error", str(exc), None)
            print(json.dumps(response, ensure_ascii=False))
            return 1

        if request.get("jsonrpc") != "2.0":
            response = self._build_error_response(
                -32600, "Invalid Request", None, request.get("id")
            )
            print(json.dumps(response, ensure_ascii=False))
            return 1

        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "query":
            response = self.handle_query(params, request_id)
        elif method == "action":
            response = self.handle_action(params, request_id)
        else:
            response = self._build_error_response(
                -32601,
                "Method not found",
                f"Method '{method}' not supported",
                request_id,
            )

        print(json.dumps(response, ensure_ascii=False))
        return 0


class BaiduTranslatorPlugin(WoxPluginBase):
    """Wox plugin that translates text via Baidu Translate."""

    def _get_settings_map(self) -> Dict[str, str]:
        merged: Dict[str, str] = {}
        for candidate_key in ("settings", "plugin_settings", "Settings", "PluginSettings"):
            raw_settings = self._current_params.get(candidate_key)
            if isinstance(raw_settings, dict):
                for key, value in raw_settings.items():
                    if value is not None:
                        merged[str(key)] = str(value)
        return merged

    def _get_setting(self, key: str, env_name: str, default: str = "") -> str:
        settings_map = self._get_settings_map()
        value = settings_map.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

        top_level_value = self._current_params.get(key)
        if isinstance(top_level_value, str) and top_level_value.strip():
            return top_level_value.strip()

        env_value = os.getenv(env_name, "")
        if env_value.strip():
            return env_value.strip()

        return default

    def _get_app_id(self) -> str:
        return self._get_setting("app_id", "BAIDU_TRANSLATE_APP_ID", APP_ID)

    def _get_app_key(self) -> str:
        return self._get_setting("app_key", "BAIDU_TRANSLATE_APP_KEY", APP_KEY)

    def _get_target_language(self) -> str:
        value = self._get_setting(
            "target_language",
            "BAIDU_TRANSLATE_TARGET_LANGUAGE",
            DEFAULT_TARGET_LANGUAGE,
        )
        return value or DEFAULT_TARGET_LANGUAGE

    def _build_sign(self, app_id: str, text: str, salt: str, app_key: str) -> str:
        raw = f"{app_id}{text}{salt}{app_key}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def _is_configured(self) -> bool:
        app_id = self._get_app_id()
        app_key = self._get_app_key()
        return (
            app_id.strip() not in {"", "abcdefg"}
            and app_key.strip() not in {"", "abc@12345"}
        )

    def _translate(self, text: str) -> Tuple[str, str]:
        normalized = text.strip()
        if not normalized:
            return "", "请输入要翻译的内容"
        if not self._is_configured():
            return "", "请先在插件设置中配置 APP ID 和 APP KEY"

        app_id = self._get_app_id()
        app_key = self._get_app_key()
        target_language = self._get_target_language()
        salt = str(random.randint(32768, 65536))
        params = {
            "q": normalized,
            "from": "auto",
            "to": target_language,
            "appid": app_id,
            "salt": salt,
            "sign": self._build_sign(app_id, normalized, salt, app_key),
        }
        url = f"{API_URL}?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url, timeout=8) as response:
                payload = response.read().decode("utf-8", errors="ignore")
            data = json.loads(payload)
        except urllib.error.URLError as exc:
            self.log(f"Network error: {exc}")
            return "", f"网络请求失败: {exc}"
        except json.JSONDecodeError as exc:
            self.log(f"Invalid JSON response: {exc}")
            return "", "翻译服务返回了无效数据"
        except Exception as exc:
            self.log(f"Unexpected translation error: {exc}")
            return "", f"翻译失败: {exc}"

        if not isinstance(data, dict):
            return "", "翻译服务返回格式不正确"
        if "error_code" in data:
            return "", data.get("error_msg", "翻译失败")

        trans_result = data.get("trans_result")
        if not isinstance(trans_result, list):
            return "", "未获取到翻译结果"

        translated_parts: List[str] = []
        for item in trans_result:
            if not isinstance(item, dict):
                continue
            dst = item.get("dst")
            if isinstance(dst, str) and dst.strip():
                translated_parts.append(dst.strip())

        if not translated_parts:
            return "", "未获取到有效翻译结果"

        return "\n".join(translated_parts), ""

    def query(
        self, raw_query: str, trigger_keyword: str, command: str, search: str
    ) -> List[WoxPluginBase.QueryResult]:
        if not search or not search.strip():
            return [
                {
                    "title": "请输入要翻译的内容",
                    "subtitle": "示例: fy hello world",
                    "icon": ICON,
                    "score": 100,
                }
            ]

        result_text, error = self._translate(search)
        if error:
            return [
                {
                    "title": "百度翻译失败",
                    "subtitle": error,
                    "icon": ICON,
                    "score": 100,
                }
            ]

        return [
            {
                "title": result_text,
                "subtitle": f"百度翻译结果 -> {self._get_target_language()}",
                "icon": ICON,
                "score": 100,
                "actions": [
                    {
                        "id": "copy-to-clipboard",
                        "name": "复制翻译结果",
                        "text": result_text,
                    }
                ],
            }
        ]


if __name__ == "__main__":
    sys.exit(BaiduTranslatorPlugin().run())
