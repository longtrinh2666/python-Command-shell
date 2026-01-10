Python Command Shell 🐍💻
A custom command shell written in Python, designed primarily for Windows but with support for Linux and macOS. It features ASCII art banners, system information display, and a wide range of built‑in commands for file management, networking, and scripting.
Developed by longtrinh2666.

✨ Features
File & Directory Management
cd <path> – Change the current working directory

ls / dir – List files and subdirectories

mkdir <name> – Create a new directory

rm <file> – Delete a file

rm -f <folder> – Delete a folder and its contents

copy <src> <dst> – Copy a file

copy -f <src> <dst> – Copy a directory tree

rename/rem <old> <new> – Rename a file or folder

type <file> – Display the contents of a text file

edit <file> – Edit a text file (Ctrl+X to save & exit)

System Information
Displays CPU, RAM, OS, and hardware details at startup

date / time – Show current date and time

ver / version – Show shell version

Program Execution
bash <file> – Run .py, .exe, .com, .bat, or .sh files

Automatically requests admin rights if needed (WinError 740 handling)

Python Interactive Mode
python – Enter Python REPL directly inside the shell

Network Manager
nwm – Enter network manager mode

ipconfig / ifconfig – Show network interfaces and IP addresses

wifi scan – Scan for available Wi‑Fi networks

wifi connect <SSID> [password] – Connect to Wi‑Fi

wifi disconnect – Disconnect from Wi‑Fi

Utilities
help – Display command list

exit – Quit the shell

🖼️ Interface Example
Mã
Welcome python Command shell
=== Hardware Info ===
System: Windows
Node Name: DESKTOP-XXXX
Release: 10
Version: 10.0.17763
Machine: AMD64
Processor: Intel64 GenuineIntel
CPU cores: 2
Memory: 1.74 GB
🚀 Installation & Usage
Clone the repository:

bash
git clone https://github.com/longtrinh2666/python-Command-shell.git
cd python-Command-shell
Install required modules:

bash
pip install psutil keyboard
Run the shell:

bash
python source_1.1.0.py
📌 Roadmap
Add more Bash‑like commands (grep, head, tail, etc.)

Support .myshell scripts for batch execution

Plugin system for user‑defined Python commands

Customizable prompt (time, user, colors)

Activity logging

🏷️ Info
Current version: 1.1.0

Author: longtrinh2666
