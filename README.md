#  TCP Port Scanner 
## Internship Project for Syntecxhub
Learn socket programming, multi-threading, and network security fundamentals in Python! ⚡
Covers TCP connect scanning, concurrent threads, port range filtering, and real-time logging.

**Tech Stack:** Python (Standard Library: `socket`, `threading`, `argparse`, `logging`)

---

##  Introduction
Developed as part of my internship with **Syntecxhub (Week 1, Project 1)**, this project provides a practical implementation of a TCP Port Scanner. 
It demonstrates how to establish network connections, handle low-level socket errors, and dramatically speed up scanning using thread-based concurrency. 
The tool is designed to be lightweight, dependency-free, and highly configurable for both beginners and security enthusiasts.

---

##  Features
-  **Single/Multiple Host Scanning** – Scan any IP address or domain name.
-  **Flexible Port Selection** – Define a range (`1-1024`) or a list (`80,443,8080`).
-  **Multi-Threaded Architecture** – Uses concurrent threads to speed up the scanning process (configurable thread limit).
-  **Comprehensive Logging** – Writes every result (Open/Closed/Timeout/Error) to a timestamped log file (`port_scan_results.log`).
-  **Timeout Configuration** – Adjust connection timeout for different network conditions.
-  **Graceful Exception Handling** – Catches DNS errors, connection refusals, and timeouts without crashing.
-  **User-Friendly Summary** – Prints a clean summary of open ports and total statistics upon completion.

---

##  Technologies Used
- **Python 3.x**
- **Standard Libraries**: 
  - `socket` (Core networking)
  - `threading` (Concurrency)
  - `argparse` (Command-line interface)
  - `logging` (Debugging & result storage)
  - `ipaddress` (Validation)

*(Zero external dependencies!)*

---

##  How to Run the Project?

###  Prerequisites:
- Python 3.6+ installed on your system.
- Basic command-line knowledge.

###  Setup & Execution:

**1. Clone the repository (or navigate to the project folder):**
```bash
git clone https://github.com/neecool/Syntecxhub_Project-1_TCP-Port-Scanner.git
cd Syntecxhub_Project-1_TCP-Port-Scanner
