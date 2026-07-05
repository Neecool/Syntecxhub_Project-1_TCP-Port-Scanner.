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

git clone https://github.com/neecool/Syntecxhub_Project-1_TCP-Port-Scanner.git
cd Syntecxhub_Project-1_TCP-Port-Scanner

**2. Run the scanner (No installation required!):**

Basic Scan (Scans localhost on default ports 1-1024):

python port_scanner.py localhost
Scan a specific IP address:

python port_scanner.py 192.168.1.1
Scan a specific range of ports (e.g., 1 to 1000):

python port_scanner.py example.com -p 1-1000
Scan only specific common ports:

python port_scanner.py scanme.nmap.org -p 22,80,443,8080
Increase speed (more threads) and customize timeout:

python port_scanner.py localhost -T 200 -t 2
View verbose output (detailed logs per port):

python port_scanner.py localhost -v

##  Ethical Disclaimer
Important: This tool is intended for educational purposes, network troubleshooting, and authorized security testing only.
Scanning networks, infrastructure, or devices that you do not own or have explicit written permission to test is illegal in most jurisdictions.
The developer, Syntecxhub, and the contributors are not responsible for any misuse or damage caused by this software. Use it responsibly and only on your own systems (e.g., localhost or lab environments).

## Key Learnings (Internship)
During Week 1 at Syntecxhub, building this project helped me understand:

 Socket Programming Basics: How TCP handshakes work at the code level using connect_ex().

 Concurrency & Multi-threading: Managing thread pools efficiently to scan hundreds of ports simultaneously.

 CLI Argument Parsing: Building user-friendly command-line tools using argparse.

 Real-time Logging: The importance of logging for debugging and compliance.

 Exception Handling: Writing robust code that gracefully handles network timeouts, DNS failures, and refused connections.

##  Developer
Nikulkumar Suthar
Intern at Syntecxhub

##  Acknowledgments
Thanks to Syntecxhub for providing this valuable internship opportunity and challenging project.

Python Software Foundation for maintaining the robust Standard Library.

The open-source community for continuous inspiration and learning resources.
