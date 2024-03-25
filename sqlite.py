import sqlite3
import datetime
from UserData import UserData
from UserData import apps_with_status

db = sqlite3.connect('tasks.db')
cursor = db.cursor()
    
cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app TEXT,
        first_time_start INTEGER NOT NULL,
        time_start INTEGER NOT NULL,
        time_end INTEGER NOT NULL,
        sum_time INTEGER NOT NULL,
        status TEXT DEFAULT "Not Started"
    )""")


# функция для добавления новой задачи:    
def add_task(app):
    first_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")# Получаем текущее время в strftime()
    time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Start"
    
    # Создаем обьект класс UserData для представления новой записи
    new_task = UserData(app, first_time_start, time_start, 0, 0, status)
    
    cursor.execute("INSERT INTO user (app, first_time_start, time_start, time_end, sum_time, status) VALUES (?, ?, ?, ?, ?, ?)", 
                    (new_task.app, new_task.first_time_start, new_task.time_start, 0, 0, new_task.status))
    db.commit()
    id = cursor.lastrowid
    cursor.execute("UPDATE user SET status = ? WHERE id = ?", (status, id))
    db.commit()


#функция для завершения задачи
def end_task(task_id):
    cursor.execute("SELECT * FROM user WHERE id = ?", (task_id,))
    task_data = cursor.fetchone()

    # Создаем объект класса UserData из данных задачи
    task = UserData(task_data[1], task_data[2], task_data[3], task_data[4], task_data[5], task_data[6])
    task.id = task_id

    time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task.time_end = time_end

    start_time = datetime.datetime.strptime(task.time_start, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(task.time_end, "%Y-%m-%d %H:%M:%S")

    time_difference = end_time - start_time
    sum_time = time_difference.total_seconds()

    # Преобразуем общее время выполнения задачи в формат "часы:минуты:секунды"
    time_delta = datetime.timedelta(seconds=sum_time)
    time_formatted = str(time_delta)
    task.sum_time = time_formatted

    status = "Completed"
    task.status = status

    # Обновляем данные о задаче в базе данных
    cursor.execute("UPDATE user SET time_end = ?, sum_time = ?, status = ? WHERE id = ?", (task.time_end, task.sum_time, task.status, task_id))
    db.commit()


def same_task(task_id):
    time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Start"
    

    # Пробуем выполнить запрос обновления
    try:
        # Обновляем несколько полей
        cursor.execute("UPDATE user SET time_start = ?, time_end=0, status = ? WHERE id = ?", 
                        (time_start, status, task_id))
        db.commit()
        print("Данные успешно обновлены.")
    except sqlite3.Error as e:
        print(f"Ошибка обновления данных: {e}")
    # Закрываем соединение

# Создаем обьект класс
user_data = apps_with_status()
# Вызов метода для поиска приложения
user_data.display_apps_with_status_start()
#закрытие соедния с базой данных

user_data = apps_with_status()
# Вызов метода для поиска приложения
user_data.display_apps_with_status_Completed()
#закрытие соедния с базой данных
