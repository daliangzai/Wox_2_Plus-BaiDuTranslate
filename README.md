# 百度翻译 Wox 插件

一个基于 Wox 2 Script Plugin 的百度翻译插件。输入触发词后，会调用百度通用翻译 API，并把结果直接显示在 Wox 中，支持一键复制。

## 功能

- 自动检测源语言
- 默认翻译为中文
- 结果支持直接复制到剪贴板
- 无第三方 Python 依赖
- 支持本地手动调试

## 触发词

- `fy`
- `translate`

## 配置

推荐直接在 Wox 的插件设置页里填写这些项：

- `Baidu APP ID`
- `Baidu APP KEY`
- `Target Language`

其中 `Target Language` 默认为 `zh`，可改为 `en`、`jp`、`kor` 等百度翻译支持的语言代码。

插件也兼容从环境变量读取百度翻译凭证：

- `BAIDU_TRANSLATE_APP_ID`
- `BAIDU_TRANSLATE_APP_KEY`
- `BAIDU_TRANSLATE_TARGET_LANGUAGE`

如果你不想配环境变量，也可以直接修改 [baidutranslater.py](./baidutranslater.py) 里的默认值。

当前优先级是：插件设置页 > 环境变量 > 脚本默认值。

## 安装

1. 在 Wox 中启用 `store` 插件。
2. 执行 `store create baidutranslater`，让 Wox 创建脚本插件目录和模板文件。
3. 用仓库里的 [baidutranslater.py](./baidutranslater.py) 替换模板文件。
4. 在 Wox 插件设置页中配置百度翻译 API 的 `APP ID` 和 `APP KEY`。
5. 按需调整 `Target Language`，默认是 `zh`。
6. 在 Wox 插件管理器中重载本地插件。

## 使用

示例：

```text
fy hello world
translate good morning
```

如果未输入内容，插件会提示你继续输入。

如果未配置 API 凭证，插件会提示先在插件设置页配置，而不是直接请求失败。

## 本地调试

可以直接运行脚本：

```powershell
python .\baidutranslater.py
```

随后输入待翻译文本即可。脚本在非 Wox 环境下会进入手动调试模式。

## 修复说明

当前版本相较初始实现，主要修复了这些问题：

- 移除了重复定义的 `translate()` 函数
- 去掉了 `requests` 依赖，改用标准库 `urllib`
- 增加了网络异常、JSON 解析异常和返回格式校验
- 兼容了 Wox 调用和本地调试两种入口
- 处理了 Windows 控制台下的 UTF-8 输出问题
- 增加了 `SettingDefinitions`，允许在 Wox 插件设置页配置 `APP ID`、`APP KEY` 和目标语言
