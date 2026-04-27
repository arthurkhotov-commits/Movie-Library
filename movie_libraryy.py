"""
Movie Library - Личная кинотека
GUI-приложение для управления коллекцией фильмов
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibrary:
    """Основной класс приложения Movie Library"""
    
    def __init__(self, root):
        """Инициализация приложения"""
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("950x650")
        self.root.resizable(True, True)
        
        # Список для хранения фильмов
        self.movies = []
        
        # Файл для сохранения данных
        self.data_file = "movies.json"
        
        # Создание интерфейса
        self.setup_ui()
        
        # Загрузка данных при запуске
        self.load_movies()
        
        # Привязка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        
        # Основной контейнер с отступами
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # ===== Секция ввода данных =====
        input_frame = ttk.LabelFrame(main_frame, text=" Добавление нового фильма ", padding="15")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Название фильма
        ttk.Label(input_frame, text="Название:", font=('Arial', 10)).grid(
            row=0, column=0, sticky=tk.W, pady=8)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, 
                                     width=45, font=('Arial', 10))
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Жанр
        ttk.Label(input_frame, text="Жанр:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=8)
        self.genre_var = tk.StringVar()
        self.genre_entry = ttk.Entry(input_frame, textvariable=self.genre_var, 
                                     width=45, font=('Arial', 10))
        self.genre_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Год выпуска
        ttk.Label(input_frame, text="Год выпуска:", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=8)
        self.year_var = tk.StringVar()
        self.year_entry = ttk.Entry(input_frame, textvariable=self.year_var, 
                                    width=15, font=('Arial', 10))
        self.year_entry.grid(row=2, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        # Рейтинг
        ttk.Label(input_frame, text="Рейтинг (0-10):", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=8)
        self.rating_var = tk.StringVar()
        self.rating_entry = ttk.Entry(input_frame, textvariable=self.rating_var, 
                                      width=10, font=('Arial', 10))
        self.rating_entry.grid(row=3, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить фильм", 
                                     command=self.add_movie, width=20)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Настройка растягивания input_frame
        input_frame.columnconfigure(1, weight=1)
        
        # ===== Секция фильтрации =====
        filter_frame = ttk.LabelFrame(main_frame, text=" Фильтрация ", padding="15")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Фильтр по жанру
        ttk.Label(filter_frame, text="По жанру:", font=('Arial', 10)).grid(
            row=0, column=0, sticky=tk.W, pady=8)
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_entry = ttk.Entry(filter_frame, textvariable=self.filter_genre_var, 
                                           width=20, font=('Arial', 10))
        self.filter_genre_entry.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(10, 20))
        
        # Фильтр по году
        ttk.Label(filter_frame, text="По году:", font=('Arial', 10)).grid(
            row=0, column=2, sticky=tk.W, pady=8)
        self.filter_year_var = tk.StringVar()
        self.filter_year_entry = ttk.Entry(filter_frame, textvariable=self.filter_year_var, 
                                          width=12, font=('Arial', 10))
        self.filter_year_entry.grid(row=0, column=3, sticky=tk.W, pady=8, padx=(10, 20))
        
        # Кнопки фильтрации
        self.filter_button = ttk.Button(filter_frame, text="Применить", 
                                       command=self.apply_filter)
        self.filter_button.grid(row=0, column=4, pady=8, padx=(0, 10))
        
        self.clear_filter_button = ttk.Button(filter_frame, text="Сбросить", 
                                             command=self.clear_filter)
        self.clear_filter_button.grid(row=0, column=5, pady=8)
        
        # ===== Таблица фильмов =====
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Настройка стиля таблицы
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        # Создание таблицы
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Заголовки столбцов
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        # Ширина и выравнивание столбцов
        self.tree.column("title", width=350, minwidth=200)
        self.tree.column("genre", width=200, minwidth=100)
        self.tree.column("year", width=80, anchor=tk.CENTER, minwidth=60)
        self.tree.column("rating", width=80, anchor=tk.CENTER, minwidth=60)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение таблицы и полосы прокрутки
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка двойного клика для просмотра деталей
        self.tree.bind("<Double-1>", self.show_movie_details)
        
        # ===== Кнопки управления =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        self.delete_button = ttk.Button(button_frame, text="Удалить", 
                                       command=self.delete_movie, width=15)
        self.delete_button.pack(side=tk.LEFT, padx=8)
        
        self.save_button = ttk.Button(button_frame, text="Сохранить", 
                                     command=self.save_movies, width=15)
        self.save_button.pack(side=tk.LEFT, padx=8)
        
        self.load_button = ttk.Button(button_frame, text="Загрузить", 
                                     command=self.load_movies, width=15)
        self.load_button.pack(side=tk.LEFT, padx=8)
        
        self.stats_button = ttk.Button(button_frame, text="Статистика", 
                                      command=self.show_statistics, width=15)
        self.stats_button.pack(side=tk.LEFT, padx=8)
        
        # ===== Статусная строка =====
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(8, 4))
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(8, 0))
        
        # Настройка растягивания
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def validate_input(self, title, genre, year, rating):
        """Проверка корректности вводимых данных"""
        errors = []
        
        # Проверка названия
        if not title.strip():
            errors.append("Название фильма не может быть пустым")
        
        # Проверка жанра
        if not genre.strip():
            errors.append("Жанр не может быть пустым")
        
        # Проверка года
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1888:
                errors.append("Год не может быть раньше 1888")
            elif year_int > current_year:
                errors.append(f"Год не может быть больше {current_year}")
        except ValueError:
            errors.append("Год должен быть целым числом (например: 2024)")
        
        # Проверка рейтинга
        try:
            rating_float = float(rating.replace(',', '.'))
            if rating_float < 0 or rating_float > 10:
                errors.append("Рейтинг должен быть от 0 до 10")
        except ValueError:
            errors.append("Рейтинг должен быть числом (например: 8.5)")
        
        return errors
    
    def add_movie(self):
        """Добавление нового фильма в библиотеку"""
        # Получение данных из полей ввода
        title = self.title_var.get().strip()
        genre = self.genre_var.get().strip()
        year = self.year_var.get().strip()
        rating = self.rating_var.get().strip()
        
        # Валидация данных
        errors = self.validate_input(title, genre, year, rating)
        if errors:
            messagebox.showerror("Ошибка ввода", "\n".join(errors))
            return
        
        # Проверка на дубликаты
        for movie in self.movies:
            if movie['title'].lower() == title.lower():
                if not messagebox.askyesno("Дубликат", 
                    f"Фильм '{title}' уже существует в библиотеке.\nДобавить ещё раз?"):
                    return
                break
        
        # Создание объекта фильма
        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating.replace(',', '.'))
        }
        
        # Добавление в список
        self.movies.append(movie)
        
        # Обновление отображения
        self.refresh_table()
        self.clear_input_fields()
        
        # Обновление статуса
        self.status_var.set(f"Фильм '{title}' успешно добавлен! Всего фильмов: {len(self.movies)}")
        
        # Автоматическое сохранение
        self.save_movies(show_message=False)
        
        # Фокус на поле названия
        self.title_entry.focus()
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return
        
        # Получение данных выбранного фильма
        item = self.tree.item(selected[0])
        movie_title = item['values'][0]
        
        # Подтверждение удаления
        if not messagebox.askyesno("Подтверждение", 
                                   f"Вы действительно хотите удалить фильм:\n'{movie_title}'?"):
            return
        
        # Удаление из списка
        self.movies = [m for m in self.movies if m['title'] != movie_title]
        
        # Обновление отображения
        self.refresh_table()
        
        self.status_var.set(f"Фильм '{movie_title}' удален. Осталось фильмов: {len(self.movies)}")
        
        # Автоматическое сохранение
        self.save_movies(show_message=False)
    
    def apply_filter(self):
        """Применение фильтров к списку фильмов"""
        filter_genre = self.filter_genre_var.get().strip().lower()
        filter_year = self.filter_year_var.get().strip()
        
        filtered_movies = self.movies.copy()
        
        # Фильтрация по жанру (частичное совпадение)
        if filter_genre:
            filtered_movies = [m for m in filtered_movies 
                             if filter_genre in m['genre'].lower()]
        
        # Фильтрация по году (точное совпадение)
        if filter_year:
            try:
                year_int = int(filter_year)
                filtered_movies = [m for m in filtered_movies 
                                 if m['year'] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год в фильтре должен быть числом")
                return
        
        # Отображение результатов
        self.display_movies(filtered_movies)
        
        # Обновление статуса
        if filter_genre or filter_year:
            self.status_var.set(f"Найдено фильмов: {len(filtered_movies)}")
        else:
            self.status_var.set(f"Показаны все фильмы: {len(self.movies)}")
    
    def clear_filter(self):
        """Сброс фильтров"""
        self.filter_genre_var.set("")
        self.filter_year_var.set("")
        self.refresh_table()
        self.status_var.set(f"Фильтры сброшены. Всего фильмов: {len(self.movies)}")
    
    def refresh_table(self):
        """Обновление таблицы (показывает все фильмы)"""
        self.display_movies(self.movies)
    
    def display_movies(self, movies_list):
        """Отображение списка фильмов в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление фильмов с чередованием цветов
        for i, movie in enumerate(movies_list):
            # Определение тега для чередования строк
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            self.tree.insert("", tk.END, values=(
                movie['title'],
                movie['genre'],
                movie['year'],
                movie['rating']
            ), tags=(tag,))
        
        # Настройка цветов для чередования строк
        self.tree.tag_configure('evenrow', background='#f0f0f0')
        self.tree.tag_configure('oddrow', background='#ffffff')
    
    def clear_input_fields(self):
        """Очистка полей ввода"""
        self.title_var.set("")
        self.genre_var.set("")
        self.year_var.set("")
        self.rating_var.set("")
    
    def save_movies(self, show_message=True):
        """Сохранение данных в JSON файл"""
        try:
            # Сохраняем в текущей директории
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   self.data_file)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            
            if show_message:
                self.status_var.set(f"Данные сохранены в {self.data_file}. "
                                  f"Фильмов: {len(self.movies)}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", 
                               f"Не удалось сохранить данные:\n{str(e)}")
    
    def load_movies(self):
        """Загрузка данных из JSON файла"""
        try:
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   self.data_file)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
                self.refresh_table()
                self.status_var.set(f"Данные загружены из {self.data_file}. "
                                  f"Всего фильмов: {len(self.movies)}")
            else:
                self.status_var.set("Создана новая библиотека фильмов")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", f"Файл {self.data_file} поврежден")
            self.movies = []
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", 
                               f"Не удалось загрузить данные:\n{str(e)}")
            self.movies = []
    
    def show_movie_details(self, event):
        """Показать детальную информацию о фильме"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            details = f"Название: {values[0]}\n"
            details += f"Жанр: {values[1]}\n"
            details += f"Год выпуска: {values[2]}\n"
            details += f"Рейтинг: {values[3]}/10"
            
            messagebox.showinfo("Информация о фильме", details)
    
    def show_statistics(self):
        """Показать статистику библиотеки"""
        if not self.movies:
            messagebox.showinfo("Статистика", "Библиотека пуста")
            return
        
        total = len(self.movies)
        
        # Средний рейтинг
        avg_rating = sum(m['rating'] for m in self.movies) / total
        
        # Количество по жанрам
        genres = {}
        for movie in self.movies:
            genre = movie['genre']
            genres[genre] = genres.get(genre, 0) + 1
        
        # Самый популярный жанр
        popular_genre = max(genres.items(), key=lambda x: x[1])
        
        # Статистика по годам
        years = [m['year'] for m in self.movies]
        oldest = min(years)
        newest = max(years)
        
        # Формирование сообщения
        stats = "Статистика библиотеки\n"
        stats += "=" * 30 + "\n\n"
        stats += f"Всего фильмов: {total}\n"
        stats += f"Средний рейтинг: {avg_rating:.1f}\n\n"
        stats += f"Самый старый фильм: {oldest} год\n"
        stats += f"Самый новый фильм: {newest} год\n\n"
        stats += f"Самый популярный жанр: {popular_genre[0]} "
        stats += f"({popular_genre[1]} фильмов)\n\n"
        stats += "Распределение по жанрам:\n"
        
        for genre, count in sorted(genres.items(), key=lambda x: x[1], reverse=True):
            stats += f"  • {genre}: {count}\n"
        
        messagebox.showinfo("Статистика", stats)
    
    def on_closing(self):
        """Действия при закрытии приложения"""
        if messagebox.askyesno("Выход", "Сохранить изменения перед выходом?"):
            self.save_movies(show_message=False)
        self.root.destroy()


def main():
    """Главная функция"""
    print("=" * 50)
    print("Movie Library - Личная кинотека")
    print("=" * 50)
    print("Запуск приложения...")
    
    # Создание главного окна
    root = tk.Tk()
    
    # Создание экземпляра приложения
    app = MovieLibrary(root)
    
    # Запуск главного цикла
    root.mainloop()
    
    print("Приложение закрыто")


# Точка входа
if __name__ == "__main__":
    main()