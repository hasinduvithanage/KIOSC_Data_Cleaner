# KIOSC Survey Data Cleaner App

---

## 🚀 Project Overview

This desktop application is designed to simplify and automate the data cleaning process for KIOSC staff. Currently, survey data collected from various programs is delivered in inconsistent CSV formats, leading to time-consuming, error-prone, and inconsistent manual cleaning efforts.

This app aims to provide a **lightweight, user-friendly, and offline solution** that allows non-technical KIOSC staff to:
1.  **Select** the specific type of survey data (e.g., Discovery, VCE, or VCES).
2.  **Upload** the corresponding raw CSV file.
3.  **Automatically clean** the data based on predefined, survey-specific logic.
4.  **Save** the cleaned file, ready for immediate analysis.

Our goal is to ensure consistent, fast, and accurate data preparation, eliminating the need for manual data manipulation in tools like Excel or through programming.

---

## ✨ Features

* **Intuitive Graphical User Interface (GUI):** Easy-to-use interface with clear options for selecting survey types.
* **Survey-Specific Cleaning Logic:** Automated cleaning tailored for three distinct survey data formats (Discovery, VCE, VCES).
* **CSV File Handling:** Seamless upload of raw CSVs and saving of cleaned data.
* **Offline Capability:** The application runs completely offline, requiring no internet connection after installation.
* **Standalone Executable:** Distributed as a simple `.exe` file for easy installation and double-click execution on any Windows computer.
* **Error Handling:** Provides clear user notifications for issues like invalid CSV formats.
* **Maintainable Codebase:** Designed for easy extension to incorporate future survey types.

---

## 🛠️ How to Use (for KIOSC Staff)

*(This section will be detailed once the app is packaged. For now, it's a placeholder.)*

1.  **Download:** Obtain the latest `KIOSC_Data_Cleaner.exe` file from [Link to release/shared drive - *To be added*].
2.  **Install:** Simply double-click the `.exe` file to run the application (no complex installation required).
3.  **Launch:** Once opened, you'll see a simple window.
4.  **Select Survey Type:** Choose the button corresponding to the type of survey data you wish to clean (e.g., "Clean Survey A Data").
5.  **Upload CSV:** A file dialog will appear. Navigate to your raw survey CSV file and select it.
6.  **Clean & Save:** The app will automatically process the data. Once complete, a save dialog will appear, allowing you to choose where to save your newly cleaned CSV file.
7.  **Confirmation:** A success message will confirm that your data has been cleaned and saved.

---

## ⚙️ Development Setup (for Developers)

### Prerequisites

* Python 3.x (recommended 3.8+)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/KIOSC_Data_Cleaner.git](https://github.com/YourGitHubUsername/KIOSC_Data_Cleaner.git)
    cd KIOSC_Data_Cleaner
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You'll need to create a `requirements.txt` file after installing pandas: `pip freeze > requirements.txt`)*

### Running the Application

To run the application in development mode:

```bash
python main_gui.py
```
Or run the local file
