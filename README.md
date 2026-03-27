# 📡 Stream-Catcher-Pro: Lightweight Live Stream Recorder

## 📖 Overview
**Stream-Catcher-Pro** is an ultra-lightweight, resource-efficient live stream recording dashboard designed to effortlessly capture your favorite content creators across multiple broadcasting platforms, including Bigo Live, TikTok, and YouTube. 

Engineered specifically to maintain maximum stability on low-specification hardware (e.g., 4GB RAM environments), this application streamlines the media archiving process by eliminating the need for heavy browser rendering during active recordings. 

As an open-source initiative, this project aims to provide a robust, accessible, and elegant tool for the community. We hope it brings substantial value to your media archiving workflow!

## ✨ Key Features
* **Low-Spec Optimized Architecture:** Bypasses heavy browser video rendering by securely capturing raw `.ts` streams directly to the local storage, preserving CPU and RAM.
* **Automated HLS Fetching:** Seamlessly integrates with `Streamlink` to automatically retrieve the highest quality `.m3u8` stream URLs.
* **"The Brake System" (Safe Termination):** Employs a secure termination protocol to safely halt `FFmpeg` background processes without corrupting the finalized video files.
* **Smart Auto-Detector:** Continuously monitors background `FFmpeg` tasks and automatically resets the UI if a live stream abruptly disconnects.
* **Advanced Host Management:** A complete CRUD (Create, Read, Update, Delete) database system with pagination and a smart search filter that normalizes aesthetic Unicode fonts.

## 🔗 Optional: Automated Host Sync (Brave Browser)
To eliminate the friction of manually entering host details, this application includes an **optional** automated synchronization feature tailored for Brave Browser users. 

**Purpose:** It allows you to seamlessly import live stream profiles directly from your browser bookmarks into the application's database with zero manual data entry.

**How to use this feature:**
1. Open your Brave Browser and create a specific bookmark folder named exactly `bg`.
2. Bookmark your target host profiles (e.g., Bigo Live or TikTok pages) into this `bg` folder.
3. Upon launching the dashboard, the background script will automatically detect, extract, and append these new bookmarks into your `hosts_data.json` database.
*Note: If you prefer not to use this feature, simply ignore it. You can fully manage your database manually via the built-in "Database" menu in the dashboard.*

## 🛠️ Technology Stack
* **Python 3** (Core Logic)
* **Streamlit** (Interactive Web GUI)
* **Streamlink** (Stream Extraction)
* **FFmpeg** (Direct Stream Copy / Recording)
* **Requests** (Lightweight HTTP Header Polling)

## 🚀 Installation Guide

### Prerequisites
1. Ensure **Python 3.x** is installed on your machine.
2. Install **FFmpeg** and ensure it is added to your system's PATH variable.

### Setup Instructions

**1. Clone this repository to your local machine:**
    
    git clone [https://github.com/HandiSetiawanHamdani/Stream-Catcher-Pro.git](https://github.com/HandiSetiawanHamdani/Stream-Catcher-Pro.git)

**2. Navigate to the project directory and create a virtual environment:**
    
    cd Stream-Catcher-Pro
    python -m venv venv

**3. Activate the virtual environment:**
* **Windows:** `.\venv\Scripts\activate`
* **macOS/Linux:** `source venv/bin/activate`

**4. Install the required dependencies:**
    
    pip install -r requirements.txt

**5. Initialize Database:**
Rename the provided `hosts_data_template.json` to `hosts_data.json` to initialize your local database.

## 💻 Usage
To launch the dashboard, execute the following command within your activated virtual environment:
    
    streamlit run app.py

*Tip: To further minimize resource consumption on low-spec machines, you can run the app with usage stats disabled:* `streamlit run app.py --browser.gatherUsageStats false`.

## 🤝 Contribution
Contributions, issues, and feature requests are highly welcome! Feel free to check the issues page.

## 📄 License
This project is open-source and available under the MIT License.
