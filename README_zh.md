# 🎧 脚本集合

## 📜 概述

本仓库包含各种功能的Python脚本，包括播客数据抓取、规则解析和Cursor应用程序的配置管理。

## ✨ 特性

- **播客爬虫**：从小宇宙网站抓取播客数据，提取相关的`pid`值以供进一步处理。
- **规则解析器**：解析文本文件中的结构化规则块，并将每个块保存为单独的Markdown文件，以便更好地组织。
- **Cursor配置管理器**：通过交互式命令行界面管理Cursor应用程序的配置设置。

## 🚀 安装

1. 克隆仓库：

   ```bash
   git clone https://github.com/yourusername/script-collection.git
   cd script-collection
   ```

2. 安装所需依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ 用法

- **播客爬虫**：运行 `podcast_scraper.py` 以获取并显示指定播客集合中的所有 `pid` 值。
- **规则解析器**：执行 `rule_parser.py`，提供一个包含规则块的输入文件和一个输出目录以保存解析后的文件。
- **生成 .mdc 文件**：使用 [Cursor Directory](https://cursor.directory/generate) 通过上传 `.cursorrules`、`package.json`、`requirements.txt` 或其他项目文件来生成新的 .mdc 文件。
- **Cursor配置管理器**：启动 `cursor_config_manager.py` 以交互式管理配置设置。

## 🤝 贡献

欢迎贡献！请提出问题或提交拉取请求以进行任何增强或修复。

## 📄 许可证

本项目根据MIT许可证进行许可 - 详见 [LICENSE](LICENSE) 文件。
