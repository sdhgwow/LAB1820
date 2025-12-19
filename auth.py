# модуль управляет авторизацией, регистрацией и хранением пользователей
import os
import json
import re
from datetime import datetime
from pathlib import Path
from config import get_base_dir


def get_users_file_path(filename: str = 'users.json') -> str:
    """
    Возвращает путь к файлу с пользователями.
    В режиме .exe (PyInstaller) файл лежит рядом с исполняемым файлом,
    в режиме .py — рядом с проектом (config.py).
    """
    base_dir = get_base_dir()

    # если запущено как собранный .exe — сохраняем рядом с .exe
    if getattr(__import__('sys'), 'frozen', False):
        exe_dir = Path(__import__('sys').executable).parent
        return str(exe_dir / filename)

    # обычный режим разработки
    return str(base_dir / filename)


class AuthManager:
    # класс отвечает за работу с пользователями и их данными
    def __init__(self, users_file: str | None = None):
        # вычисляем путь к файлу с пользователями
        self.users_file = users_file or get_users_file_path()
        self.users = self.load_users()
        self.current_user = None
    
    def load_users(self):
        # загружаем список пользователей из json файла
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки пользователей: {e}")
                return {}
        return {}
    
    def save_users(self):
        # сохраняем данные всех пользователей в файл
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения пользователей: {e}")
            return False
    
    def validate_email(self, email):
        # проверяем корректность формата email адреса
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        # проверяем минимальные требования к паролю
        return len(password) >= 4
    
    def validate_login(self, login):
        # проверяем корректность логина
        return len(login) >= 3 and login.isalnum()
    
    def register_user(self, login, password, email, gender, age_category):
        # регистрируем нового пользователя с валидацией данных
        
        # валидация логина
        if not self.validate_login(login):
            return False, "Логин должен содержать минимум 3 символа (только буквы и цифры)"
        
        # проверка на существование пользователя
        if login in self.users:
            return False, "Пользователь с таким логином уже существует"
        
        # валидация пароля
        if not self.validate_password(password):
            return False, "Пароль должен содержать минимум 4 символа"
        
        # валидация email
        if not self.validate_email(email):
            return False, "Некорректный формат email (должен быть xxx@xxx.x)"
        
        # создаем запись нового пользователя
        self.users[login] = {
            'password': password,
            'email': email,
            'gender': gender,
            'age_category': age_category,
            'stats': {
                'games': 0,
                'wins': 0,
                'losses': 0
            },
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # сохраняем данные в файл
        if self.save_users():
            return True, "Регистрация успешна!"
        else:
            return False, "Ошибка сохранения данных"
    
    def login_user(self, login, password):
        # авторизуем пользователя по логину и паролю
        if login not in self.users:
            return False, "Пользователь не найден"
        
        if self.users[login]['password'] != password:
            return False, "Неверный пароль"
        
        self.current_user = login
        return True, "Авторизация успешна!"
    
    def logout_user(self):
        # выходим из текущей сессии
        self.current_user = None
    
    def get_current_user(self):
        # возвращаем данные текущего пользователя
        if self.current_user:
            return self.users.get(self.current_user)
        return None
    
    def get_current_username(self):
        # возвращаем логин текущего пользователя
        return self.current_user
    
    def update_user_stats(self, result):
        # обновляем статистику текущего пользователя после игры
        if not self.current_user:
            return False
        
        user_data = self.users[self.current_user]
        user_data['stats']['games'] += 1
        
        if result == 'win':
            user_data['stats']['wins'] += 1
        elif result == 'loss':
            user_data['stats']['losses'] += 1
        
        return self.save_users()
    
    def get_leaderboard(self):
        # получаем отсортированную таблицу лидеров
        leaderboard = []
        
        for login, data in self.users.items():
            stats = data['stats']
            winrate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
            
            leaderboard.append({
                'login': login,
                'games': stats['games'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'winrate': winrate
            })
        
        # сортируем по количеству побед (по убыванию)
        leaderboard.sort(key=lambda x: x['wins'], reverse=True)
        
        return leaderboard