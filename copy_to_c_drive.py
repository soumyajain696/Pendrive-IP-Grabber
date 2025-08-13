import shutil
import os
import sys
import ctypes
from tkinter import messagebox, Tk

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def copy_data_to_c_drive(source_path):
    destination_path = r"C:\external data"
    if not os.path.exists(source_path):
        messagebox.showerror("Error", f"Source path does not exist:\n{source_path}")
        return

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    try:
        for item in os.listdir(source_path):
            s = os.path.join(source_path, item)
            d = os.path.join(destination_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        messagebox.showinfo("Success", f"Data copied successfully to:\n{destination_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error copying data:\n{e}")

if __name__ == "__main__":
    # Check for admin rights
    if not is_admin():
        # Relaunch the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

    # Hide the root Tk window
    root = Tk()
    root.withdraw()

    # Get the current directory (USB root or folder where script runs)
    usb_root = os.path.abspath(os.path.dirname(sys.argv[0]))

    copy_data_to_c_drive(usb_root)
