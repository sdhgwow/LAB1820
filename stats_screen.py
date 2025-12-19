# модуль отображает таблицу лидеров со статистикой игроков
import customtkinter as ctk
from config import COLORS, FONTS, SIZES, get_base_dir
from utils import IconLoader


class StatsScreen(ctk.CTkToplevel):
    # окно показывает сводную статистику всех пользователей
    def __init__(self, parent, auth_manager):
        super().__init__(parent)
        self.auth_manager = auth_manager
        
        # настройка окна
        self.title("Таблица лидеров")
        width, height = 800, 600
        self.minsize(width, height)
        
        # центрируем окно
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.configure(fg_color=COLORS['bg_primary'])
        self.resizable(False, False)
        
        try:
            icon_path = get_base_dir() / "app.ico"
            self.iconbitmap(str(icon_path))
        except Exception:
            pass
        
        self.create_widgets()
    
    def create_widgets(self):
        # основной контейнер окна
        main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=SIZES['padding_xl'], pady=SIZES['padding_xl'])
        
        # заголовок
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, SIZES['padding_lg']))
        
        trophy_icon, trophy_text = IconLoader.get_text_with_icon('trophy', ' Таблица лидеров', size=(28, 28))
        title_label = ctk.CTkLabel(
            header_frame,
            text=trophy_text if trophy_icon is None else "Таблица лидеров",
            image=trophy_icon,
            font=FONTS['heading_lg'],
            text_color=COLORS['text_primary'],
            compound="left"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Рейтинг игроков по количеству побед",
            font=FONTS['body_md'],
            text_color=COLORS['text_muted']
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # карточка с таблицей
        table_card = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['bg_card'],
            corner_radius=SIZES['border_radius'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border']
        )
        table_card.pack(fill="both", expand=True, pady=(0, SIZES['padding_md']))
        
        # заголовок таблицы
        header_row = ctk.CTkFrame(
            table_card,
            fg_color=COLORS['bg_secondary'],
            height=50
        )
        header_row.pack(fill="x", padx=SIZES['padding_md'], pady=(SIZES['padding_md'], 0))
        header_row.pack_propagate(False)
        
        # настройка колонок для grid
        header_row.grid_columnconfigure(0, minsize=60, weight=0)
        header_row.grid_columnconfigure(1, minsize=200, weight=1)
        header_row.grid_columnconfigure(2, minsize=100, weight=0)
        header_row.grid_columnconfigure(3, minsize=100, weight=0)
        header_row.grid_columnconfigure(4, minsize=120, weight=0)
        header_row.grid_columnconfigure(5, minsize=130, weight=0)
        
        headers = [
            ("#", 0),
            ("Игрок", 1),
            ("Игр", 2),
            ("Побед", 3),
            ("Поражений", 4),
            ("Процент побед", 5)
        ]
        
        for header, col in headers:
            label = ctk.CTkLabel(
                header_row,
                text=header,
                font=FONTS['body_lg'],
                text_color=COLORS['text_primary'],
                anchor="w" if col == 1 else "center"
            )
            label.grid(row=0, column=col, padx=SIZES['padding_sm'], pady=SIZES['padding_sm'], sticky="ew")
        
        # прокручиваемая область с данными
        scroll_frame = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=SIZES['padding_md'], pady=SIZES['padding_md'])
        
        # настройка колонок для строк данных (должны совпадать с заголовками)
        scroll_frame.grid_columnconfigure(0, minsize=60, weight=0)
        scroll_frame.grid_columnconfigure(1, minsize=200, weight=1)
        scroll_frame.grid_columnconfigure(2, minsize=100, weight=0)
        scroll_frame.grid_columnconfigure(3, minsize=100, weight=0)
        scroll_frame.grid_columnconfigure(4, minsize=120, weight=0)
        scroll_frame.grid_columnconfigure(5, minsize=130, weight=0)
        
        # получаем данные лидеров
        leaderboard = self.auth_manager.get_leaderboard()
        current_user = self.auth_manager.get_current_username()
        
        if not leaderboard:
            no_data_label = ctk.CTkLabel(
                scroll_frame,
                text="Пока нет статистики. Сыграйте первую игру!",
                font=FONTS['body_lg'],
                text_color=COLORS['text_muted']
            )
            no_data_label.grid(row=0, column=0, columnspan=6, pady=SIZES['padding_xl'])
        else:
            # выводим строки с данными игроков
            for row_idx, player in enumerate(leaderboard):
                position = row_idx + 1  # позиция начинается с 1
                is_current = player['login'] == current_user
                
                # медали для топ-3
                if position == 1:
                    medal = "🥇"
                elif position == 2:
                    medal = "🥈"
                elif position == 3:
                    medal = "🥉"
                else:
                    medal = str(position)
                
                # фон для текущего пользователя
                bg_color = COLORS['primary'] if is_current else COLORS['bg_secondary']
                text_color = "white" if is_current else COLORS['text_primary']
                
                # номер позиции
                pos_label = ctk.CTkLabel(
                    scroll_frame,
                    text=medal,
                    font=FONTS['body_lg'],
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=SIZES['border_radius_sm'],
                    anchor="center"
                )
                pos_label.grid(row=row_idx, column=0, padx=2, pady=2, sticky="ew")
                
                # логин игрока
                login_text = f"{player['login']} (Вы)" if is_current else player['login']
                login_label = ctk.CTkLabel(
                    scroll_frame,
                    text=login_text,
                    font=FONTS['body_lg'],
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=SIZES['border_radius_sm'],
                    anchor="w"
                )
                login_label.grid(row=row_idx, column=1, padx=2, pady=2, sticky="ew")
                
                # статистика - игры
                games_label = ctk.CTkLabel(
                    scroll_frame,
                    text=str(player['games']),
                    font=FONTS['body_lg'],
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=SIZES['border_radius_sm'],
                    anchor="center"
                )
                games_label.grid(row=row_idx, column=2, padx=2, pady=2, sticky="ew")
                
                # статистика - победы
                wins_label = ctk.CTkLabel(
                    scroll_frame,
                    text=str(player['wins']),
                    font=FONTS['body_lg'],
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=SIZES['border_radius_sm'],
                    anchor="center"
                )
                wins_label.grid(row=row_idx, column=3, padx=2, pady=2, sticky="ew")
                
                # статистика - поражения
                losses_label = ctk.CTkLabel(
                    scroll_frame,
                    text=str(player['losses']),
                    font=FONTS['body_lg'],
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=SIZES['border_radius_sm'],
                    anchor="center"
                )
                losses_label.grid(row=row_idx, column=4, padx=2, pady=2, sticky="ew")
                
                # процент побед
                winrate_label = ctk.CTkLabel(
                    scroll_frame,
                    text=f"{player['winrate']:.1f}%",
                    font=FONTS['body_lg'],
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=SIZES['border_radius_sm'],
                    anchor="center"
                )
                winrate_label.grid(row=row_idx, column=5, padx=2, pady=2, sticky="ew")
        
        # кнопка закрытия
        close_btn = ctk.CTkButton(
            main_frame,
            text="Закрыть",
            font=FONTS['body_lg'],
            height=SIZES['button_height'],
            fg_color=COLORS['bg_secondary'],
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=SIZES['border_width'],
            border_color=COLORS['border'],
            corner_radius=SIZES['border_radius_sm'],
            command=self.destroy
        )
        close_btn.pack(fill="x")