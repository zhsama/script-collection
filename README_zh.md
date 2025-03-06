# 🎧 脚本集合

## 📜 概述

本仓库包含各种功能的Python脚本，包括播客数据抓取、规则解析和Cursor应用程序的配置管理。

## 📂 项目结构

```
src/
├── cursor/
│   ├── mdc_rules/           # MDC规则模板
│   ├── cursor_rules_convert.py  # 规则转换为MDC格式
│   ├── rule_parser.py       # 规则块解析器
│   └── cursor_config_manager.py # Cursor设置管理
├── telegram/
│   └── webp2gif.py         # Telegram表情包转换器
└── xiaoyuzhou/
    └── podcast_scraper.py  # 播客数据爬虫
```

## ✨ 特性

- **播客爬虫**：从小宇宙网站抓取播客数据，提取相关的`pid`值以供进一步处理。
- **规则解析器**：解析文本文件中的结构化规则块，并将每个块保存为单独的Markdown文件，以便更好地组织。
- **Telegram表情包转换器**：将Telegram表情包（WebP格式）转换为符合微信要求的GIF格式。
- **Cursor规则转换器**：将自定义规则格式转换为MDC（Markdown配置）文件，以增强Cursor功能。

## 🚀 安装

1. 克隆仓库：

   ```bash
   git clone https://github.com/zhsama/script-collection.git
   cd script-collection
   ```

2. 安装所需依赖：

   ```bash
   pip install -r requirements.txt
   ```

### 模块特定依赖

- **播客爬虫**：`requests`, `beautifulsoup4`
- **Telegram表情包转换器**：`opencv-python`, `Pillow`, `numpy`, `psutil`, `tqdm`
- **Cursor工具**：`pyyaml`, `markdown`

## 🛠️ 用法

- **播客爬虫**：运行 `podcast_scraper.py` 以获取并显示指定播客集合中的所有 `pid` 值。
- **规则解析器**：执行 `rule_parser.py`，提供一个包含规则块的输入文件和一个输出目录以保存解析后的文件。
- **生成 .mdc 文件**：使用 [Cursor Directory](https://cursor.directory/generate) 通过上传 `.cursorrules`、`package.json`、`requirements.txt` 或其他项目文件来生成新的 .mdc 文件。
- **Cursor规则转换器**：使用 `cursor_rules_convert.py` 将自定义规则转换为MDC格式：

  ```bash
  python cursor_rules_convert.py -i input_rules.txt -o output_directory
  ```

- **Telegram表情包转换器**：使用 `webp2gif.py` 将Telegram表情包转换为微信格式：

  ```bash
  python webp2gif.py -i ./webp -o ./gif -q 80 -opt -c 256 -f 0 -w 800
  ```

  参数说明：
  - `-i, --input`：WebP文件输入目录（默认：./webp）
  - `-o, --output`：GIF文件输出目录（默认：./gif）
  - `-q, --quality`：GIF质量（1-100，默认：80）
  - `-opt, --optimize`：启用GIF文件大小优化
  - `-c, --max-colors`：最大颜色数（2-256，默认：256）
  - `-f, --fps`：帧率（0=使用原始帧率，默认：0）
  - `-w, --max-width`：最大宽度（像素，默认：800）

## 🤝 贡献

欢迎贡献！请提出问题或提交拉取请求以进行任何增强或修复。

## 📄 许可证

本项目根据MIT许可证进行许可 - 详见 [LICENSE](LICENSE) 文件。
