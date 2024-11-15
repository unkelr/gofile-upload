import sys
import os
import requests
import json
from colorama import Fore, Style, init

init()

if len(sys.argv) == 1:
    print(f'{Fore.RED}ERROR\nPlease Enter The Path To Your File')
    print(f"{Fore.GREEN}USAGE: python main.py test.txt")
    sys.exit(1)

file_path = sys.argv[1]

response = requests.get("https://api.gofile.io/servers")
if response.status_code != 200:
    print(f"{Fore.RED}ERROR: Failed to fetch servers list!")
    sys.exit(1)

servers_data = response.json()
server = servers_data.get('data', {}).get('servers', [])[0].get('name', '')

if not server:
    print(f"{Fore.RED}ERROR: No valid server found!")
    sys.exit(1)

url = f"https://{server}.gofile.io/uploadFile"
with open(file_path, 'rb') as file:
    files = {'file': (os.path.basename(file_path), file)}
    upload_response = requests.post(url, files=files)
    
    if upload_response.status_code != 200:
        print(f"{Fore.RED}ERROR: File upload failed!")
        sys.exit(1)

upload_data = upload_response.json()
download_link = upload_data.get('data', {}).get('downloadPage', '')

if not download_link:
    print(f"{Fore.RED}ERROR")
    sys.exit(1)

print(f"{Fore.GREEN}{Style.BRIGHT}  Successfuly Uploaded",file_path+'\n',Fore.BLUE,download_link)
