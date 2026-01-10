import os
import sys
import platform
import code
import subprocess
import datetime
import socket
run = True
try:
    import keyboard
    import psutil
except ModuleNotFoundError:
    print("your system doesn't has some python Module to run , do you want install?")
    while True:
        install = input("(y/n):")
        if install.lower() == "y":
            try: 
                 subprocess.run([sys.executable, "-m", "pip", "install", "keyboard"], check=True)
                 subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=True)
                 import keyboard
                 import psutil
                 break
            except Exception as e:
                print("Error:", e)
                #print("does pip installed on your python? if error not installed choose y")
                #while True:
                    #install_pip_question = input("(y/n):")
                    #if install_pip_question.lower() == "y":
                        #try:
                            #subprocess.run([sys.executable, "get-pip.py"], check=True)
                        #except Exception as e:
                            #print("Error installing pip:", e)
                    #if install_pip_question.lower() == "n":
                        #run = False
                        #break
                    #else:
                        #print("error, only use y/n")

                run = False
                break
        if install.lower() == "n":
            run = False
            break
        else:
            print("error, only use y/n")
    
import time
import shutil
ver = ("1.1.0")
startup_path = os.path.expanduser("~")
os.chdir(startup_path)
dir = os.getcwd()
#__________________________network mgr code____________________________
def wifi_connect(ssid, password=None):
    system = platform.system()
    if system == "Windows":
        # Windows: dùng netsh
        if password:
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"])
        else:
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"])
    elif system == "Linux":
        # Linux: dùng nmcli
        if password:
            subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password])
        else:
            subprocess.run(["nmcli", "d", "wifi", "connect", ssid])
    elif system == "Darwin":  # macOS
        device = "Wi-Fi"
        if password:
            subprocess.run(["networksetup", "-setairportnetwork", device, ssid, password])
        else:
            subprocess.run(["networksetup", "-setairportnetwork", device, ssid])
    else:
        print("Unsupported OS")

def wifi_disconnect():
    system = platform.system()
    if system == "Windows":
        subprocess.run(["netsh", "wlan", "disconnect"])
    elif system == "Linux":
        subprocess.run(["nmcli", "d", "disconnect", "wlan0"])
    elif system == "Darwin":  # macOS
        subprocess.run(["networksetup", "-setairportpower", "Wi-Fi", "off"])
    else:
        print("Unsupported OS")
        
def wifi_scan():
    system = platform.system()
    if system == "Windows":
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks"],
            capture_output=True, text=True
        )
        print(result.stdout)
    elif system == "Linux":
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"],
            capture_output=True, text=True
        )
        print(result.stdout)
    elif system == "Darwin":  # macOS
        result = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
            capture_output=True, text=True
        )
        print(result.stdout)
    else:
        print("Unsupported OS")            
        
#________________________________________________________________________

def run_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == ".py":
            subprocess.run([sys.executable, filename])
        elif ext in (".exe", ".com") and platform.system() == "Windows":
            try:
                subprocess.run([filename])
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 740:
                    print("Program requires admin rights, requesting elevation...")
                    os.startfile(filename, "runas")
                else:
                    print("E: Cannot run exe/com file:", e)
        elif ext == ".bat" and platform.system() == "Windows":
            try:
                subprocess.run([filename], shell=True)
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 740:
                    print("Batch file requires admin rights, requesting elevation...")
                    os.startfile(filename, "runas")
                else:
                    print("E: Cannot run bat file:", e)
        elif ext == ".sh":
            if platform.system() == "Linux":
                subprocess.run(["bash", filename])
            else:
                print("Unsupported OS for .sh")
        else:
            print(f"E: Unsupported file type '{ext}'")
    except Exception as e:
        print("E: Error running file:", e)


