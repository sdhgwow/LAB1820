# модуль содержит экраны авторизации, регистрации и стартовый экран
import customtkinter as ctk
from config import COLORS, FONTS, SIZES, EMOJI
from utils import IconLoader


class StartScreen(ctk.CTkFrame):
    # стартовый экран с приветствием и кнопкой начала
    def __init__(self, parent, on_start):
        super().__init__(parent, fg_color=COLORS['bg_primary'])
        self.on_start = on_start
        self.create_widgets()
    
    def create_widgets(self):
        # центральный контейнер размещается по центру экрана
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # иконка игры
        bricks_icon, _ = IconLoader.get_text_with_icon('bricks', '', size=(80, 80))
        if bricks_icon:
            icon_label = ctk.CTkLabel(
                container,
                text="",
                image=bricks_icon
            )
        else:
            icon_label = ctk.CTkLabel(
                container,
                text="🧱",
                font=("SF Pro Display", 80)
            )
        icon_label.pack(pady=(0, SIZES['padding_lg']))
        
        # заголовок приложения
        title = ctk.CTkLabel(
            container,
            text="Игра «Кирпичи»",
            font=FONTS['heading_xl'],
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(0, SIZES['padding_sm']))
        
        # подзаголовок
        subtitle = ctk.CTkLabel(
            container,
            text="Стратегическая игра против AI",
            font=FONTS['body_lg'],
            text_color=COLORS['text_muted']
        )
        subtitle.pack(pady=(0, SIZES['padding_xl']))
        
        # кнопка начала игры
        start_btn = ctk.CTkButton(
            container,
            text="Начать",
            font=FONTS['heading_md'],
            width=250,
            height=SIZES['button_height_lg'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=SIZES['border_radius_sm'],
            command=self.on_start
        )
        start_btn.pack()


class LoginScreen(ctk.CTkFrame):
    # экран авторизации с полями логина и пароля
    def __init__(self, parent, on_login, on_register):
        super().__init__(parent, fg_color=COLORS['bg_primary'])
        self.on_login = on_login
        self.on_register = on_register
        self.create_widgets()
    
    def create_widgets(self):
        # центральный контейнер
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # карточка авторизации
        card = ctk.CTkFrame(
            container,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        card.pack(padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        # заголовок
        title = ctk.CTkLabel(
            content,
            text="Вход в аккаунт",
            font=FONTS['heading_lg'],
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(0, SIZES['padding_lg']))
        
        # поле логина
        login_label = ctk.CTkLabel(
            content,
            text="Логин:",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        login_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.login_entry = ctk.CTkEntry(
            content,
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['border'],
            placeholder_text="Введите логин"
        )
        self.login_entry.pack(pady=(0, SIZES['padding_md']))
        
        # поле пароля
        password_label = ctk.CTkLabel(
            content,
            text="Пароль:",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.password_entry = ctk.CTkEntry(
            content,
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['border'],
            placeholder_text="Введите пароль",
            show="*"
        )
        self.password_entry.pack(pady=(0, SIZES['padding_md']))
        
        # сообщение об ошибке
        self.error_label = ctk.CTkLabel(
            content,
            text="",
            font=FONTS['body_sm'],
            text_color=COLORS['error']
        )
        self.error_label.pack(pady=(0, SIZES['padding_sm']))
        
        # кнопка входа
        login_btn = ctk.CTkButton(
            content,
            text="Войти",
            font=FONTS['body_lg'],
            width=350,
            height=SIZES['button_height'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=SIZES['border_radius_sm'],
            command=self.handle_login
        )
        login_btn.pack(pady=(SIZES['padding_sm'], SIZES['padding_md']))
        
        # разделитель
        divider_frame = ctk.CTkFrame(content, fg_color="transparent")
        divider_frame.pack(fill="x", pady=SIZES['padding_md'])
        
        divider = ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['divider']
        )
        divider.pack(fill="x")
        
        # ссылка на регистрацию
        register_frame = ctk.CTkFrame(content, fg_color="transparent")
        register_frame.pack()
        
        register_text = ctk.CTkLabel(
            register_frame,
            text="Нет аккаунта?",
            font=FONTS['body_md'],
            text_color=COLORS['text_muted']
        )
        register_text.pack(side="left", padx=(0, SIZES['padding_xs']))
        
        register_link = ctk.CTkButton(
            register_frame,
            text="Зарегистрироваться",
            font=FONTS['body_md'],
            fg_color="transparent",
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['primary'],
            width=150,
            height=30,
            command=self.on_register
        )
        register_link.pack(side="left")
        
        # привязываем Enter к входу
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
    
    def handle_login(self):
        # получаем данные и передаем в callback
        login = self.login_entry.get().strip()
        password = self.password_entry.get()
        
        if not login or not password:
            self.show_error("Заполните все поля")
            return
        
        self.on_login(login, password)
    
    def show_error(self, message):
        # отображаем сообщение об ошибке
        self.error_label.configure(text=message)
    
    def clear_fields(self):
        # очищаем поля ввода
        self.login_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.error_label.configure(text="")


class RegisterScreen(ctk.CTkFrame):
    # экран регистрации с расширенными данными пользователя
    def __init__(self, parent, on_register, on_back):
        super().__init__(parent, fg_color=COLORS['bg_primary'])
        self.on_register = on_register
        self.on_back = on_back
        self.create_widgets()
    
    def create_widgets(self):
        # создаем прокручиваемый контейнер
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        # центруем содержимое
        container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        container.pack(expand=True)
        
        # карточка регистрации
        card = ctk.CTkFrame(
            container,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        card.pack(padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        # заголовок
        title = ctk.CTkLabel(
            content,
            text="Регистрация",
            font=FONTS['heading_lg'],
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(0, SIZES['padding_lg']))
        
        # поле логина
        login_label = ctk.CTkLabel(
            content,
            text="Логин (минимум 3 символа):",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        login_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.login_entry = ctk.CTkEntry(
            content,
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['border'],
            placeholder_text="Придумайте логин"
        )
        self.login_entry.pack(pady=(0, SIZES['padding_md']))
        
        # поле email
        email_label = ctk.CTkLabel(
            content,
            text="Email:",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        email_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.email_entry = ctk.CTkEntry(
            content,
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['border'],
            placeholder_text="example@mail.com"
        )
        self.email_entry.pack(pady=(0, SIZES['padding_md']))
        
        # поле пароля
        password_label = ctk.CTkLabel(
            content,
            text="Пароль (минимум 4 символа):",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.password_entry = ctk.CTkEntry(
            content,
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['border'],
            placeholder_text="Придумайте пароль",
            show="*"
        )
        self.password_entry.pack(pady=(0, SIZES['padding_md']))
        
        # выбор пола
        gender_label = ctk.CTkLabel(
            content,
            text="Пол:",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        gender_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.gender_var = ctk.StringVar(value="Не указан")
        gender_menu = ctk.CTkOptionMenu(
            content,
            variable=self.gender_var,
            values=["Мужской", "Женский", "Не указан"],
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            button_color=COLORS['primary'],
            button_hover_color=COLORS['primary_hover']
        )
        gender_menu.pack(pady=(0, SIZES['padding_md']))
        
        # выбор возрастной категории
        age_label = ctk.CTkLabel(
            content,
            text="Возрастная категория:",
            font=FONTS['body_md'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        age_label.pack(fill="x", pady=(0, SIZES['padding_xs']))
        
        self.age_var = ctk.StringVar(value="18-25")
        age_menu = ctk.CTkOptionMenu(
            content,
            variable=self.age_var,
            values=["До 18", "18-25", "26-35", "36-45", "46+"],
            font=FONTS['body_lg'],
            width=350,
            height=45,
            fg_color=COLORS['bg_secondary'],
            button_color=COLORS['primary'],
            button_hover_color=COLORS['primary_hover']
        )
        age_menu.pack(pady=(0, SIZES['padding_md']))
        
        # сообщение об ошибке
        self.error_label = ctk.CTkLabel(
            content,
            text="",
            font=FONTS['body_sm'],
            text_color=COLORS['error'],
            wraplength=320
        )
        self.error_label.pack(pady=(0, SIZES['padding_sm']))
        
        # кнопка регистрации
        register_btn = ctk.CTkButton(
            content,
            text="Зарегистрироваться",
            font=FONTS['body_lg'],
            width=350,
            height=SIZES['button_height'],
            fg_color=COLORS['success'],
            hover_color=self.darken_color(COLORS['success']),
            corner_radius=SIZES['border_radius_sm'],
            command=self.handle_register
        )
        register_btn.pack(pady=(SIZES['padding_sm'], SIZES['padding_md']))
        
        # кнопка назад
        back_btn = ctk.CTkButton(
            content,
            text="Назад к входу",
            font=FONTS['body_md'],
            width=350,
            height=40,
            fg_color="transparent",
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_muted'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=SIZES['border_radius_sm'],
            command=self.on_back
        )
        back_btn.pack()
    
    def handle_register(self):
        # собираем данные формы и передаем в callback
        login = self.login_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        gender = self.gender_var.get()
        age_category = self.age_var.get()
        
        if not login or not email or not password:
            self.show_error("Заполните все обязательные поля")
            return
        
        self.on_register(login, password, email, gender, age_category)
    
    def show_error(self, message):
        # отображаем сообщение об ошибке
        self.error_label.configure(text=message)
    
    def clear_fields(self):
        # очищаем все поля формы
        self.login_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.gender_var.set("Не указан")
        self.age_var.set("18-25")
        self.error_label.configure(text="")
    
    def darken_color(self, hex_color):
        # уменьшаем яркость цвета для эффекта hover
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'