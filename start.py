import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

mouse = Controller()
time.sleep(0.5)
print(bcolors.HEADER + "    ____  __                   ______                   ")
print(bcolors.HEADER + "   / __ )/ /_  ______ ___     / ____/___ __________ ___ ")
print(bcolors.HEADER + "  / __  / / / / / __ `__ \   / /_  / __ `/ ___/ __ `__ \ ")
print(bcolors.HEADER + " / /_/ / / /_/ / / / / / /  / __/ / /_/ / /  / / / / / / ")
print(bcolors.HEADER + "/_____/_/\__,_/_/ /_/ /_/  /_/    \__,_/_/  /_/ /_/ /_/  \n")
print(bcolors.ENDC + '🛠️ Автор: https://github.com/meKryztal')
print('🔗 Модифицировал: https://github.com/StormachOrange\n')
def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def choose_window_gui():
    root = tk.Tk()
    root.withdraw()

    windows = gw.getAllTitles()
    if not windows:
        return None

    choice = simpledialog.askstring("Выбор окна Telegram", "Введите номер окна:\n" + "\n".join(f"{i}: {window}" for i, window in enumerate(windows)))

    if choice is None or not choice.isdigit():
        return None

    choice = int(choice)
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        return None

def check_white_color(scrn, window_rect):
    width, height = scrn.size
    for x in range(0, width, 20):
        y = height - height // 8
        r, g, b = scrn.getpixel((x, y))
        if (r, g, b) == (255, 255, 255):
            screen_x = window_rect[0] + x
            screen_y = window_rect[1] + y
            click(screen_x, screen_y)
            print('Начинаю новую игру')
            time.sleep(0.001)
            return True
    return False

window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)

if not check:
    print(bcolors.FAIL + f"\nОкно {window_name} не найдено!\nПожалуйста, выберите другое окно.")
    window_name = choose_window_gui()

if not window_name or not gw.getWindowsWithTitle(window_name):
    print(bcolors.WARNING + "\nНе удалось найти указанное окно!\nЗапустите Telegram, после чего перезапустите бота!")
else:

    print(bcolors.OKGREEN + f"\nОкно {window_name} найдено\nНажмите 'S' для старта, а также чтобы поставить на паузу.")

telegram_window = gw.getWindowsWithTitle(window_name)[0]
paused = True
last_check_time = time.time()

while True:
    if keyboard.is_pressed('S'):
        paused = not paused
        if paused:
            print(bcolors.OKCYAN + 'Пауза')
        else:
            print(bcolors.OKBLUE + 'Работаю')
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False
    if pixel_found == True:
        break

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))
            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                screen_x = window_rect[0] + x + 3
                screen_y = window_rect[1] + y + 5
                click(screen_x, screen_y)
                time.sleep(0.002)
                pixel_found = True
                break

    current_time = time.time()
    if current_time - last_check_time >= 10:
        if check_white_color(scrn, window_rect):
            last_check_time = current_time

print('Стоп')