def help():
    print("""
 __________________________________________________________________________ 
|______________________________Command List________________________________|
|cd <path>      Displays the name of or changes the current directory.     |
|dir / ls       Displays a list of files and subdirectories in a directory.|
|mkdir <name>   Creates a directory.                                       |
|rm <file>      Deletes one or more files.                                 |
|rm -f <folder> Removes a directory tree.                                  |
|copy <src> <dst>        Copies one or more files to another location.     |
|copy -f <src> <dst>     Copies directory trees.                           |
|rename/rem <old> <new>  Renames a file or folder.                         |
|type <file>    Displays the contents of a text file.                      |
|edit <file>    Opens a text file for editing (Ctrl+X to save & exit).     |
|python         Enter Python interactive shell mode.                       |
|date / time    Displays current date and time.                            |
|ver / version  Displays shell version.                                    |
|exit           Quits the shell program.                                   |
|bash <file>    Executes a file (.py/.exe/.bat/.com/.sh).                  |
|nwm            Enter network manager mode.                                |
|   ipconfig    Show network interfaces and IP addresses.                  |
|   wifi scan   Scan for available Wi-Fi networks.                         |
|   wifi connect <SSID> [password] Connect to Wi-Fi.                       |
|   wifi disconnect Disconnect from Wi-Fi.                                 |
|help           Displays this help information.                            |
|__________________________________________________________________________|
""")

