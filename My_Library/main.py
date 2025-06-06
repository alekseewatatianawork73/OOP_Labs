# подключаем библиотеки и модули
import mysql.connector
import customtkinter as ctk
from tkinter import messagebox


# функция для подключения к базе данных my_library
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="************",
            database="my_library"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось подключиться: {e}")
        return None


# функция для инициализации базы данных (создаём БД и таблицу с книгами, если её не существовало)
def initialize_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="************"
        )
        cursor = conn.cursor()  # курсор для выполнения sql-запросов
        cursor.execute("CREATE DATABASE IF NOT EXISTS my_library")
        cursor.execute("USE my_library")
        cursor.execute("""CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, 
        title VARCHAR(100) NOT NULL, author VARCHAR(100), year INT)""")
        conn.commit()  # сохраняем изменения в базе данных
        conn.close()  # закрываем соединение с клиентом
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка БД: {e}")


# функция для получения списка всех книг, хранящихся в БД
def get_all_books():
    # подключение к БД
    conn = create_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()  # возвращаем записи в виде упорядоченного списка
    finally:
        conn.close()  # закрываем соединение с клиентом


# функция для добавления книг в БД
def add_book(title, author="", year=""):
    conn = create_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
            (title, author if author else None, int(year) if year.isdigit() else None))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка добавления: {e}")
        return False
    finally:
        conn.close()


# функция для поиска книг, хранящихся в БД
def search_books(query):
    conn = create_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE LOWER(%s) ORDER BY title",
                       (f"%{query}%",))
        return cursor.fetchall()
    finally:
        conn.close()


# функция для регулярного обновления списка книг
def update_books_list():
    books = get_all_books()
    books_list.configure(state="normal")
    books_list.delete("0.0", "end")

    if not books:
        books_list.insert("end", "Каталог пуст")
    else:
        pos = 1
        for book in books:
            book_info = f"{pos}. {book[1]}"
            if book[2]: book_info += f" ({book[2]})"
            if book[3]: book_info += f", {book[3]} г."
            books_list.insert("end", book_info + "\n")
            pos += 1

    books_list.configure(state="disabled")


# функция-обработчик для кнопки "Добавить"
def add_new_book():
    title = title_entry.get().strip()
    if not title:
        messagebox.showwarning("Ошибка", "Введите название")
        return

    if add_book(title, author_entry.get(), year_entry.get()):
        title_entry.delete(0, "end")
        author_entry.delete(0, "end")
        year_entry.delete(0, "end")
        update_books_list()
        messagebox.showinfo("Успех", "Книга добавлена")


# функция-обработчик для кнопки "Искать"
def perform_search():
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Ошибка", "Введите запрос")
        return

    results = search_books(query)
    search_results.configure(state="normal")
    search_results.delete("1.0", "end")

    if not results:
        search_results.insert("end", "Не найдено")
    else:
        for book in results:
            book_info = f"{book[1]}"
            if book[2]: book_info += f" ({book[2]})"
            if book[3]: book_info += f", {book[3]} г."
            search_results.insert("end", book_info + "\n")

    search_results.configure(state="disabled")


# функция для задания шрифта на виджете CTkTabview (вкладки)
def apply_font_to_tabs(tabs: ctk.CTkTabview):
    tabs._segmented_button.configure(font=my_font)


# создание основного окна
app = ctk.CTk()
app.title("Каталог книг")
app.geometry("900x700")
app.configure(fg_color='darkseagreen1')

# задаём стандартный шрифт в приложении
my_font = ctk.CTkFont(family='Arial', size=20, weight='bold')

# инициализируем БД
initialize_database()

# вкладки
tabview = ctk.CTkTabview(app)
tabview.configure(fg_color='darkseagreen3', segmented_button_fg_color='darkseagreen1',
                  segmented_button_selected_color='darkolivegreen4',
                  segmented_button_unselected_color='darkolivegreen', segmented_button_selected_hover_color='grey',
                  segmented_button_unselected_hover_color='grey')
tabview.pack(padx=10, pady=10, fill="both", expand=True)

# вкладка "Все книги"
view_tab = tabview.add("Все книги")
books_list = ctk.CTkTextbox(view_tab, wrap="word", font=my_font)
books_list.pack(padx=10, pady=10, fill="both", expand=True)
ctk.CTkButton(view_tab, text="Обновить", fg_color='darkolivegreen', hover_color='grey', command=update_books_list, font=my_font).pack(pady=5)

# вкладка "Добавить книгу"
add_tab = tabview.add("Добавить книгу")
ctk.CTkLabel(add_tab, text="Название:", font=my_font).pack(pady=(10, 0))
title_entry = ctk.CTkEntry(add_tab, font=my_font)
title_entry.pack(padx=20, pady=5, fill="x")

ctk.CTkLabel(add_tab, text="Автор (необяз.):", font=my_font).pack(pady=(10, 0))
author_entry = ctk.CTkEntry(add_tab, font=my_font)
author_entry.pack(padx=20, pady=5, fill="x")

ctk.CTkLabel(add_tab, text="Год (необяз.):", font=my_font).pack(pady=(10, 0))
year_entry = ctk.CTkEntry(add_tab, font=my_font)
year_entry.pack(padx=20, pady=5, fill="x")

ctk.CTkButton(add_tab, text="Добавить", fg_color='darkolivegreen', hover_color='grey',
              command=add_new_book, font=my_font).pack(pady=20)

# вкладка "Поиск книг"
search_tab = tabview.add("Поиск книг")
ctk.CTkLabel(search_tab, text="Введите название книги:", font=my_font).pack(pady=(10, 0))
search_entry = ctk.CTkEntry(search_tab, font=my_font)
search_entry.pack(padx=20, pady=5, fill="x")
ctk.CTkButton(search_tab, text="Искать", fg_color='darkolivegreen', hover_color='grey', command=perform_search, font=my_font).pack(pady=5)
search_results = ctk.CTkTextbox(search_tab, wrap="none", font=my_font)
search_results.pack(padx=10, pady=10, fill="both", expand=True)

# задаём шрифт на вкладках
apply_font_to_tabs(tabview)

# обновляем список книг
update_books_list()

# цикл для работы приложения
app.mainloop()
