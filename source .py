import os
import subprocess
import datetime
run = True
try:
    import keyboard
except ModuleNotFoundError:
    print("your system does has keyboard python Module do you want install?")
    while True:
        install = input("(y/n):")
        if install.lower() == "y":
            install_code = ("pip install keyboard")
            try:
                result = subprocess.run(install_code, shell=True, text=True)
            except Exception as e:
                print("Error:", e)
            break
        if install.lower() == "n":
            run = False
            break
        else:
            print("error, only use y/n")
    
import time
import shutil

startup_path = os.path.expanduser("~")
os.chdir(startup_path)
dir = os.getcwd()
print(" _________________________________________________________________________")
print("|________________________________Welcome__________________________________|")
print("|                     Welcome python Command shell                        |")
print("|                     ┌──────────────────────────┐                        |")
print("|                     │      __                  │                        |")
print("|                     │     |  \                 │                        |")
print("|                     │      \$$\                │                        |")
print("|                     │       \$$\               │                        |")
print("|                     │        >$$\              │                        |")
print("|                     │       /  $$              │                        |")
print("|                     │      /  $$               │                        |")
print("|                     │     |  $$     _________  │                        |")
print("|                     │      \$$     |         \ │                        |")
print("|                     │              \$$$$$$$$$$ │                        |")
print("|                     └──────────────────────────┘                        |")
print("|                  (c) 1/8/2026 Shell by longtrinh2666.                   |")
print("|_________________________________________________________________________|")
print()
while run:
    user_input = input(f"|{dir}| >>>").lower()
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
                print(" _____________________________________________ ")
                print("|E:The system cannot find the path specified. |")
                print("|_____________________________________________|")
            except OSError:
                print(" _____________________________________________ ")
                print("|E:Invalid path syntax                        |")
                print("|_____________________________________________|")
            
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
        print(" _____________________________________________ ")
        print("|folder created successfully✅                |")
        print("|_____________________________________________|")
    elif user_input.startswith("rm "):
        file_to_remove = user_input[3:]
        try:
            os.remove(file_to_remove)
            print(" _____________________________________________ ")
            print("|file deleted successfully✅                  |")
            print("|_____________________________________________|")
        except FileNotFoundError:
            print(" _____________________________________________ ")
            print("|E:The program cannot find the file specified.|")
            print("|_____________________________________________|")
        except IsADirectoryError:
            print(" _____________________________________________ ")
            print("|E:The program cannot find the file specified.|")
            print("|_____________________________________________|")
    elif user_input.startswith("rm -f "):
        folder_to_remove = user_input[6:]
        try:
            shutil.rmtree(folder_to_remove)
            print(" _____________________________________________ ")
            print("|folder deleted successfully✅                |")
            print("|_____________________________________________|")
        except FileNotFoundError:
            print(" _____________________________________________ ")
            print("|E:The program cannot find the file specified.|")
            print("|_____________________________________________|")
    
    elif user_input == "help":
        print(" __________________________________________________________________________ ")
        print("|______________________________Command List________________________________|")
        print("|cd             Displays the name of or changes the current directory.     |")
        print("|copy -f        Copies files and directory trees.                          |")
        print("|copy           Copies one or more files to another location.              |")
        print("|rm -f          Removes a directory.                                       |")
        print("|rm             Deletes one or more files.                                 |")
        print("|ls/dir         Displays a list of files and subdirectories in a directory.|")
        print("|exit           Quits the shell program (command interpreter).             |")
        print("|help           Provides Help information for Windows commands.            |")
        print("|mkdir          Creates a directory.                                       |")
        print("|edit           changer the contents of a text file.                       |")
        print("|rename/rem     Renames a file or files.                                   |")
        print("|type           Displays the contents of a text file.                      |")
        print("|python         Enter python shell mode                                    |")
        print("|date           Displays or sets the date.                                 |")
        print("|__________________________________________________________________________|")
    
    elif user_input.startswith("copy "):
        parts = user_input.split()
        if len(parts) >= 3:
            src, dst = parts[1], parts[2]
            try:
               shutil.copy(src, dst)
               print(" _____________________________________________ ")
               print("|file copy successfully✅                     |")
               print("|_____________________________________________|")
            except FileNotFoundError:
                print(" _____________________________________________ ")
                print("|E:The program cannot find the file specified.|")
                print("|_____________________________________________|")
        else:
            print(" _____________________________________________ ")
            print("|E:error syntax, try again                    |")
            print("|_____________________________________________|")
    elif user_input.startswith("copy -f "):
        parts = user_input.split()
        if len(parts) >= 3:
            src, dst = parts[1], parts[2]
            try:
                shutil.copytree(src, dst)
                print(" _____________________________________________ ")
                print("|folder copy successfully✅                   |")
                print("|_____________________________________________|")
            except FileExistsError:
                print(" _____________________________________________ ")
                print("|E:The directory folder already exists.       |")
                print("|_____________________________________________|")
            except FileNotFoundError:
                print(" _____________________________________________ ")
                print("|E:The program cannot find the path specified.|")
                print("|_____________________________________________|")
        else:
            print(" _____________________________________________ ")
            print("|E:error syntax, try again                    |")
            print("|_____________________________________________|")
    
    elif user_input.startswith("edit "):
        file_to_edit = user_input.split(maxsplit=1)[1]
        try:
            if os.path.exists(file_to_edit):
                with open(file_to_edit, "r", encoding="utf-8") as f:
                    old_content = f.read()
                print(" _____________________________________________ ")
                print("|Current content in the file:                |")
                print("|_____________________________________________|")
                print(old_content)
            else:
                print("w:The file does not exist yet, a new one will be created.")
                
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
                print(" _____________________________________________ ")
                print("|The file name has been edited successfully✅ |")
                print("|_____________________________________________|")
            except FileNotFoundError:
                print(" _____________________________________________ ")
                print("|E:The system cannot find the file specified. |")
                print("|_____________________________________________|")
            except Exception as e:
                print(" _____________________________________________ ")
                print(f"|E:Error changing name                        |")
                print("|_____________________________________________|")
        else:
            print(" _____________________________________________ ")
            print("|E:error syntax, try again                    |")
            print("|_____________________________________________|")
    
    elif user_input.startswith("type "):
        file_to_read = user_input.split(maxsplit=1)[1]
        try:
            with open(file_to_read, "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print(" _____________________________________________ ")
            print("|E:File not found                             |")
            print("|_____________________________________________|")

    elif user_input == "python":
        print("Entering Python interactive mode (type 'exit' to quit)")
        while True:
            cmd = input(">>> ")
            if cmd.lower() == "exit":
                break
            try:
                result = subprocess.run(cmd, shell=True, text=True)
            except Exception as e:
                print("Error:", e)
                
    elif user_input in ("date", "time"):
        now = datetime.datetime.now()
        print(f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')} ")
                    
    else:
        print(" ___________________________________________________________________________ ")
        print("|E:This command is not recognized as an internal , program or executor file.|")
        print("|___________________________________________________________________________|")      