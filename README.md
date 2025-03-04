# 🎧 Script Collection

## 📜 Overview

This repository contains a collection of Python scripts designed for various functionalities, including podcast data scraping, rule parsing, and configuration management for the Cursor application.

## ✨ Features

- **Podcast Scraper**: Scrapes podcast data from the Xiaoyuzhou website, extracting relevant `pid` values for further processing.
- **Rule Parser**: Parses structured rule blocks from a text file and saves each block as a separate Markdown file for better organization.
- **Cursor Config Manager**: Manages configuration settings for the Cursor application through an interactive command-line interface.

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/zhsama/script-collection.git
   cd script-collection
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

- **Podcast Scraper**: Run `podcast_scraper.py` to fetch and display all `pid` values from the specified podcast collection.
- **Rule Parser**: Execute `rule_parser.py` and provide an input file containing rule blocks along with an output directory to save the parsed files.
- **Generate .mdc Files**: Use [Cursor Directory](https://cursor.directory/generate) to generate new .mdc files for your project by uploading your `.cursorrules`, `package.json`, `requirements.txt`, or other project files.
- **Cursor Config Manager**: Launch `cursor_config_manager.py` to reset the machine code of Cursor to achieve unlimited free trial extension.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
