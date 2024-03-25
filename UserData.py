import sqlite3

class UserData:
    def __init__(self, app, first_time_start, time_start, time_end, sum_time, status):
        self.app = app
        self.first_time_start = first_time_start
        self.time_start = time_start
        self.time_end = time_end
        self.sum_time = sum_time
        self.status = status
        
class apps_with_status:
    def __init__(self):
        self.connection = sqlite3.connect('tasks.db')
        self.cursor = self.connection.cursor()

    def display_apps_with_status_start(self):
        try:
            self.cursor.execute("SELECT * FROM user WHERE status = 'Start'")
            apps = self.cursor.fetchall()
            
            print("Приложения со стасуом 'Start':")
            for app in apps:
                print(app)
        except sqlite3.Error as error:
            print(f"Ошибка при выводе приложений: {error}")
            
    def display_apps_with_status_Completed(self):
        try:
            self.cursor.execute("SELECT * FROM user WHERE status = 'Completed'")
            apps = self.cursor.fetchall()
            
            print("Приложения со статусом 'Completed'")
            for app in apps:
                print(app)
        except sqlite3.Error as error:
            print(f"Ошибка при выводе приложений: {error}")
    def close_connection(self):
        if self.connection:
            self.connection.close()
