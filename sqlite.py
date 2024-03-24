import sqlite3
import datetime

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
    cursor.execute("INSERT INTO user (app, first_time_start, time_start, time_end, sum_time, status) VALUES (?, ?, ?, ?, ?, ?)", 
                    (app, first_time_start, time_start, 0, 0, status))
    db.commit()
    id = cursor.lastrowid
    cursor.execute("UPDATE user SET status = ? WHERE id = ?", (status, id))
    db.commit()

def end_task(task_id):
    
    
    time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE user SET time_end = ? WHERE id = ?", (time_end, task_id))
    db.commit()
    
    cursor.execute("SELECT sum_time FROM user WHERE id = ?", (task_id,))
    sum_results = cursor.fetchall()
    
    
    cursor.execute("SELECT time_start, time_end FROM user WHERE id = ?", (task_id,))
    start_time, end_time = cursor.fetchone()
    
    
    
    start_time= datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    
    
    time_difference = end_time - start_time
    sum_time = time_difference.total_seconds()
    
    # Преобразовываю общую продолжительность выполнения задачи в секундах в объект timedelta
    time_delta = datetime.timedelta(seconds=sum_time)
    # Сформироваваю строку с продолжительностью в формате "часы:минуты:секунды"
    time_formatted = str(time_delta)
    # Обновляю значение sum_time в базе данных в формате "часы:минуты:секунды"
    cursor.execute("UPDATE user SET sum_time = ? WHERE id = ?", (time_formatted, task_id))
    
    
    #Устанавливаю статус задачи:
    status = "comleted"
    cursor.execute("UPDATE user SET status = ? WHERE id = ?", (status, task_id))
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
    

# Вызываем функцию для обновления данных
#same_task()



same_task(9)