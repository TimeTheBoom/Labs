from subprocess import call
import os
import sys


dir = os.getcwd()

files = os.listdir(dir)

print(f"[~] Current working directory: {dir}")

if not ".ca.flag" in files:
    print("[!] App directory - ERROR")
    print("[!] Please change the current working directory to the Channels Analyzer directory")
    input("\nPress Enter to exit... \n")
    exit()

print("[+] App dir - OK")
   
python_exe = sys.executable

try:
    print("[~] Creating VENV...")
    call((python_exe, "-m", "venv", dir+"/venv"))
    print("[+] VENV created")
    print("[~] Processing packages...")
    call(( dir+"/venv/scripts/pip.exe", "install", "--no-index", "--find-links", dir+"/__MODULES__", "-r", dir+"/__req.txt"))
    print("[~] Packages processed")
except Exception as e:
    print(f"[!] Uncaught error: {e}")
    
input("\nPress Enter to exit... \n")