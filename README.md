# 🎧 Script Collection

## 📜 Overview

This repository contains a collection of Python scripts designed for various functionalities, including podcast data scraping, rule parsing, and configuration management for the Cursor application.

## 📂 Project Structure

```
src/
├── cursor/
│   ├── mdc_rules/           # MDC rules templates
│   ├── cursor_rules_convert.py  # Converts rules to MDC format
│   ├── rule_parser.py       # Parses rule blocks
│   └── cursor_config_manager.py # Cursor settings manager
├── docker/
│   └── docker_restart.sh    # Docker container auto-restart script
├── telegram/
│   └── webp2gif.py         # Telegram sticker converter
└── xiaoyuzhou/
    └── podcast_scraper.py  # Podcast data scraper
```

## ✨ Features

- **Podcast Scraper**: Scrapes podcast data from the Xiaoyuzhou website, extracting relevant `pid` values for further processing.
- **Rule Parser**: Parses structured rule blocks from a text file and saves each block as a separate Markdown file for better organization.
- **Telegram Sticker Converter**: Converts Telegram stickers (WebP) to WeChat-compatible GIF format with optimized settings.
- **Cursor Rules Converter**: Converts custom rule formats into MDC (Markdown Configuration) files for enhanced Cursor functionality.
- **Docker Container Auto-restart**: Sets up scheduled restarts for Docker containers using cron jobs.

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

### Module-specific Dependencies

- **Podcast Scraper**: `requests`, `beautifulsoup4`
- **Telegram Sticker Converter**: `opencv-python`, `Pillow`, `numpy`, `psutil`, `tqdm`
- **Cursor Tools**: `pyyaml`, `markdown`
- **Docker Tools**: Docker Engine installed on the system

## 🛠️ Usage

- **Podcast Scraper**: Run `podcast_scraper.py` to fetch and display all `pid` values from the specified podcast collection.
- **Rule Parser**: Execute `rule_parser.py` and provide an input file containing rule blocks along with an output directory to save the parsed files.
- **Generate .mdc Files**: Use [Cursor Directory](https://cursor.directory/generate) to generate new .mdc files for your project by uploading your `.cursorrules`, `package.json`, `requirements.txt`, or other project files.
- **Cursor Rules Converter**: Use `cursor_rules_convert.py` to convert custom rule formats to MDC:

  ```bash
  python cursor_rules_convert.py -i input_rules.txt -o output_directory
  ```

- **Telegram Sticker Converter**: Use `webp2gif.py` to convert Telegram stickers to WeChat format:

  ```bash
  python webp2gif.py -i ./webp -o ./gif -q 80 -opt -c 256 -f 0 -w 800
  ```

  Parameters:
  - `-i, --input`: Input directory with WebP files (default: ./webp)
  - `-o, --output`: Output directory for GIF files (default: ./gif)
  - `-q, --quality`: GIF quality (1-100, default: 80)
  - `-opt, --optimize`: Enable GIF size optimization
  - `-c, --max-colors`: Maximum colors (2-256, default: 256)
  - `-f, --fps`: Frame rate (0=original, default: 0)
  - `-w, --max-width`: Maximum width in pixels (default: 800)

- **Docker Container Auto-restart**: Use `docker_restart.sh` to set up scheduled container restarts:

  ```bash
  sudo bash docker_restart.sh <container_name> [cron_expression]
  ```

  Parameters:
  - `container_name`: Name of the Docker container to restart
  - `cron_expression`: Optional cron expression (default: "0 4 ** *" - 4 AM daily)

  Example:

  ```bash
  # Restart container 'web-app' every day at 4 AM
  sudo bash docker_restart.sh web-app

  # Restart container 'db-server' every Sunday at 2 AM
  sudo bash docker_restart.sh db-server "0 2 * * 0"
  ```

  The script will:
  1. Create a restart script in `/usr/local/bin/`
  2. Set up a cron job for scheduled execution
  3. Log all restarts to `/var/log/docker_restart.log`

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