print(r"""
 _________________________________________________________________________ 
|________________________________Welcome__________________________________|
|                     Welcome python Command shell                        |
|                     ┌──────────────────────────┐                        |
|                     │      __                  │                        |
|                     │     |  \                 │                        |
|                     │      \$$\                │                        |
|                     │       \$$\               │                        |
|                     │        >$$\              │                        |
|                     │       /  $$              │                        |
|                     │      /  $$               │                        |
|                     │     |  $$     _________  │                        |
|                     │      \$$     |         \ │                        |
|                     │              \$$$$$$$$$$ │                        |
|                     └──────────────────────────┘                        |
|          create at 1/8/2026 Shell by longtrinh2666 on github.           |
|_________________________________________________________________________|
""")
print("=== Hardware Info ===")
print("System:", platform.system())
print("Node Name:", platform.node())
print("Release:", platform.release())
print("Version:", platform.version())
print("Machine:", platform.machine())
print("Processor:", platform.processor())
print("CPU cores:", psutil.cpu_count(logical=True))
print("Memory:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")
while run:
    user_input = input(f"({dir}) >>>").lower()
    if user_input.startswith("cd "):
        parts = user_input.split(maxsplit=1)
        if len(parts) == 1:
            print(dir)
        else:
            path_2 = parts[1]
            try:
                os.chdir(path_2)
                dir = os.getcwd()
            except FileNotFoundError:
                print("E:The system cannot find the path specified.")
            except OSError:
                print("E:Invalid path syntax")
            
    elif user_input in ("dir", "ls"):
        print(f"\n Directory of {dir}\n")
        for item in os.listdir(dir):
            full_path = os.path.join(dir, item)
            stats = os.stat(full_path)
            size = stats.st_size
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime))
            
            if os.path.isdir(full_path):
                print(f"[Folder] {item:30} {mtime}")
            else:
                print(f"{item:30} {size:10} bytes {mtime}")
                
    elif user_input == "exit":
        run = False
        
    elif user_input.startswith("mkdir "):
        new_folder = user_input[6:]
        os.mkdir(new_folder)
        print("folder created successfully✅")
    elif user_input.startswith("rm "):
        file_to_remove = user_input[3:]
        try:
            os.remove(file_to_remove)
            print("file deleted successfully✅")
        except FileNotFoundError:
            print("E:The program cannot find the file specified.")
        except IsADirectoryError:
            print("E:The program cannot find the file specified.")
    elif user_input.startswith("rm -f "):
        folder_to_remove = user_input[6:]
        try:
            shutil.rmtree(folder_to_remove)
            print("folder deleted successfully✅")
        except FileNotFoundError:
            print("E:The program cannot find the file specified.")
    
    elif user_input == "help":
        help()
    
    elif user_input.startswith("copy "):
        parts = user_input.split()
        if len(parts) >= 3:
            src, dst = parts[1], parts[2]
            try:
               shutil.copy(src, dst)
               print("file copy successfully✅")
            except FileNotFoundError:
                print("E:The program cannot find the file specified.")
        else:
            print("E:error syntax, try again")
    elif user_input.startswith("copy -f "):
        parts = user_input.split()
        if len(parts) >= 3:
            src, dst = parts[1], parts[2]
            try:
                shutil.copytree(src, dst)
                print("folder copy successfully✅")
            except FileExistsError:
                print("E:The directory folder already exists.")
            except FileNotFoundError:
                print("E:The program cannot find the path specified.")
        else:
            print("E:error syntax, try again")
    
    elif user_input.startswith("edit "):
        file_to_edit = user_input.split(maxsplit=1)[1]
        try:
            if os.path.exists(file_to_edit):
                with open(file_to_edit, "r", encoding="utf-8") as f:
                    old_content = f.read()
                print(" ____________________________________________ ")
                print("|Current content in the file:                |")
                print("|____________________________________________|")
                print(old_content)
            else:
                print("W:The file does not exist yet, a new one will be created.")
                
            print(" _______________________________________________________________ ")
            print("|Enter new content (crtl+x+enter at same time to save and exit):|")
            print("|_______________________________________________________________|")
            
            new_lines = []
            while True:
                line = input()
                new_lines.append(line)
                
                if keyboard.is_pressed("ctrl+x"):
                    break
                
            new_content = "\n".join(new_lines)
            
            with open(file_to_edit, "w", encoding="utf-8") as f:
               f.write(new_content)
               
            print(" _____________________________________________ ")
            print("|The file has been edited successfully✅      |")
            print("|_____________________________________________|")
            
        except Exception as e:
            print(" _____________________________________________ ")
            print(f"|E:Error while editing file                   |")
            print("|_____________________________________________|")
        
    elif user_input.startswith(("rename ", "rem ")):
        parts = user_input.split()
        if len(parts) >= 3:
            old_name, new_name = parts[1], parts[2]
            try:
                os.rename(old_name, new_name)
                print("The file name has been edited successfully✅")
            except FileNotFoundError:
                print("E:The system cannot find the file specified.")
            except Exception as e:
                print(f"E:Error changing name")
        else:
            print("E:error syntax, try again")
    
    elif user_input.startswith("type "):
        file_to_read = user_input.split(maxsplit=1)[1]
        try:
            with open(file_to_read, "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("E:File not found")

    elif user_input in ("python"):
        print("Entering Python interactive mode (type exit() or Ctrl+D to quit)")
        code.interact(local=dict(globals(), **locals()))
                
    elif user_input in ("date", "time"):
        now = datetime.datetime.now()
        print(f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')} ")

    elif user_input in ("version", "ver"):
        print(f"ver: {ver}")
        
    elif user_input in ("nwm"):
        print("network mgr (type exit to quit)")
        while True:
            user_input_nwm = input("(network mgr mode) >>>").strip().split()

            if not user_input_nwm:
                continue

            cmd = user_input_nwm[0]

            if cmd == "ipconfig" or cmd == "ifconfig":
                print("=== Network Info ===")
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                print("Hostname:", hostname)
                print("IP Address:", ip_address)

                interfaces = psutil.net_if_addrs()
                for interface_name, interface_addresses in interfaces.items():
                    print(f"\nInterface: {interface_name}")
                    for addr in interface_addresses:
                        if addr.family == socket.AF_INET:
                            print("  IPv4:", addr.address)
                        elif addr.family == socket.AF_INET6:
                            print("  IPv6:", addr.address)
                        elif addr.family == psutil.AF_LINK:
                            print("  MAC:", addr.address)

            elif cmd == "wifi":
                if len(user_input_nwm) >= 2 and user_input_nwm[1] == "connect":
                    ssid = user_input_nwm[2] if len(user_input_nwm) > 2 else None
                    password = user_input_nwm[3] if len(user_input_nwm) > 3 else None
                    if ssid:
                        wifi_connect(ssid, password)
                    else:
                        print("Usage: wifi connect <SSID> [password]")
                elif len(user_input_nwm) >= 2 and user_input_nwm[1] == "disconnect":
                    wifi_disconnect()
                elif len(user_input_nwm) >= 2 and user_input_nwm[1] == "scan":
                    wifi_scan()
                else:
                    print("Usage: wifi connect <SSID> [password] | wifi disconnect | wifi scan")

            elif cmd == "exit":
                break

            elif cmd == "help":
                help()

            else:
                print(f"E:'{' '.join(user_input_nwm)}' is not recognized as an internal.")

        
    elif not user_input:
        continue
    elif user_input.startswith("bash "):
        filename = user_input.split(maxsplit=1)[1]
        run_file(filename)
        
    else:
        print(f"E:'{user_input}' is not recognized as an internal , program or executor file.")      
