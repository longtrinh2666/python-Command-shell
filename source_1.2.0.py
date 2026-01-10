import os
import importlib.util
import zipfile
import sys
import zipfile
import tarfile
import platform
import code
import subprocess
import datetime
import socket
import atexit
run = True
try:
    import psutil
    import speedtest
    import requests
    system = platform.system()
    if system in ("Darwin", "Linux"):
        import readline 
    elif system == "Windows":
        import pyreadline3
except ModuleNotFoundError:
    print("your system doesn't has some python Module to run , do you want install?")
    while True:
        install = input("(y/n):")
        if install.lower() == "y":
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "speedtest-cli"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=True)
                if system in ("Darwin", "Linux"):
                    subprocess.run([sys.executable, "-m", "pip", "install", "readline"], check=True)
                    import readline
                    import psutil
                    import requests
                    import speedtest
                    break
                elif system == "Windows":    
                    subprocess.run([sys.executable, "-m", "pip", "install", "pyreadline3"], check=True)
                    import pyreadline3
                    import psutil
                    import requests
                    import speedtest
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
try:
    import readline   # Linux/macOS có sẵn
except ImportError:
    import pyreadline3 as readline  # Windows
    
if platform.system() == "Windows":
    histfile = os.path.join(os.environ.get("TEMP", os.getcwd()), "myshell_history.txt")
else:
    histfile = os.path.join("/tmp", "myshell_history.txt")
    
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)
ver = ("1.2.0")
startup_path = os.path.expanduser("~")
os.chdir(startup_path)
dir = os.getcwd()
#__________________________network mgr code____________________________
def wifi_connect(ssid, password=None):
    system = platform.system()
    if system == "Windows":
        if password:
            # tạo thư mục profiles nếu chưa có
            os.makedirs("profiles", exist_ok=True)
            profile_path = os.path.join("profiles", f"{ssid}.xml")

            profile_xml = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
  <name>{ssid}</name>
  <SSIDConfig>
    <SSID>
      <name>{ssid}</name>
    </SSID>
  </SSIDConfig>
  <connectionType>ESS</connectionType>
  <connectionMode>auto</connectionMode>
  <MSM>
    <security>
      <authEncryption>
        <authentication>WPA2PSK</authentication>
        <encryption>AES</encryption>
        <useOneX>false</useOneX>
      </authEncryption>
      <sharedKey>
        <keyType>passPhrase</keyType>
        <protected>false</protected>
        <keyMaterial>{password}</keyMaterial>
      </sharedKey>
    </security>
  </MSM>
</WLANProfile>
"""
            with open(profile_path, "w", encoding="utf-8") as f:
                f.write(profile_xml)

            # add profile vĩnh viễn
            subprocess.run(["netsh", "wlan", "add", "profile", f"filename={profile_path}", "user=all"], check=False)
            # connect
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=False)
        else:
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=False)

    elif system == "Linux":
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
        
#____________________________plugins loader______________________________
commands = {}
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
def load_plugins():
    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        print("Plugins folder not found, skipping plugin load.")
        return
    
    loaded = 0
    for file in os.listdir(plugin_dir):
        if file.endswith(".py"):
            file_path = os.path.join(plugin_dir, file)
            module_name = file[:-3]  # bỏ .py
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "register"):
                    module.register(commands)
                    loaded += 1
            except Exception as e:
                print(f"E: Failed to load plugin {file}: {e}")
    
    if loaded == 0:
        print("No plugins found in plugin folder.")
        os.chdir(startup_path)
    else:
        print(f"{loaded} plugin(s) loaded successfully ✅")
        os.chdir(startup_path)
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

def zip_files(zip_name, files):
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for f in files:
                zipf.write(f)
        print(f"Files compressed into {zip_name} ✅")
    except Exception as e:
        print("E: Error creating zip:", e)

def unzip_file(zip_path, extract_to="."):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)
        print(f"File {zip_path} extracted successfully to {extract_to} ✅")
    except Exception as e:
        print("E: Error extracting zip:", e)

def tar_files(tar_name, files):
    try:
        with tarfile.open(tar_name, "w") as tarf:
            for f in files:
                tarf.add(f)
        print(f"Files compressed into {tar_name} ✅")
    except Exception as e:
        print("E: Error creating tar:", e)

def untar_file(tar_path, extract_to="."):
    try:
        with tarfile.open(tar_path, "r") as tarf:
            tarf.extractall(extract_to)
        print(f"File {tar_path} extracted successfully to {extract_to} ✅")
    except Exception as e:
        print("E: Error extracting tar:", e)

def zip_folder(folder_path, output_name):
    try:
        shutil.make_archive(output_name, 'zip', folder_path)
        print(f"Folder '{folder_path}' compressed into '{output_name}.zip' ✅")
    except Exception as e:
        print("E: Error zipping folder:", e)
        
def tar_folder(folder_path, output_name):
    try:
        with tarfile.open(output_name, "w") as tarf:
            tarf.add(folder_path, arcname=os.path.basename(folder_path))
        print(f"Folder '{folder_path}' compressed into '{output_name}' ✅")
    except Exception as e:
        print("E: Error creating tar:", e)

def list_zip(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            for name in zipf.namelist():
                print(name)
    except FileNotFoundError:
        print("E: Zip file not found")
    except zipfile.BadZipFile:
        print("E: Invalid zip file")

def list_tar(tar_path):
    try:
        with tarfile.open(tar_path, 'r') as tarf:
            for member in tarf.getmembers():
                print(member.name)
    except FileNotFoundError:
        print("E: Tar file not found")
    except tarfile.ReadError:
        print("E: Invalid tar file")
def help():
    print("""
 __________________________________________________________________________ 
