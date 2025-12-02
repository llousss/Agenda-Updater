# 📞 Agenda-Updater

**Automatic Network Scanner & Corporate Phonebook Updater**

[![Status](https://img.shields.io/badge/status-active-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.x-yellow)]()

Agenda-Updater is a tool designed to automatically scan your local network for IP phones and update their internal contact directory (phonebook).
This eliminates the manual, repetitive process of updating each phone individually.

---

## 🚀 Features

### 🔍 Network IP Scanner

* Scans a configurable range of IP addresses
* Detects active devices (phones) in the network
* Filters reachable/unreachable devices
* Generates a list of phones eligible for update

### 📁 Phonebook Updater

* Uploads the selected directory file to all detected phones
* Supports batch update
* Logs success and failure for each device
* Creates backup files for safety (if configured)

### 🧩 Simple Structure & Easy to Customize

* Clean source code
* Editable configuration file
* Output logs in CSV format for easy tracking

---

## 📂 Project Structure

```
Agenda-Updater/
├── backup agenda/          # Optional backup directory for previous phonebooks
├── dist/                   # Build/output files (if used)
├── build/                  # Build artifacts
├── resultado.csv           # Generated update log
├── phonebook.csv           # Example phonebook file 
├── scanner.py              # IP scanning logic
├── updater.py              # Phonebook update logic
├── config.py               # Settings (IPs, credentials, file paths)
└── README.md               # Documentation
```

---

## ⚙️ Configuration

Edit the file **`config.py`** to adjust the scanner and updater behavior:

```python
# Example Configuration

IP_RANGE_START = "192.168.0.1"
IP_RANGE_END   = "192.168.0.255"

PHONEBOOK_FILE = "phonebook.csv"   # or .xml / .json depending on your phones

CREDENTIALS = {
    "username": "admin",
    "password": "your_password"
}

TIMEOUT = 5   # Timeout for ping/HTTP requests in seconds
```

Make sure to set the correct:

* IP range
* File path for your phonebook
* Login credentials (if your phones require authentication)

---

## ▶️ How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/llousss/Agenda-Updater
   cd Agenda-Updater
   ```

2. Ensure Python 3.x is installed.

3. Install dependencies (if needed):

   ```bash
   pip install -r requirements.txt
   ```

   *(Create this file if you want dependency automation.)*

4. Update the configuration in `config.py`.

5. Run the scanner:

   ```bash
   python scanner.py
   ```

6. Run the updater:

   ```bash
   python updater.py
   ```

7. After execution, check **`resultado.csv`** for:

   * IP address
   * Connection status
   * Update status (success/failure)
   * Error details (if any)

---

## 📝 Output Example (resultado.csv)

| IP Address   | Reachable | Updated | Message               |
| ------------ | --------- | ------- | --------------------- |
| 192.168.0.12 | Yes       | Yes     | Successfully updated  |
| 192.168.0.15 | No        | -       | Device unreachable    |
| 192.168.0.22 | Yes       | No      | Authentication failed |

---

## 🏢 Why Use It?

* Ideal for companies that use multiple IP phones
* Ensures every phone has the same updated contact list
* Eliminates slow manual updates
* Improves IT workflow and reduces errors

---

## 🔒 Notes & Recommendations

* Ensure that your phones support remote phonebook updates (HTTP, TFTP, XML upload, etc.)
* Make sure the network allows ping/HTTP communication
* Run during maintenance windows for large batches
* Always keep backups of your phonebook files

---

## 🤝 Contributing

Contributions are welcome!
You can:

* Open issues
* Submit pull requests
* Suggest new features
* Improve documentation
