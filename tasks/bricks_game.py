# модуль описывает игру "кирпичи" с интерфейсом customtkinter
import customtkinter as ctk
import random
import json
import os
import math
from datetime import datetime
from pathlib import Path
from config import COLORS, FONTS, WINDOW_SIZES, BRICKS_GAME, SIZES, get_base_dir
from utils import IconLoader


class BricksGameTask(ctk.CTkToplevel):
    # окно запускает игру "кирпичи" и управляет ее состоянием
    def __init__(self, parent):
        super().__init__(parent)
        
        # подготавливаем окно и заголовок с иконкой
        icon, title_text = IconLoader.get_text_with_icon('bricks', ' Кирпичи', size=(24, 24))
        self.title(title_text)
        
        width, height = WINDOW_SIZES['bricks']
        
        # фиксируем минимальные размеры и размещаем окно по центру
        self.minsize(width, height)
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(fg_color=COLORS['bg_primary'])
        
        # создаем игровые переменные и параметры отображения стены
        self.bricks_left = 0
        self.current_turn = "player"
        self.game_active = False
        
        # подгружаем накопленную статистику
        self.stats_file = self.get_stats_file_path()
        self.stats = self.load_stats()
        
        # инициализируем историю ходов и параметры кирпичей
        self.move_history = []
        self.brick_size = (36, 36)
        self.brick_icon = IconLoader.load_icon('brick', size=self.brick_size)
        self.bricks_per_row = 8
        self.max_brick_rows = 6
        
        # собираем интерфейс и запрещаем изменение размера
        self.create_widgets()
        
        self.resizable(False, False)

        try:
            # иконка приложения — берем из каталога ресурсов
            icon_path = get_base_dir() / "app.ico"
            self.iconbitmap(str(icon_path))
        except Exception:
            pass
    
    def create_widgets(self):
        # формируем основной контейнер окна и размещаем секции
        main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        # верхняя часть показывает название игры и правила
        self.create_header(main_frame)
        
        # центральная зона делится на игровое поле и боковую панель
        game_container = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        game_container.pack(fill="both", expand=True, pady=(0, SIZES['padding_md']))
        
        game_container.grid_columnconfigure(0, weight=2)
        game_container.grid_columnconfigure(1, weight=1)
        game_container.grid_rowconfigure(0, weight=1)
        
        # на левой части располагается поле с кирпичами
        self.create_game_panel(game_container)
        
        # справа выводим статистику и историю ходов
        self.create_side_panel(game_container)
        
        # снизу размещаем кнопки новой игры и сохранения статистики
        self.create_control_panel(main_frame)
        
    def create_header(self, parent):
        # выводим заголовок игры и краткое правило
        header_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(0, SIZES['padding_lg']))
        
        icon, title_text = IconLoader.get_text_with_icon('bricks', '  Кирпичи', size=(28, 28))
        title_label = ctk.CTkLabel(
            header_frame,
            text=title_text,
            image=icon,
            font=FONTS['heading_lg'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        title_label.pack(anchor="w")
        
        rules_label = ctk.CTkLabel(
            header_frame,
            text="Забирайте от 1 до 3 кирпичей. Кто не может сделать ход - проиграл!",
            font=FONTS['body_md'],
            text_color=COLORS['text_muted']
        )
        rules_label.pack(anchor="w", pady=(4, 0))
        
    def create_game_panel(self, parent):
        # игровая панель содержит стену кирпичей и элементы хода
        game_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        game_panel.grid(row=0, column=0, sticky="nsew", padx=(0, SIZES['padding_sm']))
        
        content_frame = ctk.CTkFrame(
            game_panel,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=SIZES['padding_lg'], pady=SIZES['padding_lg'])
        
        # отображаем стену кирпичей и подписи
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
        
        # текстовый индикатор показывает, чей сейчас ход
        self.turn_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=FONTS['heading_md'],
            text_color=COLORS['text_secondary']
        )
        self.turn_label.pack(pady=(0, SIZES['padding_md']))
        
        # блок кнопок позволяет выбрать количество снимаемых кирпичей
        self.create_move_buttons(content_frame)
        
    def create_move_buttons(self, parent):
        # блок с кнопками дает игроку выбрать 1-3 кирпича
        buttons_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x")
        
        label = ctk.CTkLabel(
            buttons_frame,
            text="Выберите количество кирпичей:",
            font=FONTS['body_lg'],
            text_color=COLORS['text_secondary']
        )
        label.pack(pady=(0, SIZES['padding_sm']))
        
        btn_container = ctk.CTkFrame(
            buttons_frame,
            fg_color="transparent"
        )
        btn_container.pack()
        
        self.move_buttons = []
        for i in range(1, 4):
            btn = ctk.CTkButton(
                btn_container,
                text=f"{i} кирпич" + ("а" if i == 2 else "ей" if i == 3 else ""),
                font=FONTS['body_lg'],
                width=150,
                height=SIZES['button_height_lg'],
                fg_color=COLORS['primary'],
                hover_color=COLORS['primary_hover'],
                corner_radius=SIZES['border_radius_sm'],
                command=lambda x=i: self.player_move(x)
            )
            btn.pack(side="left", padx=SIZES['padding_sm'])
            self.register_button_styles(
                btn,
                enabled_style={
                    "fg_color": COLORS['primary'],
                    "hover_color": COLORS['primary_hover'],
                    "text_color": COLORS['text_primary']
                },
                disabled_style={
                    "fg_color": COLORS['border'],
                    "hover_color": COLORS['border'],
                    "text_color": COLORS['text_muted']
                }
            )
            self.apply_button_state(btn, False)
            self.move_buttons.append(btn)
    
    def create_side_panel(self, parent):
        # боковая панель держит статистику и историю ходов
        side_panel = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        side_panel.grid(row=0, column=1, sticky="nsew", padx=(SIZES['padding_sm'], 0))
        
        # верхняя часть панели показывает статистику пользователя
        stats_frame = ctk.CTkFrame(
            side_panel,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        stats_frame.pack(fill="x", pady=(0, SIZES['padding_md']))
        
        stats_content = ctk.CTkFrame(
            stats_frame,
            fg_color="transparent"
        )
        stats_content.pack(fill="both", expand=True, padx=SIZES['padding_md'], pady=SIZES['padding_md'])
        
        trophy_icon, trophy_text = IconLoader.get_text_with_icon('trophy', ' Статистика', size=(25, 25))
        stats_title = ctk.CTkLabel(
            stats_content,
            text=trophy_text if trophy_icon is None else "Статистика",
            image=trophy_icon,
            font=FONTS['heading_sm'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        stats_title.pack(anchor="w", pady=(0, SIZES['padding_sm']))
        
        self.stats_labels = {}
        stats_data = [
            ("games", "Всего игр:", COLORS['info']),
            ("wins", "Побед игрока:", COLORS['success']),
            ("losses", "Побед AI:", COLORS['error']),
            ("winrate", "Процент побед:", COLORS['warning'])
        ]
        
        for key, text, color in stats_data:
            stat_frame = ctk.CTkFrame(
                stats_content,
                fg_color="transparent"
            )
            stat_frame.pack(fill="x", pady=2)
            
            label = ctk.CTkLabel(
                stat_frame,
                text=text,
                font=FONTS['body_sm'],
                text_color=COLORS['text_muted'],
                anchor="w"
            )
            label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text="0",
                font=FONTS['body_lg'],
                text_color=color,
                anchor="e"
            )
            value_label.pack(side="right")
            self.stats_labels[key] = value_label
        
        self.update_stats_display()
        
        # нижняя часть панели хранит историю ходов
        history_frame = ctk.CTkFrame(
            side_panel,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        history_frame.pack(fill="both", expand=True)
        
        history_content = ctk.CTkFrame(
            history_frame,
            fg_color="transparent"
        )
        history_content.pack(fill="both", expand=True, padx=SIZES['padding_md'], pady=SIZES['padding_md'])
        
        scroll_icon, scroll_text = IconLoader.get_text_with_icon('scroll', ' История ходов', size=(20, 20))
        history_title = ctk.CTkLabel(
            history_content,
            text=scroll_text if scroll_icon is None else "История ходов",
            image=scroll_icon,
            font=FONTS['heading_sm'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        history_title.pack(anchor="w", pady=(0, SIZES['padding_sm']))
        
        self.history_text = ctk.CTkTextbox(
            history_content,
            font=FONTS['mono'],
            fg_color=COLORS['bg_secondary'],
            text_color=COLORS['text_secondary'],
            wrap="word",
            state="disabled"
        )
        self.history_text.pack(fill="both", expand=True)
        
    def create_control_panel(self, parent):
        # нижняя панель объединяет кнопки запуска игры и сохранения
        control_panel = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        control_panel.pack(fill="x")
        
        # кнопка запускает новую партию игры
        play_icon, play_text = IconLoader.get_text_with_icon('play', ' Новая игра', size=(13, 13))
        self.new_game_btn = ctk.CTkButton(
            control_panel,
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
        self.new_game_btn.pack(side="left", expand=True, fill="x", padx=(0, SIZES['padding_sm']))
        self.register_button_styles(
            self.new_game_btn,
            enabled_style={
                "fg_color": COLORS['success'],
                "hover_color": self.darken_color(COLORS['success']),
                "text_color": COLORS['text_primary']
            },
            disabled_style={
                "fg_color": COLORS['border'],
                "hover_color": COLORS['border'],
                "text_color": COLORS['text_muted']
            }
        )
        self.apply_button_state(self.new_game_btn, True)
        
        # кнопка справа сохраняет результаты на диск
        save_icon, save_text = IconLoader.get_text_with_icon('save', ' Сохранить статистику', size=(13, 13))
        save_btn = ctk.CTkButton(
            control_panel,
            text=save_text if save_icon is None else "Сохранить статистику",
            image=save_icon,
            font=FONTS['body_lg'],
            height=SIZES['button_height'],
            fg_color=COLORS['info'],
            hover_color=self.darken_color(COLORS['info']),
            corner_radius=SIZES['border_radius_sm'],
            compound="left",
            command=self.save_stats_to_file
        )
        save_btn.pack(side="left", expand=True, fill="x", padx=(SIZES['padding_sm'], 0))
        
    def start_new_game(self):
        # подготавливаем новое состояние игры и очищаем историю
        if self.game_active:
            return
        
        self.bricks_left = random.randint(BRICKS_GAME['min_bricks'], BRICKS_GAME['max_bricks'])
        self.current_turn = "player"
        self.game_active = True
        self.move_history = []
        self.apply_button_state(self.new_game_btn, False)
        
        self.update_bricks_display()
        self.update_turn_display()
        self.update_move_buttons()
        self.clear_history()
        
        text = f"Новая игра! Кирпичей: {self.bricks_left}"
        self.add_to_history(text)
        
    def player_move(self, amount):
        # обрабатываем выбор игрока и валидируем количество кирпичей
        if not self.game_active or self.current_turn != "player":
            return
        
        if amount > self.bricks_left:
            self.show_message("Нельзя взять больше кирпичей, чем осталось!", "error")
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
        # выполняем ход компьютера после небольшой задержки
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
        # выбираем допустимое количество кирпичей для хода ai
        if self.bricks_left <= BRICKS_GAME['max_take']:
            return self.bricks_left
        
        max_take = min(BRICKS_GAME['max_take'], self.bricks_left)
        return random.randint(BRICKS_GAME['min_take'], max_take)
        
    def end_game(self, loser):
        # фиксируем результат партии и обновляем статистику
        self.game_active = False
        self.update_move_buttons()
        self.apply_button_state(self.new_game_btn, True)
        
        if loser == "player":
            self.stats['losses'] += 1
            cross_icon, _ = IconLoader.get_text_with_icon('cross', '', size=(16, 16))
            self.add_to_history(f"\n{'✗' if cross_icon is None else ''} Вы проиграли! Победил AI")
            self.show_message("AI победил!", "error")
        else:
            self.stats['wins'] += 1
            trophy_icon, _ = IconLoader.get_text_with_icon('trophy', '', size=(16, 16))
            self.add_to_history(f"\n{'🏆' if trophy_icon is None else ''} Вы победили!")
            self.show_message("Поздравляем! Вы победили!", "success")
        
        self.stats['games'] += 1
        self.save_stats()
        self.update_stats_display()
        
    def update_bricks_display(self):
        # обновляем визуализацию стены и подпись о количестве
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
        # строим сетку кирпичей и центрируем ее внутри контейнера
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
        total_rows = full_rows + (1 if remainder else 0)
        total_rows = min(total_rows, self.max_brick_rows)

        row_counts = []
        if remainder and len(row_counts) < self.max_brick_rows:
            row_counts.append(remainder)
        for _ in range(full_rows):
            if len(row_counts) >= self.max_brick_rows:
                break
            row_counts.append(self.bricks_per_row)

        # добавляем дополнительные полные ряды, чтобы стена не смещалась
        while len(row_counts) < self.max_brick_rows and self.bricks_left >= bricks_capacity:
            row_counts.append(self.bricks_per_row)

        wall_content = ctk.CTkFrame(self.bricks_wall_container, fg_color="transparent")
        wall_content.place(relx=0.5, rely=0.5, anchor="center")

        for bricks_in_row in row_counts:
            row_frame = ctk.CTkFrame(
                wall_content,
                fg_color="transparent"
            )
            row_frame.pack(anchor="center", pady=2)
            inner_row = ctk.CTkFrame(
                row_frame,
                fg_color="transparent"
            )
            inner_row.pack()

            for _ in range(bricks_in_row):
                brick_widget = self.create_brick_widget(inner_row)
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
        # возвращаем виджет кирпича, используя svg или emoji
        if isinstance(self.brick_icon, str):
            return ctk.CTkLabel(
                parent,
                text=self.brick_icon,
                font=FONTS['heading_md'],
                text_color=COLORS['warning']
            )
        return ctk.CTkLabel(
            parent,
            text="",
            image=self.brick_icon
        )
    
    def update_turn_display(self):
        # выводим информацию о текущем игроке или ai
        if self.game_active:
            if self.current_turn == "player":
                user_icon, user_text = IconLoader.get_text_with_icon('user', 'Ваш ход', size=(20, 20))
                self.turn_label.configure(
                    text=user_text if user_icon is None else "Ваш ход",
                    image=user_icon if user_icon else None,
                    text_color=COLORS['success'],
                    compound="left"
                )
            else:
                robot_icon, robot_text = IconLoader.get_text_with_icon('robot', 'Ход AI...', size=(20, 20))
                self.turn_label.configure(
                    text=robot_text if robot_icon is None else "Ход AI...",
                    image=robot_icon if robot_icon else None,
                    text_color=COLORS['info'],
                    compound="left"
                )
        else:
            self.turn_label.configure(text="", image=None, text_color=COLORS['text_secondary'])
    
    def update_move_buttons(self):
        # включаем доступные кнопки в зависимости от количества кирпичей
        if self.game_active and self.current_turn == "player":
            for i, btn in enumerate(self.move_buttons, 1):
                if i <= self.bricks_left:
                    self.apply_button_state(btn, True)
                else:
                    self.apply_button_state(btn, False)
        else:
            for btn in self.move_buttons:
                self.apply_button_state(btn, False)
    
    def register_button_styles(self, button, enabled_style, disabled_style):
        # сохраняем стили кнопки для активного и неактивного состояния
        button._enabled_style = enabled_style
        button._disabled_style = disabled_style
    
    def apply_button_state(self, button, enabled):
        # применяем нужные цвета и состояние к кнопке
        style = getattr(button, "_enabled_style" if enabled else "_disabled_style", {})
        button.configure(
            state="normal" if enabled else "disabled",
            **style
        )
    
    def add_to_history(self, text):
        # добавляем новую запись в текстовую историю
        self.history_text.configure(state="normal")
        self.history_text.insert("end", text + "\n")
        self.history_text.see("end")
        self.history_text.configure(state="disabled")
        
    def clear_history(self):
        # очищаем текстовое поле истории
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.configure(state="disabled")
    
    def update_stats_display(self):
        # перерисовываем значения статистики и процент побед
        self.stats_labels['games'].configure(text=str(self.stats['games']))
        self.stats_labels['wins'].configure(text=str(self.stats['wins']))
        self.stats_labels['losses'].configure(text=str(self.stats['losses']))
        
        if self.stats['games'] > 0:
            winrate = (self.stats['wins'] / self.stats['games']) * 100
            self.stats_labels['winrate'].configure(text=f"{winrate:.1f}%")
        else:
            self.stats_labels['winrate'].configure(text="0.0%")
    
    def get_stats_file_path(self) -> str:
        """
        Возвращает путь к файлу с общей статистикой игры.
        В режиме .exe файл лежит рядом с исполняемым файлом,
        в режиме .py — рядом с проектом (config.py).
        """
        filename = BRICKS_GAME['save_file']
        # если запущено как собранный .exe — сохраняем рядом с .exe
        if getattr(__import__('sys'), 'frozen', False):
            exe_dir = Path(__import__('sys').executable).parent
            return str(exe_dir / filename)

        # обычный режим разработки
        return str(get_base_dir() / filename)

    def load_stats(self):
        # читаем сохраненную статистику из файла, если он есть
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {'games': 0, 'wins': 0, 'losses': 0}
    
    def save_stats(self):
        # сохраняем статистику в память (пока заглушка)
        pass
    
    def save_stats_to_file(self):
        # записываем текущее состояние статистики на диск
        try:
            stats_with_time = self.stats.copy()
            stats_with_time['last_saved'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_with_time, f, ensure_ascii=False, indent=2)
            
            self.show_message("Статистика сохранена!", "success")
        except Exception as e:
            self.show_message(f"Ошибка сохранения: {e}", "error")
    
    def show_message(self, text, msg_type="info"):
        # рисуем временное уведомление в верхней части окна
        color_map = {
            "success": COLORS['success'],
            "error": COLORS['error'],
            "info": COLORS['info'],
            "warning": COLORS['warning']
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
        notification.place(relx=0.5, rely=0.05, anchor="center")
        
        self.after(2000, notification.destroy)
    
    def get_brick_suffix(self, amount):
        # подбираем окончание в зависимости от количества кирпичей
        if amount == 1:
            return "кирпич"
        elif amount in [2, 3, 4]:
            return "кирпича"
        else:
            return "кирпичей"
    
    def darken_color(self, hex_color):
        # уменьшаем яркость цвета для состояний hover
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'