# Web Screenshot

Web Screenshot is an automated tool that captures screenshots of websites from a list of URLs provided in a JSON file. It is designed to process multiple sites in batches and save the images to a specified directory.

## Features

- Automation using Selenium and Chrome/Brave.
- Batch processing for efficiency.
- Progress tracking to avoid processing duplicates.
- Screenshots saved with descriptive filenames based on domain and ID.

## Prerequisites

- Python 3.x
- Google Chrome or Brave Browser installed.
- WebDriver Manager to handle browser driver management.

## Installation

1. Clone this repository or download the project files.
2. Ensure the following dependencies are installed:

```bash
pip install selenium webdriver-manager pillow
```

3. Configure the Brave browser path in the script if not using the default location:

```python
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
```

4. Create an `items.json` file in the project directory with the following format:

```json
[
  {
    "id": 1,
    "name": "Example Golf Course",
    "web": "https://example.com"
  },
  {
    "id": 2,
    "name": "Another Golf Course",
    "web": "https://anotherexample.com"
  }
]
```

## Usage

1. Define the base paths for your project:

```python
BASE_DIR = r"<project_base_path>"
JSON_FILE = os.path.join(BASE_DIR, 'items.json')
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'img')
```

2. Run the script:

```bash
python <script_name>.py
```

The script will process the URLs from the JSON file and save screenshots in the configured directory.

## Generated Files

- **Screenshots:** Saved in the specified directory (`img`) with filenames combining the ID and domain.
- **Progress:** The `screenshot_progress.txt` file tracks the last processed ID to avoid duplicates.

## Customization

- Adjust the batch size by modifying the `batch_size` parameter in the `capture_website_screenshots` function.
- Modify the wait time between batches if needed:

```python
time.sleep(5)  # 5-second pause between batches
```

## Author

- **Laymon López**
- Email: [info@laylop.com](mailto:info@laylop.com)

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
