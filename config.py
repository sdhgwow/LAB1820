# конфигурационный модуль содержит цвета, размеры и ресурсы приложения
import os
import sys
from pathlib import Path

COLORS = {
    'bg_primary': '#0a0e27',
    'bg_secondary': '#151932',
    'bg_card': '#1a1f3a',
    'bg_hover': '#252a4a',
    
    'primary': '#6366f1',
    'primary_hover': '#4f46e5',
    'secondary': '#8b5cf6',
    'accent': '#06b6d4',
    
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'info': '#3b82f6',
    
    'text_primary': '#f1f5f9',
    'text_secondary': '#cbd5e1',
    'text_muted': '#94a3b8',
    'text_dark': '#1e293b',
    
    'border': '#334155',
    'divider': '#1e293b',
}

RAINBOW_COLORS = {
    'red': {
        'hex': '#ff0000',
        'name': 'Красный',
        'rgb': (255, 0, 0)
    },
    'orange': {
        'hex': '#ff7d00',
        'name': 'Оранжевый',
        'rgb': (255, 125, 0)
    },
    'yellow': {
        'hex': '#ffff00',
        'name': 'Желтый',
        'rgb': (255, 255, 0)
    },
    'green': {
        'hex': '#00ff00',
        'name': 'Зеленый',
        'rgb': (0, 255, 0)
    },
    'cyan': {
        'hex': '#007dff',
        'name': 'Голубой',
        'rgb': (0, 125, 255)
    },
    'blue': {
        'hex': '#0000ff',
        'name': 'Синий',
        'rgb': (0, 0, 255)
    },
    'violet': {
        'hex': '#7d00ff',
        'name': 'Фиолетовый',
        'rgb': (125, 0, 255)
    }
}

FONTS = {
    'family': 'SF Pro Display',
    'family_alt': 'Segoe UI',
    'heading_xl': ('SF Pro Display', 36, 'bold'),
    'heading_lg': ('SF Pro Display', 28, 'bold'),
    'heading_md': ('SF Pro Display', 22, 'bold'),
    'heading_sm': ('SF Pro Display', 18, 'bold'),
    'body_lg': ('SF Pro Display', 16),
    'body_md': ('SF Pro Display', 14),
    'body_sm': ('SF Pro Display', 12),
    'mono': ('Consolas', 14),
    'mono_lg': ('Consolas', 16, 'bold'),
}

WINDOW_SIZES = {
    'main': (900, 650),
    'rainbow': (800, 600),
    'bricks': (1000, 700),
}

SIZES = {
    'padding_xl': 32,
    'padding_lg': 24,
    'padding_md': 16,
    'padding_sm': 12,
    'padding_xs': 8,
    'border_radius': 16,
    'border_radius_sm': 12,
    'border_width': 2,
    'button_height': 48,
    'button_height_lg': 56,
}

ANIMATIONS = {
    'duration_fast': 100,
    'duration_normal': 200,
    'duration_slow': 300,
}

APP = {
    'title': 'Лабораторные работы №11-13',
    'subtitle': 'Графический интерфейс',
    'version': '1.0.0',
    'author': 'Дмитрий Твардовский',
}

BRICKS_GAME = {
    'min_bricks': 12,
    'max_bricks': 20,
    'min_take': 1,
    'max_take': 3,
    'save_file': 'bricks_stats.json',
}


def get_base_dir() -> Path:
    """
    Возвращает каталог, из которого читаются ресурсы (icons, app.ico и т.п.).
    Корректно работает как при запуске .py, так и внутри PyInstaller .exe.
    """
    # PyInstaller кладет распакованные данные в sys._MEIPASS
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    # обычный режим - рядом с config.py
    return Path(__file__).resolve().parent


BASE_DIR: Path = get_base_dir()
ICONS_DIR: Path = BASE_DIR / 'icons'


def get_icon_path(icon_name: str) -> str:
    # строим путь к svg-иконке с учетом режима PyInstaller
    return str(ICONS_DIR / f'{icon_name}.svg')

ICONS = {
    'rainbow': get_icon_path('rainbow'),
    'bricks': get_icon_path('bricks'),
    'brick': get_icon_path('brick'),
    'trophy': get_icon_path('trophy'),
    'check': get_icon_path('check'),
    'cross': get_icon_path('cross'),
    'save': get_icon_path('save'),
    'play': get_icon_path('play'),
    'reset': get_icon_path('reset'),
    'copy': get_icon_path('copy'),
    'scroll': get_icon_path('scroll')
}

EMOJI = {
    'rainbow': '🌈',
    'bricks': '🧱',
    'trophy': '🏆',
    'fire': '🔥',
    'star': '⭐',
    'check': '✓',
    'cross': '✗',
    'robot': '🤖',
    'user': '👤',
    'save': '💾',
    'play': '▶',
    'reset': '🔄',
    'copy': '📋',
    'scroll': '📜',
    'gamepad': '🎮',
}