|______________________________Command List________________________________|
| cd <path>        Change current directory or show current path.          |
| dir / ls         List files and folders in current directory.            |
| mkdir <name>     Create a new folder.                                    |
| rm <file>        Delete a file.                                          |
| rm -f <folder>   Delete a folder tree.                                   |
| copy <src> <dst> Copy a file.                                            |
| copy -f <src> <dst> Copy a folder tree.                                  |
| rename/rem <old> <new> Rename a file or folder.                          |
| type <file>      Show contents of a text file.                           |
| edit <file>      Edit a text file (':save' to save, ':exit' to discard). |
| python           Enter Python interactive shell.                         |
| date / time      Show current date and time.                             |
| ver / version    Show shell version.                                     |
| exit             Quit the shell.                                         |
| bash <file>      Run a file (.py/.exe/.bat/.com/.sh).                     |
| zip <zip> <files...>   Compress files into a zip archive.                |
| unzip <zip> [dst]     Extract a zip archive.                             |
| tar <tar> <files...>   Compress files into a tar archive.                |
| untar <tar> [dst]     Extract a tar archive.                             |
| zip -f <zip> <folder> Compress a folder into zip.                        |
| tar -f <tar> <folder> Compress a folder into tar.                        |
| zip ls <zip>     List contents of a zip archive.                         |
| tar ls <tar>     List contents of a tar archive.                         |
| clear / cls      Clear the console screen.                               |
| nwm              Enter network manager mode.                             |
|   ipconfig/ifconfig   Show network interfaces and IP addresses.          |
|   wifi scan           Scan for available Wi-Fi networks.                 |
|   wifi connect <SSID> [password] Connect to Wi-Fi (creates profile).     |
|   wifi disconnect     Disconnect from Wi-Fi.                             |
|   ping <host>         Ping a hostname or IP.                             |
|   speedtest           Run a network speed test.                          |
|   publicip            Show current public IP address.                    |
| help             Show this help information.                             |
|__________________________________________________________________________|
""")


print(r"""
 _________________________________________________________________________ 
