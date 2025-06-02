import time
from pynput.mouse import Controller
from datetime import datetime
import os


current_directory = os.getcwd()
file_path = os.path.join(current_directory, "activity.txt")

def check_activity_file(activity_file_path):
    if not os.path.exists(activity_file_path):
        with open(activity_file_path, "w") as f:
            pass
        print("Файл activity.txt был создан в текущей папке.")
    else:
        print("Файл activity.txt уже существует в текущей папке.")

def get_mouse_position():
    mouse = Controller()
    return mouse.position

def remove_empty_lines(file_path):
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()

def get_last_line(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if lines:
            return lines[-1]
        else:
            return None

check_activity_file(file_path)
while True:
    current_time = datetime.now()
    postiton = get_mouse_position()
    try:
        previous_row = get_last_line(file_path)
        print("Было: ", previous_row.strip())
    except:
        previous_row="="
    try: remove_empty_lines(file_path)
    except: pass

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip()
            split_time = last_line.split('=')[0].strip()
            current_time = datetime.now()
            extracted_time = datetime.strptime(split_time, '%Y-%m-%d %H:%M:%S')
            time_difference = current_time - extracted_time
            time_difference_minutes = str(int(time_difference.total_seconds() / 60))
            last_difference = str(last_line.split('=')[2].strip())
    except:
        time_difference_minutes = 0
        last_difference = 0

    with open(file_path, "a") as file:
        row = f"\n{current_time.strftime('%Y-%m-%d %H:%M:%S')} = {postiton} = {time_difference_minutes} = {last_difference}"
        if previous_row.split('=')[1].strip()!=row.split('=')[1].strip():
            file.write(row)
            print("Стало: ",row.strip())
    time.sleep(60)

