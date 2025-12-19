# главный модуль приложения управляет навигацией между экранами
import customtkinter as ctk
from config import COLORS, WINDOW_SIZES, get_base_dir
from auth import AuthManager
from screens import StartScreen, LoginScreen, RegisterScreen
from game_screen import GameScreen


class BricksGameApp(ctk.CTk):
    # главное окно приложения с системой навигации
    def __init__(self):
        super().__init__()
        
        # настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # настройка окна
        self.title("Игра «Кирпичи»")
        width, height = WINDOW_SIZES['bricks']
        self.minsize(width, height)
        
        # центрирование окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.configure(fg_color=COLORS['bg_primary'])
        
        try:
            # иконка рядом с ресурсами (учитываем PyInstaller)
            icon_path = get_base_dir() / "app.ico"
            self.iconbitmap(str(icon_path))
        except Exception:
            pass
        
        # инициализация менеджера авторизации
        self.auth_manager = AuthManager()
        
        # контейнер для экранов
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        # словарь экранов
        self.screens = {}
        
        # показываем стартовый экран
        self.show_start_screen()
    
    def clear_container(self):
        # очищаем контейнер от текущего экрана
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_start_screen(self):
        # показываем стартовый экран
        self.clear_container()
        screen = StartScreen(self.container, self.show_login_screen)
        screen.pack(fill="both", expand=True)
    
    def show_login_screen(self):
        # показываем экран авторизации
        self.clear_container()
        screen = LoginScreen(
            self.container,
            self.handle_login,
            self.show_register_screen
        )
        screen.pack(fill="both", expand=True)
    
    def show_register_screen(self):
        # показываем экран регистрации
        self.clear_container()
        screen = RegisterScreen(
            self.container,
            self.handle_register,
            self.show_login_screen
        )
        screen.pack(fill="both", expand=True)
    
    def show_game_screen(self):
        # показываем игровой экран
        self.clear_container()
        screen = GameScreen(
            self.container,
            self.auth_manager,
            self.handle_logout,
            self.handle_exit
        )
        screen.pack(fill="both", expand=True)
    
    def handle_login(self, login, password):
        # обработка попытки входа
        success, message = self.auth_manager.login_user(login, password)
        
        if success:
            self.show_game_screen()
        else:
            # показываем ошибку на экране авторизации
            for widget in self.container.winfo_children():
                if isinstance(widget, LoginScreen):
                    widget.show_error(message)
                    break
    
    def handle_register(self, login, password, email, gender, age_category):
        # обработка регистрации нового пользователя
        success, message = self.auth_manager.register_user(
            login, password, email, gender, age_category
        )
        
        if success:
            # автоматически входим в аккаунт после регистрации
            self.auth_manager.login_user(login, password)
            self.show_game_screen()
        else:
            # показываем ошибку на экране регистрации
            # ищем текущий экран регистрации в контейнере
            for widget in self.container.winfo_children():
                if isinstance(widget, RegisterScreen):
                    widget.show_error(message)
                    break
    
    def handle_logout(self):
        # обработка выхода из аккаунта
        self.auth_manager.logout_user()
        self.show_login_screen()
    
    def handle_exit(self):
        # закрытие приложения
        self.destroy()


def main():
    # точка входа в приложение
    app = BricksGameApp()
    app.mainloop()


if __name__ == "__main__":
    main()