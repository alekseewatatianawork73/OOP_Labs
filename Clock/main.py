import customtkinter as ctk
import threading
import time
from datetime import datetime, timedelta
from pygame import mixer

# загружаем звонок для таймера
mixer.init()
timer_sound = mixer.Sound('show_time_out_01.mp3')

# глобальные переменные
running = True  # работа основного потока (отображение интерфейса приложения)
timer_running = False  # состояние таймера
stopwatch_running = False  # состояние секундомера
timer_seconds = 0
timer_end_time = None
stopwatch_start_time = None
stopwatch_elapsed = timedelta()
stopwatch_lap_times = []


# функция для корректного закрытия
def on_closing():
    global running
    running = False
    root.destroy()


# функция для запуска таймера
def start_timer():
    global timer_running, timer_seconds, timer_end_time

    try:
        time_str = timer_entry.get()
        if ":" in time_str:
            mins, secs = map(int, time_str.split(":"))
        else:
            mins, secs = int(time_str), 0

        if mins < 0 or secs < 0 or secs >= 60:
            raise ValueError

        timer_seconds = mins * 60 + secs
        timer_end_time = datetime.now() + timedelta(seconds=timer_seconds)
        timer_running = True

        timer_start_btn.configure(state="disabled")
        timer_stop_btn.configure(state="normal")
        timer_entry.configure(state="disabled")

    except ValueError:
        timer_display.configure(text="Неверный формат!")


# функция для остановки таймера
def stop_timer():
    global timer_running
    timer_running = False
    timer_start_btn.configure(state="normal")
    timer_stop_btn.configure(state="disabled")
    timer_entry.configure(state="normal")


# функция для сброса времени таймера
def reset_timer():
    global timer_running
    timer_running = False
    timer_display.configure(text="00:00")
    timer_entry.configure(state="normal")
    timer_start_btn.configure(state="normal")
    timer_stop_btn.configure(state="disabled")
    timer_entry.delete(0, "end")


# функция-обработчик завершения таймера
def timer_finished():
    global timer_running
    timer_running = False
    timer_display.configure(text="00:00")
    timer_start_btn.configure(state="normal")
    timer_stop_btn.configure(state="disabled")
    timer_entry.configure(state="normal")

    def blink():
        for _ in range(5):
            timer_sound.play(0)
            timer_display.configure(text_color="red")
            time.sleep(0.5)
            timer_display.configure(text_color="white")
            time.sleep(0.5)

    threading.Thread(target=blink, daemon=True).start()


# функция для запуска секундомера
def start_stopwatch():
    global stopwatch_running, stopwatch_start_time
    if not stopwatch_running:
        stopwatch_start_time = datetime.now()
        stopwatch_running = True

        stopwatch_start_btn.configure(state="disabled")
        stopwatch_stop_btn.configure(state="normal")
        stopwatch_reset_btn.configure(state="normal")
        lap_button.configure(state="normal")


# функция для остановки секундомера
def stop_stopwatch():
    global stopwatch_running, stopwatch_elapsed, stopwatch_start_time
    if stopwatch_running:
        stopwatch_elapsed += datetime.now() - stopwatch_start_time
        stopwatch_running = False

        stopwatch_start_btn.configure(state="normal")
        stopwatch_stop_btn.configure(state="disabled")
        lap_button.configure(state="disabled")


# функция для сброса времени секундомера
def reset_stopwatch():
    global stopwatch_running, stopwatch_elapsed
    stopwatch_running = False
    stopwatch_elapsed = timedelta()
    stopwatch_display.configure(text="00:00:00.00")
    stopwatch_start_btn.configure(state="normal")
    stopwatch_stop_btn.configure(state="disabled")
    stopwatch_reset_btn.configure(state="disabled")
    lap_button.configure(state="disabled")

    for widget in lap_frame.winfo_children():
        widget.destroy()
    global stopwatch_lap_times
    stopwatch_lap_times = []


# функция для фиксации времени на секундомере
def record_lap():
    global stopwatch_lap_times, stopwatch_start_time, stopwatch_elapsed
    if stopwatch_running:
        elapsed = datetime.now() - stopwatch_start_time + stopwatch_elapsed
        stopwatch_lap_times.append(elapsed)

        lap_num = len(stopwatch_lap_times)
        hours, remainder = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (elapsed.total_seconds() - int(elapsed.total_seconds())) * 100
        lap_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):02d}"

        lap_label = ctk.CTkLabel(lap_frame, text=f"Круг {lap_num}: {lap_time}", font=("Arial", 15))
        lap_label.pack(anchor="w")


