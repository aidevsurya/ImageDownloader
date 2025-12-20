## 🖼️ Image Downloader GUI (DuckDuckGo + Bing)

A stable, dark-themed desktop GUI application to download images from DuckDuckGo and Bing without APIs, captchas, or scraping issues.

Built with Python + Tkinter, designed for dataset creation, research, and general image collection.

✨ Features

🎨 Modern dark UI (clean & aesthetic)

🧩 Simple GUI – no command-line required

🔍 Search images by keyword

🌐 Search engines:

DuckDuckGo

Bing

All (Duck + Bing combined)

📁 Custom output folder selection

📊 Live progress bar

🧠 Duplicate image removal

⚡ Non-freezing UI (threaded downloads)

🐧 Works perfectly on Linux

❌ No Google

❌ No APIs

❌ No Selenium

❌ No scraping instability

## 📸 Screenshot (Optional)



## 🛠️ Tech Stack

Python 3.8+

Tkinter (built-in GUI framework)

duckduckgo-search

requests

tqdm

## 📦 Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/image-downloader-gui.git
cd image-downloader-gui

2️⃣ (Recommended) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

## ▶️ Usage
Run the GUI
python ImageDownloader.py
or
ImageDownloader
Using the App

Enter search keywords

Enter number of images

Select search engine:

Duck

Bing

All

Choose output folder

Click Download Images

Images will be saved to:

<output_folder>/<search_keywords>/

📁 Project Structure
image-downloader-gui/
├── img_downloader_gui.py
├── requirements.txt
├── README.md
└── images/
    └── example_keyword/

📄 requirements.txt
duckduckgo-search>=5.3.0
requests>=2.31.0
tqdm>=4.66.0


Tkinter is included with Python by default.

🚫 Why Google Is Not Included

Google Images:

Aggressively blocks scraping

Causes silent failures

Breaks frequently

Requires paid APIs for stability

This project prioritizes:
✅ Reliability
✅ Clean dependencies
✅ Reproducibility

DuckDuckGo and Bing are more than sufficient for:

Computer Vision datasets

ML experiments

Research collections

🧠 Use Cases

AI / ML dataset creation

Computer Vision projects

Research & experimentation

Educational use

Bulk image collection

🔒 Stability & Safety

No API keys required

No captcha handling

No browser automation

No dependency conflicts

Safe for repeated use

🚀 Future Improvements (Optional)

Image preview grid

Pause / Resume downloads

Image size & format filters

Batch keyword file support

Dataset export (YOLO / COCO)

Windows .exe / Linux .AppImage

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a new branch

Commit changes

Open a pull request

📜 License

MIT License
Free to use, modify, and distribute.

⭐ Support

If this project helped you:

⭐ Star the repository

🐛 Report issues

💡 Suggest features
