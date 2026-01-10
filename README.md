# Python Command Shell 🐍💻

A custom command shell written in Python, designed for Windows (with Linux/macOS support).
It features ASCII art banners, system information display, and a wide range of built‑in commands.

Developed by: longtrinh2666
Version: 1.1.0

===========================================================
✨ Features
===========================================================

File & Directory Management:
  cd <path>        Change current directory
  ls / dir         List files and folders
  mkdir <name>     Create a new directory
  rm <file>        Delete a file
  rm -f <folder>   Delete a folder and its contents
  copy <src> <dst> Copy a file
  copy -f <src> <dst> Copy a directory tree
  rename/rem <old> <new> Rename a file/folder
  type <file>      Display contents of a text file
  edit <file>      Edit a text file (Ctrl+X to save & exit)

System Information:
  date / time      Show current date and time
  ver / version    Show shell version
  Hardware info    Displayed at startup (CPU, RAM, OS)

Program Execution:
  bash <file>      Run .py, .exe, .com, .bat, .sh
                   (auto requests admin rights if needed)

Python Interactive Mode:
  python           Enter Python REPL inside the shell

Network Manager:
  nwm              Enter network manager mode
    ipconfig/ifconfig   Show network interfaces
    wifi scan           Scan for Wi-Fi networks
    wifi connect <SSID> [password] Connect to Wi-Fi
    wifi disconnect     Disconnect from Wi-Fi

Utilities:
  help             Show this command list
  exit             Quit the shell

===========================================================
🚀 Installation & Usage
===========================================================

Clone the repository:
  git clone https://github.com/longtrinh2666/python-Command-shell.git
  cd python-Command-shell

Install required modules:
  pip install psutil keyboard

Run the shell:
  python source_1.1.0.py

===========================================================
📌 Roadmap
===========================================================

- Add more Bash-like commands (grep, head, tail, etc.)
- Support .myshell scripts for batch execution
- Plugin system for user-defined Python commands
- Customizable prompt (time, user, colors)
- Activity logging

===========================================================
🏷️ Info
===========================================================

Author: longtrinh2666
Version: 1.1.0