# основной поток обновления времени
def update_clock():
    global running, timer_running, stopwatch_running
    global timer_end_time, stopwatch_start_time, stopwatch_elapsed

    while running:
        now = datetime.now()

        # обновляем часы
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d %B %Y")
        clock_label.configure(text=time_str)
        date_label.configure(text=date_str)

        # обновляем таймер
        if timer_running:
            remaining = timer_end_time - now
            if remaining.total_seconds() <= 0:
                timer_finished()
            else:
                mins, secs = divmod(int(remaining.total_seconds()), 60)
                timer_display.configure(text=f"{mins:02d}:{secs:02d}")

        # обновляем секундомер
        if stopwatch_running:
            elapsed = now - stopwatch_start_time + stopwatch_elapsed
            hours, remainder = divmod(elapsed.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = (elapsed.total_seconds() - int(elapsed.total_seconds())) * 100
            stopwatch_display.configure(text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):02d}")

        time.sleep(0.1)


# функция для задания шрифта на виджете CTkTabview (вкладки)
def apply_font_to_tabs(tabs: ctk.CTkTabview):
    tabs._segmented_button.configure(font=my_font)


# настройка внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# создаем главное окно
root = ctk.CTk()
root.title("Приложение Часы")
root.geometry("700x500")

# задаём стандартный шрифт в приложении
my_font = ctk.CTkFont(family='Arial', size=20, weight='bold')

# создаем вкладки
tabview = ctk.CTkTabview(root)
tabview.pack(pady=10, padx=10, fill="both", expand=True)

# добавляем вкладки
tab_clock = tabview.add("Часы")
tab_timer = tabview.add("Таймер")
tab_stopwatch = tabview.add("Секундомер")

# задаём шрифт на вкладках
apply_font_to_tabs(tabview)

# вкладка часов
clock_label = ctk.CTkLabel(tab_clock, font=("Arial", 48), text="00:00:00")
clock_label.pack(pady=40)

date_label = ctk.CTkLabel(tab_clock, font=("Arial", 24, 'italic'), text="01 января 2023")
date_label.pack(pady=10)

# вкладка таймера
timer_entry = ctk.CTkEntry(tab_timer, placeholder_text="ММ:СС", font=("Arial", 24), justify="center")
timer_entry.pack(pady=20)

timer_display = ctk.CTkLabel(tab_timer, font=("Arial", 48), text="00:00")
timer_display.pack(pady=10)

button_frame = ctk.CTkFrame(tab_timer)
button_frame.pack(pady=10)

timer_start_btn = ctk.CTkButton(button_frame, text="Старт", font=my_font, command=lambda: start_timer())
timer_start_btn.pack(side="left", padx=5)

timer_stop_btn = ctk.CTkButton(button_frame, text="Стоп", font=my_font, command=lambda: stop_timer(), state="disabled")
timer_stop_btn.pack(side="left", padx=5)

timer_reset_btn = ctk.CTkButton(button_frame, text="Сброс", font=my_font, command=lambda: reset_timer())
timer_reset_btn.pack(side="left", padx=5)

# вкладка секундомера
stopwatch_display = ctk.CTkLabel(tab_stopwatch, font=("Arial", 48), text="00:00:00.00")
stopwatch_display.pack(pady=20)

button_frame_sw = ctk.CTkFrame(tab_stopwatch)
button_frame_sw.pack(pady=10)

stopwatch_start_btn = ctk.CTkButton(button_frame_sw, text="Старт", font=my_font, command=lambda: start_stopwatch())
stopwatch_start_btn.pack(side="left", padx=5)

stopwatch_stop_btn = ctk.CTkButton(button_frame_sw, text="Стоп", font=my_font, command=lambda: stop_stopwatch(), state="disabled")
stopwatch_stop_btn.pack(side="left", padx=5)

stopwatch_reset_btn = ctk.CTkButton(button_frame_sw, text="Сброс", font=my_font, command=lambda: reset_stopwatch())
stopwatch_reset_btn.pack(side="left", padx=5)

lap_frame = ctk.CTkScrollableFrame(tab_stopwatch, height=150)
lap_frame.pack(pady=10, fill="both", expand=True)

lap_button = ctk.CTkButton(tab_stopwatch, text="Круг", font=my_font, command=lambda: record_lap(), state="disabled")
lap_button.pack(pady=5)

# запуск потока обновления
clock_thread = threading.Thread(target=update_clock, daemon=True)
clock_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

# запуск основного потока
root.mainloop()
