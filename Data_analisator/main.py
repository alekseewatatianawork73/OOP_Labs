from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# настройка внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

data = None
current_plot = None


# функция для загрузки файла
def load_file():
    global data
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel/CSV", "*.xlsx *.xls *.csv")],
        title="Выберите файл данных"
    )
    if not file_path:
        return 0

    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)

        update_table()
        update_comboboxes()

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")


# обновление таблицы с данными
def update_table():
    if data is None:
        return 0

    text_table.delete(1.0, 'end')
    text_table.insert('end', data.to_string(index=False))


# обновление выпадающих списков
def update_comboboxes():
    if data is None:
        return 0

    columns = data.columns.tolist()
    combo_x.configure(values=columns)
    combo_y.configure(values=columns)

    if len(columns) >= 1:
        combo_x.set(columns[0])
        if len(columns) >= 2:
            combo_y.set(columns[1])


# построение графика
def plot_data():
    global current_plot
    if data is None:
        messagebox.showwarning("Ошибка", "Данные не загружены!")
        return 0

    x_col = combo_x.get()
    y_col = combo_y.get()
    chart_type = chart_type_var.get()

    if not x_col or not y_col:
        messagebox.showwarning("Ошибка", "Выберите столбцы для графика!")
        return 0

    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(8, 4))

    try:
        if chart_type == "Столбчатая":
            ax.bar(data[x_col], data[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title("Столбчатая диаграмма")
        elif chart_type == "Линейная":
            ax.plot(data[x_col], data[y_col], marker='o')
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title("Линейный график")
        elif chart_type == "Круговая":
            ax.pie(data[y_col], labels=data[x_col], autopct='%1.1f%%')
            ax.set_title("Круговая диаграмма")
        plt.xticks(rotation=90)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        current_plot = canvas

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось построить график:\n{e}")


# фильтрация данных
def filter_data():
    if data is None:
        messagebox.showwarning("Ошибка", "Данные не загружены!")
        return 0

    filter_dialog = ctk.CTkInputDialog(text="Введите условие фильтрации (например: 'Возраст > 30'):", title="Фильтр данных")
    condition = filter_dialog.get_input()

    if not condition:
        return 0

    try:
        filtered_data = data.query(condition)
        text_table.delete('0.0', 'end')
        text_table.insert('end', filtered_data.to_string(index=False))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неверное условие фильтрации:\n{e}")


# Создание главного окна
root = ctk.CTk()
root.title("Визуализатор данных Excel/CSV")
root.geometry("1200x900")
root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

# фрейм для "панели инструментов"
frame_left = ctk.CTkFrame(root, width=300, corner_radius=10)
frame_left.pack(side="left", fill="y", padx=10, pady=10)

# фрейм для визуализации данных
frame_right = ctk.CTkFrame(root, corner_radius=10)
frame_right.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# Виджеты в левом фрейме
label_title = ctk.CTkLabel(frame_left, text="Анализатор данных", font=("Arial", 20))
label_title.pack(pady=10)

button_load = ctk.CTkButton(frame_left, text="Загрузить файл", command=load_file)
button_load.pack(pady=10)

label_columns = ctk.CTkLabel(frame_left, text="Столбцы для графика:")
label_columns.pack(pady=5)

# выпадающие списки с названиями столбцов (изначально оставляем их пустыми)
combo_x = ctk.CTkComboBox(frame_left, values=[], state="readonly")
combo_x.pack(pady=5)
combo_y = ctk.CTkComboBox(frame_left, values=[], state="readonly")
combo_y.pack(pady=5)

label_chart = ctk.CTkLabel(frame_left, text="Тип графика:")
label_chart.pack(pady=5)

chart_type_var = ctk.StringVar(value="Столбчатая")
chart_type = ctk.CTkComboBox(master=frame_left, values=["Столбчатая", "Линейная", "Круговая"], variable=chart_type_var)
chart_type.pack(pady=5)

button_plot = ctk.CTkButton(frame_left, text="Построить график", command=plot_data)
button_plot.pack(pady=10)

button_filter = ctk.CTkButton(frame_left, text="Фильтровать данные", command=filter_data)
button_filter.pack(pady=10)

# таблица для отображения данных
table_frame = ctk.CTkFrame(frame_right)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)
text_table = ctk.CTkTextbox(table_frame)
text_table.pack(fill="both", expand=True)

# фрейм для графика
plot_frame = ctk.CTkFrame(frame_right, height=300)
plot_frame.pack(fill="x", padx=10, pady=10)

root.mainloop()
