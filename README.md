# 百度翻译 Wox 插件

基于 **Wox 2.0** 框架开发的百度翻译插件，支持输入关键词后调用百度开放平台通用翻译 API 获取实时翻译结果。

使用者输入关键字即可快速翻译文字，并在结果中点击复制翻译内容。

---

## 🔍 功能

- 支持中英互译及其他语言自动检测  
- 输入内容后调用百度翻译 API 实时返回结果  
- 支持关键词触发  
- 结果可一键复制到剪贴板

---

## ⚙️ 激活关键词

| 关键词 | 功能 |
|--------|------|
| `fy` | 翻译输入内容 |
| `translate` | 翻译输入内容 |

---

## 🚀 快速开始

1. 激活 wox自己的`stroe`插件管理器
2. 输入 `store create baidutranslater` 命令，此时会自行打开插件目录的同时创建`baidutranslater.py`模板文件
3. 将插件（`baidutranslater.py`）直接复制到 Wox 插件文件夹下替换模板文件
4. 安装 Python 依赖，替换`baidutranslater.py`中的APP_IP和API_KEY参数
   ```shell
      pip install requests
   ```
5. 在wox2中打开插件管理器并重载本地插件<img width="1198" height="798" alt="Snipaste_2026-03-05_01-29-18" src="https://github.com/user-attachments/assets/da871dec-d431-4b06-88e6-6b6b1e1beb02" />

6. 指定你所喜欢的快捷键<img width="1198" height="798" alt="Snipaste_2026-03-05_01-30-53" src="https://github.com/user-attachments/assets/cd7f9d67-54f3-4ee2-9bea-e6a702a80630" />

7. 激活使用，示例：
   
   <img width="798" height="177" alt="Snipaste_2026-03-05_01-31-47" src="https://github.com/user-attachments/assets/9a6b2bf3-bcde-4118-9516-bfa4310c2fb8" />

   <img width="798" height="177" alt="Snipaste_2026-03-05_01-32-31" src="https://github.com/user-attachments/assets/fd3bfdeb-1f56-45f4-9155-9d2ca072a6e5" />