|________________________________Welcome__________________________________|
|                       Welcome klpython terminal                         |
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
load_plugins()

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
    user_input = input(f"({dir})@" + platform.node() + ">>>").strip()
    if not user_input:
        continue

    parts = user_input.split()
    cmd = parts[0].lower()   
    args = parts[1:]         

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
        confirm = input("Are you sure? (y/n)").lower()
        if confirm == "y":
            try:
                os.remove(file_to_remove)
                print("file deleted successfully✅")
            except FileNotFoundError:
                print("E:The program cannot find the file specified.")
            except IsADirectoryError:
                print("E:The program cannot find the file specified.")
        elif confirm == "n":
            print("canceled")
            continue
        else:
            print("canceled")
            continue
    elif user_input.startswith("rm -f "):
        folder_to_remove = user_input[6:]
        confirm = input("Are you sure? (y/n)").lower()
        if confirm == "y":
            try:
                shutil.rmtree(folder_to_remove)
                print("folder deleted successfully✅")
            except FileNotFoundError:
                print("E:The program cannot find the file specified.")
        elif confirm == "n":
            print("canceled")
            continue
        else:
            print("canceled")
            continue
    
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
                
            print(" _______________________________________________________________________________ ")
            print("|Enter new content(type ':save' to save and exit, type ':exit' to exit discard):|")
            print("|_______________________________________________________________________________|")
            
            new_lines = []
            while True:
                line = input()
                if line.strip() == ":save":
                    new_content = "\n".join(new_lines)
            
                    with open(file_to_edit, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(" _____________________________________________ ")
                    print("|The file has been edited successfully✅      |")
                    print("|_____________________________________________|")
                    break
                if line.strip() == ":exit":
                    print(" _____________________________________________ ")
                    print("|Edit discarded, no changes saved ❌          |")
                    print("|_____________________________________________|")
                    break
                else:                    
                    new_lines.append(line)
                
               

            
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

            elif cmd == "ping":
                if len(user_input_nwm) >= 2:
                    host = user_input_nwm[1]
                    subprocess.run(["ping", host])
                else:
                    print("Usage: ping <hostname>")
            elif cmd == "speedtest":
                try:
                    st = speedtest.Speedtest()
                    print("Finding best server...")
                    st.get_best_server()
                    print("Download speed:", round(st.download() / 1e6, 2), "Mbps")
                    print("Upload speed:", round(st.upload() / 1e6, 2), "Mbps")
                    print("Ping:", st.results.ping, "ms")
                except Exception as e:
                    print("E: Cannot run speedtest:", e)
            elif cmd == "publicip":
                try:
                    ip = requests.get("https://api.ipify.org").text
                    print("Public IP:", ip)
                except Exception as e:
                    print("E: Cannot fetch public IP:", e)
            else:
                print(f"E:'{' '.join(user_input_nwm)}' is not recognized as an internal.")

        
    elif user_input.startswith("bash "):
        filename = user_input.split(maxsplit=1)[1]
        run_file(filename)

    elif user_input.startswith("zip "):
        parts = user_input.split()
        if len(parts) >= 3:
            zip_name = parts[1]
            files = parts[2:]
            zip_files(zip_name, files)
        else:
            print("Usage: zip <zipfile> <file1> <file2> ...")

    elif user_input.startswith("unzip "):
        parts = user_input.split()
        if len(parts) >= 2:
            zip_path = parts[1]
            extract_to = parts[2] if len(parts) > 2 else "."
            unzip_file(zip_path, extract_to)
        else:
            print("Usage: unzip <zipfile> [destination]")

    elif user_input.startswith("tar "):
        parts = user_input.split()
        if len(parts) >= 3:
            tar_name = parts[1]
            files = parts[2:]
            tar_files(tar_name, files)
        else:
            print("Usage: tar <tarfile> <file1> <file2> ...")

    elif user_input.startswith("untar "):
        parts = user_input.split()
        if len(parts) >= 2:
            tar_path = parts[1]
            extract_to = parts[2] if len(parts) > 2 else "."
            untar_file(tar_path, extract_to)
        else:
            print("Usage: untar <tarfile> [destination]")

    elif user_input.startswith("zip -f"):
        parts = user_input.split()
        if len(parts) == 3:
            output_name = parts[1].replace(".zip", "")
            folder_path = parts[2]
            zip_folder(folder_path, output_name)
        else:
            print("Usage: zip <output.zip> <folder>")

    elif user_input.startswith("tar -f"):
        parts = user_input.split()
        if len(parts) == 3:
            output_name = parts[1]
            folder_path = parts[2]
            tar_folder(folder_path, output_name)
        else:
            print("Usage: tar <output.tar> <folder>")

    elif user_input.startswith("zip ls "):
        parts = user_input.split()
        if len(parts) == 3:
            list_zip(parts[2])
        else:
            print("Usage: zip ls <zipfile>")

    elif user_input.startswith("tar ls "):
        parts = user_input.split()
        if len(parts) == 3:
            list_tar(parts[2])
        else:
            print("Usage: tar ls <tarfile>")
    elif user_input in ("clear", "cls"):
        # Windows dùng 'cls', Linux/macOS dùng 'clear'
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")


    elif cmd in commands:
        commands[cmd](args)

    else:
        print(f"E:'{user_input}' is not recognized as an internal , program or executor file.")      
