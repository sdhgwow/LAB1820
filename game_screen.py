# модуль содержит основной игровой экран с меню и функционалом
import customtkinter as ctk
import random
from config import COLORS, FONTS, SIZES, BRICKS_GAME
from utils import IconLoader
from stats_screen import StatsScreen


class GameScreen(ctk.CTkFrame):
    # основной экран с игрой, меню и пользовательской информацией
    def __init__(self, parent, auth_manager, on_logout, on_exit):
        super().__init__(parent, fg_color=COLORS['bg_primary'])
        self.auth_manager = auth_manager
        self.on_logout = on_logout
        self.on_exit = on_exit
        
        # игровые переменные
        self.bricks_left = 0
        self.current_turn = "player"
        self.game_active = False
        self.move_history = []
        
        # параметры отображения кирпичей
        self.brick_size = (36, 36)
        self.brick_icon = IconLoader.load_icon('brick', size=self.brick_size)
        self.bricks_per_row = 8
        self.max_brick_rows = 6
        
        self.create_widgets()
    
    def create_widgets(self):
        # главный контейнер
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # верхняя панель с меню
        self.create_top_panel(main_container)
        
        # основное игровое пространство
        game_area = ctk.CTkFrame(main_container, fg_color="transparent")
        game_area.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=(SIZES['padding_md'], SIZES['padding_xl']))
        
        game_area.grid_columnconfigure(0, weight=2)
        game_area.grid_columnconfigure(1, weight=1)
        game_area.grid_rowconfigure(0, weight=1)
        
        # левая панель с игрой
        self.create_game_panel(game_area)
        
        # правая панель с историей
        self.create_side_panel(game_area)
    
    def create_top_panel(self, parent):
        # верхняя панель с приветствием и кнопками управления
        top_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_card'],
            corner_radius=0,
            border_width=0,
            height=70
        )
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        content = ctk.CTkFrame(top_panel, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_md'])
        
        # левая часть с приветствием
        left_section = ctk.CTkFrame(content, fg_color="transparent")
        left_section.pack(side="left", fill="y")
        
        username = self.auth_manager.get_current_username()
        user_icon, _ = IconLoader.get_text_with_icon('user', '', size=(24, 24))
        
        greeting = ctk.CTkLabel(
            left_section,
            text=f"Добро пожаловать, {username}!",
            image=user_icon if user_icon else None,
            font=FONTS['heading_md'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        greeting.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            left_section,
            text="Игра «Кирпичи»",
            font=FONTS['body_md'],
            text_color=COLORS['text_muted']
        )
        subtitle.pack(anchor="w")
        
        # правая часть с кнопками
        right_section = ctk.CTkFrame(content, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        buttons_frame = ctk.CTkFrame(right_section, fg_color="transparent")
        buttons_frame.pack(fill="y", anchor="e")
        
        # кнопка статистики
        trophy_icon, _ = IconLoader.get_text_with_icon('trophy', '', size=(20, 20))
        stats_btn = ctk.CTkButton(
            buttons_frame,
            text="Статистика",
            image=trophy_icon if trophy_icon else None,
            font=FONTS['body_md'],
            width=130,
            height=40,
            fg_color=COLORS['info'],
            hover_color=self.darken_color(COLORS['info']),
            corner_radius=SIZES['border_radius_sm'],
            compound="left",
            command=self.show_stats
        )
        stats_btn.pack(side="left", padx=(SIZES['padding_xs'], SIZES['padding_xs']))
        
        # кнопка выхода из аккаунта
        logout_btn = ctk.CTkButton(
            buttons_frame,
            text="Выйти",
            font=FONTS['body_md'],
            width=100,
            height=40,
            fg_color=COLORS['warning'],
            hover_color=self.darken_color(COLORS['warning']),
            corner_radius=SIZES['border_radius_sm'],
            command=self.confirm_logout
        )
        logout_btn.pack(side="left", padx=(0, SIZES['padding_xs']))
        
        # кнопка закрытия приложения
        exit_btn = ctk.CTkButton(
            buttons_frame,
            text="Закрыть",
            font=FONTS['body_md'],
            width=100,
            height=40,
            fg_color=COLORS['error'],
            hover_color=self.darken_color(COLORS['error']),
            corner_radius=SIZES['border_radius_sm'],
            command=self.confirm_exit
        )
        exit_btn.pack(side="left")
    
    def create_game_panel(self, parent):
        # панель с игровым полем
        game_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        game_panel.grid(row=0, column=0, sticky="nsew", padx=(0, SIZES['padding_sm']))
        
        content_frame = ctk.CTkFrame(game_panel, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=SIZES['padding_lg'], pady=SIZES['padding_lg'])
        
        # заголовок
        bricks_icon, title_text = IconLoader.get_text_with_icon('bricks', '  Игровое поле', size=(24, 24))
        title = ctk.CTkLabel(
            content_frame,
            text=title_text if bricks_icon is None else "Игровое поле",
            image=bricks_icon,
            font=FONTS['heading_md'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        title.pack(pady=(0, SIZES['padding_md']))
        
        # отображение стены кирпичей
        self.bricks_display_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=SIZES['border_radius_sm']
        )
        self.bricks_display_frame.pack(fill="both", expand=True, pady=(0, SIZES['padding_md']))
        
        self.bricks_wall_container = ctk.CTkFrame(
            self.bricks_display_frame,
            fg_color="transparent"
        )
        self.bricks_wall_container.pack(
            fill="both",
            expand=True,
            padx=SIZES['padding_md'],
            pady=(SIZES['padding_md'], SIZES['padding_sm'])
        )
        
        self.bricks_label = ctk.CTkLabel(
            self.bricks_display_frame,
            text='Нажмите "Новая игра" для начала',
            font=FONTS['heading_xl'],
            text_color=COLORS['text_muted']
        )
        self.bricks_label.pack(pady=(0, SIZES['padding_sm']))
        self.render_brick_wall()
        
        # индикатор хода
        self.turn_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=FONTS['heading_md'],
            text_color=COLORS['text_secondary']
        )
        self.turn_label.pack(pady=(0, SIZES['padding_md']))
        
        # кнопки хода
        self.create_move_buttons(content_frame)
        
        # кнопка новой игры
        play_icon, play_text = IconLoader.get_text_with_icon('play', ' Новая игра', size=(16, 16))
        self.new_game_btn = ctk.CTkButton(
            content_frame,
            text=play_text if play_icon is None else "Новая игра",
            image=play_icon,
            font=FONTS['body_lg'],
            height=SIZES['button_height'],
            fg_color=COLORS['success'],
            hover_color=self.darken_color(COLORS['success']),
            corner_radius=SIZES['border_radius_sm'],
            compound="left",
            command=self.start_new_game
        )
        self.new_game_btn.pack(fill="x", pady=(SIZES['padding_md'], 0))
    
    def create_move_buttons(self, parent):
        # кнопки выбора количества кирпичей
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        label = ctk.CTkLabel(
            buttons_frame,
            text="Выберите количество кирпичей:",
            font=FONTS['body_lg'],
            text_color=COLORS['text_secondary']
        )
        label.pack(pady=(0, SIZES['padding_sm']))
        
        btn_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        btn_container.pack()
        
        self.move_buttons = []
        for i in range(1, 4):
            btn = ctk.CTkButton(
                btn_container,
                text=f"{i} кирпич" + ("а" if i == 2 else "ей" if i == 3 else ""),
                font=FONTS['body_lg'],
                width=150,
                height=SIZES['button_height_lg'],
                fg_color=COLORS['border'],
                hover_color=COLORS['border'],
                text_color=COLORS['text_muted'],
                corner_radius=SIZES['border_radius_sm'],
                state="disabled",
                command=lambda x=i: self.player_move(x)
            )
            btn.pack(side="left", padx=SIZES['padding_sm'])
            self.move_buttons.append(btn)
    
    def create_side_panel(self, parent):
        # боковая панель с историей ходов
        side_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        side_panel.grid(row=0, column=1, sticky="nsew", padx=(SIZES['padding_sm'], 0))
        
        content = ctk.CTkFrame(side_panel, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SIZES['padding_md'], pady=SIZES['padding_md'])
        
        scroll_icon, scroll_text = IconLoader.get_text_with_icon('scroll', ' История ходов', size=(20, 20))
        title = ctk.CTkLabel(
            content,
            text=scroll_text if scroll_icon is None else "История ходов",
            image=scroll_icon,
            font=FONTS['heading_sm'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        title.pack(anchor="w", pady=(0, SIZES['padding_sm']))
        
        self.history_text = ctk.CTkTextbox(
            content,
            font=FONTS['mono'],
            fg_color=COLORS['bg_secondary'],
            text_color=COLORS['text_secondary'],
            wrap="word",
            state="disabled"
        )
        self.history_text.pack(fill="both", expand=True)
    
    def start_new_game(self):
        # запуск новой игры
        self.bricks_left = random.randint(BRICKS_GAME['min_bricks'], BRICKS_GAME['max_bricks'])
        self.current_turn = "player"
        self.game_active = True
        self.move_history = []
        
        self.update_bricks_display()
        self.update_turn_display()
        self.update_move_buttons()
        self.clear_history()
        
        self.add_to_history(f"Новая игра! Кирпичей: {self.bricks_left}")
    
    def player_move(self, amount):
        # обработка хода игрока
        if not self.game_active or self.current_turn != "player":
            return
        
        if amount > self.bricks_left:
            self.show_notification("Нельзя взять больше кирпичей!", "error")
            return
        
        self.bricks_left -= amount
        self.add_to_history(f"Игрок взял {amount} {self.get_brick_suffix(amount)}")
        self.update_bricks_display()
        
        if self.bricks_left == 0:
            self.end_game("ai")
            return
        
        self.current_turn = "ai"
        self.update_turn_display()
        self.update_move_buttons()
        self.after(1000, self.ai_move)
    
    def ai_move(self):
        # ход компьютера
        if not self.game_active or self.current_turn != "ai":
            return
        
        amount = self.calculate_ai_move()
        self.bricks_left -= amount
        self.add_to_history(f"AI взял {amount} {self.get_brick_suffix(amount)}")
        self.update_bricks_display()
        
        if self.bricks_left == 0:
            self.end_game("player")
            return
        
        self.current_turn = "player"
        self.update_turn_display()
        self.update_move_buttons()
    
    def calculate_ai_move(self):
        # расчет хода AI
        if self.bricks_left <= BRICKS_GAME['max_take']:
            return self.bricks_left
        
        max_take = min(BRICKS_GAME['max_take'], self.bricks_left)
        return random.randint(BRICKS_GAME['min_take'], max_take)
    
    def end_game(self, loser):
        # завершение игры и сохранение статистики
        self.game_active = False
        self.update_move_buttons()
        
        if loser == "player":
            self.auth_manager.update_user_stats('loss')
            self.add_to_history("\n✗ Вы проиграли! Победил AI")
            self.show_notification("AI победил!", "error")
        else:
            self.auth_manager.update_user_stats('win')
            self.add_to_history("\n🏆 Вы победили!")
            self.show_notification("Поздравляем! Вы победили!", "success")
    
    def update_bricks_display(self):
        # обновление визуализации кирпичей
        self.render_brick_wall()
        if self.game_active:
            self.bricks_label.configure(
                text=f"Осталось: {self.bricks_left}",
                text_color=COLORS['warning'] if self.bricks_left <= 5 else COLORS['text_primary']
            )
        else:
            self.bricks_label.configure(
                text="Нажмите 'Новая игра' для начала",
                text_color=COLORS['text_muted']
            )
    
    def render_brick_wall(self):
        # отрисовка стены из кирпичей
        for child in self.bricks_wall_container.winfo_children():
            child.destroy()
        
        if not self.game_active or self.bricks_left == 0:
            placeholder = ctk.CTkLabel(
                self.bricks_wall_container,
                text="Стена появится после начала игры",
                font=FONTS['body_md'],
                text_color=COLORS['text_muted']
            )
            placeholder.place(relx=0.5, rely=0.5, anchor="center")
            return
        
        bricks_capacity = self.bricks_per_row * self.max_brick_rows
        bricks_to_show = min(self.bricks_left, bricks_capacity)
        
        full_rows, remainder = divmod(bricks_to_show, self.bricks_per_row)
        row_counts = []
        if remainder:
            row_counts.append(remainder)
        for _ in range(min(full_rows, self.max_brick_rows - len(row_counts))):
            row_counts.append(self.bricks_per_row)
        
        wall_content = ctk.CTkFrame(self.bricks_wall_container, fg_color="transparent")
        wall_content.place(relx=0.5, rely=0.5, anchor="center")
        
        for bricks_in_row in row_counts:
            row_frame = ctk.CTkFrame(wall_content, fg_color="transparent")
            row_frame.pack(anchor="center", pady=2)
            
            for _ in range(bricks_in_row):
                brick_widget = self.create_brick_widget(row_frame)
                brick_widget.pack(side="left", padx=2, pady=1)
        
        if self.bricks_left > bricks_to_show:
            more_label = ctk.CTkLabel(
                wall_content,
                text=f"+ ещё {self.bricks_left - bricks_to_show}",
                font=FONTS['body_sm'],
                text_color=COLORS['text_secondary']
            )
            more_label.pack(pady=(SIZES['padding_xs'], 0))
    
    def create_brick_widget(self, parent):
        # создание виджета одного кирпича
        if isinstance(self.brick_icon, str):
            return ctk.CTkLabel(
                parent,
                text=self.brick_icon,
                font=FONTS['heading_md'],
                text_color=COLORS['warning']
            )
        return ctk.CTkLabel(parent, text="", image=self.brick_icon)
    
    def update_turn_display(self):
        # обновление индикатора хода
        if self.game_active:
            if self.current_turn == "player":
                user_icon, _ = IconLoader.get_text_with_icon('user', 'Ваш ход', size=(20, 20))
                self.turn_label.configure(
                    text="Ваш ход" if not user_icon else "",
                    image=user_icon,
                    text_color=COLORS['success'],
                    compound="left"
                )
            else:
                robot_icon, _ = IconLoader.get_text_with_icon('robot', 'Ход AI...', size=(20, 20))
                self.turn_label.configure(
                    text="Ход AI..." if not robot_icon else "",
                    image=robot_icon,
                    text_color=COLORS['info'],
                    compound="left"
                )
        else:
            self.turn_label.configure(text="", image=None)
    
    def update_move_buttons(self):
        # обновление состояния кнопок хода
        if self.game_active and self.current_turn == "player":
            for i, btn in enumerate(self.move_buttons, 1):
                if i <= self.bricks_left:
                    btn.configure(
                        state="normal",
                        fg_color=COLORS['primary'],
                        hover_color=COLORS['primary_hover'],
                        text_color=COLORS['text_primary']
                    )
                else:
                    btn.configure(
                        state="disabled",
                        fg_color=COLORS['border'],
                        hover_color=COLORS['border'],
                        text_color=COLORS['text_muted']
                    )
        else:
            for btn in self.move_buttons:
                btn.configure(
                    state="disabled",
                    fg_color=COLORS['border'],
                    hover_color=COLORS['border'],
                    text_color=COLORS['text_muted']
                )
    
    def add_to_history(self, text):
        # добавление записи в историю
        self.history_text.configure(state="normal")
        self.history_text.insert("end", text + "\n")
        self.history_text.see("end")
        self.history_text.configure(state="disabled")
    
    def clear_history(self):
        # очистка истории
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.configure(state="disabled")
    
    def show_stats(self):
        # открытие окна статистики
        stats_window = StatsScreen(self, self.auth_manager)
        stats_window.grab_set()
    
    def confirm_logout(self):
        # подтверждение выхода из аккаунта
        dialog = ConfirmDialog(
            self,
            "Выход из аккаунта",
            "Вы уверены, что хотите выйти из аккаунта?",
            self.on_logout
        )
    
    def confirm_exit(self):
        # подтверждение закрытия приложения
        dialog = ConfirmDialog(
            self,
            "Закрытие приложения",
            "Вы уверены, что хотите закрыть приложение?",
            self.on_exit
        )
    
    def show_notification(self, text, msg_type="info"):
        # показ уведомления
        color_map = {
            "success": COLORS['success'],
            "error": COLORS['error'],
            "info": COLORS['info']
        }
        
        notification = ctk.CTkLabel(
            self,
            text=text,
            font=FONTS['body_md'],
            fg_color=color_map.get(msg_type, COLORS['info']),
            text_color="white",
            corner_radius=SIZES['border_radius_sm'],
            width=300,
            height=50
        )
        notification.place(relx=0.5, rely=0.1, anchor="center")
        self.after(2000, notification.destroy)
    
    def get_brick_suffix(self, amount):
        # склонение слова "кирпич"
        if amount == 1:
            return "кирпич"
        elif amount in [2, 3, 4]:
            return "кирпича"
        return "кирпичей"
    
    def darken_color(self, hex_color):
        # затемнение цвета
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'


class ConfirmDialog(ctk.CTkToplevel):
    # диалоговое окно подтверждения действия
    def __init__(self, parent, title, message, on_confirm):
        super().__init__(parent)
        self.on_confirm = on_confirm
        
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(fg_color=COLORS['bg_primary'])
        
        # центрирование окна
        self.transient(parent)
        self.grab_set()
        
        # содержимое
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        # сообщение
        message_label = ctk.CTkLabel(
            content,
            text=message,
            font=FONTS['body_lg'],
            text_color=COLORS['text_primary'],
            wraplength=300
        )
        message_label.pack(expand=True)
        
        # кнопки
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Отмена",
            font=FONTS['body_lg'],
            width=150,
            height=SIZES['button_height'],
            fg_color=COLORS['bg_secondary'],
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=SIZES['border_radius_sm'],
            command=self.destroy
        )
        cancel_btn.pack(side="left", expand=True, padx=(0, SIZES['padding_sm']))
        
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Подтвердить",
            font=FONTS['body_lg'],
            width=150,
            height=SIZES['button_height'],
            fg_color=COLORS['error'],
            hover_color=self.darken_color(COLORS['error']),
            corner_radius=SIZES['border_radius_sm'],
            command=self.handle_confirm
        )
        confirm_btn.pack(side="left", expand=True, padx=(SIZES['padding_sm'], 0))
    
    def handle_confirm(self):
        # обработка подтверждения
        self.destroy()
        self.on_confirm()
    
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'